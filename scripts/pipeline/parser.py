"""Markdown parsing for resume documents.

Handles frontmatter stripping, inline formatting (bold, italic, links),
and structural element recognition (h1, h2, contact, bullets, entries).
"""

from __future__ import annotations

import re

from .config import Element, Segment


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- ... ---) if present.

    Args:
        text: Raw markdown content that may start with YAML frontmatter.

    Returns:
        Content with frontmatter removed, or original text if none found.
    """
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


def parse_inline(text: str) -> list[Segment]:
    """Parse inline markdown into (style, content, url) segments.

    Handles **bold**, *italic*, and [text](url) links. Returns a list
    of segments where each is a tuple of (style, content, url_or_none).

    Args:
        text: A single line of markdown with inline formatting.

    Returns:
        List of (style, content, url_or_none) tuples. Style is one of:
        "plain", "bold", "italic", "link".
    """
    segments: list[Segment] = []
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

    Args:
        text: Resume markdown content (frontmatter already stripped).

    Returns:
        List of (element_type, content) tuples representing the document
        structure in order.
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
