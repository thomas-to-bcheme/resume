"""PDF rendering and page-fit optimization.

Converts parsed resume elements into an ATS-optimized PDF using fpdf2.
Includes a page-fit optimizer that progressively tightens layout
parameters until content fits on two pages.
"""

from __future__ import annotations

import dataclasses
import logging
import re
from pathlib import Path

from fpdf import FPDF

from .config import (
    BULLET_CHAR,
    BULLET_HANG,
    BULLET_INDENT,
    CONTACT_SPACE_AFTER,
    CONTENT_WIDTH,
    Element,
    FONT_FAMILY,
    FONT_SIZE_CONTACT,
    FONT_SIZE_H1,
    FONT_SIZE_H2,
    H1_SPACE_AFTER,
    H2_RULE_WEIGHT,
    LayoutConfig,
    LINK_COLOR,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    PAGE_FORMAT,
    PAGE_WIDTH,
)
from .parser import parse_inline

logger = logging.getLogger("resume_pipeline")


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


def render_h2(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render H2: uppercase bold 11pt with bottom rule line.

    Args:
        pdf: Active FPDF instance.
        text: Section header text.
        cfg: Layout configuration.
    """
    pdf.set_y(pdf.get_y() + cfg.h2_space_before)
    pdf.set_font(FONT_FAMILY, "B", FONT_SIZE_H2)
    h = _line_h(FONT_SIZE_H2, cfg)
    pdf.cell(CONTENT_WIDTH, h, sanitize(text).upper(), new_x="LMARGIN", new_y="NEXT")
    y_rule = pdf.get_y() + H2_RULE_WEIGHT / 2
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(H2_RULE_WEIGHT)
    pdf.line(MARGIN_LEFT, y_rule, PAGE_WIDTH - MARGIN_RIGHT, y_rule)
    pdf.set_y(y_rule + cfg.h2_space_after)


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


def render_entry_header(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render job/education entry header (bold title | italic date).

    Args:
        pdf: Active FPDF instance.
        text: Entry header with bold and pipe separator.
        cfg: Layout configuration.
    """
    pdf.set_y(pdf.get_y() + cfg.entry_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    render_text(pdf, text, h)
    pdf.ln(h)


def render_bullet(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render bullet point with hanging indent for wrapped lines.

    Args:
        pdf: Active FPDF instance.
        text: Bullet content (without the leading "- ").
        cfg: Layout configuration.
    """
    h = _line_h(cfg.font_size_body, cfg)
    x_bullet = MARGIN_LEFT + BULLET_INDENT
    x_text = x_bullet + BULLET_HANG

    orig_margin = pdf.l_margin
    pdf.set_left_margin(x_text)

    y = pdf.get_y() + cfg.bullet_space
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    pdf.set_xy(x_bullet, y)
    pdf.cell(BULLET_HANG, h, BULLET_CHAR)

    pdf.set_xy(x_text, y)
    render_text(pdf, text, h)
    pdf.ln(h)

    pdf.set_left_margin(orig_margin)


# ── PDF Generation ───────────────────────────────────────────────────

def _try_render(elements: list[Element], cfg: LayoutConfig) -> tuple[FPDF, int]:
    """Render elements into an in-memory PDF without writing to disk.

    Used by generate_pdf() to test whether content fits within the target
    page count before committing to a file.

    Args:
        elements: Parsed (type, content) pairs from parse_resume().
        cfg: Layout configuration controlling font sizes, spacing, and margins.

    Returns:
        Tuple of (pdf_object, page_count).
    """
    pdf = FPDF(orientation="P", unit="in", format=PAGE_FORMAT)
    pdf.set_margins(MARGIN_LEFT, cfg.margin_top, MARGIN_RIGHT)
    pdf.set_auto_page_break(auto=True, margin=cfg.margin_bottom)
    pdf.add_page()

    for elem_type, content in elements:
        if elem_type == "h1":
            render_h1(pdf, content, cfg)
        elif elem_type == "contact":
            render_contact(pdf, content, cfg)
        elif elem_type == "h2":
            render_h2(pdf, content, cfg)
        elif elem_type == "paragraph":
            render_paragraph(pdf, content, cfg)
        elif elem_type == "entry_header":
            render_entry_header(pdf, content, cfg)
        elif elem_type == "bullet":
            render_bullet(pdf, content, cfg)

    return pdf, pdf.page


# Each optimization step tightens the LayoutConfig.
# Steps are applied in order until the PDF fits on one page or all
# steps are exhausted. Order: highest visual impact first.
_OPTIMIZATION_STEPS: list[tuple[str, ...]] = [
    ("Reduce body font 10.5 -> 10.0",),
    ("Reduce line height 1.25 -> 1.20",),
    ("Reduce all spacing by 25%",),
    ("Reduce body font 10.0 -> 9.5, line height 1.20 -> 1.15",),
    ("Reduce top/bottom margins 0.4 -> 0.3",),
]


def _apply_optimization_step(cfg: LayoutConfig, step: int) -> LayoutConfig:
    """Apply a single optimization step to the layout config.

    Args:
        cfg: Current layout config (not mutated).
        step: Zero-based step index into the optimization sequence.

    Returns:
        New LayoutConfig with tightened parameters.
    """
    cfg = dataclasses.replace(cfg)
    if step == 0:
        cfg.font_size_body = 10.0
    elif step == 1:
        cfg.line_height_mult = 1.20
    elif step == 2:
        cfg.h2_space_before *= 0.75
        cfg.h2_space_after *= 0.75
        cfg.paragraph_space_before *= 0.75
        cfg.bullet_space *= 0.75
        cfg.entry_space_before *= 0.75
    elif step == 3:
        cfg.font_size_body = 9.5
        cfg.line_height_mult = 1.15
    elif step == 4:
        cfg.margin_top = 0.3
        cfg.margin_bottom = 0.3
    return cfg


def generate_pdf(
    elements: list[Element], output_path: Path
) -> tuple[bool, int, list[str]]:
    """Generate an ATS-optimized PDF from parsed resume elements.

    Attempts to render with default layout. If the result exceeds two pages,
    progressively tightens layout parameters (font size, line spacing,
    margins) until the content fits or all optimization steps are exhausted.

    Creates parent directories automatically if they do not exist.

    Args:
        elements: Parsed (type, content) pairs from parse_resume().
        output_path: Destination file path for the generated PDF.

    Returns:
        Tuple of (success, page_count, adjustments_applied). Adjustments is
        a list of human-readable descriptions of layout changes made.
    """
    cfg = LayoutConfig()
    adjustments: list[str] = []

    pdf, page_count = _try_render(elements, cfg)

    step = 0
    while page_count > 2 and step < len(_OPTIMIZATION_STEPS):
        cfg = _apply_optimization_step(cfg, step)
        adjustments.append(_OPTIMIZATION_STEPS[step][0])
        pdf, page_count = _try_render(elements, cfg)
        step += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    return True, page_count, adjustments
