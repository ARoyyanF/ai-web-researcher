# Markdown Output Format

Save one Markdown file per web research task under:

```text
artifacts/web-searches/<topic-slug>.md
```

Use this structure.

```markdown
# Web Research: [Topic]

## Query / Task
[User request or search query]

## Collection Metadata
- Generated at: [timestamp]
- Tooling: LLM harness web tools
- Scope: [search collection / opened pages / focused source collection]
- Limitations: [blocked pages, partial content, search-only results, etc.]

## Sources
### 1. [Source Title]
- URL: [url]
- Accessed: [timestamp]
- Source type: [search result / opened page / extracted page]
- Relevance: [brief note]
- Limitations: [none / blocked / partial / search-only / paywalled]

[Copied or lightly cleaned tool result, extracted content, or key snippets.]

## Notes for Downstream Distillation
- [How this source set should be treated]
- [Uncertainty or provenance caveat]
```

## Writing guidance

Keep the artifact factual and source-oriented.

- Copy or lightly organize harness tool results where practical.
- Avoid turning the artifact into a polished essay.
- Keep quoted or extracted snippets short.
- Preserve URLs and source titles exactly when available.
- Include uncertainty rather than smoothing it away.

## Slugs

Use lowercase ASCII slugs when practical.

Examples:

- `ai-job-market-2026.md`
- `openai-api-pricing.md`
- `entry-level-hiring-sources.md`

