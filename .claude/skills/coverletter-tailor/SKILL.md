---
name: coverletter-tailor
description: Use when generating a cover letter tailored to a job description. Reads the golden dataset and produces a job-specific cover letter PDF.
argument-hint: "[JD URL or pasted JD text; folder name auto-derived as company_position]"
---

# Cover Letter Tailor Skill

Read `docs/resume.md` as a READ-ONLY golden dataset, tailor a cover letter to a job description, and generate a named PDF. The golden dataset is NEVER modified. Folder naming is fully automatic from the JD — no human-in-the-loop prompt. Folder naming is aligned with `/resume-tailor` so both skills write to the same `markdown/<folder_name>/` directory.

## Arguments

`$ARGUMENTS` is interpreted in priority order:

1. **URL** (`https://` / `http://`): fetched, JD extracted, folder name auto-derived as `<company>_<position>`.
2. **Pasted JD text**: parsed in place, folder name auto-derived as `<company>_<position>`.
3. **Plain folder name** (lowercase, underscore-delimited, e.g. `google_mle`): honored verbatim as an explicit override. JD is reused from `markdown/<name>/jd.md` if present, otherwise extracted from the preceding message or URL.
4. **Empty**: look for URL or JD text in the preceding message. If none, ask the user for a JD source (not a folder name).

Folder naming never requires user input when a JD is available.

## Workflow

### Step 1: Load Writing Standards

Read `docs/writing_style_guide.md` as the writing style reference. All generated text must comply with these rules.

### Step 2: Determine JD Source and Extract

Select the JD source in priority order:

1. If `$ARGUMENTS` is a plain folder name and `markdown/$ARGUMENTS/jd.md` already exists (e.g., from a prior `/resume-tailor` run), read that file and use its content. Set `<folder_name> = $ARGUMENTS` and skip Step 3.
2. Otherwise if `$ARGUMENTS` or the preceding message contains a URL, use that URL.
3. Otherwise if a JD text block is present in `$ARGUMENTS` or the preceding message, use that.
4. Otherwise ask the user to provide a JD URL or paste the JD text.

If a URL is selected:

1. Use `WebFetch` to retrieve the page content and extract the job description.
2. If WebFetch returns only the page title / company name (common on JS-rendered job boards like Ashby, Greenhouse, Lever, Workday, Loxo), fall back to **HTML inspection** before asking the user to paste:
   1. `curl -sS "<url>" -o /tmp/jd_page.html` to download the static HTML.
   2. Search the HTML for an embedded JSON hydration payload. Common keys by provider:
      - **Ashby** (`jobs.ashbyhq.com`): `descriptionPlainText`, `descriptionHtml`, `title`, `teamName`, `locationName`.
      - **Greenhouse** (`boards.greenhouse.io`): `<div id="content">`, often inline HTML.
      - **Lever** (`jobs.lever.co`): `data-qa="job-description"` blocks or JSON under `__NEXT_DATA__`.
      - **Loxo** (`app.loxo.co`): JSON under `__NEXT_DATA__`, or inline `"description"` / `"title"` / `"company"` keys.
      - **Workday** (`myworkdayjobs.com`): usually requires API call to `/jobs/{id}` endpoint; may be JS-rendered beyond this fallback's reach.
      - **Generic Next.js**: `<script id="__NEXT_DATA__" type="application/json">{...}</script>`.
      - **Generic Remix**: `window.__remixContext = {...}`.
   3. Extract the matching key using a small Python snippet. Example for Ashby:
      ```bash
      python3 -c "
      import re, json, pathlib
      src = pathlib.Path('/tmp/jd_page.html').read_text()
      m = re.search(r'\"descriptionPlainText\":\"((?:[^\"\\\\\\\\]|\\\\\\\\.)*)\"', src)
      if m: print(json.loads('\"' + m.group(1) + '\"'))
      "
      ```
      Use JSON-string decoding (`json.loads('\"' + raw + '\"')`) to handle `\\n`, `\\\"`, and `\\uXXXX` escapes correctly.
   4. If a payload is recovered, treat it as the JD text and continue. Clean up `/tmp/jd_page.html` after.
3. If HTML inspection also fails (unknown payload, auth-gated), inform the user and ask them to paste the JD directly.

Retain in memory: JD text, job title, employer/company name, source URL (if any), location (if available).

### Step 3: Derive Folder Name (automatic)

**Skip if `<folder_name>` was already set in Step 2** (plain folder name with existing `jd.md`).

**Skip if `$ARGUMENTS` is a plain folder name without existing `jd.md`.** In that case, `<folder_name> = $ARGUMENTS` verbatim, and Step 4 will archive the freshly extracted JD into that folder.

Otherwise derive `<folder_name> = <company>_<position>` from the JD, fully automatic, no user prompt:

**`<company>`** — employer name, pulled from the JD headline, "About [Company]" section, or `companyName` / `organization` key in extracted payloads. Normalize:
- Lowercase.
- Strip legal suffixes: `, inc`, `inc.`, `llc`, `l.l.c.`, `ltd`, `ltd.`, `corp`, `corporation`, `co.`, `gmbh`, `pte`, `ag`, `sa`.
- Strip punctuation and whitespace; concatenate multi-word names into one token.
- Examples: "CareBrain, Inc." → `carebrain`, "Open AI" → `openai`, "Two Sigma" → `twosigma`, "Ramp Business Corporation" → `ramp`.
- Never use the job-board host (`loxo`, `ashby`, `greenhouse`, `lever`) as the company.

**`<position>`** — role title, pulled from the JD headline or `title` key. Normalize to a compacted abbreviation:

1. Strip articles (`a`, `an`, `the`), punctuation, and parenthesized specializations. E.g., "Software Engineer (Backend, Payments)" → "Software Engineer".
2. Extract optional seniority prefix (apply first match):
   - "Senior" / "Sr." → `sr`
   - "Staff" → `staff`
   - "Principal" → `principal`
   - "Lead" → `lead`
   - "Junior" / "Jr." → `jr`
   - Otherwise no prefix.
3. Map the remaining role core to an acronym (case-insensitive; longest match wins):

    | Title phrase | Acronym |
    |---|---|
    | Software Engineer / Software Developer | `swe` |
    | Machine Learning Engineer / ML Engineer | `mle` |
    | AI Engineer | `aie` |
    | Applied Scientist | `as` |
    | Research Scientist | `rs` |
    | Research Engineer | `re` |
    | Data Scientist | `ds` |
    | Data Engineer | `de` |
    | Data Analyst | `da` |
    | Full Stack Engineer / Fullstack Engineer | `fse` |
    | Backend Engineer | `be` |
    | Frontend Engineer | `fe` |
    | Site Reliability Engineer | `sre` |
    | DevOps Engineer | `devops` |
    | Solutions Engineer / Solutions Architect | `sa` |
    | Product Manager | `pm` |
    | Engineering Manager | `em` |
    | Technical Program Manager | `tpm` |

4. If no table entry matches, fall back to a generated acronym: take the first letter of each content word, dropping a trailing "Engineer" / "Scientist" / "Manager" when it's the last token. E.g., "Quantitative Research Developer" → `qrd`, "Computer Vision Engineer" → `cve`.
5. Combine as `<seniority>_<acronym>` (drop the prefix segment if none). Examples:
   - "Machine Learning Engineer" → `mle`
   - "Senior Software Engineer" → `sr_swe`
   - "Staff Data Scientist" → `staff_ds`
   - "Principal ML Engineer" → `principal_mle`

**Final `<folder_name>`**: `<company>_<position>` (all lowercase, underscore-joined). Examples:
- "Machine Learning Engineer at Google" → `google_mle`
- "Senior Software Engineer, Stripe" → `stripe_sr_swe`
- "Staff Data Scientist — Databricks" → `databricks_staff_ds`
- "Computer Vision Engineer at Anduril Industries" → `anduril_cve`

This derivation is identical to `/resume-tailor` so both skills resolve to the same folder for a given JD.

Report the derived `<folder_name>` to the user in the final summary so they can verify.

### Step 4: Archive the JD

If `markdown/<folder_name>/jd.md` already exists, reuse it as-is (it was written by `/resume-tailor` or a prior cover letter run).

Otherwise create `markdown/<folder_name>/` if needed and write the extracted JD to `markdown/<folder_name>/jd.md`. Prepend a self-describing header:

```
# Job Description: <Title> — <Company>

- Company: <Company>
- Title: <Title>
- Location: <Location or "not specified">
- Source: <URL or "pasted">
- Fetched: <YYYY-MM-DD>

---

<raw JD text>
```

### Step 5: Read Golden Dataset as READ-ONLY

Read `docs/resume.md` to get the full professional history (~9274 chars, multi-page). Store the content for passing to the cover letter agent.

**DO NOT modify `docs/resume.md` under any circumstances.**

### Step 6: Delegate to Cover Letter Agent

Use the `Agent` tool with `subagent_type: coverletter` to generate the cover letter. Pass these instructions to the agent:

