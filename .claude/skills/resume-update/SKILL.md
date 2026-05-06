---
name: resume-update
description: Use when editing the golden dataset docs/resume.md (add/rename/remove sections, roles, bullets, projects, certifications). Sanctioned exception to the READ-ONLY rule.
argument-hint: "[free-text instructions describing the edit, e.g. 'rename Open Source Founder to Founding AI Engineer']"
---

# Resume Update Skill

Edit the golden dataset at `docs/resume.md`. This skill is the **single sanctioned exception** to the READ-ONLY rule in CLAUDE.md §7. All other skills, agents, and scripts treat `docs/resume.md` as immutable.

## Arguments

- `$ARGUMENTS` = free-text instructions describing the edit(s). Example: `"rename Open Source Founder to Founding AI Engineer; add PROJECTS section after Professional Experience"`.
- If `$ARGUMENTS` is empty, prompt the user for the edit instructions before proceeding.

## Section Map (authoritative for golden dataset)

The golden dataset supports these H2 sections:

- `## PROFESSIONAL SUMMARY`
- `## TECHNICAL SKILLS`
- `## PROFESSIONAL EXPERIENCE`
- `## PROJECTS`
- `## EDUCATION`
- `## CERTIFICATIONS, AWARDS, & LEADERSHIP`

Tailored outputs (produced by `/resume-tailor`) are validated against a narrower ATS set. Adding non-ATS sections here does not auto-propagate them to tailored resumes.

## Workflow

### Step 1: Load Writing Standards

Read `docs/writing_style_guide.md`. All edits must comply with:
- No em dashes, no semicolons, no asterisks in body text.
- Active voice only.
- Banned words list applies to golden dataset content.

### Step 2: Parse Edit Instructions

Interpret `$ARGUMENTS` into a structured edit list. Classify each edit as one of:

- **Rename**: change a role title, section heading, or label.
- **Add**: insert a new section, role, bullet, or line.
- **Remove**: delete a bullet, role, or section.
- **Replace**: swap content in place.

If any instruction is ambiguous (truncated text, missing dates, unclear placement), ASK the user before proceeding. Do not infer missing content (CLAUDE.md §1 directive 4).

### Step 3: Snapshot Golden Dataset

Back up the current golden dataset before any edits:

```bash
cp docs/resume.md docs/.resume.md.bak
```

Tell the user the recovery command: `mv docs/.resume.md.bak docs/resume.md`. The `.bak` file is gitignored via the project `*.bak` pattern.

### Step 4: Delegate to resume-update Agent

Use the `Agent` tool with `subagent_type: resume-update`. Pass these instructions:

```
You are editing the golden dataset at docs/resume.md.

## Edit Instructions
<structured edit list from Step 2>

## Current Golden Dataset Content
<paste current docs/resume.md content here for context>

## Writing Style Rules
<paste key rules from docs/writing_style_guide.md>

## Rules
1. Use the Edit tool for surgical changes. Do NOT use Write to replace the whole file unless explicitly instructed.
2. Preserve all existing content NOT targeted by the edit instructions.
3. Preserve markdown hyperlink syntax `[text](url)` exactly.
4. No em dashes, no semicolons, no banned words.
5. Active voice only.
6. Preserve date formatting: `*Mon YYYY – Mon YYYY*` or `*Mon YYYY – Present*`.
7. Valid H2 sections: PROFESSIONAL SUMMARY, TECHNICAL SKILLS, PROFESSIONAL EXPERIENCE, PROJECTS, EDUCATION, CERTIFICATIONS, AWARDS, & LEADERSHIP.
8. If an instruction is under-specified or would erase content, STOP and report back. Do not guess.
```

### Step 5: Validate Updated Golden Dataset

```bash
python3 scripts/resume_pdf.py --validate-only --input docs/resume.md
```

**Expected WARNs (accept these):**
- Over-budget character count (golden dataset is multi-page by design).
- Non-standard sections (PROJECTS, CERTIFICATIONS, AWARDS, & LEADERSHIP) — validator is scoped to tailored outputs.

**FAIL conditions (stop, do not proceed):**
- Passive voice.
- Em dashes, double hyphens, or semicolons in body text.
- Missing any required ATS section (PROFESSIONAL SUMMARY, TECHNICAL SKILLS, PROFESSIONAL EXPERIENCE, EDUCATION).

If validation FAILs, delegate back to the agent with the specific failures. Do not attempt manual fixes in the skill layer.

### Step 6: Show Diff and Confirm

Show the user the diff:

```bash
git diff docs/resume.md
```

Ask the user to confirm the changes. Two outcomes:

- **Accepted**: delete the backup — `rm docs/.resume.md.bak`.
- **Rejected**: restore — `mv docs/.resume.md.bak docs/resume.md`. Report the restoration.

### Step 7: Report Results

Summarize to the user:
- Sections added / removed.
- Roles renamed.
- Bullets added / removed.
- Validation status (PASS / WARN summary).
- Recovery command if the backup still exists.
- Suggested next step: re-run `/resume-tailor <app>` for any in-flight applications so tailored outputs pick up golden dataset changes.

## Key References

| Resource | Path | Access |
|----------|------|--------|
| Golden dataset | `docs/resume.md` | **READ/WRITE (this skill only)** |
| Writing style | `docs/writing_style_guide.md` | READ-ONLY |
| Update agent | `.claude/agents/resume-update.md` | Delegated |
| Validator | `scripts/resume_pdf.py --validate-only --input docs/resume.md` | Execute |
| Backup | `docs/.resume.md.bak` | WRITE (transient, gitignored) |

## Boundaries

- Does NOT push to git, commit, or create PRs.
- Does NOT regenerate tailored resumes in `markdown/` or PDFs in `pdf/`.
- Does NOT fabricate content. Asks the user when instructions are under-specified.
- Does NOT run destructive edits (full file replace, section delete without replacement) without explicit user confirmation.
- Honors CLAUDE.md §1 directives at every step.
