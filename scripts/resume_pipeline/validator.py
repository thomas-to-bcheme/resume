"""ATS compliance validation for resume markdown.

Checks: banned words, passive voice, punctuation, character budget,
ATS section headers, and XYZ bullet quality. Each check is an
independent function returning a list of (severity, message) issues.
"""

from __future__ import annotations

import re

from .config import (
    ATS_OPTIONAL_SECTIONS,
    ATS_REQUIRED_SECTIONS,
    BANNED_WORDS,
    Issue,
    SECTION_ORDER,
)
from .parser import strip_frontmatter


def _check_banned_words(body_lower: str) -> list[Issue]:
    """Check for banned words from the writing style guide.

    Args:
        body_lower: Lowercased resume body text.

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
        body_lower: Lowercased resume body text.

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
        body: Resume body text (original case preserved).

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


def _count_visible_chars(body: str) -> int:
    """Count visible characters after stripping markdown syntax.

    Args:
        body: Resume body text.

    Returns:
        Visible character count.
    """
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    plain = re.sub(r"[*#\-|]", "", plain)
    plain = re.sub(r"<br>", "", plain)
    visible = re.sub(r"\s+", " ", plain).strip()
    return len(visible)


def _check_ats_sections(body: str) -> list[Issue]:
    """Check ATS section headers against required + optional allowlists.

    Required sections must all be present (missing = FAIL).
    Optional sections are permitted when JD-relevant (present = PASS, absent = PASS).
    Unknown sections (neither required nor optional) trigger WARN.

    Args:
        body: Resume body text.

    Returns:
        List of PASS/WARN/FAIL issues for section header compliance.
    """
    issues: list[Issue] = []
    found = set(re.findall(r"^## (.+)$", body, re.MULTILINE))
    allowed = ATS_REQUIRED_SECTIONS | ATS_OPTIONAL_SECTIONS
    missing = ATS_REQUIRED_SECTIONS - found
    unknown = found - allowed
    if missing:
        issues.append(("FAIL", f"Missing required sections: {', '.join(sorted(missing))}"))
    if unknown:
        issues.append(("WARN", f"Unknown sections: {', '.join(sorted(unknown))}"))
    if not missing and not unknown:
        issues.append(("PASS", "ATS sections valid"))
    return issues


def _check_section_order(body: str) -> list[Issue]:
    """Check that sections appear in canonical order.

    Extracts H2 headers in document order, filters to known sections
    (required or optional), and verifies their positions are a monotonically
    non-decreasing subsequence of SECTION_ORDER. Unknown sections are ignored
    here (already flagged by _check_ats_sections).

    Args:
        body: Resume body text.

    Returns:
        List with one PASS or FAIL issue.
    """
    found_in_order = re.findall(r"^## (.+)$", body, re.MULTILINE)
    canonical_idx = {name: i for i, name in enumerate(SECTION_ORDER)}
    indices = [canonical_idx[s] for s in found_in_order if s in canonical_idx]
    if indices != sorted(indices):
        known = [s for s in found_in_order if s in canonical_idx]
        return [("FAIL", f"Sections out of canonical order: {known}")]
    return [("PASS", "Section order valid")]


def _check_bullet_quality(body: str) -> list[Issue]:
    """Check XYZ bullet formula compliance and link validity.

    Args:
        body: Resume body text.

    Returns:
        List of WARN issues for weak bullets and FAIL for empty URLs.
    """
    issues: list[Issue] = []

    bullets = re.findall(r"^- (.+)$", body, re.MULTILINE)
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
        4. ATS section headers (required + optional allowlist)
        5. Section order (canonical sequence)
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

    char_count = _count_visible_chars(body)

    issues.extend(_check_ats_sections(body))
    issues.extend(_check_section_order(body))
    issues.extend(_check_bullet_quality(body))

    return issues, char_count
