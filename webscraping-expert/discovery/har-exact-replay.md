# HAR exact replay — from capture to a proven stateful request

Use this workflow when copying one cURL is not enough and the replica must match the original request's observable shape exactly: request order, URLs, methods, header names and order, static header values, form-field order, serialization, and application state.

The reference example is a Natural for Ajax vehicle-yard lookup, but the method applies to WebForms, Aura, and other stateful flows.

## Non-negotiable meaning of “exact”

Separate three claims:

1. **Application equivalence:** the live service accepts the flow and returns the right data.
2. **HAR-observable equivalence:** every request property preserved by the reference HAR matches after replacing proven dynamic values with placeholders.
3. **Wire equivalence:** TLS, HTTP framing, header order, and cookie multiplicity match on the wire.

A normal HAR can support (1) and partially support (2); it does **not** prove (3). Do not claim byte-for-byte wire fidelity from HAR evidence alone. If wire fidelity is required, capture the replica with an appropriate wire/NetLog harness and use the same browser or a transport profile proven against that browser.

“Close enough” headers are not exact. A generic current-Chrome profile can be application-compatible and still fail the required HAR diff.

## Reference capture

The worked example comes from a 115-entry HAR with one query. Its original entry numbers are retained only in the appendix as historical evidence; they are not selection parameters. Cache state, support resources, and another run can shift every position.

Keep the original HAR private and work on a local copy. Never commit raw captures, cookies, tokens, session IDs, plates, or result rows.

## Phase 1 — Inventory before replaying

Create a chronological table of every server-side entry before deleting anything:

```text
entry | startedDateTime | method | host | path | status | mime | request-body size | response-body size
```

Include static resources and apparent no-ops initially. Then classify entries without immediately removing them:

- **Application:** entry servlet, Natural pages, `/servlet/Connector`, business events.
- **Protection:** `/TSPD/`, challenge scripts, challenge cookies.
- **Static/support:** JavaScript, CSS, images, favicon, source maps.
- **Third party:** anything outside the application host.

This separation prevents two common mistakes: treating a protection script as the data API, and deleting an apparently boring application request that creates required state.

Do not use HTTP status as the classifier. In the reference capture, challenge-related markers and valid application responses can coexist in HTTP 200 pages.

## Phase 2 — Find the data by content, not by URL or position

Search response bodies for a unique value visible in the UI. In the example, the visible vehicle situation leads to this request, wherever it appears in the capture:

```text
POST /detran-portal-servicos/servlet/Connector
```

Inspect both sides of that entry:

- request form fields and their order;
- event name inside the `XML` field;
- business input (`v_placa`) and filter properties;
- response model and the value that proves the result;
- `STAMP`, `delta`, and application error fields.

The URL is deliberately uninformative: every business action uses the same endpoint. The request body and the preceding state are the operation.

List candidates by parsed content, then filter by the event identified from the response evidence:

```bash
python webscraping-expert/scripts/natural_for_ajax.py discover private-reference.har
python webscraping-expert/scripts/natural_for_ajax.py discover private-reference.har \
  --event cmd_consultar_placa
```

The reported entry number is only an address in this HAR. Never carry it into another capture as a selection rule.

## Phase 3 — Walk backward through provenance

For every value in the final POST, record where the live browser obtained it. Do not copy the captured literal into the replica.

| Final-request dependency | Evidence to find | Reference origin |
|---|---|---|
| Session ID | Entry HTML variable | `m_currentSessionId` in the entry document. |
| Process ID | Entry HTML variable | `m_currentProcessId` in the entry document. |
| `pageInitParam` | Entry HTML variable | Entry document, then used by `NatLogon` initialization. |
| Model ID | Page initialization JavaScript | `C.initWithModelIdAndSessionIdAndProcessId(...)` on each page. |
| Current page | Navigation / `nextPage` | `NatLogon` → `SIM1000X` → interceptor → `VES0009X`. |
| `STAMP` | Previous `Connector` response | `INIT` for page initialization; latest response value afterward. |
| `delta` | Page convention and previous response | `inittini` on page open in this case, then response `x` opcode. |
| Cookies | Response `Set-Cookie` and cookie jar | Current live session only. |
| Filter state | Earlier UI event | The preceding `cmd_filtro` request. |
| Plate | User input | Business input, not a session secret. |

The conclusion comes from this dependency graph: the final POST is not independently replayable. Saving only cookies still loses the model, stamp, delta, page, and filter state.

## Phase 4 — Reconstruct the minimum complete sequence

Derive the sequence from provenance, then prove it by removing optional static/support traffic rather than by guessing. Logical steps below describe order and purpose, not HAR positions.

