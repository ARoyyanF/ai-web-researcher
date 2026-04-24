# Evidence Style

Use this guide to keep reports accurate, useful, and appropriately skeptical.

## Source hierarchy

Use sources in this order:

1. Analytical digest JSON files in `artifacts/digests/`
2. `artifact_inventory.json` as an index or fallback
3. Original artifacts referenced by paths in the digest or inventory

When multiple digest files exist, prefer non-inventory digests that include fields such as:

- `themes`
- `claims`
- `contradictions`
- `implications`
- `open_questions`
- `llm_brief`

## Citation style

Use compact inline citations.

Examples:

- `(digest: artifacts/digests/jobs-ai-digest.json)`
- `(source: artifacts/transcripts_clean/example.md, 03:35)`
- `(inventory: artifacts/digests/artifact_inventory.json)`

If a claim comes from a digest item that already cites a source artifact, cite both when useful:

```text
The corpus repeatedly frames entry-level hiring as structurally weaker, but the evidence appears mostly commentary-based rather than primary-data-based (digest: artifacts/digests/jobs-ai-digest.json; source: artifacts/transcripts_clean/Entry-Level Jobs are Dead... Now What？.md, 00:00).
```

## Evidence labels

Use plain language in the report:

- "The digest directly states..."
- "Across sources, the pattern suggests..."
- "A reasonable inference is..."
- "The evidence is thin here because..."

Do not overuse labels if the writing becomes stiff. Use them where the distinction changes how the reader should trust the point.

## Confidence handling

When confidence is high:

- state the finding directly
- include the source basis

When confidence is medium:

- state the finding with context
- mention the limitation

When confidence is low:

- write it as a tentative interpretation
- explain what evidence would be needed to firm it up

## Repeated claims

Repeated claims are a pattern, not proof.

If several artifacts repeat a similar statistic or argument:

- identify the repetition
- avoid calling it corroboration unless the sources are independent
- mention the limitation in the relevant caveat or confidence section

## Original artifact fallback

Inspect original artifacts when the digest lacks enough detail to write responsibly.

Record fallback reads in `Source Notes`:

```markdown
## Source Notes

- Digest used: `artifacts/digests/jobs-ai-digest.json`
- Original artifacts inspected for citation context: `artifacts/transcripts_clean/example.md`
- Limitation: several claims were repeated across commentary transcripts without primary sources in the local corpus.
```

## Style rules

Keep the prose professional and specific.

- Prefer concrete claims over broad abstractions.
- Avoid filler transitions.
- Avoid dramatic phrasing unsupported by evidence.
- Do not hide uncertainty.
- Do not quote long passages unless wording is itself important.

