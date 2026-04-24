# AI Web Researcher

Small local workflow for turning curated source URLs into transcript and web research artifacts, then distilling those artifacts into structured JSON and reports for downstream LLM use.

## Not Sure Where To Start?

Use the workflow guide skill at [.agents/skills/workflow-guide-assistant/SKILL.md](.agents/skills/workflow-guide-assistant/SKILL.md).

It is the repo's orientation layer for new users. Ask it things like:

- `How do I use this repo from sources.txt to a final report?`
- `Which skill should I use next?`
- `What is artifacts/digests/ for?`

The guide stays instructional and points you to the right operational skill for the next step.

## What this repo does

This repo has a staged workflow:

1. Start with `sources.txt`
2. Generate transcript and web-search artifacts
3. Refresh and inspect the artifact inventory
4. Distill `artifacts/` into compact JSON
5. Turn digests into reports when needed

## Repo layout

```text
.
|-- .agents/
|   `-- skills/
|       |-- artifact-digest-report-writer/
|       |-- artifacts-to-json-distiller/
|       |-- harness-web-research-scraper/
|       |-- source-intake-orchestrator/
|       `-- workflow-guide-assistant/
|-- artifacts/
|   |-- digests/
|   |-- reports/
|   |-- transcripts/
|   |-- transcripts_clean/
|   `-- web-searches/
|-- outputs/
|   |-- analytical-report.md
|   |-- critical-review.md
|   |-- decision-memo.md
|   `-- executive-brief.md
|-- raw/
|   |-- other-url.txt
|   `-- youtube-url.txt
|-- sources.txt
`-- tools/
    |-- categorize-sources.py
    `-- transcript-extractor.py