| Logical step | Request | Required conclusion |
|---:|---|---|
| 1 | `GET easynat-app?op=S37` | Session, process, and initial parameter exist. |
| 2 | `GET NatLogon.html` | Logon model is discoverable. |
| 3 | `POST Connector`, initialize | `nextPage` selects `SIM1000X`. |
| 4 | `GET SIM1000X.html` | Services model is discoverable. |
| 5 | `POST Connector`, initialize | Services page is live. |
| 6 | `POST Connector`, `on_interceptor` | `nextPage` selects `VES0009X`. |
| 7 | `GET VES0009X.html` | Yard-page model is discoverable. |
| 8 | `POST Connector`, initialize | Yard page is live. |
| 9 | `POST Connector`, `cmd_filtro` | Plate filter is selected. |
| 10 | `POST Connector`, `cmd_consultar_placa` | Result model confirms the requested plate. |

That is nine priming calls plus one query. To prove reuse, continue in the same client:

```text
cmd_nova → cmd_consultar_placa (a different input)
```

The second query is a separate acceptance test. It catches stale page state and responses that contain only deltas.

## Phase 5 — Build a per-resource request contract

Do not define one global header dictionary. Record an ordered header list for each request class. The reference capture uses Brave 156 on macOS; a Chromium 141 or generic Chrome profile is not an exact match.

Static values observed in this capture include:

```text
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8
Accept-Language: pt-BR,pt;q=0.6
Sec-GPC: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36
sec-ch-ua: "Not:A-Brand";v="8", "Chromium";v="156", "Brave";v="156"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
```

Resource-specific differences matter:

| Request class | Required differences in the reference |
|---|---|
| Entry document | `Sec-Fetch-Dest=document`, `Sec-Fetch-Site=none`, `Sec-Fetch-User=?1`; no `Cache-Control` in this capture. |
| Natural page iframe | `Sec-Fetch-Dest=iframe`, `Sec-Fetch-Site=same-origin`, entry `Referer`. |
| Connector initialization | `Cache-Control=max-age=0`, `Origin`, `Referer` ending in `/HTMLBasedGUI/general/cscform.html`. |
| Connector event | `Cache-Control=max-age=0`, `Origin`, `Referer` ending in `/servlet/Connector`; `cmd_*` events also have `Sec-Fetch-User=?1`. |
| Connector POST | `Content-Type=application/x-www-form-urlencoded`. |

Preserve the observed header order in the intended request. Do not manually set `Cookie`, `Host`, or `Content-Length`: the transport must own them. The comparator still checks their presence and behavior.

Initialization form-field order in this capture:

```text
SESSIONID, PAGEINITPARAM, XML, STAMP
```

Event form-field order:

```text
SESSIONID, PAGEINITPARAM, XML, ERRORMESSAGE, STAMP
```

## Phase 6 — Reproduce the serialization exactly

The field named `XML` is a length-prefixed protocol stream. In this capture, component lengths are calculated on the decoded string in UTF-16 code units, and each component is then encoded with JavaScript-compatible `encodeURIComponent` semantics.

This distinction is easy to miss when an unencoded implementation still works. It changes the observable request for:

- the current page URL (`:` and `/`);
- the model ID (`+`);
- `#f12_selected` (`#`);
- `interceptor_params.items[N]...` (`[` and `]`).

Use JavaScript's safe set, not Python's default `quote()` behavior:

```python
from urllib.parse import quote

JS_ENCODE_SAFE = "-_.!~*'()"


def js_length(value: str) -> int:
    return len(value.encode("utf-16-le", "surrogatepass")) // 2


def encode_component(value: str) -> str:
    return quote(value, safe=JS_ENCODE_SAFE)
```

The request prefix starts with `i` or `v`, then stores **all eight lengths first**, using widths `2,2,2,2,2,3,5,1`, followed by **all eight encoded parts**. `p` properties and an `x` delta come afterward. Length prefixes are decimal and zero-padded; calculate each length before encoding its component:

```python
widths = (2, 2, 2, 2, 2, 3, 5, 1)
lengths = [str(js_length(value)).zfill(width) for value, width in zip(parts, widths)]
stream = kind + "".join(lengths) + "".join(encode_component(value) for value in parts)
```

Use the bundled validator to prove that parsing and reserializing every reference POST reproduces the original stream exactly:

```bash
python webscraping-expert/scripts/natural_for_ajax.py roundtrip private-reference.har
```

Round-trip validation does not reuse the captured values in a live run. It only proves that the implementation understands their format.

## Phase 7 — Implement in proof order

Do not start with a batch scraper.

