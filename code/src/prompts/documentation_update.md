Update, create, or delete Markdown pages so they match a code change. You see one code patch or change (plus any changed C# methods) and the candidate documentation pages that might need that change.

## Flow

1. For each candidate page, name its job from its H1, sections, and `## Sources`.
2. Keep a change only if that page's `## Sources` include the changed file, or the page already documents that env var, proto field, method, or deploy value.
3. If documentation file is empty, build it from the new code change to proper markdown files.
4. From those changes, list facts that are missing or now false on that page.
5. Empty list → that page is `status=unchanged`, `documentation=""`.
6. Otherwise rewrite that **entire** page and set `status=updated`.
7. If documentation is empty, set `status=created`.

Return one JSON object per candidate page you were given. Use that page's path as `documentation_path`.

A true sentence is not an update. A missing fact this page is responsible for is.

## Page job

Each page owns only what it already covers. Do not infer unrelated facts between two pages (e.g. Document processing logic in Shipment query service should not be added - they dont correlate).

A page must be updated when it documents that kind of thing and the change adds or alters:

- env vars or config keys
- proto / RPC fields
- method steps, cache, TTL, or error behavior
- deployment values this page already lists
- anything correlated with the change

Leave a page unchanged when the change is off-topic, already stated correctly, or belongs on a sibling page.

## Rewrite

- Same headings, tone, tables, links, and `## Sources`.
  - Sources can be added IF they are related to the change and are not already present.
  - Sources can be removed IF they are not related to the change and are already present.
- Same house style: short lede, Purpose, Who calls, Interfaces or Data, Architecture, Deployment if present, Sources.
- Audience is a new joiner, maintainer, architect. Plain sentences. No marketing. No "Note that…".
- Use only facts on this page or in the provided change. Do not invent APIs, defaults, or behavior.
- Put new facts in the existing section that already holds that kind of fact.
- `documentation` is the full page Markdown, not a patch.

## Create

A page must be created when it does not exist and the change adds new information or facts.

- Create the page with the proper structure and content presented in Table of contents.
- Set `status=created`.

## Table of contents structure

Table of contents displays how each page is organized. Content structure is an alignment and not mandatory structure.
Table of contents:

- What is the purpose of the page (Mandatory)
- Who calls / is called by (Mandatory)
- Interfaces/Data/Configuration (if present)
- Architecture
- Deployment
- Sources (Mandatory)

## Json Structure

- `status`: An enum representing the status of the documentation.
  - possible values: "updated", "created", "unchanged", "removed"
  - If documentation file contains empty Purpose and Sources, set `status=created`.
- `documentation_path`: The path to the page.
- `documentation`: The full page Markdown, not a patch.

## JSON Output

One object per candidate page. `documentation_path` is the documentation page path you were given, not the code file.

JSON output when some pages change:

```json
[
  {
    "status": "updated",
    "documentation_path": "path/to/page.md",
    "documentation": "# Page Title\n\n## Purpose\n\n## Who calls / is called by\n\n## Interfaces/Data/Configuration\n\n## Architecture\n\n## Deployment\n\n## Sources"
  },
  {
    "status": "created",
    "documentation_path": "path/to/sibling.md",
    "documentation": ""
  }
]
```

JSON output when every page is unchanged:

```json
[
  {
    "status": "unchanged",
    "documentation_path": "path/to/page.md",
    "documentation": ""
  }
]
```
