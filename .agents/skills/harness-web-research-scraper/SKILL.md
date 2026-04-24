---
name: harness-web-research-scraper
description: Use the LLM harness web tooling to collect web research into Markdown artifacts under artifacts/web-searches/. Use this skill whenever the user asks to search the web, scrape web pages, collect sources, browse for evidence, gather current information, or save browsing-backed research artifacts for later distillation. This skill should use harness-provided web/search/open/browser tools rather than custom HTTP scraping unless the user explicitly asks for script-based scraping.
---

# Harness Web Research Scraper

Use this skill to collect web research with the LLM harness web tools and save the results as source-oriented Markdown artifacts.

Default output root: `artifacts/web-searches/`
Default output format: Markdown
Default indexing step: refresh `artifacts/digests/artifact_inventory.json`

This skill collects sources. It does not write final analytical reports. Use `artifacts-to-json-distiller` after this skill to convert saved web-search artifacts into LLM-friendly JSON, then use `artifact-digest-report-writer` for stakeholder-facing Markdown reports.

## When to use this skill

Use this skill when the user asks to:

- search the web and save the results
- scrape or extract source material from web pages
- collect sources for a research task
- gather current evidence with browsing
- create local web-search artifacts for later distillation
- build a source set under `artifacts/`

Use browsing by default for current, factual, legal, financial, product, market, regulatory, or rapidly changing topics.

## Tooling rule

Use the web tooling provided by the active LLM harness, such as search, open, browser, or page extraction tools.

Do not write ad hoc HTTP scraping scripts or use direct network requests unless the user explicitly asks for script-based scraping.

## Workflow

1. Clarify scope only if the request is too broad to search responsibly.
2. Use harness web tooling to search, open relevant pages, and collect visible source content.
3. Track provenance for every source using `references/source-provenance.md`.
4. Save one Markdown file per research task under `artifacts/web-searches/<slug>.md`.
5. Follow the Markdown structure in `references/output-format.md`.
6. Keep the artifact source-oriented. Copy or lightly organize tool results instead of rewriting them into a synthetic essay.
7. Record blocked, paywalled, unavailable, partial, or search-only sources as limitations.
8. Refresh the artifact inventory after saving the Markdown:

```powershell
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py
```

9. Mention that the updated artifacts can now be digested with `artifacts-to-json-distiller`.

## Source handling

For each source, capture:

- title when available
- URL
- access timestamp
- source type
- relevance note
- extracted content, key snippets, or copied tool result
- limitations such as blocked page, paywall, partial content, or search-result-only evidence

Do not claim a source says something unless the opened page or search result supports it.

## Output behavior

Use this file path pattern:

```text
artifacts/web-searches/<topic-slug>.md
```

If the user gives a specific topic, use it for the slug. If not, create a short slug from the search task.

Avoid large crawls by default. For multi-page research, prefer a focused source set over exhaustive crawling.

## Relationship to downstream skills

After the inventory refresh:

- use `artifacts-to-json-distiller` to turn `artifacts/` into compact JSON
- use `artifact-digest-report-writer` to turn digest JSON into professional Markdown reports

## Safety and access limits

- Do not bypass access controls.
- Do not invent inaccessible page content.
- Do not summarize paywalled or blocked pages as if they were read.
- Record uncertainty and extraction limitations directly in the artifact.