1. **Offline inventory:** save a sanitized request table and dependency map.
2. **Offline round-trip:** every captured `Connector` request stream parses and reserializes exactly.
3. **Offline response decoder:** known full and delta responses produce known results; unknown states stay unknown.
4. **Priming only:** reach an explicit `ready` state after `cmd_filtro`, without issuing a query.
5. **Controlled first query:** use an input already evidenced by the private capture; validate application shape and echoed input.
6. **Second consecutive query:** prove `cmd_nova`, updated stamp/delta, and delta-result interpretation.
7. **Request diff:** compare each intended replica request with its reference counterpart.
8. **Controlled batch:** write incrementally, preserve input order, and stop on ambiguous state.

At every live step, validate `nextPage`, `XML`, `STAMP`, `ERRORMESSAGE`, `xciErrorMessage`, and `easy_syserror_visible`. HTTP 200 alone never advances the state machine.

## Phase 8 — Diff reference and replica

Pair requests by semantic role and logical sequence position, never by raw HAR index or URL alone. All `Connector` calls share a URL.

The diff must check:

- method, full URL, and logical sequence position;
- ordered header names;
- every static header value, including browser brands and versions;
- dynamic headers by provenance and shape rather than captured value;
- form-field names and order;
- Natural part order, event name, property names and order;
- every static property value;
- dynamic values by their live origin and internal consistency;
- decoded page/model values and exact encoded serialization.

Run `discover` independently on the reference and replica, select the semantically matching requests, and set the comparison indices from those results:

```bash
python webscraping-expert/scripts/natural_for_ajax.py compare \
  private-reference.har "$REFERENCE_ENTRY" \
  private-replica.har "$REPLICA_ENTRY" \
  --dynamic-property v_placa
```

Only protocol-state values such as session IDs, process IDs, stamps, deltas, page-init parameters, cookies, and content length are dynamic by default. Declare every business input explicitly with `--dynamic-property`, after proving its origin; repeat the option when needed. In this reference case, `v_placa` is dynamic because it is the user's query input, not because its name contains `placa`. The comparator reports declared business exceptions and requires all other observable values to match. Review the JSON verdict; do not ignore a mismatch because the query returned data.

For full wire validation, supplement this HAR comparison with NetLog or wire evidence. HAR comparison alone cannot certify TLS or HTTP/2 framing.

## Stop conditions and ambiguous POSTs

Stop the current session without blind retry on:

- HTTP 403 or 429;
- a challenge, `/TSPD/`, CAPTCHA, or access rejection;
- HTTP 200 without the expected application model;
- application error fields or an unexpected `nextPage`;
- a protocol/decoder failure;
- a transport failure after a state-changing POST.

A lost response does not prove that the server did not process the POST. Replaying it can duplicate the UI event. Mark the state ambiguous, preserve evidence, and rebuild only after review.

## Definition of done

The reverse-engineering task is complete only when the deliverable contains:

- [ ] A chronological inventory separating application, protection, static, and third-party traffic.
- [ ] A final-request dependency/provenance map.
- [ ] The complete priming sequence and explicit `ready` criteria.
- [ ] Per-resource ordered request contracts based on the actual capture.
- [ ] Exact serializer round-trip evidence for every captured `Connector` POST.
- [ ] Offline full-response and delta-response tests.
- [ ] A controlled first-query and second-query result.
- [ ] A passing HAR-observable diff for every paired request, or an explicit unresolved mismatch.
- [ ] Content-based selection that still works after support requests shift the HAR indices.
- [ ] A clear statement separating HAR-observable fidelity from unproven wire fidelity.
- [ ] Sanitized artifacts only; no raw HAR, cookies, tokens, personal inputs, or result rows in the PR.

A valid business result with a failing request diff is **not** an exact replica.

## Appendix — original capture cross-references

Use these numbers only to locate evidence in the original 115-entry reference after deriving the flow semantically. They are not protocol constants, expected positions, or inputs for another HAR.

| Logical step | Original HAR entry |
|---:|---:|
| 1 | 0 |
| 2 | 21 |
| 3 | 48 |
| 4 | 57 |
| 5 | 79 |
| 6 | 83 |
| 7 | 87 |
| 8 | 104 |
| 9 | 109 |
| 10 | 112 |

A longer capture adds `cmd_nova` and a second query at entries 129 and 132. The synthetic test suite inserts support traffic and shifts query positions to ensure discovery does not depend on these numbers.

## Related

- `har-driven-workflow.md` — broader HAR-to-scraper workflow
- `har-parser.md` — HAR parsing basics
- `../site-patterns/natural-for-ajax.md` — Natural-specific state machine and result rules
- `../site-patterns/aspnet-webforms.md` — another provenance-heavy event flow
- `../reliability/resumable-extraction.md` — safe incremental execution after the protocol is proven
