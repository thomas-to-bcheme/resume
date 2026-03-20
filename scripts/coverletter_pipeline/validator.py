"""Validation for cover letter markdown.

Checks: banned words, passive voice, punctuation, character budget,
and word count. Each check is an independent function returning a
list of (severity, message) issues.
"""

from __future__ import annotations

import re

from .config import (
    BANNED_WORDS,
    CHAR_BUDGET_MAX,
    CHAR_BUDGET_MIN,
    Issue,
    WORD_COUNT_MAX,
    WORD_COUNT_MIN,
)
from .parser import strip_frontmatter


def _check_banned_words(body_lower: str) -> list[Issue]:
    """Check for banned words from the writing style guide.

    Args:
        body_lower: Lowercased cover letter body text.

    Returns:
        List of WARN issues for each banned word found.
    """
    issues: list[Issue] = []
    for word in BANNED_WORDS:
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = re.findall(pattern, body_lower)
        if matches:
            issues.append(("WARN", f"Banned word: '{word}' ({len(matches)}x)"))
    return issues


def _check_passive_voice(body_lower: str) -> list[Issue]:
    """Check for passive voice constructions.

    Detects "was/were/been/being + past participle" patterns using
    a \\w+ed\\b heuristic for past participles.

    Args:
        body_lower: Lowercased cover letter body text.

    Returns:
        List of FAIL issues for each passive voice match.
    """
    issues: list[Issue] = []
    passive_patterns = [
        r"\bwas\s+\w+ed\b", r"\bwere\s+\w+ed\b",
        r"\bbeen\s+\w+ed\b", r"\bbeing\s+\w+ed\b",
    ]
    for pat in passive_patterns:
        for m in re.finditer(pat, body_lower):
            issues.append(("FAIL", f"Passive voice: '{m.group()}'"))
    return issues


def _check_punctuation(body: str) -> list[Issue]:
    """Check for prohibited punctuation: em dashes, double hyphens, semicolons.

    Args:
        body: Cover letter body text (original case preserved).

    Returns:
        List of FAIL issues for each punctuation violation.
    """
    issues: list[Issue] = []

    if "\u2014" in body:
        issues.append(("FAIL", "Em dash (\u2014) found"))
    if "--" in body:
        issues.append(("FAIL", "Double hyphen (--) found"))

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

    Strips markdown syntax to count only visible characters.

    Args:
        body: Cover letter body text.

    Returns:
        Tuple of (issues, char_count) where char_count is the visible
        character count after stripping markdown syntax.
    """
    issues: list[Issue] = []
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    plain = re.sub(r"[*#\-|]", "", plain)
    plain = re.sub(r"<br>", "", plain)
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


def _check_word_count(body: str) -> list[Issue]:
    """Check word count against target range.

    Args:
        body: Cover letter body text.

    Returns:
        List of PASS/WARN issues for word count compliance.
    """
    issues: list[Issue] = []
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    plain = re.sub(r"[*#]", "", plain)
    words = plain.split()
    word_count = len(words)

    target_range = f"{WORD_COUNT_MIN}-{WORD_COUNT_MAX}"
    if word_count < WORD_COUNT_MIN:
        issues.append(("WARN", f"Under word count: {word_count} words (target {target_range})"))
    elif word_count > WORD_COUNT_MAX:
        issues.append(("WARN", f"Over word count: {word_count} words (target {target_range})"))
    else:
        issues.append(("PASS", f"Word count: {word_count} (target {target_range})"))

    return issues


def _check_structure(body: str) -> list[Issue]:
    """Check cover letter structural requirements.

    A valid cover letter must have a greeting, a signature, no bullet points,
    and at least 2 body paragraphs between greeting and signature.

    Args:
        body: Cover letter body text.

    Returns:
        List of PASS/FAIL issues for structural compliance.
    """
    issues: list[Issue] = []

    # Greeting check
    has_greeting = bool(re.search(r"^Dear .+,$", body, re.MULTILINE))
    if has_greeting:
        issues.append(("PASS", "Greeting line present"))
    else:
        issues.append(("FAIL", "Missing greeting line (expected 'Dear ...,')"))

    # Signature check
    has_signature = "Sincerely," in body
    if has_signature:
        issues.append(("PASS", "Signature block present"))
    else:
        issues.append(("FAIL", "Missing signature block (expected 'Sincerely,')"))

    # No bullet points
    bullets = re.findall(r"^- .+$", body, re.MULTILINE)
    if bullets:
        issues.append(("FAIL", f"Cover letter contains {len(bullets)} bullet point(s). Use paragraphs only"))
    else:
        issues.append(("PASS", "No bullet points found"))

    # Paragraph count between greeting and signature
    if has_greeting and has_signature:
        greeting_match = re.search(r"^Dear .+,$", body, re.MULTILINE)
        sig_idx = body.index("Sincerely,")
        if greeting_match:
            between = body[greeting_match.end():sig_idx].strip()
            # Split on double newlines to count paragraphs
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n", between) if p.strip()]
            if len(paragraphs) < 2:
                issues.append(("FAIL", f"Only {len(paragraphs)} body paragraph(s) found (minimum 2)"))
            else:
                issues.append(("PASS", f"{len(paragraphs)} body paragraphs found"))

    return issues


def validate(text: str) -> tuple[list[Issue], int]:
    """Run all validation checks on cover letter markdown content.

    Checks performed (in order):
        1. Banned words from writing style guide
        2. Passive voice constructions
        3. Prohibited punctuation (em dashes, double hyphens, semicolons)
        4. Character budget (visible text within target range)
        5. Word count (250-400 words)
        6. Cover letter structure (greeting, signature, no bullets, min paragraphs)

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

    issues.extend(_check_word_count(body))
    issues.extend(_check_structure(body))

    return issues, char_count
