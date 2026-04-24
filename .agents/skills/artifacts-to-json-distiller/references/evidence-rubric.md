# Evidence Rubric

Use this rubric when deciding how to classify and phrase findings.

## Claim types

### `evidence`

Use `evidence` when the point is directly stated in one or more source artifacts.

Examples:

- a transcript explicitly states a number, date, quote, or assertion
- a CSV row directly contains a field value
- a JSON file directly contains a property

### `synthesis`

Use `synthesis` when the point emerges by combining multiple sources.

Examples:

- several artifacts repeat the same narrative arc
- sources from different files point to a shared theme
- a timeline emerges only after combining statements across files

### `inference`

Use `inference` when the point is a reasoned conclusion that is plausible but not directly established by the corpus.

Examples:

- a likely implication for hiring behavior
- a plausible interpretation of source bias
- a cautious projection based on local evidence

Use `inference` sparingly. If something is thinly supported, say so.

## Confidence levels

Use simple labels:

- `high`: directly supported by multiple clear local sources or one authoritative structured source
- `medium`: supported, but with limitations such as commentary framing, partial corroboration, or ambiguous wording
- `low`: tentative, interpretive, or weakly evidenced

## Provenance rules

Every nontrivial claim should include:

- source path
- local anchor if available
- a short evidence note

Examples of useful anchors:

- transcript timestamps such as `03:35`
- Markdown headings
- CSV row references if easy to identify
- JSON key paths if relevant

## Contradictions

Record contradictions when they matter for reasoning:

- conflicting causal explanations
- conflicting timelines
- conflicting quantitative claims
- optimistic vs skeptical framings that materially change interpretation

Do not create a contradiction entry for minor wording differences.

## Repetition and corroboration

Do not confuse repeated statements with independent confirmation.

If several similar commentary artifacts repeat the same statistic or framing:

- mention the repetition as a pattern
- lower confidence if no primary evidence exists locally
- note the absence of independent corroboration in `gaps` or `open_questions`

## Compression guidance

The final JSON should be LLM-friendly.

- prefer one distilled sentence over a long quote
- quote only when wording is itself important
- keep arrays selective and useful
- avoid turning the digest into a transcript dump

