# Natural for Ajax — stateful `Connector` flows

Natural for Ajax applications often look like a single form POST in DevTools, but behave like a stateful desktop UI over HTTP. The same `/servlet/Connector` endpoint can initialize pages, change filters, run searches, and clear results. Replaying only the final search request usually fails because the server-side page model does not exist yet.

## When you see this

- Entry URLs contain `/servlet/easynat-app?op=...`.
- Pages have names such as `NatLogon.html`, `SIM1000X.html`, or other uppercase Natural program names.
- Page source calls `C.initWithModelIdAndSessionIdAndProcessId(...)`.
- Requests go to `/servlet/Connector` with URL-encoded fields `SESSIONID`, `PAGEINITPARAM`, `XML`, `ERRORMESSAGE`, and `STAMP`.
- The field named `XML` contains a compact stream of opcodes and length-prefixed values, not conventional XML.
- Consecutive UI actions use the same URL and method but carry different event streams, stamps, and deltas.

## How it works

The browser first builds a live application model through a sequence of page loads and `Connector` initializations. Only then does it dispatch business events such as selecting a filter or running a query.

A client must carry two kinds of state:

1. **Transport state:** cookies and the HTTP/TLS session, normally owned by one `curl_cffi.requests.Session`.
2. **Application state:** session ID, process ID, current page and model, latest `STAMP`, latest `delta`, and whether the previous result must be cleared.

Cookies alone do not capture application state. Keep priming and queries on the same client object unless you have a proven serialization format for both kinds of state.

Treat `HTTP 200` as a transport result only. A challenge page, expired-session page, or generic error page can also arrive with status 200. A successful `Connector` response must contain the expected application model, including `XML` and `STAMP`, and must not contain an application error.

## Reference case — vehicle-yard plate lookup

This sequence distills a validated public-sector vehicle-yard consultation. Paths and event names below are an example of the pattern, not a universal Natural for Ajax API; rediscover them for each deployment.

### Full request sequence

The example includes **two consecutive plate queries**. That second query is essential: it proves that the reset event and delta responses work, rather than only reproducing the first captured request.

| # | Request | Purpose | State produced or consumed |
|---:|---|---|---|
| 1 | `GET ${APP}/servlet/easynat-app?op=S37` | Enter service `S37`. | Discover session ID, process ID, and `pageInitParam`; accept cookies. |
| 2 | `GET ${APP}/cisnatural/NatLogon.html` | Open the automatic-logon page. | Discover the `NatLogon` model ID. |
| 3 | `POST ${APP}/servlet/Connector` | Initialize `NatLogon`. | Send `STAMP=INIT`; consume the returned model, `STAMP`, `delta`, and `nextPage`. |
| 4 | `GET ${APP}/UIC-SERVICOS/SIM1000X.html` | Open the services page promised by `nextPage`. | Discover the `SIM1000X` model ID. |
| 5 | `POST ${APP}/servlet/Connector` | Initialize `SIM1000X`. | Start with the page's initial delta, then advance `STAMP` and `delta`. |
| 6 | `POST ${APP}/servlet/Connector` | Dispatch `on_interceptor` for service `S37`. | Require `nextPage=/UIC-SERVICOS/VES0009X.html`. |
| 7 | `GET ${APP}/UIC-SERVICOS/VES0009X.html` | Open the vehicle-yard page. | Discover the `VES0009X` model ID. |
| 8 | `POST ${APP}/servlet/Connector` | Initialize `VES0009X`. | Advance the page model, `STAMP`, and `delta`. |
| 9 | `POST ${APP}/servlet/Connector` | Dispatch `cmd_filtro`. | Select plate lookup with `v_filtro_sel=2.0` and `#f12_selected=2.0`. |
| 10 | `POST ${APP}/servlet/Connector` | Dispatch `cmd_consultar_placa` for plate A. | Send the plate and current state; validate the returned model and echoed plate. |
| 11 | `POST ${APP}/servlet/Connector` | Dispatch `cmd_nova`. | Clear plate A's result before reusing the page. |
| 12 | `POST ${APP}/servlet/Connector` | Dispatch `cmd_consultar_placa` for plate B. | Accept a delta response; validate plate B independently. |

Steps 1–9 are **priming**. One query therefore takes ten application requests, and two queries take twelve. “Five queries per session” does **not** mean five HTTP calls.

### Event payloads

All example `Connector` calls are URL-encoded and include the common fields:

```text
SESSIONID
PAGEINITPARAM
XML
STAMP
ERRORMESSAGE
```

The `XML` field carries the serialized event and properties. The business properties in this case are:

```text
# Filter by plate
event=cmd_filtro
v_filtro_sel=2.0
#f12_selected=2.0

# Query
 event=cmd_consultar_placa
v_filtro_error=
v_placa=<PLATE>
#f12_selected=2.0

# Clear before the next query
event=cmd_nova
#f12_selected=2.0
```

`event` is shown here as a logical property inside the serialized stream; it is not an additional top-level form field.

