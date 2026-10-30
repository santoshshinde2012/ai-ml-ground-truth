"""Meaningful contract, evaluation and delivery checks for the reference lab."""

import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

LAB = Path(__file__).resolve().parents[1] / "ground_truth_lab.py"
REFERENCE = LAB.parent / "reference"
SPEC = importlib.util.spec_from_file_location("ground_truth_lab", LAB)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def run_lab(*arguments):
    """Run the documented command line exactly as a reader would."""
    return subprocess.run([sys.executable, str(LAB), *arguments], capture_output=True, text=True, timeout=120)


def tree(folder):
    """Every file below a folder as relative path -> bytes."""
    return {path.relative_to(folder).as_posix(): path.read_bytes() for path in sorted(folder.rglob("*")) if path.is_file()}


def relative_links(markdown):
    return [target for target in re.findall(r"\]\(([^)\s]+)\)", markdown) if not re.match(r"[a-z]+:|#", target)]


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


class ReleaseGateTests(unittest.TestCase):
    """The default simulator always passes, so each other path is constructed directly."""

    def gate(self, lower, upper, candidate_brier, baseline_brier=0.25):
        return lab.release_gate({"lower_95": lower, "upper_95": upper},
                                {"brier": baseline_brier}, {"brier": candidate_brier})

    def test_a_clear_probability_gain_passes(self):
        self.assertEqual(self.gate(-0.29, -0.12, 0.17), "pass_simulated_gate")
        self.assertEqual(self.gate(-0.29, -0.12, 0.25), "pass_simulated_gate")

    def test_an_uncertain_gain_defers(self):
        self.assertEqual(self.gate(-0.08, 0.01, 0.17), "defer")
        self.assertEqual(self.gate(-0.08, -0.005, 0.17), "defer")
        self.assertEqual(self.gate(-0.08, -0.01, 0.17), "defer")

    def test_a_worse_brier_score_defers_despite_a_log_loss_gain(self):
        self.assertEqual(self.gate(-0.29, -0.12, 0.2501), "defer")

    def test_a_regression_keeps_the_baseline(self):
        # There is no separate regression label: a reliably worse candidate defers.
        self.assertEqual(self.gate(0.02, 0.09, 0.30), "defer")


