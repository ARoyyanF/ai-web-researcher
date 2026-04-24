---
name: artifact-digest-report-writer
description: Turn JSON digests in artifacts/digests/ into professional Markdown reports, briefs, memos, and critical reviews. Use this skill whenever the user asks to create a report, executive brief, analytical report, holistic document, critical review, insight memo, decision memo, or professional write-up from artifact digests, artifact_inventory.json, or JSON knowledge bundles. Prefer this skill after artifacts-to-json-distiller has produced structured digest JSON.
---

# Artifact Digest Report Writer

Use this skill to write professional Markdown reports from JSON digests under `artifacts/digests/`.

Default input root: `artifacts/digests/`
Default output root: `artifacts/reports/`
Default output format: Markdown only

This is a downstream companion to `artifacts-to-json-distiller`. Use digest JSON as the main source of truth, then inspect original artifacts only when the digest lacks enough evidence, context, or citation detail.

## When to use this skill

Use this skill when the user asks for:

- a professional report from artifact digests
- an executive brief, decision memo, analytical report, or critical review
- a holistic document based on `artifacts/digests/`
- a stakeholder-ready synthesis from a JSON knowledge bundle
- an accurate, critical-thinking report with citations and caveats

If the user asks for JSON distillation first, use `artifacts-to-json-distiller` before this skill.

## Workflow

1. Discover digest files with `artifacts/digests/*.json`.
2. Prefer the most relevant non-inventory digest.
3. Treat `artifact_inventory.json` as an index, not a full analytical digest, unless it is the only digest available.
4. Read `references/report-variants.md` and select the variant that best matches the user's wording.
5. Read `references/evidence-style.md` before drafting.
6. Inspect original artifact paths referenced by the digest only when:
- the digest has thin evidence
- citation anchors are missing
- a claim needs context before it can be written accurately
- the user asks for especially critical or detailed treatment
7. Write one Markdown report to `artifacts/reports/<variant-name>.md` unless the user specifies another path.
8. Include a `Source Notes` section listing digest files used and any original artifacts inspected.

## Variant selection

Use these defaults:

- `executive_brief`: user asks for brief, summary, leadership update, stakeholder summary, concise report, or key takeaways
- `analytical_report`: user asks for report, holistic document, full analysis, synthesis, or comprehensive write-up
- `critical_review`: user asks for critique, skeptical review, evidence quality, bias, contradictions, weak claims, or critical thinking
- `decision_memo`: user asks for recommendation, decision, strategy, options, tradeoffs, next steps, or what to do

If the user asks for multiple variants, generate each requested report as a separate Markdown file.

## Grounding rules

Every report should be accurate before it is elegant.

- Cite digest files and source artifact paths where available.
- Label direct evidence, synthesis, and inference clearly when the distinction matters.
- Do not overstate claims with low confidence.
- Do not treat repeated claims as independently verified unless the digest shows distinct evidence.
- Surface contradictions, missing context, and uncertainty.
- Keep numbers, dates, names, and quoted phrases exact when you include them.
- Avoid generic filler and inflated certainty.

## Report quality

Write like a sharp analyst, not a transcript summarizer.

- Lead with the most decision-relevant insight.
- Convert raw findings into implications.
- Separate what the digest supports from what it merely suggests.
- Include practical caveats.
- Keep the structure professional and scannable.
- Avoid padding sections that have little evidence.

## Output files

Use these default filenames:

- `artifacts/reports/executive-brief.md`
- `artifacts/reports/analytical-report.md`
- `artifacts/reports/critical-review.md`
- `artifacts/reports/decision-memo.md`

Create `artifacts/reports/` if it does not exist.

## Source notes

End each report with `## Source Notes`.

Include:

- digest JSON files used
- original artifacts inspected as fallback
- limitations caused by missing, thin, or inventory-only digests

If only `artifact_inventory.json` exists, say that the report is based on inventory previews and should be treated as a preliminary source map, not a full analytical synthesis.

