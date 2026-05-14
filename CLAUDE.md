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

Standalone resume tailoring microservice powered by Claude Code. Reads a golden dataset (`docs/resume.md`), tailors content to job descriptions using AI agents, and generates ATS-optimized PDFs.

### Workflow: Resume
1. User invokes `/resume-tailor <application_name>` with a job description (URL or pasted text)
2. Claude Code reads the golden dataset and writing style rules from `docs/`
3. Resume agent tailors content to the JD using XYZ bullet formula
4. Validation script checks ATS compliance and banned words
5. PDF generator produces a two-page resume

### Workflow: Cover Letter
1. User invokes `/coverletter-tailor <application_name>` with a job description (URL or pasted text)
2. Claude Code reads the golden dataset and writing style rules from `docs/`
3. If `jd.md` exists from a prior resume-tailor run, it is reused
4. Cover letter agent generates narrative paragraphs tailored to the JD
5. Validation script checks banned words, passive voice, punctuation, word count
6. PDF generator produces a single-page cover letter

### Workflow: Application Response
1. User invokes `/resume-response [folder_name or JD URL] <prompt>` with a free-text question
2. Claude Code reads the golden dataset and writing style rules from `docs/`
3. If `jd.md` exists from a prior resume-tailor or coverletter-tailor run, it is reused
4. Response agent generates a <=300-word answer grounded in resume facts and JD context
5. Response is written to `markdown/<folder_name>/response_<slug>.md` and displayed in conversation

### Key Directories
- `docs/` - Golden datasets and reference files (IMMUTABLE, READ-ONLY)
- `markdown/` - Generated markdown output (one subfolder per application)
- `pdf/` - Generated PDF output
- `scripts/` - Python pipeline packages (`resume_pdf.py` + `resume_pipeline/`, `coverletter_pdf.py` + `coverletter_pipeline/`)
- `.claude/skills/resume-tailor/` - Resume skill orchestrator (7-step workflow)
- `.claude/skills/coverletter-tailor/` - Cover letter skill orchestrator (7-step workflow)
- `.claude/skills/resume-response/` - Application response skill orchestrator (9-step workflow)
- `.claude/agents/` - Resume, cover letter, and application response sub-agents

### Tech Stack
- **AI**: Claude Code with sub-agents
- **PDF Generation**: Python 3.12+, fpdf2 (modular pipeline in `scripts/resume_pipeline/`)
- **Containerization**: Docker (optional)

## 4. Commands

### Operational Standards
- **Idempotency:** Commands must be runnable multiple times without side effects.
- **Parameters:** Prefer named flags (`--input`) over positional args.
- **Exit Codes:** Return `0` for success, non-zero for failure.

### Resume PDF Script
```bash
# Validate golden dataset
python3 scripts/resume_pdf.py --validate-only

# Validate a tailored resume
python3 scripts/resume_pdf.py --validate-only --input markdown/google_mle/final.md

# Generate PDF (outputs to pdf/ by default)
python3 scripts/resume_pdf.py --input markdown/google_mle/final.md --output Thomas_To_Resume_Google_MLE
```

### Cover Letter PDF Script
```bash
# Validate a tailored cover letter
python3 scripts/coverletter_pdf.py --validate-only --input markdown/google_mle/coverletter_final.md

# Generate PDF (outputs to pdf/ by default)
python3 scripts/coverletter_pdf.py --input markdown/google_mle/coverletter_final.md --output Thomas_To_CoverLetter_Google_MLE
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
- `docs/resume.md` is the **READ-ONLY golden dataset**. It is NEVER modified by any skill, agent, or script, with one sanctioned exception: `/resume-update` (`.claude/skills/resume-update/`) is the single authorized edit path, which delegates writes to the `resume-update` agent.
- `docs/` directory is IMMUTABLE. No script or agent writes to this directory, except the `resume-update` agent writing to `docs/resume.md` via the `/resume-update` skill.
- Tailored resumes are written to `markdown/<application_name>/generated.md` as new files.
- Tailored cover letters are written to `markdown/<application_name>/coverletter_generated.md` as new files.
- Editable copies live at `markdown/<application_name>/final.md` (resume) and `coverletter_final.md` (cover letter) for iteration.
- Application responses are written to `markdown/<application_name>/response_<slug>.md` as new files.
- PDFs are generated to `pdf/` from the editable copies.
- The PDF scripts read from the tailored markdown, not the golden dataset directly (unless validating the golden dataset).