class ExperimentTests(unittest.TestCase):
    def test_sample_ratio_mismatch_blocks_the_analysis(self):
        with self.assertRaisesRegex(ValueError, "Sample ratio mismatch: 249 control vs 426 contact"):
            lab.sample_ratio_check({0: 249, 1: 426})
        check = lab.sample_ratio_check({0: 374, 1: 426})
        self.assertAlmostEqual(check["chi_square"], 2 * 26 ** 2 / 400)
        self.assertAlmostEqual(check["p_value"], 0.0659921, places=6)
        with self.assertRaisesRegex(ValueError, "control/contact counts"):
            lab.sample_ratio_check({0: 0, 1: 0})

    def test_sample_ratio_uses_the_designed_allocation(self):
        self.assertGreater(lab.sample_ratio_check({0: 600, 1: 200}, probability=0.25)["p_value"], 0.001)
        with self.assertRaisesRegex(ValueError, "Sample ratio mismatch"):
            lab.sample_ratio_check({0: 400, 1: 400}, probability=0.25)

    def test_intention_to_treat_interval_power_and_decision(self):
        control = [0.0] * 50 + [100.0] * 50
        contact = [0.0] * 40 + [100.0] * 60
        result = lab.intention_to_treat(control, contact, known_effect=10)
        variances = (100 * 50 ** 2 / 99, (40 * 60 ** 2 + 60 * 40 ** 2) / 99)
        error = math.sqrt(variances[0] / 100 + variances[1] / 100)
        self.assertAlmostEqual(result["difference"], 10)
        self.assertAlmostEqual(result["standard_error"], error)
        self.assertAlmostEqual(result["lower_95"], 10 - 1.96 * error)
        self.assertAlmostEqual(result["minimum_detectable_effect_80_power"], 2.8 * error)
        self.assertEqual(result["accounts_per_arm_to_detect_designed_effect"],
                         math.ceil(2 * 2.8 ** 2 * (variances[0] + variances[1]) / 2 / 10 ** 2))
        self.assertEqual(result["decision"], "inconclusive")
        self.assertEqual(lab.intention_to_treat(control, [100.0] * 99 + [0.0], 10)["decision"], "positive_simulated_effect")
        self.assertEqual(lab.intention_to_treat([100.0] * 99 + [0.0], control, 10)["decision"], "negative_simulated_effect")
        with self.assertRaisesRegex(ValueError, "at least two"):
            lab.intention_to_treat([1.0], contact, 10)

    def test_power_constants_reproduce_the_delivery_plan_example(self):
        # 09-business-machine-learning/delivery-plan.md: SD 200, effect 5 -> about 25,088 per arm.
        self.assertAlmostEqual(2 * (lab.Z_ALPHA + lab.Z_POWER) ** 2 * 200 ** 2 / 5 ** 2, 25088)


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
        cls.output = Path(cls.directory.name) / "run"
        lab.generate(cls.output)
        cls.result = lab.evaluate(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def copy(self):
        """A disposable copy of the shared run, so no test can leak edits into another."""
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        return Path(shutil.copytree(self.output, Path(folder.name) / "run"))

    def rewrite(self, run, name, change):
        lab.write_csv(run / name, change(lab.read_csv(run / name)))

    def refresh_hashes(self, run):
        """Simulate a careless editor who also updates the checksums."""
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        manifest["files"] = {name: lab.digest(run / name) for name in manifest["files"]}
        lab.write_json(run / "manifest.json", manifest)
        return manifest

    def test_data_and_chronological_maturity_contracts(self):
        rows, manifest = lab.load_rows(self.output)
        self.assertEqual(len(rows), 600)
        self.assertEqual(self.result["cohort_sizes"], {"train": 300, "calibration": 150, "test": 150})
        self.assertEqual(manifest["seed"], 42)
        self.assertEqual(set(manifest["files"]), lab.SOURCE_FILES)
        invalid = [dict(row) for row in rows]
        invalid[0]["label_available_at"] = "2030-01-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "mature-label gap"):
            lab.validate_cohorts(invalid)

    def test_missing_coverage_is_rejected_even_with_a_new_source_hash(self):
        run = self.copy()
        self.rewrite(run, "data/outcomes.csv", lambda rows: [{**rows[0], "coverage_complete": 0}, *rows[1:]])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "Unknown outcome coverage"):
            lab.load_rows(run)

    def test_an_unfinished_label_is_rejected_even_with_a_new_source_hash(self):
        run = self.copy()
        self.rewrite(run, "data/outcomes.csv",
                     lambda rows: [{**rows[0], "label_available_at": "2030-01-01T00:00:00Z"}, *rows[1:]])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "Immature outcome"):
            lab.load_rows(run)

    def test_source_changes_are_detected(self):
        run = self.copy()
        (run / "data/documents/contact-policy.md").write_text("silently changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "checksum"):
            lab.load_rows(run)

    def test_a_deleted_manifest_entry_cannot_hide_a_changed_source(self):
        run = self.copy()
        self.rewrite(run, "data/outcomes.csv", lambda rows: [{**row, "churn_30d": 1 - int(row["churn_30d"])} for row in rows])
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        del manifest["files"]["data/outcomes.csv"]
        lab.write_json(run / "manifest.json", manifest)
        with self.assertRaisesRegex(ValueError, r"exactly the lab's source files \(missing: data/outcomes.csv; unexpected: none\)"):
            lab.evaluate(run)

    def test_an_unexpected_manifest_entry_is_rejected(self):
        run = self.copy()
        (run / "data/notes.txt").write_text("not a lab input", encoding="utf-8")
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        manifest["files"]["data/notes.txt"] = lab.digest(run / "data/notes.txt")
        lab.write_json(run / "manifest.json", manifest)
        with self.assertRaisesRegex(ValueError, "missing: none; unexpected: data/notes.txt"):
            lab.load_rows(run)

    def test_manifest_paths_cannot_escape_the_output_directory(self):
        run = self.copy()
        (run.parent / "outside.csv").write_text("x\n", encoding="utf-8")
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        manifest["files"]["../outside.csv"] = lab.digest(run.parent / "outside.csv")
        lab.write_json(run / "manifest.json", manifest)
        with self.assertRaisesRegex(ValueError, "escapes output directory"):
            lab.load_rows(run)

    def test_data_from_another_lab_version_must_be_regenerated(self):
        run = self.copy()
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        manifest["lab_version"] = "0.9.0"
        lab.write_json(run / "manifest.json", manifest)
        with self.assertRaisesRegex(ValueError, "Regenerate data using this lab version"):
            lab.load_rows(run)

    def test_a_snapshot_must_match_its_point_in_time_rebuild(self):
        run = self.copy()
        self.rewrite(run, "data/snapshots.csv",
                     lambda rows: [{**rows[0], "purchases_30d": float(rows[0]["purchases_30d"]) + 1}, *rows[1:]])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "Point-in-time feature mismatch: purchases_30d"):
            lab.load_rows(run)

    def test_duplicate_outcomes_are_rejected(self):
        run = self.copy()
        self.rewrite(run, "data/outcomes.csv", lambda rows: [*rows, rows[0]])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "Duplicate outcomes"):
            lab.load_rows(run)

    def test_experiment_outcomes_must_not_be_zero_filled(self):
        run = self.copy()
        self.rewrite(run, "data/experiment_outcomes.csv",
                     lambda rows: [{**rows[0], "coverage_complete": 0, "net_contribution": 0}, *rows[1:]])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "replacing missing outcomes with zeros"):
            lab.evaluate(run)

    def test_sample_ratio_mismatch_stops_the_experiment_analysis(self):
        run = self.copy()
        dropped = {row["decision_id"] for row in lab.read_csv(run / "data/assignments.csv")
                   if row["assigned_contact"] == "0"}
        dropped = set(sorted(dropped)[:125])
        self.rewrite(run, "data/assignments.csv", lambda rows: [row for row in rows if row["decision_id"] not in dropped])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "join one-to-one"):
            lab.evaluate(run)
        self.rewrite(run, "data/experiment_outcomes.csv",
                     lambda rows: [row for row in rows if row["decision_id"] not in dropped])
        self.refresh_hashes(run)
        with self.assertRaisesRegex(ValueError, "Sample ratio mismatch: 249 control vs 426 contact"):
            lab.evaluate(run)

    def test_the_experiment_is_reported_as_inconclusive_with_its_uncertainty(self):
        experiment = self.result["business"]["randomized_experiment"]
        itt = experiment["intention_to_treat"]
        self.assertEqual(experiment["arm_sizes"], {"0": 374, "1": 426})
        self.assertEqual(experiment["delivered_by_arm"]["0"], 0)
        self.assertGreater(experiment["sample_ratio_check"]["p_value"], lab.SRM_ALPHA)
        self.assertLess(itt["lower_95"], 0)
        self.assertGreater(itt["upper_95"], 0)
        self.assertAlmostEqual(itt["standard_error"], 3.4, delta=0.1)
        self.assertAlmostEqual(itt["simulator_designed_effect"], 2.7, delta=0.01)
        self.assertGreater(itt["accounts_per_arm_to_detect_designed_effect"], 10 * max(experiment["arm_sizes"].values()))
        self.assertEqual(self.result["experiment_decision"], "inconclusive")
        report = (self.output / "reports/evaluation.md").read_text(encoding="utf-8")
        self.assertIn("**Contact experiment:** `inconclusive`", report)
        self.assertIn(f"[{itt['lower_95']:.6f}, {itt['upper_95']:.6f}]", report)
        self.assertIn("underpowered", report)

    def test_seed_recreates_source_bytes_and_reports(self):
        with tempfile.TemporaryDirectory() as folder:
            another = Path(folder)
            lab.generate(another)
            lab.evaluate(another)
            original, repeated = tree(self.output), tree(another)
            self.assertEqual(sorted(original), sorted(repeated))
            for name in original:
                with self.subTest(file=name):
                    self.assertEqual(original[name], repeated[name])
            lab.generate(another, seed=7)
            self.assertNotEqual((another / "data/events.csv").read_bytes(), original["data/events.csv"])

    def test_test_labels_and_features_cannot_change_fitted_parameters(self):
        run = self.copy()
        test_ids = {row["snapshot_id"]: row["customer_id"]
                    for row in lab.read_csv(run / "data/snapshots.csv") if row["cohort"] == "test"}
        test_customers = set(test_ids.values())
        # Flip every final-test label and delete every final-test event, rebuilding
        # those snapshots so all data contracts still pass. Only the test cohort changes.
        self.rewrite(run, "data/outcomes.csv", lambda rows: [
            {**row, "churn_30d": 1 - int(row["churn_30d"])} if row["snapshot_id"] in test_ids else row for row in rows])
        self.rewrite(run, "data/events.csv", lambda rows: [row for row in rows if row["customer_id"] not in test_customers])
        self.rewrite(run, "data/snapshots.csv", lambda rows: [
            {**row, **lab.features_at([], row["as_of"])} if row["snapshot_id"] in test_ids else row for row in rows])
        self.refresh_hashes(run)
        changed = lab.evaluate(run)
        self.assertEqual((run / "reports/model.json").read_bytes(), (self.output / "reports/model.json").read_bytes())
        self.assertNotEqual(changed["candidate"]["log_loss"], self.result["candidate"]["log_loss"])
        self.assertNotEqual(changed["baseline"]["prevalence"], self.result["baseline"]["prevalence"])

    def test_a_deferred_gate_flows_into_every_record(self):
        run = self.copy()
        with mock.patch.object(lab, "release_gate", return_value="defer"):
            result = lab.evaluate(run)
        self.assertEqual(result["prototype_decision"], "defer")
        release = json.loads((run / "reports/release-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(release["decision"], "defer")
        self.assertFalse(release["real_world_launch_approved"])
        self.assertIn("**Decision:** `defer`", (run / "reports/evaluation.md").read_text(encoding="utf-8"))

    def test_business_example_and_bundle_have_honest_boundaries(self):
        business = self.result["business"]
        self.assertEqual(business["conversion_winner"], 20)
        self.assertEqual(business["contribution_winner"], 25)
        self.assertEqual(business["retention"]["risk_expected_increment"], -4)
        self.assertEqual(business["retention"]["value_expected_increment"], 28)
        release = json.loads((self.output / "reports/release-manifest.json").read_text())
        self.assertFalse(release["real_world_launch_approved"])
        self.assertEqual(release["experiment_decision"], "inconclusive")
        self.assertEqual(release["model_sha256"], lab.digest(self.output / "reports/model.json"))
        self.assertEqual(release["source_sha256"], lab.digest(LAB))
        self.assertTrue((self.output / "figures/calibration.svg").is_file())
        self.assertTrue((self.output / "reports/incident-report.md").is_file())

    def test_run_report_links_resolve_in_the_run_layout(self):
        reports = self.output / "reports"
        links = relative_links((reports / "evaluation.md").read_text(encoding="utf-8"))
        self.assertIn("../figures/calibration.svg", links)
        for link in links:
            with self.subTest(link=link):
                self.assertTrue((reports / link).is_file())


class CommandLineTests(unittest.TestCase):
    def test_all_then_evaluate_succeed(self):
        with tempfile.TemporaryDirectory() as folder:
            completed = run_lab("all", "--output", folder)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("Simulated gate: pass_simulated_gate; contact experiment: inconclusive", completed.stdout)
            self.assertEqual(run_lab("evaluate", "--output", folder).returncode, 0)

    def test_lab_errors_exit_with_status_two(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = run_lab("evaluate", "--output", str(Path(folder) / "never-generated"))
            self.assertEqual(missing.returncode, 2)
            self.assertTrue(missing.stderr.startswith("Lab error:"), missing.stderr)
            self.assertEqual(run_lab("generate", "--output", folder, "--seed", "3").returncode, 0)
            (Path(folder) / "data/documents/price-policy.md").write_text("changed", encoding="utf-8")
            tampered = run_lab("evaluate", "--output", folder)
            self.assertEqual(tampered.returncode, 2)
            self.assertIn("Lab error: Source checksum mismatch: data/documents/price-policy.md", tampered.stderr)


class ReferenceTests(unittest.TestCase):
    """labs/reference/ must be exactly what the documented command writes."""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.fresh = Path(cls.directory.name)
        cls.completed = run_lab("reference", "--output", str(cls.fresh))

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_checked_in_reference_is_byte_identical_to_a_fresh_regeneration(self):
        self.assertEqual(self.completed.returncode, 0, self.completed.stderr)
        checked_in = sorted(path.name for path in REFERENCE.iterdir() if not path.name.startswith("."))
        self.assertEqual(checked_in, sorted(lab.REFERENCE_FILES))
        self.assertEqual(sorted(path.name for path in self.fresh.iterdir()), sorted(lab.REFERENCE_FILES))
        for name in lab.REFERENCE_FILES:
            with self.subTest(file=name):
                self.assertEqual(lab.digest(REFERENCE / name), lab.digest(self.fresh / name),
                                 f"labs/reference/{name} is stale. From the repository root run "
                                 "`python3 labs/ground_truth_lab.py reference`, review the diff and commit it.")

    def test_reference_report_links_are_flat_siblings(self):
        # The website serves labs/reference/ as /lab-reference/ and resolves links against it.
        links = relative_links((REFERENCE / "evaluation.md").read_text(encoding="utf-8"))
        self.assertIn("calibration.svg", links)
        self.assertIn("pricing.svg", links)
        for link in links:
            with self.subTest(link=link):
                self.assertNotIn("/", link)
                self.assertTrue((REFERENCE / link).is_file())


if __name__ == "__main__":
    unittest.main()
