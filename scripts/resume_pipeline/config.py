"""Paths, constants, layout configuration, and type aliases.

All project-wide constants live here. No other module should define paths
or layout values — import from this module instead.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Optional, Tuple


# ── Type Aliases ─────────────────────────────────────────────────────
Segment = Tuple[str, str, Optional[str]]   # (style, content, url_or_none)
Element = Tuple[str, str]                  # (element_type, content)
Issue = Tuple[str, str]                    # (severity_level, message)


# ── Project Paths ────────────────────────────────────────────────────
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
DOCS_DIR: Path = PROJECT_ROOT / "docs"
MARKDOWN_DIR: Path = PROJECT_ROOT / "markdown"
PDF_DIR: Path = PROJECT_ROOT / "pdf"

DEFAULT_INPUT: Path = DOCS_DIR / "resume.md"
DEFAULT_OUTPUT_NAME: str = "Thomas_To_Resume"


# ── Layout Constants (fixed across optimization) ─────────────────────
PAGE_FORMAT: str = "Letter"
PAGE_WIDTH: float = 8.5   # inches
PAGE_HEIGHT: float = 11.0
MARGIN_LEFT: float = 0.5
MARGIN_RIGHT: float = 0.5
CONTENT_WIDTH: float = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

FONT_FAMILY: str = "Times"
FONT_SIZE_H1: int = 20
FONT_SIZE_H2: int = 11
FONT_SIZE_CONTACT: int = 10

LINK_COLOR: tuple[int, int, int] = (17, 85, 204)
BULLET_CHAR: str = "-"
BULLET_INDENT: float = 0.2   # inches from left margin
BULLET_HANG: float = 0.15    # hanging indent for wrapped lines

H1_SPACE_AFTER: float = 2 / 72
CONTACT_SPACE_AFTER: float = 0 / 72
H2_RULE_WEIGHT: float = 1.5 / 72


# ── ATS Sections ─────────────────────────────────────────────────────
# Required sections must appear in every tailored resume. Missing = FAIL.
ATS_REQUIRED_SECTIONS: set[str] = {
    "PROFESSIONAL SUMMARY",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "EDUCATION",
}

# Optional sections are permitted when they add JD-relevant context.
# Tailoring agents include them case-by-case based on job description fit.
ATS_OPTIONAL_SECTIONS: set[str] = {
    "PROJECTS",
    "CERTIFICATIONS, AWARDS, & LEADERSHIP",
}

# Canonical rendering order. Sections outside this sequence trigger FAIL.
SECTION_ORDER: tuple[str, ...] = (
    "PROFESSIONAL SUMMARY",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "PROJECTS",
    "EDUCATION",
    "CERTIFICATIONS, AWARDS, & LEADERSHIP",
)


# ── Banned Words (from docs/writing_style_guide.md) ─────────────────
BANNED_WORDS: list[str] = [
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


# ── Adjustable Layout Config ────────────────────────────────────────

@dataclasses.dataclass
class LayoutConfig:
    """Adjustable layout parameters for PDF optimization.

    The page-fit optimizer creates a default LayoutConfig and progressively
    tightens values (smaller fonts, reduced spacing, narrower margins) until
    the rendered PDF fits on two pages. Fixed constants like PAGE_WIDTH,
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


def ensure_dirs() -> None:
    """Create markdown/ and pdf/ directories if they do not exist.

    Idempotent — safe to call multiple times without side effects.
    """
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
