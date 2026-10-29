#!/usr/bin/env python3
"""Synthetic tests for natural_for_ajax.py; no private HAR required."""

import unittest

from natural_for_ajax import (
    ProtocolError,
    compare_entries,
    discover_requests,
    encode_component,
    js_length,
    parse_natural_stream,
    serialize_natural_stream,
)


def make_stream(*, plate="ABC1234", stamp="INIT"):
    del stamp  # The stream carries delta; STAMP is a sibling form field.
    return serialize_natural_stream(
        "v",
        [
            "CASA_123456",
            "process-id",
            "",
            "com.example+VES0009X",
            "dummy",
            "https://target.example.com/portal/UIC-SERVICOS/VES0009X.html",
            "cmd_consultar_placa",
            "false",
        ],
        [
            ("v_filtro_error", ""),
            ("v_placa", plate),
            ("#f12_selected", "2.0"),
            ("interceptor_params.items[0].interceptor_value", "S37"),
            ("unicode", "A😀"),
        ],
        "delta-01",
    )


def make_entry(*, plate="ABC1234", user_agent="Brave/156", reverse_headers=False):
    stream = make_stream(plate=plate)
    headers = [
        {"name": "Accept", "value": "text/html"},
        {"name": "User-Agent", "value": user_agent},
        {"name": "Cookie", "value": "JSESSIONID=first; TS=second"},
        {"name": "Content-Length", "value": "999"},
    ]
    if reverse_headers:
        headers = list(reversed(headers))
    return {
        "request": {
            "method": "POST",
            "url": "https://target.example.com/portal/servlet/Connector",
            "headers": headers,
            "cookies": [{"name": "JSESSIONID"}, {"name": "TS"}],
            "postData": {
                "params": [
                    {"name": "SESSIONID", "value": "CASA_123456"},
                    {"name": "PAGEINITPARAM", "value": ""},
                    {"name": "XML", "value": stream},
                    {"name": "ERRORMESSAGE", "value": ""},
                    {"name": "STAMP", "value": "dynamic-stamp"},
                ]
            },
        }
    }


class NaturalProtocolTests(unittest.TestCase):
    def test_javascript_length_counts_utf16_units(self):
        self.assertEqual(js_length("A😀"), 3)

    def test_encode_component_uses_javascript_safe_set(self):
        self.assertEqual(
            encode_component("https://x.test/a+b#c[0]!~*'()"),
            "https%3A%2F%2Fx.test%2Fa%2Bb%23c%5B0%5D!~*'()",
        )

    def test_roundtrip_preserves_encoding_property_order_and_unicode(self):
        original = make_stream()
        self.assertIn("%23f12_selected", original)
        self.assertIn("%5B0%5D", original)
        self.assertIn("com.example%2BVES0009X", original)
        parsed = parse_natural_stream(original)
        self.assertEqual(parsed.event, "cmd_consultar_placa")
        self.assertEqual(dict(parsed.properties)["unicode"], "A😀")
        self.assertEqual(
            serialize_natural_stream(parsed.kind, parsed.parts, parsed.properties, parsed.delta),
            original,
        )

    def test_truncated_stream_is_rejected(self):
        with self.assertRaises(ProtocolError):
            parse_natural_stream(make_stream()[:-1])

    def test_compare_accepts_only_proven_dynamic_differences(self):
        reference = make_entry(plate="ABC1234")
        replica = make_entry(plate="XYZ9Z99")
        replica["request"]["postData"]["params"][0]["value"] = "CASA_123456"
        result = compare_entries(reference, replica, dynamic_properties={"v_placa"})
        self.assertTrue(result["ok"], result)

    def test_compare_rejects_undeclared_business_input_difference(self):
        result = compare_entries(make_entry(plate="ABC1234"), make_entry(plate="XYZ9Z99"))
        self.assertFalse(result["ok"])
        self.assertIn("XML.properties.v_placa", {item["path"] for item in result["mismatches"]})

    def test_discovery_and_compare_survive_shifted_har_indices(self):
        static = {
            "request": {
                "method": "GET",
                "url": "https://target.example.com/static/app.js",
                "headers": [],
            },
        }
        reference = [static, make_entry(plate="ABC1234")]
        replica = [static] * 9 + [make_entry(plate="XYZ9Z99")]

        reference_matches = discover_requests(reference, event="cmd_consultar_placa")
        replica_matches = discover_requests(replica, event="cmd_consultar_placa")

        self.assertEqual([item["entry"] for item in reference_matches], [1])
        self.assertEqual([item["entry"] for item in replica_matches], [9])
        result = compare_entries(
            reference[reference_matches[0]["entry"]],
            replica[replica_matches[0]["entry"]],
            dynamic_properties={"v_placa"},
        )
        self.assertTrue(result["ok"], result)

    def test_compare_rejects_static_header_change(self):
        result = compare_entries(make_entry(), make_entry(user_agent="Chrome/141"))
        self.assertFalse(result["ok"])
        self.assertIn("headers[1].user-agent", {item["path"] for item in result["mismatches"]})

    def test_compare_rejects_static_property_change(self):
        replica = make_entry()
        params = replica["request"]["postData"]["params"]
        parsed = parse_natural_stream(params[2]["value"])
        properties = [
            (name, "OTHER" if name == "interceptor_params.items[0].interceptor_value" else value)
            for name, value in parsed.properties
        ]
        params[2]["value"] = serialize_natural_stream(parsed.kind, parsed.parts, properties, parsed.delta)
        result = compare_entries(make_entry(), replica)
        self.assertFalse(result["ok"])
        self.assertIn(
            "XML.properties.interceptor_params.items[0].interceptor_value",
            {item["path"] for item in result["mismatches"]},
        )

    def test_compare_rejects_header_reordering(self):
        result = compare_entries(make_entry(), make_entry(reverse_headers=True))
        self.assertFalse(result["ok"])
        self.assertIn("headers.order", {item["path"] for item in result["mismatches"]})

    def test_compare_rejects_session_provenance_mismatch(self):
        replica = make_entry()
        replica["request"]["postData"]["params"][0]["value"] = "different-session"
        result = compare_entries(make_entry(), replica)
        self.assertFalse(result["ok"])
        self.assertIn("replica.SESSIONID.provenance", {item["path"] for item in result["mismatches"]})


if __name__ == "__main__":
    unittest.main()
