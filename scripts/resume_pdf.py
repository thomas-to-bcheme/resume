#!/usr/bin/env python3
"""Resume PDF generator and validator.

Reads a resume markdown file and generates an ATS-optimized single-page PDF
using fpdf2. Includes a page-fit optimizer that automatically adjusts layout
parameters (font size, spacing, margins) if content overflows one page.

All styling is defined as constants in this script. No CSS or YAML config
consumed. Validation checks enforce writing style rules from
src/docs/writing_style_guide.md.

Usage:
    python3 scripts/resume_pdf.py --validate-only
    python3 scripts/resume_pdf.py --input tailored.md --output tailored
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from fpdf import FPDF


# ── Type Aliases ─────────────────────────────────────────────────────
Segment = Tuple[str, str, Optional[str]]   # (style, content, url_or_none)
Element = Tuple[str, str]                  # (element_type, content)
Issue = Tuple[str, str]                    # (severity_level, message)


# ── Project Paths ────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "src" / "docs" / "resume.md"
DEFAULT_OUTPUT_NAME = "Thomas_To_Resume"


# ── Layout Constants (fixed across optimization) ─────────────────────
PAGE_FORMAT = "Letter"
PAGE_WIDTH = 8.5   # inches
PAGE_HEIGHT = 11.0
MARGIN_LEFT = 0.5
MARGIN_RIGHT = 0.5
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

FONT_FAMILY = "Times"
FONT_SIZE_H1 = 20
FONT_SIZE_H2 = 11
FONT_SIZE_CONTACT = 10

LINK_COLOR = (17, 85, 204)
BULLET_CHAR = "-"
BULLET_INDENT = 0.2   # inches from left margin
BULLET_HANG = 0.15    # hanging indent for wrapped lines

H1_SPACE_AFTER = 2 / 72
CONTACT_SPACE_AFTER = 0 / 72
H2_RULE_WEIGHT = 1.5 / 72


# ── ATS Required Sections ───────────────────────────────────────────
ATS_SECTIONS = {
    "PROFESSIONAL SUMMARY",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "EDUCATION",
}


# ── Banned Words (from writing_style_guide.md) ──────────────────────
BANNED_WORDS = [
    "can", "may", "just", "that", "very", "really", "literally",
    "actually", "certainly", "probably", "basically", "could", "maybe",
    "delve", "embark", "enlightening", "esteemed", "shed light", "craft",
    "curating", "imagine", "realm", "game-changer", "unlock", "discover",
    "skyrocket", "abyss", "not alone", "in a world where", "revolutionize",
    "disruptive", "utilize", "utilizing", "dive deep", "tapestry",
    "illuminate", "unveil", "pivotal", "intricate", "elucidate", "hence",
    "furthermore", "however", "harness", "exciting", "groundbreaking",
    "cutting-edge", "remarkable", "it remains to be seen", "glimpse into",
    "navigating", "landscape", "stark", "testament", "in summary",
    "in conclusion", "moreover", "boost", "skyrocketing", "opened up",
    "powerful", "inquiries", "ever-evolving",
]


# ── Validation Thresholds ───────────────────────────────────────────
CHAR_BUDGET_MIN = 4500
CHAR_BUDGET_MAX = 5000


# ── Adjustable Layout Config ────────────────────────────────────────

@dataclasses.dataclass
class LayoutConfig:
    """Adjustable layout parameters for single-page PDF optimization.

    The page-fit optimizer creates a default LayoutConfig and progressively
    tightens values (smaller fonts, reduced spacing, narrower margins) until
    the rendered PDF fits on one page. Fixed constants like PAGE_WIDTH,
    FONT_FAMILY, and FONT_SIZE_H1 are not adjustable.
    """

    font_size_body: float = 10.5
    line_height_mult: float = 1.25
    h2_space_before: float = 6 / 72    # inches (converted from points)
    h2_space_after: float = 3 / 72
    paragraph_space_before: float = 3 / 72
    bullet_space: float = 1 / 72
    entry_space_before: float = 2 / 72
    margin_top: float = 0.4
    margin_bottom: float = 0.4


# ── Parsing ──────────────────────────────────────────────────────────

def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- ... ---) if present."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


def parse_inline(text: str) -> list[Segment]:
    """Parse inline markdown into (style, content, url) segments.

    Handles **bold**, *italic*, and [text](url) links. Returns a list
    of segments where each is a tuple of (style, content, url_or_none).
    """
    segments: list[Segment] = []
    # Match inline markdown: **bold**, *italic*, or [text](url)
    # Group 2 = bold content, Group 3 = italic content,
    # Group 4 = link display text, Group 5 = link URL
    pattern = r"(\*\*(.+?)\*\*|\*([^*]+?)\*|\[([^\]]+?)\]\(([^)]+?)\))"
    last_end = 0
    for m in re.finditer(pattern, text):
        if m.start() > last_end:
            segments.append(("plain", text[last_end:m.start()], None))
        if m.group(2) is not None:
            segments.append(("bold", m.group(2), None))
        elif m.group(3) is not None:
            segments.append(("italic", m.group(3), None))
        elif m.group(4) is not None:
            segments.append(("link", m.group(4), m.group(5)))
        last_end = m.end()
    if last_end < len(text):
        segments.append(("plain", text[last_end:], None))
    return segments


def parse_resume(text: str) -> list[Element]:
    """Parse resume markdown into structured (type, content) elements.

    Recognizes: h1 (name), contact (line after h1), h2 (section headers),
    bullet (- prefixed), entry_header (bold with pipe), and paragraph.
    """
    elements: list[Element] = []
    prev_type = None
    for raw_line in text.split("\n"):
        line = raw_line.strip().replace("<br>", "")
        if not line:
            continue
        if line.startswith("# "):
            elements.append(("h1", line[2:]))
            prev_type = "h1"
        elif line.startswith("## "):
            elements.append(("h2", line[3:]))
            prev_type = "h2"
        elif line.startswith("- "):
            elements.append(("bullet", line[2:]))
            prev_type = "bullet"
        elif prev_type == "h1":
            elements.append(("contact", line))
            prev_type = "contact"
        elif line.startswith("**") and "|" in line:
            elements.append(("entry_header", line))
            prev_type = "entry_header"
        else:
            elements.append(("paragraph", line))
            prev_type = "paragraph"
    return elements


# ── Rendering ────────────────────────────────────────────────────────

def _line_h(font_size: float, cfg: LayoutConfig) -> float:
    """Compute line height in inches from font size (points) and config multiplier."""
    return font_size * cfg.line_height_mult / 72


def sanitize(text: str) -> str:
    """Replace Unicode characters unsupported by standard PDF fonts.

    Standard PDF fonts (Times, Helvetica, Courier) only support Latin-1
    (ISO 8859-1). This replaces common Unicode punctuation:
        U+2013 (en dash) -> ASCII hyphen
        U+2014 (em dash) -> ASCII hyphen
        U+2022 (bullet)  -> ASCII hyphen
    """
    return text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2022", "-")


def render_text(pdf: FPDF, text: str, h: float) -> None:
    """Render text with inline bold, italic, and link formatting via write()."""
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
    """Render H1: centered name, 20pt bold."""
    pdf.set_font(FONT_FAMILY, "B", FONT_SIZE_H1)
    h = _line_h(FONT_SIZE_H1, cfg)
    pdf.cell(CONTENT_WIDTH, h, sanitize(text), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(pdf.get_y() + H1_SPACE_AFTER)


def render_contact(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render contact line: centered, 10pt, with clickable links."""
    pdf.set_font(FONT_FAMILY, "", FONT_SIZE_CONTACT)
    h = _line_h(FONT_SIZE_CONTACT, cfg)
    # Strip markdown link syntax to measure plain text width for centering
    plain = re.sub(r"\[([^\]]+?)\]\([^)]+?\)", r"\1", text)
    total_w = pdf.get_string_width(plain)
    start_x = max(MARGIN_LEFT, (PAGE_WIDTH - total_w) / 2)
    pdf.set_x(start_x)
    render_text(pdf, text, h)
    pdf.ln(h + CONTACT_SPACE_AFTER)


