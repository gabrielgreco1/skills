# Discovery

**Scope:** How to figure out *what* to scrape and *where* the data actually lives — before writing a single line of extraction code.

When you hit a new target, start here.

## Files

| File | When to read |
|---|---|
| `autonomous-discovery.md` | Before asking the user anything. 5-minute checklist (robots.txt, sitemaps, embedded JSON, common API paths) to find the data yourself. |
| `google-deep-research.md` | When the user has no URL — only a topic. 4-phase workflow: 2–10 user keywords → expand to ≥12 → ≥300 Google queries → triage candidates. |
| `link-graph-traversal.md` | When the user gives an entry URL but the data is buried inside the site. Scored BFS traversal to find the data page; tries cheap shortcuts (sitemap, search box, `site:` Google) first. |
| `devtools-workflow.md` | When autonomous discovery fails. Step-by-step for asking the user to inspect DevTools and copy a curl. |
| `devtools-prompts.md` | Templates for asking the user to extract a specific request from DevTools — always anchor to a visible value on the page. |
| `har-parser.md` | How to parse a `.har` file in Python: filter the relevant entry, extract URL/headers/body, reconstruct curl. |
| `har-driven-workflow.md` | The full 8-step workflow used to bootstrap a new scraper from a HAR file. |
| `har-exact-replay.md` | When a stateful replica must match the original HAR exactly: backward provenance, complete priming, per-resource ordered headers, serialization round-trips, and reference-vs-replica diffs. |
| `exhaustion-checklist.md` | Before reporting a target as blocked or impossible. Ten route families (A–J, including archives and asking for access), each needing logged evidence in a fixed attempt shape; agents may only report `stuck`, with the stuck-report format. |
