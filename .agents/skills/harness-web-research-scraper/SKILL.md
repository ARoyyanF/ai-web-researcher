---
name: harness-web-research-scraper
description: Use the LLM harness web tooling to collect web research into Markdown artifacts under artifacts/web-searches/. Use this skill whenever the user asks to search the web, scrape web pages, collect sources, browse for evidence, gather current information, or save browsing-backed research artifacts for later distillation. This skill should use harness-provided web/search/open/browser tools rather than custom HTTP scraping unless the user explicitly asks for script-based scraping.
---

# Harness Web Research Scraper

Use this skill to collect web research with the LLM harness web tools and save the results as source-oriented Markdown artifacts.

Default output root: `artifacts/web-searches/`
Default output format: Markdown
Default indexing step: refresh `artifacts/digests/artifact_inventory.json`

This skill collects sources by default. It does not write final analytical reports. For ordinary research requests, use `artifacts-to-json-distiller` after this skill to convert saved web-search artifacts into LLM-friendly JSON, then use `artifact-digest-report-writer` for stakeholder-facing Markdown reports.

When the user's real deliverable is a stakeholder-facing Markdown report, brief, memo, review, or similar piece of writing that maps to `artifact-digest-report-writer`, this skill should switch into a report-preparation mode:

- collect and save the relevant web-search artifact first
- refresh `artifacts/digests/artifact_inventory.json`
- spawn one or more relevant `artifacts-to-json-distiller` subagents to create the digest JSON needed for the requested writing
- keep the final Markdown writing as a downstream `artifact-digest-report-writer` step

## When to use this skill

Use this skill when the user asks to:

- search the web and save the results
- scrape or extract source material from web pages
- collect sources for a research task
- gather current evidence with browsing
- create local web-search artifacts for later distillation
- build a source set under `artifacts/`

Use browsing by default for current, factual, legal, financial, product, market, regulatory, or rapidly changing topics.

If the user asks for web research in service of a final Markdown report, brief, memo, review, or other report-like writing, still use this skill first for the web collection step, then follow the report-preparation branch below.

## Tooling rule

Use the web tooling provided by the active LLM harness, such as search, open, browser, or page extraction tools.

Do not write ad hoc HTTP scraping scripts or use direct network requests unless the user explicitly asks for script-based scraping.

## Workflow

Before you start, decide which mode applies:

- `source collection mode`: the user wants saved web research artifacts or source gathering only
- `report-preparation mode`: the user wants web research whose real deliverable is a stakeholder-facing Markdown report that should later be written with `artifact-digest-report-writer`

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

## Report-Preparation Branch

Use this branch only when the user's real deliverable is a Markdown report or other writing that belongs to `artifact-digest-report-writer`.

After the web-search artifact is saved and the inventory is refreshed:

1. Spawn one or more subagents to run the relevant `artifacts-to-json-distiller` work.
2. Scope the distillation to the newly created or directly relevant artifacts for the requested report, not the full `artifacts/` corpus by default.
3. Instruct the subagent to produce digest JSON that is ready for the downstream report-writing step.
4. Return in a digest-ready state for `artifact-digest-report-writer`.

Do not use this branch for ordinary source-gathering requests.

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

In report-preparation mode:

- this skill owns source collection and inventory refresh
- spawned `artifacts-to-json-distiller` subagents own digest creation only
- `artifact-digest-report-writer` remains the only skill responsible for writing the final Markdown deliverable

## End-of-turn behavior

Close the turn by being proactive about the next step.

- Always tell the user what artifact was created or updated and whether the inventory was refreshed.
- In `source collection mode`, always suggest concrete next prompts the user can send next. Be eager here: do not wait for the user to ask what to do next.
- In `source collection mode`, prefer 2 to 4 short, copy-ready prompt suggestions tailored to the work that was just saved.
- In `source collection mode`, bias the suggestions toward the canonical repo flow:
  - first suggest `artifacts-to-json-distiller` when the research artifact is ready for synthesis
  - then suggest `artifact-digest-report-writer` when a digest already exists or is likely to be the next step
  - include one task-specific follow-up prompt when it would help, such as broadening the source set, focusing the search, or comparing subtopics
- Phrase the suggestions as direct user prompts, not abstract advice.
- If the user seems to be exploring loosely, still end with suggested prompts instead of a generic "let me know if you want more."

In `report-preparation mode`:

- say that the research artifact was saved
- say whether `artifact_inventory.json` was refreshed
- say that relevant distillation was delegated or prepared through `artifacts-to-json-distiller`
- point explicitly to `artifact-digest-report-writer` as the next step once the digest exists
- do not imply that this skill itself writes the final report

Example closing pattern:

```text
Saved research to artifacts/web-searches/<slug>.md and refreshed artifacts/digests/artifact_inventory.json.

Next prompts you can use:
- Distill everything under artifacts/ into a JSON digest focused on this research.
- Write a stakeholder-facing Markdown report from the latest digest.
- Gather 5 more current sources specifically about <subtopic>.
```

## Safety and access limits

- Do not bypass access controls.
- Do not invent inaccessible page content.
- Do not summarize paywalled or blocked pages as if they were read.
- Record uncertainty and extraction limitations directly in the artifact.