Initialization uses `STAMP=INIT` and properties such as `pageInitParam`, `pagePixelHeight`, `pagePixelWidth`, and `timeZoneOffset`. Later events use the most recent `STAMP` returned by the server.

### Dynamic-state map

Never copy these values from an old HAR into a new run:

| Value | Where the live client gets it |
|---|---|
| `m_currentSessionId` | Entry HTML JavaScript. |
| `m_currentProcessId` | Entry HTML JavaScript. |
| `pageInitParam` | Entry HTML JavaScript. |
| Model ID | `C.initWithModelIdAndSessionIdAndProcessId(...)` in the current page. |
| Initial page delta | Page initialization convention observed in the capture; `inittini` in this case. |
| Later `delta` | Previous `Connector` response. |
| `STAMP` | Literal `INIT` for page initialization, otherwise the previous `Connector` response. |
| Next page | `nextPage` in the decoded application model. |
| Cookies | The live session's cookie jar. |

Do not set `Cookie`, `Host`, or `Content-Length` manually. Let the HTTP client calculate or select them. Keep headers appropriate to each resource type instead of applying one captured header list to every request.

## Reference skeleton — vehicle-yard client

The entire skeleton below, including paths, events, properties, statuses, and the helpers `serialize_event`, `parse_connector`, and `interpret_result`, belongs to this reference case. The reusable contract is only the order in which live state is read, updated, and validated; rediscover all business names for each deployment.

```python
import re
from curl_cffi.requests import Session


class NaturalClient:
    def __init__(self, app_base: str, timeout: int = 30):
        self.app = app_base.rstrip("/")
        self.connector = f"{self.app}/servlet/Connector"
        self.http = Session(impersonate="chrome")
        self.timeout = timeout
        self.ready = False
        self.needs_reset = False

    def get(self, path: str) -> str:
        response = self.http.get(f"{self.app}{path}", timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def event(self, name: str = "", properties: dict | None = None,
              *, init: bool = False, init_param: str = "") -> dict:
        stream = serialize_event(
            sid=self.sid,
            pid=self.pid,
            model=self.model,
            page=self.page,
            event=name,
            properties=properties or {},
            delta=self.delta,
            init=init,
            init_param=init_param,
        )
        response = self.http.post(
            self.connector,
            data={
                "SESSIONID": self.sid,
                "PAGEINITPARAM": init_param,
                "XML": stream,
                "STAMP": "INIT" if init else self.stamp,
                **({} if init else {"ERRORMESSAGE": ""}),
            },
            timeout=self.timeout,
        )
        response.raise_for_status()

        # This helper must reject challenge/error pages, missing XML/STAMP,
        # ERRORMESSAGE, xciErrorMessage, and easy_syserror_visible=true.
        values, new_delta, new_stamp = parse_connector(response.text)
        self.delta, self.stamp = new_delta, new_stamp
        return values

    def open_page(self, path: str, init_param: str = "") -> dict:
        self.page = path
        html = self.get(path)
        match = re.search(
            r'C\.initWithModelIdAndSessionIdAndProcessId\("([A-Za-z0-9_.+\-]+)"',
            html,
        )
        if not match:
            raise RuntimeError("Page has no Natural for Ajax model")
        self.model = match.group(1)
        self.delta = "inittini"  # Confirm for the target; do not generalize blindly.
        return self.event(init=True, init_param=init_param)

    def initialize(self) -> None:
        entry = self.get("/servlet/easynat-app?op=S37")
        self.sid = js_variable(entry, "m_currentSessionId")
        self.pid = js_variable(entry, "m_currentProcessId")
        init_param = js_variable(entry, "pageInitParam")

        values = self.open_page("/cisnatural/NatLogon.html", init_param)
        assert values.get("nextPage") == "/UIC-SERVICOS/SIM1000X.html"
        self.open_page("/UIC-SERVICOS/SIM1000X.html")

        values = self.event("on_interceptor", service_properties("S37"))
        assert values.get("nextPage") == "/UIC-SERVICOS/VES0009X.html"
        self.open_page("/UIC-SERVICOS/VES0009X.html")
        self.event("cmd_filtro", {
            "v_filtro_sel": "2.0",
            "#f12_selected": "2.0",
        })
        self.ready = True

    def query(self, plate: str) -> dict:
        if not self.ready:
            raise RuntimeError("Run the complete priming sequence first")
        values = self.event("cmd_consultar_placa", {
            "v_filtro_error": "",
            "v_placa": plate,
            "#f12_selected": "2.0",
        })
        result = interpret_result(values)
        echoed_plate = values.get("v_placa", "").strip().upper()
        if result["status"] in {"APREENDIDO", "LIBERADO"} and echoed_plate != plate:
            raise RuntimeError("Response does not confirm the queried plate")
        self.needs_reset = True
        return result

    def reset(self) -> None:
        if self.needs_reset:
            self.event("cmd_nova", {"#f12_selected": "2.0"})
            self.needs_reset = False


client = NaturalClient("https://target.example.com/portal")
client.initialize()
first = client.query("ABC1234")  # Persist this result before clearing the page.
client.reset()
second = client.query("ABC1D23")
```