```

## Requirements

- Python 3.11+
- `yt-dlp` available on `PATH`

Install `yt-dlp` if needed:

```powershell
pip install yt-dlp
```

## Workflow entrypoints

The main workflow now starts from `sources.txt`, not `raw/url.csv`.

- `workflow-guide-assistant`: explains the workflow and tells you which skill to use next
- `source-intake-orchestrator`: turns `sources.txt` into transcript and web-search artifacts
- `artifacts-to-json-distiller`: turns `artifacts/` into one LLM-friendly JSON digest
- `artifact-digest-report-writer`: turns digest JSON into Markdown reports

If you want to run transcript extraction directly, `tools/transcript-extractor.py` still works and writes:

- raw subtitle files to `artifacts/transcripts/`
- cleaned Markdown transcripts to `artifacts/transcripts_clean/`

## Skill: artifacts-to-json-distiller

The local skill lives at [.agents/skills/artifacts-to-json-distiller/SKILL.md](.agents/skills/artifacts-to-json-distiller/SKILL.md).

Its job is to digest everything under `artifacts/` into one JSON document that another LLM can use without wading through every raw file.

The skill is designed to:

- scan `artifacts/` recursively
- include supported text-like files such as `.md`, `.txt`, `.json`, and `.csv`
- record skipped or unreadable files instead of silently dropping them
- preserve provenance, confidence, contradictions, and open questions
- write a compact JSON digest under `artifacts/digests/`

### How to use the skill

When working with Codex or another agent that supports local skills, ask for the artifact digest directly. The skill should trigger from requests about digesting, synthesizing, analyzing, or compressing files in `artifacts/`.

Example prompts:

```text
Digest everything in artifacts/ into one JSON file for downstream LLM analysis.
```

```text
Create a structured JSON knowledge bundle from artifacts/ with themes, claims, contradictions, gaps, and an llm_brief section.
```

```text
Analyze all artifacts and produce an LLM-friendly JSON digest. Preserve source paths, timestamps when available, and confidence labels.
```

### Skill workflow

The skill starts by building an inventory JSON:

```powershell
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py
```

That writes:

```text
artifacts/digests/artifact_inventory.json
```

The inventory includes:

- included and skipped files
- file type and size
- short summaries
- headings for Markdown files
- timestamp anchors when available

After that, the skill reads the relevant sources and writes a synthesized JSON digest with fields such as:

- `meta`
- `corpus_overview`
- `source_inventory`
- `themes`
- `entities`
- `claims`
- `contradictions`
- `timelines`
- `implications`
- `open_questions`
- `gaps`
- `llm_brief`

## Skill: workflow-guide-assistant

The workflow guide skill lives at [.agents/skills/workflow-guide-assistant/SKILL.md](.agents/skills/workflow-guide-assistant/SKILL.md).

Its job is to help users navigate the repo without taking over the operational work.

Use it when you want to:

- understand the sequence from `sources.txt` to reports
- figure out which skill to use next
- understand what a file or artifact directory is for
- get unstuck in the current workflow stage

Example prompts:

```text
How do I use this repo from sources.txt to a final report?
```

```text
I have files in artifacts/digests. Which skill should I use now?
```

```text
What is the difference between artifacts/transcripts_clean and artifacts/digests?
```

## Skill: source-intake-orchestrator

The source intake skill lives at [.agents/skills/source-intake-orchestrator/SKILL.md](.agents/skills/source-intake-orchestrator/SKILL.md).

Its job is to turn the manually maintained `sources.txt` file into populated local artifacts.

Use it when you want to:

- categorize URLs from `sources.txt`
- extract YouTube transcripts into `artifacts/transcripts/` and `artifacts/transcripts_clean/`
- collect non-YouTube sources into `artifacts/web-searches/`
- refresh `artifacts/digests/artifact_inventory.json`

Example prompts:

```text
Process sources.txt into transcript and web-search artifacts, then refresh the artifact inventory.
```

```text
Run the source intake workflow. Use the existing categorizer and transcript extractor, collect other URLs as web artifacts, and recap failures.
```

Core commands used by the skill:

```powershell
python tools/categorize-sources.py sources.txt
python tools/transcript-extractor.py raw/youtube-url.txt --output-dir artifacts/transcripts --clean-output-dir artifacts/transcripts_clean --continue-on-error
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py
```

## Skill: harness-web-research-scraper

The web research skill lives at [.agents/skills/harness-web-research-scraper/SKILL.md](.agents/skills/harness-web-research-scraper/SKILL.md).

Its job is to use the LLM harness web tooling to collect source-oriented web research into Markdown files under `artifacts/web-searches/`.

By default it is a source-collection skill. If the user's real deliverable is a stakeholder-facing Markdown report, it should still collect the web artifacts first, refresh the inventory, and hand off the relevant newly created or directly relevant artifacts to `artifacts-to-json-distiller` so `artifact-digest-report-writer` has digest-ready inputs.

Use it when you want to:

- search the web and save the sources
- open pages and preserve visible source material
- collect current evidence for later distillation
- record blocked, paywalled, partial, or search-only sources

Example prompts:

```text
Search the web for recent sources about AI's effect on entry-level hiring and save the source collection under artifacts/web-searches/. Refresh the artifact inventory afterward.
```

```text
Open these URLs, extract the visible source material into a Markdown artifact, and record any blocked pages or partial extraction issues.
```

```text
Collect sources for a web-backed research note on the current software engineering job market. Keep the artifact factual, not a final report.
```

```text
Research the current entry-level software job market and prepare the inputs for a stakeholder Markdown brief. Save the web artifact, refresh inventory, and hand off the relevant artifacts for distillation.
```

Default output path pattern:

```text
artifacts/web-searches/<topic-slug>.md
```

After saving web-search artifacts, refresh the inventory:

```powershell
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py
```

## Skill: artifact-digest-report-writer

The report writer skill lives at [.agents/skills/artifact-digest-report-writer/SKILL.md](.agents/skills/artifact-digest-report-writer/SKILL.md).

Its job is to turn JSON digests from `artifacts/digests/` into professional Markdown reports under `artifacts/reports/`.

The skill supports four report variants:

- `executive_brief`
- `analytical_report`
- `critical_review`
- `decision_memo`

It reads digest JSON first. If the digest is too thin or lacks citation context, it can inspect the original artifact paths referenced by the digest or inventory and record that fallback in `Source Notes`.

### Report examples

```text
Create an executive brief from artifacts/digests/. Keep it concise and cite the source artifacts where available.
```

```text
Write a critical review from artifacts/digests/. Focus on evidence quality, contradictions, weak claims, bias, and missing context.
```

```text
Turn the artifact digest into a decision memo with recommendation, options considered, tradeoffs, risks, and next actions.
```

```text
Create a holistic analytical report from artifacts/digests/. If the digest is thin, inspect the referenced original artifacts and list fallback reads in Source Notes.
```

Default output paths:

- `artifacts/reports/executive-brief.md`
- `artifacts/reports/analytical-report.md`
- `artifacts/reports/critical-review.md`
- `artifacts/reports/decision-memo.md`

## Example workflow

1. Add links to `sources.txt`
2. If you need orientation, ask `workflow-guide-assistant` what the next step should be
3. Use the source intake skill to categorize URLs, extract transcripts, collect web artifacts, and refresh the inventory
4. Ask the distiller skill to digest `artifacts/` into one JSON knowledge bundle
5. Ask the report writer skill for the report variant you need

## Notes

- `artifacts/` and `raw/` are gitignored in the current repo setup.
- The skill is local to this repo under `.agents/skills/`.
- The distiller is intentionally JSON-only. Use the report writer skill when you want stakeholder-facing Markdown.
- The web research skill depends on the active LLM harness web tools; it does not bundle a custom scraper script.
