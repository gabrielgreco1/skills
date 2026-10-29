#!/usr/bin/env python3
"""Validate Natural for Ajax request streams and compare HAR-observable fidelity.

Standard library only. Outputs structural JSON without session values, cookies,
page-init parameters, stamps, deltas, or plate values.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, quote, unquote_to_bytes

JS_ENCODE_SAFE = "-_.!~*'()"
PART_WIDTHS = (2, 2, 2, 2, 2, 3, 5, 1)
PART_NAMES = ("sid", "pid", "unused", "model", "dummy", "page", "event", "flag")
DYNAMIC_PARTS = {"sid", "pid"}
PROTOCOL_DYNAMIC_PROPERTIES = {"pageInitParam"}
DYNAMIC_HEADERS = {"cookie", "content-length"}
DYNAMIC_FORM_FIELDS = {"SESSIONID", "PAGEINITPARAM"}
SENSITIVE_OUTPUT_MARKERS = (
    "cookie", "session", "pageinit", "stamp", "delta", "plate", "sid", "pid",
)


class ProtocolError(ValueError):
    """The captured stream does not follow the observed Natural protocol."""


@dataclass
class NaturalStream:
    kind: str
    parts: list[str]
    properties: list[tuple[str, str]]
    delta: str

    @property
    def event(self) -> str:
        return self.parts[6]


def js_length(value: str) -> int:
    """Return JavaScript String.length: UTF-16 code units, not UTF-8 bytes."""
    return len(value.encode("utf-16-le", "surrogatepass")) // 2


def encode_component(value: str) -> str:
    """Match JavaScript encodeURIComponent, including its safe character set."""
    return quote(value, safe=JS_ENCODE_SAFE)


def _number(stream: str, pos: int, width: int) -> tuple[int, int]:
    raw = stream[pos:pos + width]
    if len(raw) != width or not raw.isascii() or not raw.isdigit():
        raise ProtocolError(f"Invalid {width}-digit length at offset {pos}")
    return int(raw), pos + width


def _take_encoded(stream: str, pos: int, length: int) -> tuple[str, int]:
    """Take encoded characters until the decoded UTF-16 length is reached."""
    if length == 0:
        return "", pos
    start = pos
    while pos < len(stream):
        if stream[pos] == "%":
            triplet = stream[pos + 1:pos + 3]
            if len(triplet) != 2 or any(char not in "0123456789abcdefABCDEF" for char in triplet):
                raise ProtocolError(f"Invalid percent encoding at offset {pos}")
            pos += 3
        else:
            pos += 1
        raw = stream[start:pos]
        raw_bytes = unquote_to_bytes(raw)
        try:
            decoded = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            if exc.end == len(raw_bytes):
                continue  # An encoded UTF-8 sequence is still incomplete.
            raise ProtocolError(f"Invalid encoded UTF-8 at offset {start}") from exc
        current = js_length(decoded)
        if current == length:
            return decoded, pos
        if current > length:
            raise ProtocolError(f"Encoded component exceeds declared length at offset {start}")
    raise ProtocolError(f"Truncated encoded component at offset {start}")


def parse_natural_stream(stream: str) -> NaturalStream:
    if not stream or stream[0] not in {"i", "v"}:
        raise ProtocolError("Natural stream must start with 'i' or 'v'")
    kind = stream[0]
    pos = 1
    lengths = []
    for width in PART_WIDTHS:
        length, pos = _number(stream, pos, width)
        lengths.append(length)
    parts = []
    for length in lengths:
        value, pos = _take_encoded(stream, pos, length)
        parts.append(value)

    properties = []
    delta = None
    while pos < len(stream):
        opcode = stream[pos]
        pos += 1
        if opcode == "x":
            length, pos = _number(stream, pos, 2)
            delta, pos = _take_encoded(stream, pos, length)
            if pos != len(stream):
                raise ProtocolError("Trailing data after Natural delta")
            break
        if opcode != "p":
            raise ProtocolError(f"Unsupported request opcode {opcode!r} at offset {pos - 1}")
        name_length, pos = _number(stream, pos, 2)
        value_length, pos = _number(stream, pos, 5)
        name, pos = _take_encoded(stream, pos, name_length)
        value, pos = _take_encoded(stream, pos, value_length)
        properties.append((name, value))
    if delta is None:
        raise ProtocolError("Natural stream has no delta")
    return NaturalStream(kind, parts, properties, delta)


def serialize_natural_stream(
    kind: str,
    parts: list[str],
    properties: list[tuple[str, str]],
    delta: str,
) -> str:
    if kind not in {"i", "v"} or len(parts) != len(PART_WIDTHS):
        raise ProtocolError("Invalid Natural kind or part count")
    lengths = []
    for value, width in zip(parts, PART_WIDTHS):
        length = js_length(value)
        if length >= 10 ** width:
            raise ProtocolError(f"Natural part does not fit width {width}")
        lengths.append(str(length).zfill(width))
    # The header stores all eight lengths first, then all eight encoded parts.
    out = [kind, *lengths, *(encode_component(value) for value in parts)]
    for name, value in properties:
        name_length, value_length = js_length(name), js_length(value)
        if name_length >= 100 or value_length >= 100000:
            raise ProtocolError("Natural property exceeds protocol width")
        out.extend((
            "p", str(name_length).zfill(2), str(value_length).zfill(5),
            encode_component(name), encode_component(value),
        ))
    delta_length = js_length(delta)
    if delta_length >= 100:
        raise ProtocolError("Natural delta exceeds protocol width")
    out.extend(("x", str(delta_length).zfill(2), encode_component(delta)))
    return "".join(out)


def load_entries(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig") as stream:
        return json.load(stream)["log"]["entries"]


def form_pairs(entry: dict) -> list[tuple[str, str]]:
    post = entry["request"].get("postData", {})
    if post.get("params"):
        return [(item.get("name", ""), item.get("value", "")) for item in post["params"]]
    return parse_qsl(post.get("text", ""), keep_blank_values=True)


def _entry_number(entries: list[dict], raw: str) -> int:
    try:
        index = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("HAR entry must be an integer") from exc
    if not 0 <= index < len(entries):
        raise ValueError(f"HAR entry {index} outside 0..{len(entries) - 1}")
    return index


def discover_requests(entries: list[dict], event: str | None = None) -> list[dict]:
    """Find Natural POSTs by parsed content; HAR positions are report addresses only."""
    requests = []
    for index, entry in enumerate(entries):
        fields = dict(form_pairs(entry))
        if "XML" not in fields:
            continue
        item = {"entry": index, "event": None, "ok": False}
        try:
            parsed = parse_natural_stream(fields["XML"])
            item.update({
                "kind": parsed.kind,
                "event": parsed.event,
                "property_order": [name for name, _ in parsed.properties],
                "ok": True,
            })
        except (KeyError, ProtocolError, ValueError) as exc:
            item["error"] = str(exc)
        if event is None or item["event"] == event:
            requests.append(item)
    return requests


def discover(path: str | Path, event: str | None = None) -> dict:
    requests = discover_requests(load_entries(path), event)
    return {
        "command": "discover",
        "ok": bool(requests) and all(item["ok"] for item in requests),
        "natural_post_count": len(requests),
        "event_filter": event,
        "requests": requests,
    }


def roundtrip(path: str | Path) -> dict:
    entries = load_entries(path)
    requests = []
    for item in discover_requests(entries):
        if not item["ok"]:
            requests.append(item)
            continue
        entry = entries[item["entry"]]
        fields = dict(form_pairs(entry))
        parsed = parse_natural_stream(fields["XML"])
        rebuilt = serialize_natural_stream(
            parsed.kind, parsed.parts, parsed.properties, parsed.delta,
        )
        item["ok"] = rebuilt == fields["XML"]
        if not item["ok"]:
            item["error"] = "Reserialized stream differs from reference"
        requests.append(item)
    failed = [item for item in requests if not item["ok"]]
    return {
        "command": "roundtrip",
        "ok": bool(requests) and not failed,
        "natural_post_count": len(requests),
        "failed_count": len(failed),
        "requests": requests,
    }


def _safe_value(path: str, value: str):
    lowered = path.lower()
    if any(marker in lowered for marker in SENSITIVE_OUTPUT_MARKERS):
        return f"<dynamic:{len(value)}>"
    return value if len(value) <= 240 else value[:237] + "..."


def _cookie_names(entry: dict) -> list[str]:
    cookies = entry["request"].get("cookies")
    if cookies:
        return [cookie.get("name", "") for cookie in cookies]
    for header in entry["request"].get("headers", []):
        if header.get("name", "").lower() == "cookie":
            return [part.split("=", 1)[0].strip() for part in header.get("value", "").split(";") if part.strip()]
    return []


def compare_entries(
    reference: dict,
    replica: dict,
    *,
    dynamic_properties: set[str] | None = None,
) -> dict:
    allowed_dynamic_properties = PROTOCOL_DYNAMIC_PROPERTIES | (dynamic_properties or set())
    mismatches = []

    def mismatch(path: str, expected, actual):
        mismatches.append({
            "path": path,
            "expected": _safe_value(path, expected) if isinstance(expected, str) else expected,
            "actual": _safe_value(path, actual) if isinstance(actual, str) else actual,
        })

    ref_request, rep_request = reference["request"], replica["request"]
    for key in ("method", "url"):
        if ref_request.get(key) != rep_request.get(key):
            mismatch(key, ref_request.get(key, ""), rep_request.get(key, ""))

    ref_headers = ref_request.get("headers", [])
    rep_headers = rep_request.get("headers", [])
    ref_names = [header.get("name", "") for header in ref_headers]
    rep_names = [header.get("name", "") for header in rep_headers]
    if ref_names != rep_names:
        mismatch("headers.order", ref_names, rep_names)
    for index, (ref_header, rep_header) in enumerate(zip(ref_headers, rep_headers)):
        name = ref_header.get("name", "").lower()
        if name != rep_header.get("name", "").lower() or name in DYNAMIC_HEADERS:
            continue
        if ref_header.get("value", "") != rep_header.get("value", ""):
            mismatch(f"headers[{index}].{name}", ref_header.get("value", ""), rep_header.get("value", ""))
    if _cookie_names(reference) != _cookie_names(replica):
        mismatch("cookies.names_and_order", _cookie_names(reference), _cookie_names(replica))

    ref_pairs, rep_pairs = form_pairs(reference), form_pairs(replica)
    ref_order, rep_order = [name for name, _ in ref_pairs], [name for name, _ in rep_pairs]
    if ref_order != rep_order:
        mismatch("form.order", ref_order, rep_order)
    ref_fields, rep_fields = dict(ref_pairs), dict(rep_pairs)
    for index, ((ref_name, ref_value), (rep_name, rep_value)) in enumerate(zip(ref_pairs, rep_pairs)):
        if ref_name != rep_name or ref_name in DYNAMIC_FORM_FIELDS | {"XML"}:
            continue
        if ref_name == "STAMP":
            if ref_value == "INIT" or rep_value == "INIT":
                if ref_value != rep_value:
                    mismatch(f"form[{index}].STAMP", ref_value, rep_value)
            continue
        if ref_value != rep_value:
            mismatch(f"form[{index}].{ref_name}", ref_value, rep_value)

    if "XML" in ref_fields and "XML" in rep_fields:
        try:
            ref = parse_natural_stream(ref_fields["XML"])
            rep = parse_natural_stream(rep_fields["XML"])
        except ProtocolError as exc:
            mismatch("XML.protocol", "valid Natural stream", str(exc))
            return {"ok": False, "mismatch_count": len(mismatches), "mismatches": mismatches}
        if ref.kind != rep.kind:
            mismatch("XML.kind", ref.kind, rep.kind)
        for index, name in enumerate(PART_NAMES):
            if name not in DYNAMIC_PARTS and ref.parts[index] != rep.parts[index]:
                mismatch(f"XML.parts.{name}", ref.parts[index], rep.parts[index])
        ref_property_order = [name for name, _ in ref.properties]
        rep_property_order = [name for name, _ in rep.properties]
        if ref_property_order != rep_property_order:
            mismatch("XML.properties.order", ref_property_order, rep_property_order)
        for (ref_name, ref_value), (rep_name, rep_value) in zip(ref.properties, rep.properties):
            if ref_name == rep_name and ref_name not in allowed_dynamic_properties and ref_value != rep_value:
                mismatch(f"XML.properties.{ref_name}", ref_value, rep_value)
        if ref.kind == "i":
            ref_init = dict(ref.properties).get("pageInitParam")
            rep_init = dict(rep.properties).get("pageInitParam")
            if ref_init != ref_fields.get("PAGEINITPARAM"):
                mismatch("reference.PAGEINITPARAM.provenance", "matches XML pageInitParam", "inconsistent")
            if rep_init != rep_fields.get("PAGEINITPARAM"):
                mismatch("replica.PAGEINITPARAM.provenance", "matches XML pageInitParam", "inconsistent")
        for label, fields, stream in (("reference", ref_fields, ref), ("replica", rep_fields, rep)):
            if fields.get("SESSIONID") != stream.parts[0]:
                mismatch(f"{label}.SESSIONID.provenance", "matches XML sid", "inconsistent")
            if fields.get("STAMP") == "INIT" and stream.kind != "i":
                mismatch(f"{label}.STAMP.provenance", "INIT only for initialization", stream.kind)
            if stream.kind == "i" and fields.get("STAMP") != "INIT":
                mismatch(f"{label}.STAMP.provenance", "INIT for initialization", fields.get("STAMP", ""))
    elif "XML" in ref_fields or "XML" in rep_fields:
        mismatch("form.XML.presence", "XML" in ref_fields, "XML" in rep_fields)

    return {
        "ok": not mismatches,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "scope": "HAR-observable only; not TLS, HTTP framing, or wire-order certification",
    }


def compare(
    reference_path: str | Path,
    reference_index: int,
    replica_path: str | Path,
    replica_index: int,
    *,
    dynamic_properties: set[str] | None = None,
) -> dict:
    ref_entries, rep_entries = load_entries(reference_path), load_entries(replica_path)
    result = compare_entries(
        ref_entries[reference_index],
        rep_entries[replica_index],
        dynamic_properties=dynamic_properties,
    )
    result.update({
        "command": "compare",
        "reference_entry": reference_index,
        "replica_entry": replica_index,
        "business_dynamic_properties": sorted(dynamic_properties or set()),
    })
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover", help="Find Natural POSTs by content, optionally filtering by event")
    discover_parser.add_argument("har")
    discover_parser.add_argument("--event", help="Return only requests with this parsed Natural event")

    roundtrip_parser = subparsers.add_parser("roundtrip", help="Parse and exactly reserialize every Natural POST in a HAR")
    roundtrip_parser.add_argument("har")

    compare_parser = subparsers.add_parser("compare", help="Compare two HAR entries with explicit dynamic slots")
    compare_parser.add_argument("reference_har")
    compare_parser.add_argument("reference_entry", type=int)
    compare_parser.add_argument("replica_har")
    compare_parser.add_argument("replica_entry", type=int)
    compare_parser.add_argument(
        "--dynamic-property",
        action="append",
        default=[],
        help="Business property allowed to differ after provenance review; repeat as needed",
    )

    args = parser.parse_args(argv)
    try:
        if args.command == "discover":
            result = discover(args.har, args.event)
        elif args.command == "roundtrip":
            result = roundtrip(args.har)
        else:
            ref_entries, rep_entries = load_entries(args.reference_har), load_entries(args.replica_har)
            _entry_number(ref_entries, str(args.reference_entry))
            _entry_number(rep_entries, str(args.replica_entry))
            result = compare(
                args.reference_har,
                args.reference_entry,
                args.replica_har,
                args.replica_entry,
                dynamic_properties=set(args.dynamic_property),
            )
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
