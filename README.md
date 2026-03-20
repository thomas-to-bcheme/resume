# Resume Tailor

A standalone Claude Code skill for tailoring resumes to job descriptions and generating ATS-optimized single-page PDFs.

## What It Does

1. Reads a golden dataset resume (`src/docs/resume.md`) as a READ-ONLY source
2. Tailors content to a specific job description using AI agents
3. Validates ATS compliance, banned words, character budget, and XYZ bullet format
4. Generates a single-page PDF with proper formatting

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI)
- Python 3.12+ (for PDF generation)
- Docker (optional, for containerized PDF generation)

## Quick Start

### Install Python Dependencies

```bash
pip install -r scripts/requirements.txt
```

### Tailor a Resume

Open Claude Code in this directory and run:

```
/resume-tailor 
```

Then paste a job description (or provide a URL). Claude Code will:
- Read the golden dataset
- Tailor content to the JD
- Validate the output
- Generate a PDF

### Validate the Golden Dataset

```bash
python3 scripts/resume_pdf.py --validate-only
```

### Generate a PDF from a Tailored Resume

```bash
python3 scripts/resume_pdf.py --input Thomas_To_Resume_MLE.md --output Thomas_To_Resume_MLE
```

## Docker Setup

### Build

```bash
docker compose build
```

### Validate

```bash
docker compose run resume-pdf --validate-only
```

### Generate PDF

```bash
docker compose run resume-pdf --input Thomas_To_Resume_MLE.md --output Thomas_To_Resume_MLE
```

## Batch Processing

Each invocation reads the same immutable golden dataset and writes to independent output files. Run multiple tailoring sessions for different roles:

```
/resume-tailor [multiple url]
```
Recommendation to use claude-code or AI web extension to scrape, and clean each tab separated by commas.

## File Structure

```
resume/
├── CLAUDE.md                                    # Project instructions for Claude Code
├── Dockerfile                                   # Python 3.12 + fpdf2
├── docker-compose.yml                           # Single-service Docker setup
├── README.md                                    # This file
├── .gitignore                                   # Ignores generated output files
├── .claude/
│   ├── skills/resume-tailor/SKILL.md            # 7-step skill orchestrator
│   ├── agents/resume.md                         # Resume tailoring sub-agent
│   └── agentic_kit/                              # (reserved for future kits)
├── scripts/
│   ├── resume_pdf.py                            # PDF generator + validator
│   └── requirements.txt                         # Python deps (fpdf2)
└── src/docs/
    ├── resume.md                                # Golden dataset (READ-ONLY)
    └── writing_style_guide.md                   # Writing style rules (READ-ONLY)
```

## Key Concepts

- **Golden Dataset**: `src/docs/resume.md` is never modified. It contains the full professional history.
- **XYZ Bullet Formula**: Every bullet follows "Accomplished [X] as measured by [Y], by doing [Z]".
- **ATS Sections**: Only four H2 headers permitted: PROFESSIONAL SUMMARY, TECHNICAL SKILLS, PROFESSIONAL EXPERIENCE, EDUCATION.
- **Character Budget**: Tailored resumes target 4500-5000 characters for single-page fit.
- **Banned Words**: A curated list of AI-sounding words is enforced during validation.
