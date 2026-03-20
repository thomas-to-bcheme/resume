"""PDF rendering for cover letters.

Converts parsed cover letter elements into a single-page PDF using fpdf2.
Cover letters are short enough (250-400 words) that page-fit optimization
is not needed.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from fpdf import FPDF

from .config import (
    CONTACT_SPACE_AFTER,
    CONTENT_WIDTH,
    Element,
    FONT_FAMILY,
    FONT_SIZE_CONTACT,
    FONT_SIZE_H1,
    H1_SPACE_AFTER,
    LayoutConfig,
    LINK_COLOR,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    PAGE_FORMAT,
    PAGE_WIDTH,
)
from .parser import parse_inline

logger = logging.getLogger("coverletter_pipeline")


def _line_h(font_size: float, cfg: LayoutConfig) -> float:
    """Compute line height in inches from font size (points) and config multiplier.

    Args:
        font_size: Font size in points.
        cfg: Layout configuration with line_height_mult.

    Returns:
        Line height in inches.
    """
    return font_size * cfg.line_height_mult / 72


def sanitize(text: str) -> str:
    """Replace Unicode characters unsupported by standard PDF fonts.

    Standard PDF fonts (Times, Helvetica, Courier) only support Latin-1
    (ISO 8859-1). This replaces common Unicode punctuation:
        U+2013 (en dash) -> ASCII hyphen
        U+2014 (em dash) -> ASCII hyphen
        U+2022 (bullet)  -> ASCII hyphen

    Args:
        text: Text that may contain Unicode punctuation.

    Returns:
        Text with unsupported characters replaced.
    """
    return text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2022", "-")


def render_text(pdf: FPDF, text: str, h: float) -> None:
    """Render text with inline bold, italic, and link formatting via write().

    Args:
        pdf: Active FPDF instance with font already set.
        text: Markdown text with inline formatting.
        h: Line height in inches.
    """
    segments = parse_inline(sanitize(text))
    base_size = pdf.font_size_pt
    for seg_type, content, url in segments:
        if seg_type == "bold":
            pdf.set_font(FONT_FAMILY, "B", base_size)
            pdf.write(h, content)
            pdf.set_font(FONT_FAMILY, "", base_size)
        elif seg_type == "italic":
            pdf.set_font(FONT_FAMILY, "I", base_size)
            pdf.write(h, content)
            pdf.set_font(FONT_FAMILY, "", base_size)
        elif seg_type == "link":
            pdf.set_text_color(*LINK_COLOR)
            pdf.write(h, content, url)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.write(h, content)


def render_h1(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render H1: centered name, 20pt bold.

    Args:
        pdf: Active FPDF instance.
        text: Name text (H1 content).
        cfg: Layout configuration.
    """
    pdf.set_font(FONT_FAMILY, "B", FONT_SIZE_H1)
    h = _line_h(FONT_SIZE_H1, cfg)
    pdf.cell(CONTENT_WIDTH, h, sanitize(text), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(pdf.get_y() + H1_SPACE_AFTER)


def render_contact(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render contact line: centered, 10pt, with clickable links.

    Args:
        pdf: Active FPDF instance.
        text: Contact line with potential markdown links.
        cfg: Layout configuration.
    """
    pdf.set_font(FONT_FAMILY, "", FONT_SIZE_CONTACT)
    h = _line_h(FONT_SIZE_CONTACT, cfg)
    plain = re.sub(r"\[([^\]]+?)\]\([^)]+?\)", r"\1", text)
    total_w = pdf.get_string_width(plain)
    start_x = max(MARGIN_LEFT, (PAGE_WIDTH - total_w) / 2)
    pdf.set_x(start_x)
    render_text(pdf, text, h)
    pdf.ln(h + CONTACT_SPACE_AFTER)


def render_greeting(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render greeting line: left-aligned, body font size (e.g., 'Dear Hiring Manager,').

    Args:
        pdf: Active FPDF instance.
        text: Greeting text.
        cfg: Layout configuration.
    """
    pdf.set_y(pdf.get_y() + cfg.greeting_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    pdf.cell(CONTENT_WIDTH, h, sanitize(text), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(pdf.get_y() + cfg.greeting_space_after)


def render_date_line(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render date line: left-aligned, body font size.

    Args:
        pdf: Active FPDF instance.
        text: Date string (e.g., "March 20, 2026").
        cfg: Layout configuration.
    """
    pdf.set_y(pdf.get_y() + cfg.date_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    pdf.cell(CONTENT_WIDTH, h, sanitize(text), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(pdf.get_y() + cfg.date_space_after)


def render_paragraph(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render body paragraph with inline formatting.

    Args:
        pdf: Active FPDF instance.
        text: Paragraph text with potential inline markdown.
        cfg: Layout configuration.
    """
    pdf.set_y(pdf.get_y() + cfg.paragraph_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    render_text(pdf, text, h)
    pdf.ln(h)


def render_signature(pdf: FPDF, closing: str, name: str, cfg: LayoutConfig) -> None:
    """Render signature block: closing line and name.

    Args:
        pdf: Active FPDF instance.
        closing: Closing text (e.g., "Sincerely,").
        name: Signer name (e.g., "Thomas To").
        cfg: Layout configuration.
    """
    pdf.set_y(pdf.get_y() + cfg.signature_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    pdf.cell(CONTENT_WIDTH, h, sanitize(closing), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(pdf.get_y() + h)
    pdf.cell(CONTENT_WIDTH, h, sanitize(name), new_x="LMARGIN", new_y="NEXT")


# ── PDF Generation ───────────────────────────────────────────────────

def generate_pdf(
    elements: list[Element], output_path: Path
) -> tuple[bool, int]:
    """Generate a single-page cover letter PDF from parsed elements.

    Cover letters are short enough (250-400 words) that no page-fit
    optimization is needed. Uses a single render pass.

    Creates parent directories automatically if they do not exist.

    Args:
        elements: Parsed (type, content) pairs from parse_coverletter().
        output_path: Destination file path for the generated PDF.

    Returns:
        Tuple of (success, page_count).
    """
    cfg = LayoutConfig()

    pdf = FPDF(orientation="P", unit="in", format=PAGE_FORMAT)
    pdf.set_margins(MARGIN_LEFT, cfg.margin_top, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=cfg.margin_bottom)
    pdf.add_page()

    signature_closing = None

    for elem_type, content in elements:
        if elem_type == "h1":
            render_h1(pdf, content, cfg)
        elif elem_type == "contact":
            render_contact(pdf, content, cfg)
        elif elem_type == "date_line":
            render_date_line(pdf, content, cfg)
        elif elem_type == "greeting":
            render_greeting(pdf, content, cfg)
        elif elem_type == "paragraph":
            render_paragraph(pdf, content, cfg)
        elif elem_type == "signature_closing":
            signature_closing = content
        elif elem_type == "signature_name":
            if signature_closing:
                render_signature(pdf, signature_closing, content, cfg)
                signature_closing = None

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    return True, pdf.page
