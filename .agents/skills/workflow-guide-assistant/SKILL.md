---
name: workflow-guide-assistant
description: Help users understand and navigate this repo's agentic workflow from sources.txt to final reports. Use this skill when the user asks how to use the workflow, which skill to use next, how files in artifacts/ relate to each other, how to go from sources to transcripts to digests to reports, or how to get unstuck in the current stage.
---

# Workflow Guide Assistant

Use this skill to orient the user inside the repo workflow. This is an instructional skill. It explains the stages, points to the right operational skill, and gives summonable prompt examples. It does not replace the operational skills.

## When to use this skill

Use this skill when the user asks:

- how to use this repo
- how the agentic workflow works
- which skill to use next
- what a file or artifact folder is for
- how to go from `sources.txt` to a report
- how to troubleshoot a stuck workflow step

Read `references/workflow-map.md` before answering.

## Response behavior

When guiding the user:

- identify their current stage from the files or request they mention
- state the next input or artifact they need
- point to the exact operational skill to use next
- give one or two prompt examples they can use immediately
- keep the explanation short and concrete

Stay instructional. Do not absorb the behavior of:

- `source-intake-orchestrator`
- `harness-web-research-scraper`
- `artifacts-to-json-distiller`
- `artifact-digest-report-writer`

## Canonical workflow

The standard repo flow is:

1. Curate `sources.txt`.
2. Use `source-intake-orchestrator` to split sources and generate transcript and web-search artifacts.
3. Refresh and inspect `artifacts/digests/artifact_inventory.json`.
4. Use `artifacts-to-json-distiller` to create a compact JSON digest.
5. Use `artifact-digest-report-writer` to create the report variant the user wants.

Keep this canonical flow intact. If the user enters through a report-oriented web research request, you may explain that `harness-web-research-scraper` can prepare digest-ready inputs by collecting sources first and then delegating relevant distillation work, but the final Markdown writing still belongs to `artifact-digest-report-writer`.

## File orientation

Be ready to explain the role of:

- `sources.txt`
- `raw/youtube-url.txt`
- `raw/other-url.txt`
- `artifacts/transcripts/`
- `artifacts/transcripts_clean/`
- `artifacts/web-searches/`
- `artifacts/digests/`
- `artifacts/reports/`

## Troubleshooting guidance

Call out likely causes and the next check to make when the user reports:

- no URLs found
- transcript extraction failures
- blocked or partial web pages
- refreshed inventory but missing artifacts
- digest too thin for a strong report

Prefer the smallest useful next action over a long explanation.
