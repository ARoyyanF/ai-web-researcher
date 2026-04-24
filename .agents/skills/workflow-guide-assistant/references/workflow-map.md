# Workflow Map

This repo is organized as a staged workflow. Use this map to guide users toward the right next skill.

## Stage 1: collect sources

User state:
- they are gathering links or asking where to start

Primary input:
- `sources.txt`

What it is:
- the manual source list for the repo
- one URL per line

Recommended next skill:
- `source-intake-orchestrator`

Example prompts:
- `Process sources.txt into transcript and web-search artifacts, then refresh the artifact inventory.`
- `Run the source intake workflow and recap failures or skipped branches.`

Common issues:
- `sources.txt` is empty
- URLs are malformed
- the user expects artifacts before source intake has run

## Stage 2: source intake and artifact creation

User state:
- they have `sources.txt` and want transcripts or source artifacts
- they mention `raw/youtube-url.txt`, `raw/other-url.txt`, or transcript outputs

Key outputs:
- `raw/youtube-url.txt`
- `raw/other-url.txt`
- `artifacts/transcripts/`
- `artifacts/transcripts_clean/`
- `artifacts/web-searches/`
- `artifacts/digests/artifact_inventory.json`

Primary skill:
- `source-intake-orchestrator`

Supporting skill:
- `harness-web-research-scraper` when the user wants standalone web collection outside the intake flow

Example prompts:
- `Use source-intake-orchestrator to process sources.txt and update artifacts.`
- `Collect web research into artifacts/web-searches/ and refresh the inventory.`

Common issues:
- `yt-dlp` missing from `PATH`
- transcript extraction failures for some URLs
- blocked, paywalled, or partial web pages
- inventory refreshed but artifacts were not actually generated

## Stage 3: digest artifacts into JSON

User state:
- they have artifacts and want structured synthesis
- they mention `artifacts/digests/` or `artifact_inventory.json`

Primary skill:
- `artifacts-to-json-distiller`

Expected output:
- one compact JSON digest under `artifacts/digests/`

Example prompts:
- `Digest everything in artifacts/ into one JSON file for downstream LLM analysis.`
- `Create a structured JSON knowledge bundle from artifacts/ with provenance, confidence, contradictions, and gaps.`

Common issues:
- source corpus is too thin
- unsupported files were skipped
- user wants prose, but the distiller is JSON-only

## Stage 4: write reports from digests

User state:
- they already have digest JSON and want a human-facing document
- they mention `artifacts/reports/` or ask for a brief, memo, or critique

Primary skill:
- `artifact-digest-report-writer`

Supported variants:
- `executive_brief`
- `analytical_report`
- `critical_review`
- `decision_memo`

Example prompts:
- `Create an executive brief from artifacts/digests/ and cite the source artifacts where available.`
- `Write a critical review from artifacts/digests/ focused on evidence quality, contradictions, and missing context.`

Common issues:
- digest lacks enough evidence detail
- user wants stronger citations than the digest currently carries
- the report is weak because the artifact set is incomplete upstream

## Quick file guide

- `sources.txt`: starting point for manually curated URLs
- `raw/youtube-url.txt`: YouTube URLs split out of the source list
- `raw/other-url.txt`: non-YouTube URLs split out of the source list
- `artifacts/transcripts/`: raw subtitle `.srt` files
- `artifacts/transcripts_clean/`: cleaned Markdown transcripts for model use
- `artifacts/web-searches/`: source-oriented Markdown web research artifacts
- `artifacts/digests/`: inventory and JSON digest outputs
- `artifacts/reports/`: final Markdown reports

## Routing rule

When the user asks broad workflow questions, answer in this shape:

1. State where they are in the workflow.
2. State the next skill to use.
3. Give one or two exact prompts they can send next.
4. Mention the most likely failure point only if it is relevant.

