---
name: resume-response
description: Use when answering free-text application questions (e.g., "Why do you want to work here?") grounded in the golden dataset and a job description. Generates a 300-word-or-less response.
argument-hint: "[folder_name or JD URL] [prompt text, e.g. 'Why do you want to work here?']"
---

# Resume Response Skill

Read `docs/resume.md` as a READ-ONLY golden dataset, use a job description for context, and generate a short-form response to a free-text application question. The golden dataset is NEVER modified. Folder naming is fully automatic from the JD and aligned with `/resume-tailor` and `/coverletter-tailor`.

## Arguments

`$ARGUMENTS` is parsed to separate JD context from the prompt:

1. **Leading URL** (`https://` / `http://`): extracted as JD source. Everything after the URL is the prompt.
2. **Leading folder name** (first token matches `^[a-z][a-z0-9_]+$` AND the directory `markdown/<token>/` exists): treated as folder name. Everything after that token is the prompt.
3. **Otherwise**: the entire `$ARGUMENTS` is the prompt. JD context comes from a URL or pasted JD in the preceding message.
4. **Empty**: ask the user for both a prompt and a JD source.

If no prompt is identified after parsing, ask the user.

## Workflow

### Step 1: Load Writing Standards

Read `docs/writing_style_guide.md` as the writing style reference. All generated text must comply with these rules.

### Step 2: Parse Arguments

Parse `$ARGUMENTS` to separate JD context from prompt using the priority order above.

Validation:
- If `$ARGUMENTS` starts with a token matching `^[a-z][a-z0-9_]+$`, check whether `markdown/<token>/` exists as a directory. If yes, it is a folder name. If no, treat the entire string as the prompt.
- A URL is any token starting with `https://` or `http://`.
- Everything remaining after extracting a URL or folder name is the prompt.

### Step 3: Extract Job Description

Select the JD source in priority order:

1. If a folder name was identified and `markdown/<folder_name>/jd.md` exists, read that file and use its content. Skip Step 4.
2. If a URL was identified, use that URL.
3. If pasted JD text appears in `$ARGUMENTS` remainder or the preceding message, use that.
4. Otherwise ask the user to provide a JD URL, paste the JD text, or specify an existing folder name.

If a URL is selected:

1. Use `WebFetch` to retrieve the page content and extract the job description.
2. If WebFetch returns only the page title / company name (common on JS-rendered job boards like Ashby, Greenhouse, Lever, Workday, Loxo), fall back to **HTML inspection** before asking the user to paste:
   1. `curl -sS "<url>" -o /tmp/jd_page.html` to download the static HTML.
   2. Search the HTML for an embedded JSON hydration payload. Common keys by provider:
      - **Ashby** (`jobs.ashbyhq.com`): `descriptionPlainText`, `descriptionHtml`, `title`, `teamName`, `locationName`.
      - **Greenhouse** (`boards.greenhouse.io`): `<div id="content">`, often inline HTML.
      - **Lever** (`jobs.lever.co`): `data-qa="job-description"` blocks or JSON under `__NEXT_DATA__`.
      - **Loxo** (`app.loxo.co`): JSON under `__NEXT_DATA__`, or inline `"description"` / `"title"` / `"company"` keys.
      - **Workday** (`myworkdayjobs.com`): usually requires API call to `/jobs/{id}` endpoint.
      - **Generic Next.js**: `<script id="__NEXT_DATA__" type="application/json">{...}</script>`.
      - **Generic Remix**: `window.__remixContext = {...}`.
   3. Extract the matching key using a small Python snippet.
   4. If a payload is recovered, treat it as the JD text and continue. Clean up `/tmp/jd_page.html` after.
3. If HTML inspection also fails, inform the user and ask them to paste the JD directly.

Retain in memory: JD text, job title, employer/company name, source URL (if any), location (if available).

### Step 4: Derive Folder Name (automatic)

**Skip if `<folder_name>` was already set in Step 2 or Step 3.**

Otherwise derive `<folder_name> = <company>_<position>` from the JD, fully automatic, no user prompt:

**`<company>`** — employer name from the JD. Normalize:
- Lowercase.
- Strip legal suffixes: `, inc`, `inc.`, `llc`, `l.l.c.`, `ltd`, `ltd.`, `corp`, `corporation`, `co.`, `gmbh`, `pte`, `ag`, `sa`.
- Strip punctuation and whitespace; concatenate multi-word names into one token.

**`<position>`** — role title from the JD. Normalize to a compacted abbreviation:

