# Agents

This repo is set up around a small set of local skills under `.agents/skills/`.

## Workflow Guide

If the user are not sure where to start, roleplay as the `workflow-guide-assistant`.

Use it for questions like:

- how to use this repo
- which skill should I use next
- what is the sequence from `sources.txt` to reports
- what a file under `raw/` or `artifacts/` is for
- how to get unstuck in the current workflow stage

The guide is instructional. It explains the workflow, points to the right operational skill, and gives prompt examples. It does not replace:

- `source-intake-orchestrator`
- `harness-web-research-scraper`
- `artifacts-to-json-distiller`
- `artifact-digest-report-writer`

## Canonical Flow

1. Start with `sources.txt`.
2. Use `source-intake-orchestrator` to generate transcript and web-search artifacts and refresh the inventory.
3. Use `artifacts-to-json-distiller` to synthesize `artifacts/` into digest JSON.
4. Use `artifact-digest-report-writer` to turn digest JSON into a report.

For report-oriented web research requests, `harness-web-research-scraper` may still be the right entrypoint for collection. In that case it should collect the web artifacts first, refresh the inventory, and prepare the downstream distillation handoff without taking over the final report-writing step.
