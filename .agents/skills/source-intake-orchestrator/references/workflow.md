# Source Intake Workflow

This workflow turns `sources.txt` into local artifacts.

## Inputs and outputs

- Source list: `sources.txt`
- YouTube URL list: `raw/youtube-url.txt`
- Other URL list: `raw/other-url.txt`
- Raw transcript SRTs: `artifacts/transcripts/`
- Clean transcript Markdown: `artifacts/transcripts_clean/`
- Web source Markdown: `artifacts/web-searches/`
- Artifact inventory: `artifacts/digests/artifact_inventory.json`

## Step 1: categorize sources

Run:

```powershell
python tools/categorize-sources.py sources.txt
```

This script handles blank lines and `#` comments. It writes YouTube URLs to `raw/youtube-url.txt` and all other URLs to `raw/other-url.txt`.

After categorization, count non-empty lines in both output files for the final recap.

## Step 2: extract YouTube transcripts

If `raw/youtube-url.txt` contains URLs, run:

```powershell
python tools/transcript-extractor.py raw/youtube-url.txt --output-dir artifacts/transcripts --clean-output-dir artifacts/transcripts_clean --continue-on-error
```

The extractor defaults to 20 workers, English subtitles, auto-generated subtitles, and 30-second timestamp grouping for clean Markdown.

Record the extractor recap in the final response, especially:

- total queued URLs
- successful extractions
- failed extractions
- clean Markdown files written
- clean Markdown failures
- any subtitle source or format fallback notes

If the file is empty, skip this step and say no YouTube URLs were queued.

## Step 3: collect non-YouTube web sources

If `raw/other-url.txt` contains URLs, use the `harness-web-research-scraper` skill.

Follow its output contract and provenance rules:

- save Markdown under `artifacts/web-searches/`
- include URL, source title when available, access timestamp, source type, relevance, and limitations
- record blocked, paywalled, unavailable, partial, or search-only sources
- keep the artifact source-oriented instead of writing a polished report

Prefer one Markdown artifact for the current intake run unless the user asks for separate topic files.

If `raw/other-url.txt` is empty, skip this step and say no non-YouTube URLs were queued.

## Step 4: refresh artifact inventory

Run:

```powershell
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py
```

This refreshes:

```text
artifacts/digests/artifact_inventory.json
```

## Final recap format

Keep the final response short but specific:

- `sources.txt` URL count
- YouTube URL count and transcript result
- other URL count and web collection result
- artifact paths updated
- inventory refresh status
- failures, fallbacks, blocked pages, or skipped branches

Mention that the updated corpus can be digested next with `artifacts-to-json-distiller`.