Add the request wrapper's rate limiting, destination allowlist, resource-specific headers, and stop conditions before using this skeleton against a live service. For an exact replay, follow `../discovery/har-exact-replay.md` and pass the bundled request diff; a working skeleton is not fidelity evidence.

### Serialization and decoding notes

In the reference protocol, request string lengths count **UTF-16 code units** before each component is encoded with JavaScript-compatible `encodeURIComponent` semantics. The request prefix stores all eight lengths first, then all eight encoded parts:

```python
from urllib.parse import quote


def js_length(value: str) -> int:
    return len(value.encode("utf-16-le", "surrogatepass")) // 2


def encode_component(value: str) -> str:
    return quote(value, safe="-_.!~*'()")
```

Use `../scripts/natural_for_ajax.py` to discover requests by parsed content, round-trip every captured stream, and compare semantically paired requests in a replica. Treat HAR entry numbers as capture-local addresses, not protocol parameters. Do not replace the original browser headers or percent encoding with a simpler working variant when exact fidelity is required.

Observed response opcodes included:

| Opcode | Meaning in the reference decoder |
|---|---|
| `p`, `z` | Literal values. |
| `q`, `w` | Names resolved through a dictionary. |
| `s` | Define a dictionary name. |
| `b`, `c` | Enter and leave a scope. |
| `x` | New delta. |
| `k` | Remove a value. |
| `l` | Clear values. |

Build the decoder from captured responses and test it offline. Reject unknown opcodes, truncated lengths, unresolved dictionary names, unclosed scopes, and missing deltas instead of returning a partial success.

## Interpreting the reference result

The example maps application values to normalized statuses only after persisting the raw response securely:

| Application evidence | Normalized status |
|---|---|
| `v_situacao_atual=Veículo Apreendido` | `APREENDIDO` |
| `v_situacao_atual=Veículo Liberado` | `LIBERADO` |
| `v_filtro_error=Placa sem histórico de apreensão` | `NAO_LOCALIZADO` |
| Any uncatalogued message or situation | `INDETERMINADO` |

A delta response can omit `v_situacao_atual`. In this specific case, `vp_situacao_atual=true` allowed the decoder to use the last row of `situacao_rows.items[N].situacao_col1`, accepting only `Apreendido` or `Liberado`. Do not turn this into a generic Natural for Ajax rule, and do not guess states such as `Suspensão da Apreensão`.

For positive statuses, require the response to echo the same normalized plate that was requested. A valid-looking result for another input is not a successful query.

## Failure and batch rules

Stop the current session without blindly repeating the event when you see:

- HTTP 403 or 429;
- a challenge page, `/TSPD/`, CAPTCHA, or access rejection;
- HTTP 200 without `XML` or `STAMP`;
- `ERRORMESSAGE`, `xciErrorMessage`, or `easy_syserror_visible=true`;
- a decoder failure or unexpected page transition;
- a transport failure after a state-changing POST.

A POST may have reached the server even if its response was lost. Automatic retry can run the same UI event twice. Retry an idempotent GET cautiously, but mark a state-changing POST as ambiguous and rebuild the session after review.

For batches:

1. Persist each result incrementally before `cmd_nova` clears its page state.
2. Keep a per-session query counter and input position in the output.
3. Treat any session-size limit or rotation cadence as an observed run parameter, not a protocol guarantee.
4. Refuse to resume an incomplete or blocked part without reviewing which POSTs may have run.
5. Validate total count, input order, duplicate handling, per-session counts, and status totals before consolidation.

## Validation checklist

- [ ] Offline fixtures cover each known result, a delta response, and an unknown state.
- [ ] Priming reaches an explicit `ready` state after `cmd_filtro`.
- [ ] Every page transition matches the expected `nextPage`.
- [ ] A controlled first query returns a catalogued status and confirms its input.
- [ ] A second consecutive query proves `cmd_nova` and delta decoding.
- [ ] No challenge or error page is accepted merely because it returned HTTP 200.
- [ ] No cookies, tokens, session IDs, raw HARs, or personal records are committed as examples.
- [ ] Consolidated counts reconcile exactly with the input and per-session outputs.

## Gotchas

- A field named `XML` is not necessarily XML.
- Reusing cookies without the model, stamp, and delta is not session persistence.
- The final query POST is not self-contained; earlier “boring” page loads create required state.
- Responses after the first query may contain only deltas rather than the full model.
- The absence of a challenge in one batch does not prove future runs will not encounter one.
- A HAR is historical evidence. Re-validate paths, protocol details, and browser-profile compatibility against the live deployment.

## Related

- `../discovery/har-driven-workflow.md` — find the query by response content, then walk backward to reconstruct priming
- `aspnet-webforms.md` — another stateful, event-driven form pattern
- `../networking/sticky-sessions.md` — keep transport affinity when infrastructure requires it
- `../reliability/resumable-extraction.md` — incremental output and safe checkpoints
- `../anti-bot/error-decoders.md` — distinguish transport success from application success