1. Strip articles, punctuation, and parenthesized specializations.
2. Extract optional seniority prefix:
   - "Senior" / "Sr." → `sr`
   - "Staff" → `staff`
   - "Principal" → `principal`
   - "Lead" → `lead`
   - "Junior" / "Jr." → `jr`
3. Map the remaining role core to an acronym (longest match wins):

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

4. If no table entry matches, take the first letter of each content word (dropping trailing "Engineer" / "Scientist" / "Manager").
5. Combine as `<seniority>_<acronym>` (drop prefix if none).

**Final `<folder_name>`**: `<company>_<position>`.

This derivation is identical to `/resume-tailor` and `/coverletter-tailor` so all skills resolve to the same folder for a given JD.

### Step 5: Archive the JD

If `markdown/<folder_name>/jd.md` already exists, reuse it as-is.

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

### Step 6: Read Golden Dataset as READ-ONLY

Read `docs/resume.md` to get the full professional history. Store the content for passing to the response agent.

**DO NOT modify `docs/resume.md` under any circumstances.**

### Step 7: Derive Slug from Prompt

Generate a filesystem-safe slug from the prompt:

1. Lowercase the prompt
2. Remove all punctuation (`?`, `!`, `.`, `,`, `"`, `'`, `:`, `-`, `(`, `)`, etc.)
3. Remove stop words: a, an, the, is, are, do, does, your, you, what, how, with, to, for, in, of, on, at, by, and, or, us, about, me, my, we, our, has, have, been, was, were, tell, describe, explain, please
4. Take the first 5 remaining words
5. Join with underscores
6. Truncate at 50 characters (on a word boundary)

Output filename: `response_<slug>.md`

If `markdown/<folder_name>/response_<slug>.md` already exists, append `_v2`, `_v3`, etc. to avoid overwriting prior responses.

### Step 8: Delegate to Resume Response Agent

Use the `Agent` tool with `subagent_type: resume-response` to generate the response. Pass these instructions to the agent:

```
You are answering a free-text application question grounded in resume facts and a job description.

## Prompt (the question to answer)
<paste the prompt here>

## Job Description
<paste the full JD text here>

## Golden Dataset (READ-ONLY source material)
<paste the full docs/resume.md content here>

## Output File
Write the response to: {PROJECT_ROOT}/markdown/<folder_name>/response_<slug>.md

## Instructions
1. Read `docs/writing_style_guide.md` and enforce all writing rules
2. Answer the prompt in 300 words or fewer
3. Ground every claim in facts from the golden dataset. Do NOT fabricate experience, metrics, or credentials
4. Connect golden dataset experience to specific JD requirements where relevant
5. Name the company and role where natural
6. Use narrative paragraph form. No bullet points
7. Include at least 2 quantifiable metrics from the golden dataset
8. Write YAML frontmatter with: prompt, jd_source, date, word_count
9. Write the response to the specified output file using the Write tool
10. NEVER modify docs/resume.md
```

After the agent completes, validate the word count:
```bash
body=$(sed '1,/^---$/d' markdown/<folder_name>/response_<slug>.md | sed '/^$/d')
echo "$body" | wc -w
```

If word count exceeds 300, delegate back to the agent with instructions to trim.

### Step 9: Display and Report Results

Display the full response text in the conversation so the user can copy-paste immediately.

Summarize:
- Prompt answered
- JD source (URL fetched, pasted text, or reused from existing jd.md)
- **Derived folder name** (so user can verify)
- Word count
- Output file: `markdown/<folder_name>/response_<slug>.md`
- Confirm `docs/resume.md` was NOT modified

## Key References

| Resource | Path | Access |
|----------|------|--------|
| Golden dataset | `docs/resume.md` | **READ-ONLY** |
| Writing style | `docs/writing_style_guide.md` | READ-ONLY |
| Response agent | `.claude/agents/resume-response.md` | Delegated |
| JD archive | `markdown/<folder_name>/jd.md` | READ or WRITE (new) |
| Generated response | `markdown/<folder_name>/response_<slug>.md` | WRITE (new) |

## Boundaries

- Does NOT push to git or auto-commit
- Does NOT fabricate experience, metrics, or credentials
- Does NOT modify `docs/resume.md` under any circumstances
- Does NOT prompt the user for a folder name when a JD is available
- Does NOT generate PDFs (responses are short-form text only)
- Escalates to user if content changes alter the factual record
- Batch-safe: each invocation reads the same immutable golden dataset and writes to independent output files
