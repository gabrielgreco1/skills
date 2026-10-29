# Scripts

**Scope:** Deterministic helpers for fragile extraction protocols. Keep private HARs and live session values outside the skill repository.

## Files

| File | Use |
|---|---|
| `natural_for_ajax.py` | Discover Natural for Ajax POSTs by parsed content (`discover`), exactly reserialize their streams (`roundtrip`), or compare semantically paired reference and replica entries with explicit dynamic slots (`compare`). Standard library only; emits sanitized structural JSON. |
| `test_natural_for_ajax.py` | Synthetic unit tests for UTF-16 lengths, `encodeURIComponent`, round-trips, header order, static mismatches, session provenance, shifted HAR indices, and mandatory declaration of dynamic business inputs. |

Run the tests from the repository root:

```bash
python webscraping-expert/scripts/test_natural_for_ajax.py
```

Use `discover --event EVENT_NAME` to locate a semantically identified event in each HAR. Treat returned indices as capture-local addresses, never reusable constants. Read `../discovery/har-exact-replay.md` before using the comparator. A passing HAR comparison does not certify TLS, HTTP framing, or wire order.
