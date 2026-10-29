"""Meaningful contract, evaluation and delivery checks for the reference lab."""

import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("ground_truth_lab", Path(__file__).resolve().parents[1] / "ground_truth_lab.py")
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


class HistoricalFeatureTests(unittest.TestCase):
    def event(self, identity, occurred, available, kind="purchase"):
        return {"event_id": identity, "event_time": occurred, "available_at": available, "kind": kind}

    def test_event_and_availability_clocks_both_apply(self):
        events = [
            self.event("usable", "2025-01-29T12:00:00Z", "2025-01-30T12:00:00Z"),
            self.event("late", "2025-01-30T12:00:00Z", "2025-02-02T12:00:00Z"),
            self.event("future", "2025-02-02T12:00:00Z", "2025-02-02T12:00:00Z"),
            self.event("old", "2024-12-01T12:00:00Z", "2024-12-01T12:00:00Z"),
        ]
        row = lab.features_at(events, "2025-02-01T12:00:00Z")
        self.assertEqual(row["purchases_30d"], 1)
        self.assertEqual(row["recency_days"], 3)

    def test_boundary_event_is_excluded_but_boundary_availability_is_allowed(self):
        as_of = "2025-02-01T12:00:00Z"
        events = [self.event("at-cutoff", as_of, as_of),
                  self.event("arrives-at-cutoff", "2025-01-31T12:00:00Z", as_of)]
        self.assertEqual(lab.features_at(events, as_of)["purchases_30d"], 1)

    def test_duplicates_and_impossible_clocks_fail(self):
        event = self.event("same", "2025-01-30T12:00:00Z", "2025-01-30T12:00:00Z")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            lab.features_at([event, event], "2025-02-01T12:00:00Z")
        with self.assertRaisesRegex(ValueError, "before it occurs"):
            lab.features_at([self.event("bad", "2025-01-30T12:00:00Z", "2025-01-29T12:00:00Z")], "2025-02-01T12:00:00Z")

    def test_timezone_is_required(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            lab.clock("2025-01-01T12:00:00")


class EvaluationTests(unittest.TestCase):
    def test_metric_arithmetic_and_ties(self):
        report = lab.metrics([0, 0, 1, 1], [0.1, 0.4, 0.6, 0.9], 0.5)
        self.assertAlmostEqual(report["brier"], 0.085)
        self.assertEqual(report["roc_auc"], 1)
        self.assertEqual(report["confusion"], {"tn": 2, "fp": 0, "fn": 0, "tp": 2})
        self.assertEqual(lab.auc([0, 1], [0.5, 0.5]), 0.5)
        self.assertIsNone(lab.auc([1, 1], [0.2, 0.8]))
        self.assertAlmostEqual(lab.log_loss(1, 0.5), math.log(2))

    def test_bootstrap_keeps_paired_differences_and_is_reproducible(self):
        constant = lab.paired_bootstrap([-0.2] * 20, draws=100)
        self.assertAlmostEqual(constant["lower_95"], -0.2)
        self.assertAlmostEqual(constant["upper_95"], -0.2)
        varied = [-0.4, -0.1, 0.1, 0.2]
        self.assertEqual(lab.paired_bootstrap(varied), lab.paired_bootstrap(varied))

    def test_judge_confusion_has_the_intended_denominators(self):
        report = lab.judge_fixture()
        self.assertEqual(report["confusion"], {"tp": 26, "fn": 4, "fp": 3, "tn": 17})
        self.assertAlmostEqual(report["false_acceptance_rate"], 3 / 20)
        self.assertAlmostEqual(report["precision"], 26 / 29)

    def test_contact_budget_and_positive_value(self):
        rows = [{"customer_id": "a", "value": -1}, {"customer_id": "b", "value": 9},
                {"customer_id": "c", "value": 10}, {"customer_id": "d", "value": 20, "eligible": False}]
        self.assertEqual(lab.choose_contacts(rows, "value", budget=7, contact_cost=4), ["c"])
        self.assertEqual(lab.choose_contacts(rows, "value", budget=100, contact_cost=4), ["c", "b"])
        with self.assertRaisesRegex(ValueError, "unique"):
            lab.choose_contacts([rows[0], rows[0]], "value", 8)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.ledger = lab.DecisionLedger(8)

    def tearDown(self):
        self.ledger.close()

    def test_retry_does_not_reserve_or_create_an_action_twice(self):
        self.assertEqual(self.ledger.reserve("decision-1", "customer-1", 4), "reserved")
        self.assertEqual(self.ledger.reserve("decision-1", "customer-1", 4), "reserved")
        self.assertEqual(self.ledger.remaining, 4)
        self.assertEqual(len(self.ledger.rows()), 1)
        with self.assertRaisesRegex(ValueError, "second action"):
            self.ledger.reserve("decision-2", "customer-1", 4)
        self.assertEqual(self.ledger.remaining, 4)

    def test_unknown_result_keeps_reservation_until_reconciled(self):
        self.ledger.reserve("decision-1", "customer-1", 4)
        self.ledger.settle("decision-1", "unknown")
        self.assertEqual(self.ledger.reserve("decision-1", "customer-1", 4), "unknown")
        self.assertEqual(self.ledger.remaining, 4)
        self.ledger.settle("decision-1", "confirmed_not_delivered")
        self.ledger.settle("decision-1", "confirmed_not_delivered")
        self.assertEqual(self.ledger.remaining, 8)

    def test_budget_and_terminal_results_are_enforced(self):
        self.ledger.reserve("first", "one", 8)
        self.assertEqual(self.ledger.reserve("second", "two", 1), "budget_exhausted")
        self.ledger.settle("first", "delivered")
        with self.assertRaisesRegex(ValueError, "terminal"):
            self.ledger.settle("first", "confirmed_not_delivered")
        with self.assertRaisesRegex(ValueError, "different"):
            self.ledger.reserve("first", "someone-else", 8)
        self.assertEqual(self.ledger.remaining, 0)


class EndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.output = Path(cls.directory.name)
        lab.generate(cls.output)
        cls.result = lab.evaluate(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_data_and_chronological_maturity_contracts(self):
        rows, manifest = lab.load_rows(self.output)
        self.assertEqual(len(rows), 600)
        self.assertEqual(self.result["cohort_sizes"], {"train": 300, "calibration": 150, "test": 150})
        self.assertEqual(manifest["seed"], 42)
        invalid = [dict(row) for row in rows]
        invalid[0]["label_available_at"] = "2030-01-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "mature-label gap"):
            lab.validate_cohorts(invalid)

    def test_missing_coverage_is_rejected_even_with_a_new_source_hash(self):
        path = self.output / "data/outcomes.csv"
        manifest_path = self.output / "manifest.json"
        original_data = path.read_bytes()
        original_manifest = manifest_path.read_bytes()
        try:
            outcomes = lab.read_csv(path)
            outcomes[0]["coverage_complete"] = 0
            lab.write_csv(path, outcomes)
            manifest = json.loads(original_manifest)
            manifest["files"]["data/outcomes.csv"] = lab.digest(path)
            lab.write_json(manifest_path, manifest)
            with self.assertRaisesRegex(ValueError, "Unknown outcome coverage"):
                lab.load_rows(self.output)
        finally:
            path.write_bytes(original_data)
            manifest_path.write_bytes(original_manifest)

    def test_an_unfinished_label_is_rejected_even_with_a_new_source_hash(self):
        path = self.output / "data/outcomes.csv"
        manifest_path = self.output / "manifest.json"
        original_data = path.read_bytes()
        original_manifest = manifest_path.read_bytes()
        try:
            outcomes = lab.read_csv(path)
            outcomes[0]["label_available_at"] = "2030-01-01T00:00:00Z"
            lab.write_csv(path, outcomes)
            manifest = json.loads(original_manifest)
            manifest["files"]["data/outcomes.csv"] = lab.digest(path)
            lab.write_json(manifest_path, manifest)
            with self.assertRaisesRegex(ValueError, "Immature outcome"):
                lab.load_rows(self.output)
        finally:
            path.write_bytes(original_data)
            manifest_path.write_bytes(original_manifest)

    def test_source_changes_are_detected(self):
        path = self.output / "data/documents/contact-policy.md"
        original = path.read_bytes()
        try:
            path.write_text("silently changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "checksum"):
                lab.load_rows(self.output)
        finally:
            path.write_bytes(original)

    def test_seed_recreates_source_bytes_and_reports(self):
        with tempfile.TemporaryDirectory() as folder:
            another = Path(folder)
            manifest = lab.generate(another)
            self.assertEqual(manifest, json.loads((self.output / "manifest.json").read_text()))
            self.assertEqual(lab.evaluate(another), self.result)

    def test_test_labels_cannot_change_fitted_parameters(self):
        rows, _ = lab.load_rows(self.output)
        train = [row for row in rows if row["cohort"] == "train"]
        calibration = [row for row in rows if row["cohort"] == "calibration"]
        before = lab.fit_model(train, calibration)
        for row in rows:
            if row["cohort"] == "test":
                row["label"] = 1 - row["label"]
                row["purchases_30d"] = 1000000
        after = lab.fit_model(train, calibration)
        self.assertEqual(before, after)

    def test_business_example_and_bundle_have_honest_boundaries(self):
        business = self.result["business"]
        self.assertEqual(business["conversion_winner"], 20)
        self.assertEqual(business["contribution_winner"], 25)
        self.assertEqual(business["retention"]["risk_expected_increment"], -4)
        self.assertEqual(business["retention"]["value_expected_increment"], 28)
        release = json.loads((self.output / "reports/release-manifest.json").read_text())
        self.assertFalse(release["real_world_launch_approved"])
        self.assertEqual(release["model_sha256"], lab.digest(self.output / "reports/model.json"))
        self.assertTrue((self.output / "figures/calibration.svg").is_file())
        self.assertTrue((self.output / "reports/incident-report.md").is_file())


if __name__ == "__main__":
    unittest.main()
