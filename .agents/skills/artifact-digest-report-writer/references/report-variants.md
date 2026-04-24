# Report Variants

Use the variant that best matches the user's request. If the user names a variant, follow that choice.

## `executive_brief`

Purpose: concise stakeholder summary with the fewest useful details.

Default file: `artifacts/reports/executive-brief.md`

Use this section order:

```markdown
# Executive Brief: [Topic]

## Executive Summary
## Key Takeaways
## Strategic Implications
## Risks and Caveats
## Recommended Next Steps
## Source Notes
```

Write for a busy decision-maker. Use short paragraphs and crisp bullets. Keep evidence visible, but avoid turning the brief into a source catalog.

## `analytical_report`

Purpose: fuller synthesis with themes, evidence, implications, and caveats.

Default file: `artifacts/reports/analytical-report.md`

Use this section order:

```markdown
# Analytical Report: [Topic]

## Executive Summary
## Corpus Overview
## Core Themes
## Key Claims and Evidence
## Contradictions and Tensions
## Implications
## Open Questions
## Source Notes
```

Write for someone who wants the whole picture without reading every digest or transcript. This is the default variant for "holistic document" and "professional report" requests.

## `critical_review`

Purpose: skeptical assessment of evidence quality, contradictions, bias, weak claims, and missing context.

Default file: `artifacts/reports/critical-review.md`

Use this section order:

```markdown
# Critical Review: [Topic]

## Critical Summary
## Strongest Evidence
## Weakest Claims
## Contradictions
## Bias and Framing Risks
## Missing Context
## Confidence Assessment
## Source Notes
```

Write with intellectual pressure. The goal is not to dismiss the corpus, but to show which parts are strong, thin, repeated, speculative, or framed in a way that could mislead downstream reasoning.

## `decision_memo`

Purpose: recommendation-oriented document with options, tradeoffs, risks, and decision criteria.

Default file: `artifacts/reports/decision-memo.md`

Use this section order:

```markdown
# Decision Memo: [Decision or Topic]

## Decision Context
## Recommendation
## Options Considered
## Evidence Base
## Tradeoffs
## Risks
## Next Actions
## Source Notes
```

Write for action. If the digest does not support a firm recommendation, say so and recommend the next evidence-gathering step instead.

## Multi-variant requests

When a user requests multiple variants, generate separate files. Do not merge variants into one oversized report unless the user explicitly asks for a combined document.

