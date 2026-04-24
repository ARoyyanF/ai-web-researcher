---
name: source-intake-orchestrator
description: Turn manually maintained sources.txt into populated local artifacts by categorizing URLs, extracting YouTube transcripts, collecting non-YouTube web sources, and refreshing artifact_inventory.json. Use this skill when the user asks to process sources.txt, ingest sources, turn source lists into artifacts, update artifacts from sources, or run the source intake workflow.
---

# Source Intake Orchestrator

Use this skill to turn the repo's manually curated `sources.txt` into local artifacts ready for downstream distillation and reporting.

Default input: `sources.txt`  
Default categorized outputs: `raw/youtube-url.txt`, `raw/other-url.txt`  
Default transcript outputs: `artifacts/transcripts/`, `artifacts/transcripts_clean/`  
Default web artifact output: `artifacts/web-searches/`  
Default inventory output: `artifacts/digests/artifact_inventory.json`

## When to use this skill

Use this skill when the user asks to:

- process or ingest `sources.txt`
- turn manually added sources into artifacts
- populate transcript and web-search artifacts from source URLs
- update artifacts and refresh the artifact inventory
- run the full source intake workflow

This skill orchestrates existing tools. Do not reimplement URL categorization or YouTube transcript extraction.

## Workflow

Read `references/workflow.md` before running or explaining the workflow.

The standard sequence is:

1. Treat `sources.txt` as the manually maintained source of truth.
2. Run `tools/categorize-sources.py` to split URLs into:
   - `raw/youtube-url.txt`
   - `raw/other-url.txt`
3. If `raw/youtube-url.txt` has URLs, run `tools/transcript-extractor.py` against it.
4. If `raw/other-url.txt` has URLs, use the `harness-web-research-scraper` skill and harness web tooling to create Markdown artifacts under `artifacts/web-searches/`.
5. Refresh `artifacts/digests/artifact_inventory.json`.
6. Recap counts, failures, fallbacks, skipped branches, and inventory status.

## Tooling rules

- Use `tools/categorize-sources.py` for categorization.
- Use `tools/transcript-extractor.py` for YouTube transcript extraction.
- Explicitly write SRT files to `artifacts/transcripts/` so they are indexed.
- Use the existing `harness-web-research-scraper` skill for non-YouTube web sources.
- Use the artifact inventory script from `artifacts-to-json-distiller` after artifact creation.
- Do not use ad hoc HTTP scraping unless the user explicitly asks for script-based scraping.

## Recap requirements

At the end, report:

- total source URLs found in `sources.txt`
- YouTube URL count
- other web URL count
- transcript extraction success and failure counts
- web collection success, failure, blocked, or partial extraction notes
- whether `artifact_inventory.json` was refreshed
- downstream next step, usually `artifacts-to-json-distiller`

## Failure handling

- If `sources.txt` is missing or empty, stop with a clear note.
- If one category has no URLs, skip that branch cleanly.
- If `yt-dlp` fails for some videos, preserve the transcript extractor recap and continue where possible.
- If web pages are blocked, paywalled, unavailable, or partially extracted, record that in the web-search Markdown artifact.
- Do not hide failures behind a successful inventory refresh.

