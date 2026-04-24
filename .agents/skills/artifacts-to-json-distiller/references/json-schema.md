# JSON Schema Guide

Use this structure for the final digest. Do not add large free-form sections unless the user asks for them.

## Top-level shape

```json
{
  "meta": {},
  "corpus_overview": {},
  "source_inventory": [],
  "themes": [],
  "entities": [],
  "claims": [],
  "contradictions": [],
  "timelines": [],
  "implications": [],
  "open_questions": [],
  "gaps": [],
  "llm_brief": {}
}
```

## Field guide

### `meta`

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-04-24T17:30:00Z",
  "input_root": "artifacts",
  "included_file_count": 11,
  "skipped_file_count": 0,
  "notes": ["Digest built from local artifacts only."]
}
```

### `corpus_overview`

Describe the corpus in a few compact fields.

```json
{
  "summary": "Corpus of transcript-derived markdown files about jobs, AI, hiring, and early-career labor market stress.",
  "dominant_topics": ["job market", "AI", "software hiring"],
  "source_mix": {
    "md": 11
  }
}
```

### `source_inventory`

One entry per discovered file.

```json
{
  "path": "artifacts/transcripts_clean/example.md",
  "type": "md",
  "size_bytes": 8853,
  "status": "included",
  "summary": "Transcript discussing AI-assisted coding and rehiring trends.",
  "anchors": ["00:00", "03:35", "07:14"]
}
```

Use `status` values such as:

- `included`
- `skipped_unsupported`
- `skipped_unreadable`

### `themes`

Use this for recurring ideas across the corpus.

```json
{
  "name": "senior talent remains valuable",
  "summary": "Multiple sources argue AI raises the need for experienced workers rather than removing them outright.",
  "supporting_sources": [
    {
      "path": "artifacts/transcripts_clean/example.md",
      "anchors": ["03:35", "07:45"]
    }
  ],
  "confidence": "medium"
}
```

### `entities`

Capture people, companies, institutions, and repeated concepts.

```json
{
  "name": "Gartner",
  "entity_type": "organization",
  "context": "Referenced as a cited authority in multiple transcripts.",
  "source_paths": ["artifacts/transcripts_clean/example.md"]
}
```

### `claims`

Each claim should be grounded and typed.

```json
{
  "claim": "Several sources argue that AI tools increase the need for senior review rather than fully replacing experienced engineers.",
  "claim_type": "synthesis",
  "confidence": "medium",
  "evidence": [
    {
      "path": "artifacts/transcripts_clean/example.md",
      "anchor": "03:35",
      "note": "Source links AI adoption to increased senior hiring."
    }
  ],
  "limitations": ["Most sources are commentary-style transcripts, not primary datasets."]
}
```

Use `claim_type` values:

- `evidence`
- `synthesis`
- `inference`

### `contradictions`

Use this to record meaningful tension, not minor wording differences.

```json
{
  "topic": "AI productivity gains",
  "description": "Some sources frame AI as a major productivity accelerator, while others emphasize debugging overhead and quality regressions.",
  "sources_a": ["artifacts/transcripts_clean/source-a.md"],
  "sources_b": ["artifacts/transcripts_clean/source-b.md"],
  "confidence": "medium"
}
```

### `timelines`

Use when dates or sequence matter.

```json
{
  "topic": "software hiring narrative",
  "events": [
    {
      "time_ref": "early 2024",
      "description": "Sources describe layoffs and AI-driven hiring freezes."
    },
    {
      "time_ref": "2025-2026",
      "description": "Sources describe rehiring, boomerang hires, and emphasis on senior review."
    }
  ],
  "confidence": "medium"
}
```

### `implications`

These are allowed to be interpretive, but mark them clearly.

```json
{
  "point": "If the corpus is directionally right, labor market pressure may shift from total job loss toward role polarization and credential inflation.",
  "basis": "synthesis",
  "supporting_claims": [0, 3, 5],
  "confidence": "low"
}
```

### `open_questions`

```json
{
  "question": "Which claims in the corpus are independently verified beyond commentary videos?",
  "why_open": "Many sources cite statistics without linking primary evidence in the local artifacts.",
  "priority": "high"
}
```

### `gaps`

```json
{
  "gap": "No primary labor market datasets are present in artifacts.",
  "impact": "Limits confidence in repeated quantitative claims.",
  "related_paths": []
}
```

### `llm_brief`

Make this a compact handoff for another model.

```json
{
  "task_context": "Digest of local artifact corpus focused on jobs, AI, and labor market narratives.",
  "core_takeaways": [
    "The corpus repeatedly argues that AI is reshaping rather than eliminating skilled work.",
    "Junior roles appear more exposed in the corpus than senior roles.",
    "Many quantitative claims are repeated across commentary sources and should be treated cautiously."
  ],
  "reasoning_cautions": [
    "Do not treat repeated commentary as independent verification.",
    "Confidence is limited when primary sources are absent."
  ],
  "best_next_questions": [
    "Which claims can be corroborated with primary datasets?",
    "Which contradictions matter most for downstream decision-making?"
  ]
}
```

