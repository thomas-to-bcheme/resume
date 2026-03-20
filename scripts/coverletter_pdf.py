#!/usr/bin/env python3
"""Cover letter PDF generator and validator.

Thin entry point that delegates to the modular cover letter pipeline package.
See scripts/coverletter_pipeline/ for implementation:
    - config.py:    Paths, constants, LayoutConfig
    - parser.py:    Markdown parsing
    - renderer.py:  PDF rendering
    - validator.py: Cover letter validation
    - cli.py:       CLI orchestration + logging

Validation checks enforce writing style rules from docs/writing_style_guide.md.

Usage:
    python3 scripts/coverletter_pdf.py --validate-only --input markdown/company_role/coverletter_final.md
    python3 scripts/coverletter_pdf.py --input markdown/company_role/coverletter_final.md --output Thomas_To_CoverLetter_Role
"""

from coverletter_pipeline.cli import main

if __name__ == "__main__":
    main()
