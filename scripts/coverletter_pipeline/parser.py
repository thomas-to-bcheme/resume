"""Markdown parsing for cover letter documents.

Handles frontmatter stripping, inline formatting (bold, italic, links),
and structural element recognition (h1, contact, date, greeting, paragraph,
signature). Consecutive non-special lines are joined into single paragraph
elements using blank-line separation (standard markdown behavior).
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


def _is_date_line(line: str) -> bool:
    """Check if a line matches a date pattern (e.g., 'March 20, 2026')."""
    return bool(re.match(
        r"^(?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December)\s+\d{1,2},\s+\d{4}$",
        line,
    ))


def _is_greeting(line: str) -> bool:
    """Check if a line is a greeting (e.g., 'Dear Hiring Manager,')."""
    return bool(re.match(r"^Dear .+,$", line))


def parse_coverletter(text: str) -> list[Element]:
    """Parse cover letter markdown into structured (type, content) elements.

    Uses blank-line separation to group consecutive non-special lines into
    single paragraph elements. This ensures multi-line paragraphs render
    as flowing text blocks rather than separate chunks.

    Recognizes: h1 (name), contact (line after h1), date_line, greeting
    (Dear ...,), paragraph (blank-line-separated text blocks),
    signature_closing (Sincerely,), and signature_name.

    Args:
        text: Cover letter markdown content (frontmatter already stripped).

    Returns:
        List of (element_type, content) tuples representing the document
        structure in order.
    """
    elements: list[Element] = []
    prev_type = None
    in_signature = False
    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        """Emit buffered lines as a single paragraph element."""
        if paragraph_buffer:
            elements.append(("paragraph", " ".join(paragraph_buffer)))
            paragraph_buffer.clear()

    for raw_line in text.split("\n"):
        line = raw_line.strip()

        # Blank line: flush any accumulated paragraph buffer
        if not line:
            flush_paragraph()
            continue

        # H1: name header
        if line.startswith("# "):
            flush_paragraph()
            elements.append(("h1", line[2:]))
            prev_type = "h1"
            continue

        # Contact: first line after H1
        if prev_type == "h1":
            flush_paragraph()
            elements.append(("contact", line))
            prev_type = "contact"
            continue

        # Date line
        if _is_date_line(line):
            flush_paragraph()
            elements.append(("date_line", line))
            prev_type = "date_line"
            continue

        # Greeting
        if _is_greeting(line):
            flush_paragraph()
            elements.append(("greeting", line))
            prev_type = "greeting"
            continue

        # Signature closing
        if line == "Sincerely,":
            flush_paragraph()
            in_signature = True
            elements.append(("signature_closing", line))
            prev_type = "signature_closing"
            continue

        # Signature name (line after "Sincerely,")
        if in_signature:
            flush_paragraph()
            elements.append(("signature_name", line))
            prev_type = "signature_name"
            continue

        # Default: accumulate into paragraph buffer
        paragraph_buffer.append(line)
        prev_type = "paragraph"

    # Flush any remaining paragraph content
    flush_paragraph()

    return elements