def render_h2(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render H2: uppercase bold 11pt with bottom rule line."""
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
    """Render body paragraph with inline formatting."""
    pdf.set_y(pdf.get_y() + cfg.paragraph_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    render_text(pdf, text, h)
    pdf.ln(h)


def render_entry_header(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render job/education entry header (bold title | italic date)."""
    pdf.set_y(pdf.get_y() + cfg.entry_space_before)
    pdf.set_font(FONT_FAMILY, "", cfg.font_size_body)
    h = _line_h(cfg.font_size_body, cfg)
    render_text(pdf, text, h)
    pdf.ln(h)


def render_bullet(pdf: FPDF, text: str, cfg: LayoutConfig) -> None:
    """Render bullet point with hanging indent for wrapped lines."""
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

    Used by generate_pdf() to test whether content fits on one page before
    committing to a file. Returns the FPDF object and page count.

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


# Each optimization step is a function that tightens the LayoutConfig.
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
        # Reduce all spacing values by 25%
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


def generate_pdf(elements: list[Element], output_path: Path) -> tuple[bool, int, list[str]]:
    """Generate a single-page ATS-optimized PDF from parsed resume elements.

    Attempts to render with default layout. If the result exceeds one page,
    progressively tightens layout parameters (font size, line spacing,
    margins) until the content fits or all optimization steps are exhausted.

    Args:
        elements: Parsed (type, content) pairs from parse_resume().
        output_path: Destination file path for the generated PDF.

    Returns:
        Tuple of (success, page_count, adjustments_applied). Adjustments is
        a list of human-readable descriptions of layout changes made.
    """
    cfg = LayoutConfig()
    adjustments: list[str] = []

    # First pass with default layout
    pdf, page_count = _try_render(elements, cfg)

    # Progressively tighten layout until single-page or steps exhausted
    step = 0
    while page_count > 1 and step < len(_OPTIMIZATION_STEPS):
        cfg = _apply_optimization_step(cfg, step)
        adjustments.append(_OPTIMIZATION_STEPS[step][0])
        pdf, page_count = _try_render(elements, cfg)
        step += 1

    pdf.output(str(output_path))
    return True, page_count, adjustments


# ── Validation ───────────────────────────────────────────────────────

def _check_banned_words(body_lower: str) -> list[Issue]:
    """Check for banned words from the writing style guide."""
    issues: list[Issue] = []
    for word in BANNED_WORDS:
        # Word-boundary match prevents partial hits (e.g., "canvas" won't
        # match banned word "can"). re.escape handles multi-word phrases.
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = re.findall(pattern, body_lower)
        if matches:
            issues.append(("WARN", f"Banned word: '{word}' ({len(matches)}x)"))
    return issues


def _check_passive_voice(body_lower: str) -> list[Issue]:
    """Check for passive voice constructions."""
    issues: list[Issue] = []
    # Detect "was/were/been/being + past participle" patterns.
    # Uses \w+ed\b as a heuristic for past participles. Not exhaustive
    # but catches common cases like "was implemented", "were designed".
    passive_patterns = [
        r"\bwas\s+\w+ed\b", r"\bwere\s+\w+ed\b",
        r"\bbeen\s+\w+ed\b", r"\bbeing\s+\w+ed\b",
    ]
    for pat in passive_patterns:
        for m in re.finditer(pat, body_lower):
            issues.append(("FAIL", f"Passive voice: '{m.group()}'"))
    return issues


def _check_punctuation(body: str) -> list[Issue]:
    """Check for prohibited punctuation: em dashes, double hyphens, semicolons."""
    issues: list[Issue] = []

    # Em dashes and double hyphens (en dashes in date ranges are acceptable)
    if "\u2014" in body:
        issues.append(("FAIL", "Em dash (\u2014) found"))
    if "--" in body:
        issues.append(("FAIL", "Double hyphen (--) found"))

    # Semicolons outside of URLs
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        no_urls = re.sub(r"https?://[^\s)]+", "", stripped)
        if ";" in no_urls:
            issues.append(("FAIL", f"Semicolon: '{stripped[:60]}...'"))

    return issues


def _check_char_budget(body: str) -> tuple[list[Issue], int]:
    """Check visible character count against target budget.

    Returns:
        Tuple of (issues, char_count) where char_count is the visible
        character count after stripping markdown syntax.
    """
    issues: list[Issue] = []
    # Strip markdown to count only visible characters:
    # 1. Replace [text](url) links with display text only
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    # 2. Remove markdown syntax characters: *, #, -, |
    plain = re.sub(r"[*#\-|]", "", plain)
    # 3. Remove <br> HTML tags
    plain = re.sub(r"<br>", "", plain)
    # 4. Collapse all whitespace to single spaces
    visible = re.sub(r"\s+", " ", plain).strip()
    char_count = len(visible)

    budget_range = f"{CHAR_BUDGET_MIN}-{CHAR_BUDGET_MAX}"
    if char_count < CHAR_BUDGET_MIN:
        issues.append(("WARN", f"Under budget: {char_count} chars (target {budget_range})"))
    elif char_count > CHAR_BUDGET_MAX:
        issues.append(("WARN", f"Over budget: {char_count} chars (target {budget_range})"))
    else:
        issues.append(("PASS", f"Character count: {char_count} (target {budget_range})"))

    return issues, char_count


def _check_ats_sections(body: str) -> list[Issue]:
    """Check that all required ATS section headers are present."""
    issues: list[Issue] = []
    found = set(re.findall(r"^## (.+)$", body, re.MULTILINE))
    missing = ATS_SECTIONS - found
    extra = found - ATS_SECTIONS
    if missing:
        issues.append(("FAIL", f"Missing ATS sections: {', '.join(sorted(missing))}"))
    if extra:
        issues.append(("WARN", f"Non-standard sections: {', '.join(sorted(extra))}"))
    if not missing and not extra:
        issues.append(("PASS", "ATS sections valid"))
    return issues


def _check_bullet_quality(body: str) -> list[Issue]:
    """Check XYZ bullet formula compliance and link validity."""
    issues: list[Issue] = []

    # XYZ bullet quality: warn on missing quantified metrics
    bullets = re.findall(r"^- (.+)$", body, re.MULTILINE)
    # Detect quantified metrics in bullet text:
    #   \d+[%$kKmM]       -> "30%", "5K", "$2M"
    #   \$[\d,.]+          -> "$1,200", "$50.5"
    #   \d+\+?\s*(?:...)   -> "3 years", "6+ months", "2x"
    #   by \d+             -> "by 40" (as in "improved by 40%")
    metric_re = (
        r"\d+[%$kKmM]"
        r"|\$[\d,.]+"
        r"|\d+\+?\s*(?:years?|months?|min|hours?|days?|x\b)"
        r"|by \d+"
    )
    weak = [b[:60] for b in bullets if not re.search(metric_re, b)]
    if weak:
        issues.append(("WARN", f"{len(weak)} bullets lack metrics (XYZ Y-component):"))
        for w in weak[:5]:
            issues.append(("WARN", f"  - {w}..."))

    # Link validity: flag empty URLs
    for display, url in re.findall(r"\[([^\]]+)\]\(([^)]*)\)", body):
        if not url:
            issues.append(("FAIL", f"Empty URL for link '{display}'"))

    return issues


def validate(text: str) -> tuple[list[Issue], int]:
    """Run all validation checks on resume markdown content.

    Checks performed (in order):
        1. Banned words from writing style guide
        2. Passive voice constructions
        3. Prohibited punctuation (em dashes, double hyphens, semicolons)
        4. Character budget (visible text within target range)
        5. ATS-required section headers
        6. XYZ bullet quality and link validity

    Args:
        text: Raw markdown content (may include YAML frontmatter).

    Returns:
        Tuple of (issues, char_count) where issues is a list of
        (level, message) pairs with level in {"PASS", "WARN", "FAIL"}.
    """
    body = strip_frontmatter(text)
    body_lower = body.lower()

    issues: list[Issue] = []
    issues.extend(_check_banned_words(body_lower))
    issues.extend(_check_passive_voice(body_lower))
    issues.extend(_check_punctuation(body))

    budget_issues, char_count = _check_char_budget(body)
    issues.extend(budget_issues)

    issues.extend(_check_ats_sections(body))
    issues.extend(_check_bullet_quality(body))

    return issues, char_count


# ── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    """CLI entry point: parse arguments, validate resume, generate PDF.

    Exit codes:
        0 - Validation passed and PDF generated (or --validate-only passed)
        1 - File not found, validation FAIL issues detected, or PDF error
    """
    # -- Parse arguments --
    parser = argparse.ArgumentParser(description="Resume PDF generator and validator")
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT,
        help="Resume markdown file (default: src/docs/resume.md)",
    )
    parser.add_argument(
        "--output", type=str, default=DEFAULT_OUTPUT_NAME,
        help="Output PDF name without .pdf extension (default: Thomas_To_Resume)",
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Run validation without generating PDF",
    )
    args = parser.parse_args()

    # -- Read input file --
    input_path = args.input if args.input.is_absolute() else PROJECT_ROOT / args.input
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        raw_text = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Cannot read file: {input_path} ({exc})", file=sys.stderr)
        sys.exit(1)

    body = strip_frontmatter(raw_text)

    # -- Validate content --
    issues, char_count = validate(raw_text)
    has_fail = any(level == "FAIL" for level, _ in issues)

    # -- Print report --
    print("=" * 60)
    print("RESUME VALIDATION REPORT")
    print("=" * 60)
    for level, msg in issues:
        icon = {"PASS": "+", "WARN": "!", "FAIL": "x"}[level]
        print(f"  [{icon}] {level}: {msg}")
    print("=" * 60)

    if args.validate_only:
        sys.exit(1 if has_fail else 0)

    if has_fail:
        print("\nValidation failures found. Fix before generating PDF.", file=sys.stderr)
        sys.exit(1)

    # -- Generate PDF --
    elements = parse_resume(body)
    output_name = args.output.replace(".pdf", "")
    output_path = PROJECT_ROOT / f"{output_name}.pdf"

    try:
        success, page_count, adjustments = generate_pdf(elements, output_path)
    except Exception as exc:
        print(f"ERROR: PDF generation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nPDF generated: {output_path}")
    print(f"  Pages: {page_count}")
    print(f"  Characters: {char_count}")
    if adjustments:
        print(f"  Layout optimizations applied ({len(adjustments)} steps):")
        for adj in adjustments:
            print(f"    - {adj}")
    if page_count > 1:
        print(f"  WARNING: {page_count} pages after all optimizations (target: 1).")


if __name__ == "__main__":
    main()
