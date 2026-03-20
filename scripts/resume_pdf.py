#!/usr/bin/env python3
"""Resume PDF generator and validator.

Thin entry point that delegates to the modular pipeline package.
See scripts/pipeline/ for implementation:
    - config.py:    Paths, constants, LayoutConfig
    - parser.py:    Markdown parsing
    - renderer.py:  PDF rendering + single-page optimization
    - validator.py: ATS compliance validation
    - cli.py:       CLI orchestration + logging

Validation checks enforce writing style rules from docs/writing_style_guide.md.

Usage:
    python3 scripts/resume_pdf.py --validate-only
    python3 scripts/resume_pdf.py --input markdown/company_role/final.md --output Thomas_To_Resume_Role
"""

from pipeline.cli import main

if __name__ == "__main__":
    main()
