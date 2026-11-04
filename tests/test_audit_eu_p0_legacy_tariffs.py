#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_eu_p0_legacy_tariffs import (  # noqa: E402
    DEFAULT_MANIFEST,
    extract_layers,
    load_manifest,
    scan_html,
    scan_text,
)


class LegacyTariffRuleTests(unittest.TestCase):
    def legacy_fee_findings(self, text):
        return [f for f in scan_text("/test", "test.html", "visible_text", text) if f.rule == "legacy_travel_fee"]

    def test_old_fees_are_detected_in_each_required_order_and_format(self):
        examples = [
            "25 € de deslocação",
            "Deslocação: 25 €",
            "deslocação de 25 €",
            "25€ deslocação",
            "25 euros de deslocação",
            "Deslocações: 25€",
            "Taxas de saída: 25 euros",
            "custo de deslocação 25 €",
            "25 euros de despesas de deslocação",
            "15-65€ deslocação conforme zona",
            "Deslocação — 15 € a 65 euros",
        ]
        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(self.legacy_fee_findings(example), f"legacy fee not detected: {example}")

    def test_current_approved_fees_do_not_trigger_legacy_fee_rule(self):
        approved = [
            "30 € de deslocação em dias úteis, das 09h às 18h",
            "50 € de deslocação à noite, aos fins de semana e feriados",
            "70 €/h + 30 € de deslocação; 100 €/h + 50 € de deslocação",
            "Valores com IVA incluído (TTC); cada hora iniciada é devida.",
        ]
        for text in approved:
            with self.subTest(text=text):
                self.assertEqual(self.legacy_fee_findings(text), [])

    def test_old_zones_surcharges_and_hours_are_detected(self):
        cases = {
            "zona Z1 até Z6": "legacy_zone_token",
            "Zona 2 · 25 € deslocação": "legacy_zone_token",
            "Zona 2–4 · 25 € deslocação": "legacy_zone_token",
            "Z1-Z6": "legacy_zone_token",
            "Zona 3 · 45€ deslocação": "legacy_zone_token",
            "em Zona 4": "legacy_zone_token",
            "+50% à noite": "legacy_surcharge",
            "+30–50% sobre o serviço": "legacy_surcharge",
            "majoração de 50%": "legacy_surcharge",
            "horário 09h–17h": "legacy_hours",
            "horário 08:00–18:00": "legacy_hours",
            "horário 8h-18h": "legacy_hours",
        }
        for text, expected_rule in cases.items():
            with self.subTest(text=text):
                findings = scan_text("/test", "test.html", "visible_text", text)
                self.assertTrue(any(f.rule == expected_rule for f in findings), text)

    def test_obsolete_first_hour_totals_are_distinguished_from_current_totals(self):
        old_totals = ["A partir de 95€ (1h)", "A partir de 105 € (1h)", "Desde 135 euros"]
        for text in old_totals:
            with self.subTest(text=text):
                findings = scan_text("/test", "test.html", "metadata", text)
                self.assertTrue(any(f.rule == "legacy_starting_total" for f in findings), text)
        current_totals = ["A partir de 100 €", "A partir de 150€", "100 €/h + 30 € de deslocação"]
        for text in current_totals:
            with self.subTest(text=text):
                findings = scan_text("/test", "test.html", "metadata", text)
                self.assertFalse(any(f.rule == "legacy_starting_total" for f in findings), text)

    def test_html_layers_keep_body_metadata_attributes_and_jsonld_separate(self):
        raw = (
            '<html><head><title>Eletricista 55€ de deslocação</title>'
            '<meta name="description" content="25€ de deslocação + 70€/h">'
            '</head><body><p title="35€ de deslocação">45€ <strong>de deslocação</strong></p>'
            '<script type="application/ld+json">'
            '{"@type":"FAQPage","text":"Deslocação: 25 euros"}'
            '</script></body></html>'
        )
        visible, jsonld, metadata, attributes = extract_layers(raw)
        self.assertNotIn("55€", visible)
        self.assertNotIn("25€", visible)
        self.assertIn("45€ de deslocacao", " ".join(visible.split()))
        self.assertIn("Eletricista 55€ de deslocação", metadata)
        self.assertIn("25€ de deslocação + 70€/h", metadata)
        self.assertIn("35€ de deslocação", attributes)
        self.assertTrue(any("25 euros" in text for text in jsonld))
        findings = scan_html("/test", "test.html", raw)
        layers = {finding.layer for finding in findings if finding.rule == "legacy_travel_fee"}
        self.assertTrue({"raw_html", "visible_text", "metadata", "html_attribute", "jsonld"}.issubset(layers))

    def test_jsonld_unicode_escape_is_decoded_and_scanned(self):
        raw = '<script type="application/ld+json">{"text":"25 euros de desloca\\u00e7\\u00e3o"}</script>'
        findings = scan_html("/test", "test.html", raw)
        self.assertTrue(any(f.layer == "jsonld" and f.rule == "legacy_travel_fee" for f in findings))

    def test_inline_markup_fee_is_found_in_visible_text_while_raw_scan_stays_separate(self):
        samples = [
            '<p>55 <strong>€</strong> de <em>deslocação</em></p>',
            '<p><strong>55 € de</strong> <span>deslocação</span></p>',
            '<p><span>25</span><b>€</b><i> de deslocação</i></p>',
        ]
        for raw in samples:
            with self.subTest(raw=raw):
                findings = scan_html("/test", "inline.html", raw)
                self.assertTrue(any(f.layer == "visible_text" and f.rule == "legacy_travel_fee" for f in findings))
                self.assertFalse(any(f.layer == "raw_html" and f.rule == "legacy_travel_fee" for f in findings))

    def test_data_zone_attributes_are_detected_in_raw_and_attribute_layers(self):
        raw = '<div class="zone-info" data-zone="3">Deslocação 30 € ou 50 € conforme o horário</div>'
        findings = scan_html("/test", "zone.html", raw)
        self.assertTrue(any(f.layer == "raw_html" and f.rule == "legacy_zone_attribute" for f in findings))
        self.assertTrue(any(f.layer == "html_attribute" and f.rule == "legacy_zone_attribute" for f in findings))

    def test_approved_pilot_manifest_has_116_unique_routes_and_sources(self):
        rows = load_manifest(DEFAULT_MANIFEST)
        self.assertEqual(len(rows), 116)
        self.assertEqual(len({row["route"] for row in rows}), 116)
        self.assertEqual(len({row["source"] for row in rows}), 116)
        for row in rows:
            self.assertTrue((ROOT / row["source"]).is_file(), row["source"])

    def test_approved_corrective_scope_is_exactly_32_pages_within_the_116_pilot(self):
        pilot = load_manifest(DEFAULT_MANIFEST)
        target_path = ROOT / "tests" / "fixtures" / "eu-p0-32-pages.csv"
        targets = load_manifest(target_path, expected_count=32)
        self.assertTrue({r["route"] for r in targets}.issubset({r["route"] for r in pilot}))
        for row in targets:
            self.assertTrue((ROOT / row["source"]).is_file(), row["source"])

    def test_blog_renderer_regenerates_deterministically_and_output_scans_clean(self):
        renderer = ROOT / "scripts" / "render-blog-md.js"
        fixture = ROOT / "tests" / "fixtures" / "blog-safe.md"
        with tempfile.TemporaryDirectory(prefix="eu-p0-render-audit-") as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            for output_dir in (first, second):
                subprocess.run(
                    ["node", str(renderer), "--source", str(fixture), "--out-dir", str(output_dir)],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            generated = first / "teste-seguranca-eletrica.html"
            generated_again = second / "teste-seguranca-eletrica.html"
            self.assertTrue(generated.is_file())
            self.assertEqual(generated.read_bytes(), generated_again.read_bytes(), "generation must be deterministic")
            findings = scan_html("/blog/teste-seguranca-eletrica", generated.name, generated.read_text(encoding="utf-8"))
            self.assertEqual(findings, [], json.dumps([f.__dict__ for f in findings], ensure_ascii=False))


if __name__ == "__main__":
    unittest.main(verbosity=2)
