# Source Provenance

Record enough metadata for another model or human reader to understand where the web artifact came from and how much trust to place in it.

## Required metadata per research task

Include this in `## Collection Metadata`:

- user request or search query
- generated timestamp
- tooling: `LLM harness web tools`
- scope, such as `search collection`, `opened pages`, or `focused source collection`
- limitations, including blocked pages, paywalls, partial extraction, search-only results, or unavailable pages

## Required metadata per source

Each source entry should include:

- source title when available
- URL
- accessed timestamp
- source type
- relevance note
- extraction limitations if any

Use these source type labels:

- `search result`
- `opened page`
- `extracted page`
- `cited page`
- `blocked page`
- `partial extraction`

## Access timestamps

Use the current local date/time available to the agent. If the harness gives a fetch timestamp, use that. If not, use the current session date/time and be consistent within the artifact.

## Limitations

Record limitations plainly:

- page blocked
- paywall encountered
- visible excerpt only
- search result only, page not opened
- page opened but content was incomplete
- source unavailable
- source may have changed after access

## Claims discipline

Do not convert search-result snippets into verified claims. Mark them as search results unless the page was opened and the relevant content was visible.

Do not treat multiple pages repeating the same claim as independent confirmation unless the pages provide distinct evidence.