```
You are generating a cover letter tailored to a specific job description.

## Job Description
<paste the full JD text here>

## Golden Dataset (READ-ONLY source material)
<paste the full docs/resume.md content here>

## Output File
Write the tailored cover letter to: {PROJECT_ROOT}/markdown/<folder_name>/coverletter_generated.md

## Instructions
1. Read `docs/writing_style_guide.md` and enforce all writing rules
2. Select 2-3 most relevant roles and 3-5 strongest achievements from the golden dataset
3. Write in narrative paragraph form. Do NOT use bullet points
4. Weave JD-specific terminology naturally into paragraphs
5. Reference the company and role by name
6. Include quantifiable metrics from the golden dataset woven into narrative
7. Preserve all factual content. Do NOT fabricate experience, metrics, or credentials
8. Target 250-400 words (1500-2500 visible characters)
9. Write the tailored content to {PROJECT_ROOT}/markdown/<folder_name>/coverletter_generated.md using the Write tool
10. NEVER modify docs/resume.md. You are writing a NEW file only

## Cover Letter Structure (mandatory)
- H1: THOMAS TO (centered name)
- Contact line (same as resume)
- Date line (current date)
- Greeting: "Dear Hiring Manager,"
- Opening paragraph (2-3 sentences): State the role, express specific interest, one headline accomplishment
- Body paragraph 1 (3-4 sentences): Most relevant experience mapped to JD requirements with specific metrics
- Body paragraph 2 (3-4 sentences): Second cluster of relevant experience or technical skills alignment
- Optional body paragraph 3 (2-3 sentences): Only if a distinct third theme emerges from JD
- Closing paragraph (2-3 sentences): Reiterate fit, express interest in discussing further
- Sign-off: "Sincerely," followed by "Thomas To"

## Tense
- Current roles: present tense
- Prior roles: past tense

## Banned Words
can, may, just, that, very, really, literally, actually, certainly, probably, basically, could, maybe, delve, embark, enlightening, esteemed, shed light, craft, curating, imagine, realm, game-changer, unlock, discover, skyrocket, abyss, not alone, in a world where, revolutionize, disruptive, utilize, utilizing, dive deep, tapestry, illuminate, unveil, pivotal, intricate, elucidate, hence, furthermore, realm, however, harness, exciting, groundbreaking, cutting-edge, remarkable, it remains to be seen, glimpse into, navigating, landscape, stark, testament, in summary, in conclusion, moreover, boost, skyrocketing, opened up, powerful, inquiries, ever-evolving

## Formatting Rules
- No em dashes. Use commas, periods, or other standard punctuation only
- No semicolons
- No asterisks in output text
- No bullet points. Paragraphs only
- Active voice only ("Deployed" not "Was deployed")
```

After the agent completes, copy `coverletter_generated.md` to `coverletter_final.md` in the same folder:
```bash
cp markdown/<folder_name>/coverletter_generated.md markdown/<folder_name>/coverletter_final.md
```

### Step 7: Validate the Generated File

After the cover letter agent finishes, validate the tailored cover letter (NOT `docs/resume.md`):

```bash
python3 scripts/coverletter_pdf.py --validate-only --input markdown/<folder_name>/coverletter_final.md
```

If validation fails, delegate back to the cover letter agent with specific fix instructions. Do not attempt manual fixes.

### Step 8: Generate PDF from the Generated File

```bash
python3 scripts/coverletter_pdf.py --input markdown/<folder_name>/coverletter_final.md --output Thomas_To_CoverLetter_<folder_name>
```

PDF is written to `pdf/Thomas_To_CoverLetter_<folder_name>.pdf`.

### Step 9: Report Results

Summarize to the user:
- JD source (URL fetched, pasted text, or reused from existing jd.md)
- **Derived folder name** (so the user can verify the company / position parse)
- Key talking points selected (which roles, which achievements)
- Word count of the body content
- Output files:
  - JD archive: `markdown/<folder_name>/jd.md`
  - AI baseline: `markdown/<folder_name>/coverletter_generated.md`
  - Editable copy: `markdown/<folder_name>/coverletter_final.md`
  - PDF: `pdf/Thomas_To_CoverLetter_<folder_name>.pdf`
- Any validation warnings
- Confirm `docs/resume.md` was NOT modified
- Remind user: edit `coverletter_final.md` and re-run Step 8 to regenerate PDF

## Key References

| Resource | Path | Access |
|----------|------|--------|
| Golden dataset | `docs/resume.md` | **READ-ONLY** |
| Writing style | `docs/writing_style_guide.md` | READ-ONLY |
| Cover letter agent | `.claude/agents/coverletter.md` | Delegated |
| PDF script | `scripts/coverletter_pdf.py` | Execute |
| JD archive | `markdown/<folder_name>/jd.md` | READ or WRITE (new) |
| Generated markdown | `markdown/<folder_name>/coverletter_generated.md` | WRITE (new) |
| Editable markdown | `markdown/<folder_name>/coverletter_final.md` | WRITE (copy) |
| Generated PDF | `pdf/Thomas_To_CoverLetter_<folder_name>.pdf` | WRITE (new) |

## Boundaries

- Does NOT push to git or auto-commit
- Does NOT fabricate experience, metrics, or credentials
- Does NOT modify `docs/resume.md` under any circumstances
- Does NOT prompt the user for a folder name when a JD is available
- Escalates to user if content changes alter the factual record
- Batch-safe: each invocation reads the same immutable golden dataset and writes to independent output folders
