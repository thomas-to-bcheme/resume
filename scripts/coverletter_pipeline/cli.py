"""CLI entry point for the cover letter pipeline.

Handles argument parsing, logging configuration, and orchestration
of validation and PDF generation. All user-facing output goes through
the standard logging module.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import DEFAULT_OUTPUT_NAME, PDF_DIR, PROJECT_ROOT, ensure_dirs
from .parser import parse_coverletter, strip_frontmatter
from .renderer import generate_pdf
from .validator import validate

logger = logging.getLogger("coverletter_pipeline")


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the cover letter pipeline.

    Args:
        level: Logging level (default: INFO).
    """
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=level,
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments with input, output, output_dir, and validate_only.
    """
    parser = argparse.ArgumentParser(description="Cover letter PDF generator and validator")
    parser.add_argument(
        "--input", type=Path, required=True,
        help="Cover letter markdown file (e.g., markdown/google_mle/coverletter_final.md)",
    )
    parser.add_argument(
        "--output", type=str, default=DEFAULT_OUTPUT_NAME,
        help="Output PDF name without .pdf extension (default: Thomas_To_CoverLetter)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=PDF_DIR,
        help="Directory for generated PDF (default: pdf/)",
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Run validation without generating PDF",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point: parse arguments, validate cover letter, generate PDF.

    Exit codes:
        0 - Validation passed and PDF generated (or --validate-only passed)
        1 - File not found, validation FAIL issues detected, or PDF error
    """
    setup_logging()
    ensure_dirs()

    args = parse_args()

    # -- Read input file --
    input_path = args.input if args.input.is_absolute() else PROJECT_ROOT / args.input
    if not input_path.exists():
        logger.error("File not found: %s", input_path)
        sys.exit(1)

    try:
        raw_text = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        logger.error("Cannot read file: %s (%s)", input_path, exc)
        sys.exit(1)

    body = strip_frontmatter(raw_text)

    # -- Validate content --
    issues, char_count = validate(raw_text)
    has_fail = any(level == "FAIL" for level, _ in issues)

    # -- Print report --
    logger.info("=" * 60)
    logger.info("COVER LETTER VALIDATION REPORT")
    logger.info("=" * 60)
    for level, msg in issues:
        if level == "PASS":
            logger.info("  [+] PASS: %s", msg)
        elif level == "WARN":
            logger.warning("  [!] WARN: %s", msg)
        else:
            logger.error("  [x] FAIL: %s", msg)
    logger.info("=" * 60)

    if args.validate_only:
        sys.exit(1 if has_fail else 0)

    if has_fail:
        logger.error("Validation failures found. Fix before generating PDF.")
        sys.exit(1)

    # -- Generate PDF --
    elements = parse_coverletter(body)
    output_name = args.output.replace(".pdf", "")
    output_dir = args.output_dir if args.output_dir.is_absolute() else PROJECT_ROOT / args.output_dir
    output_path = output_dir / f"{output_name}.pdf"

    try:
        success, page_count = generate_pdf(elements, output_path)
    except Exception as exc:
        logger.error("PDF generation failed: %s", exc)
        sys.exit(1)

    logger.info("PDF generated: %s", output_path)
    logger.info("  Pages: %d", page_count)
    logger.info("  Characters: %d", char_count)
    if page_count > 1:
        logger.warning("  %d pages (target: 1). Consider reducing content.", page_count)
