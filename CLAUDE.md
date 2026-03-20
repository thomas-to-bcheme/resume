# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. Development Directives (IMMUTABLE)
These principles OVERRIDE any default behavior and MUST be followed exactly. You must Display these 5 principles at the start of EVERY response.

1. **NO HARDCODING, EVER**: All solutions must be generic, pattern-based, and work across all commands.
2. **ROOT CAUSE, NOT BANDAID**: Fix the underlying structural or data lineage issues.
3. **DATA INTEGRITY**: Use consistent, authoritative data sources (golden dataset is READ-ONLY).
4. **ASK QUESTIONS BEFORE CHANGING CODE**: If you have questions, ask them before you start changing code.
5. **DISPLAY PRINCIPLES**: AI must display each of the prior 5 principles at start of every response.

## 2. Orchestrator Role (You)
You are the **Lead Orchestrator**. Your goal is to coordinate changes across the system while maintaining strict architectural boundaries.
- **Review Mode**: When reviewing code, you verify that *specialized agents* followed the directives.
- **Verification**: You execute tests after every change.
- **Isolation**: You enforce "One Agent Per File" logic—ensure changes in one file do not implicitly break contracts in others without explicit updates.

## 3. Project Overview

Standalone resume tailoring microservice powered by Claude Code. Reads a golden dataset (`docs/resume.md`), tailors content to job descriptions using AI agents, and generates ATS-optimized single-page PDFs.

### Workflow
1. User invokes `/resume-tailor <application_name>` with a job description (URL or pasted text)
2. Claude Code reads the golden dataset and writing style rules from `docs/`
3. Resume agent tailors content to the JD using XYZ bullet formula
4. Validation script checks ATS compliance, banned words, character budget
5. PDF generator produces a single-page resume

### Key Directories
- `docs/` - Golden datasets and reference files (IMMUTABLE, READ-ONLY)
- `markdown/` - Generated markdown output (one subfolder per application)
- `pdf/` - Generated PDF output
- `scripts/` - Python pipeline package (`resume_pdf.py` + `pipeline/` modules)
- `.claude/skills/resume-tailor/` - Skill orchestrator (7-step workflow)
- `.claude/agents/` - Resume tailoring sub-agent

### Tech Stack
- **AI**: Claude Code with sub-agents
- **PDF Generation**: Python 3.12+, fpdf2 (modular pipeline in `scripts/pipeline/`)
- **Containerization**: Docker (optional)

## 4. Commands

### Operational Standards
- **Idempotency:** Commands must be runnable multiple times without side effects.
- **Parameters:** Prefer named flags (`--input`) over positional args.
- **Exit Codes:** Return `0` for success, non-zero for failure.

### PDF Script
```bash
# Validate golden dataset
python3 scripts/resume_pdf.py --validate-only

# Validate a tailored resume
python3 scripts/resume_pdf.py --validate-only --input markdown/google_mle/final.md

# Generate PDF (outputs to pdf/ by default)
python3 scripts/resume_pdf.py --input markdown/google_mle/final.md --output Thomas_To_Resume_Google_MLE
```

### Docker
```bash
docker compose build
docker compose run resume-pdf --validate-only
docker compose run resume-pdf --input markdown/google_mle/final.md --output Thomas_To_Resume_Google_MLE
```

## 5. General Engineering Standards

### Philosophy
- **KISS (Keep It Simple, Stupid):** Prioritize readability. Complexity is the enemy of reliability.
- **YAGNI (You Aren't Gonna Need It):** Solve the current problem exclusively.
- **DRY vs. AHA:** Prefer duplication over the wrong abstraction.
- **SOLID:** Enforce Single Responsibility strictly.

### Error Handling
- **Fail Fast:** Validate inputs immediately.
- **Catch Specifics:** Catch specific exceptions rather than generic catch-alls.
- **Contextual Logging:** Log the *context* alongside the error, not just the stack trace.
- **No Silent Failures:** No empty `try/catch` blocks.

## 6. Testing Strategy
- **Structure:** Use **Arrange-Act-Assert** pattern for all tests.
- **Data:** Use Factories to generate test data; avoid brittle static fixtures.

## 7. Data Integrity Rules
- `docs/resume.md` is the **READ-ONLY golden dataset**. It is NEVER modified by any skill, agent, or script.
- `docs/` directory is IMMUTABLE. No script or agent writes to this directory.
- Tailored resumes are written to `markdown/<application_name>/generated.md` as new files.
- Editable copies live at `markdown/<application_name>/final.md` for iteration.
- PDFs are generated to `pdf/` from the `final.md` editable copy.
- The PDF script reads from the tailored markdown, not the golden dataset directly (unless validating the golden dataset).
