---
name: artifacts-to-json-distiller
description: Distill everything under artifacts/ into one compact, LLM-friendly JSON document with provenance, confidence, contradictions, and gaps. Use this skill whenever the user asks to digest, synthesize, summarize, analyze, compare, or compress files in artifacts/, transcripts, notes, extracted documents, or mixed research artifacts into structured JSON for downstream model use. Trigger even if the user asks for a "report" or "summary" if the real goal is a machine-readable knowledge bundle rather than polished prose.
---

# Artifacts-to-JSON Distiller

Use this skill to turn a local artifact corpus into one structured JSON digest that another LLM can consume safely and efficiently.

The default input root is `artifacts/`.
The default output is one JSON file in `artifacts/digests/`.
Do not produce Markdown or DOCX unless the user explicitly overrides the format.

## What this skill is for

Use this skill when the user wants to:

- digest a folder full of artifacts into a single knowledge bundle
- compress many transcripts, notes, CSVs, JSON files, or mixed text artifacts into JSON
- preserve provenance and uncertainty for downstream LLM workflows
- identify themes, claims, contradictions, timelines, and gaps across many local files

This skill is especially appropriate when the user says things like:

- "turn this folder into an LLM friendly json"
- "digest everything in artifacts"
- "build a structured knowledge base from these files"
- "summarize these transcripts for another model"
- "extract themes and contradictions from all artifacts"

## Workflow

Follow this sequence.

1. Discover the corpus under `artifacts/` recursively.
2. Run the helper inventory script before deep synthesis:

```powershell
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py
```

If the user wants a different root or output path, pass explicit arguments:

```powershell
python .agents/skills/artifacts-to-json-distiller/scripts/build_artifact_inventory.py --root <input-root> --output <output-json>
```

3. Read the generated inventory JSON first. Use it to understand:
- which files were included
- which files were skipped
- file types and sizes
- short previews and headings
- possible anchors such as timestamps

4. Read the source files that matter most for synthesis. Do not blindly load every large file if the inventory already tells you which ones are irrelevant or redundant.
5. Produce one JSON digest that follows the schema in `references/json-schema.md`.
6. Write the final digest to `artifacts/digests/<slug>.json` unless the user specifies another path.

## Supported inputs

Treat these as first-class inputs:

- `.md`
- `.txt`
- `.json`
- `.csv`

For unsupported or unreadable files:

- do not fail the whole task
- record them in `source_inventory`
- add a corresponding note in `gaps`

## Output contract

Always emit one top-level JSON object with these fields:

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

Read `references/json-schema.md` before writing the final JSON.

## Grounding rules

Read `references/evidence-rubric.md` before drafting the digest.

These distinctions matter:

- `evidence`: directly stated in source artifacts
- `synthesis`: cross-source interpretation grounded in multiple sources
- `inference`: plausible conclusion that is not directly established

For every nontrivial claim:

- include provenance
- include confidence
- include anchors when available, such as transcript timestamps or section headers

Do not treat repeated talking points across similar sources as independent confirmation unless the sources contribute distinct evidence.

## Quality bar

Optimize for downstream model usefulness.

- Be compact.
- Prefer distilled facts over long excerpts.
- Preserve uncertainty.
- Surface contradictions instead of smoothing them away.
- Separate what the corpus says from what you infer about it.
- Keep numbers, dates, names, and quoted phrases exact when you include them.

## Writing the final JSON

The final JSON should feel like a reusable knowledge bundle, not a prose essay.

- Keep string values concise.
- Keep arrays high signal.
- Avoid giant copied passages.
- Make `llm_brief` a compact downstream handoff with the minimum context another model needs to reason well.

## Example task

User request:
"Digest everything in artifacts into one JSON file another LLM can use for analysis."

Expected response shape:

- Run the inventory script.
- Inspect the included files and important sources.
- Write one JSON digest under `artifacts/digests/`.
- Mention skipped or unsupported files.

