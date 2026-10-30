#!/usr/bin/env python3
"""A reproducible, synthetic reference lab. Python standard library only.

No customer data, network access, trained foundation model, or paid API is used.
Run ``python3 labs/ground_truth_lab.py all --output labs/output``.
Maintainers rebuild the checked-in examples with ``python3 labs/ground_truth_lab.py reference``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sqlite3
import tempfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Any

VERSION = "1.1.0"
SEED = 42
FEATURES = ("purchases_30d", "support_30d", "recency_days")
ORIGIN = datetime(2025, 1, 1, tzinfo=timezone.utc)
COHORTS = {
    "train": {"start": 0, "days": 30, "per_day": 10, "cutoff": 63},
    "calibration": {"start": 65, "days": 15, "per_day": 10, "cutoff": 119},
    "test": {"start": 120, "days": 15, "per_day": 10, "cutoff": 175},
}
TABLES = ("events.csv", "snapshots.csv", "outcomes.csv", "assignments.csv", "experiment_outcomes.csv")
DOCUMENTS = {
    "returns-policy.md": "# Simulated returns policy\n\nProducts may be returned within 30 days. This is fictional teaching material.\n",
    "contact-policy.md": "# Simulated contact policy\n\nContact only eligible consenting accounts. Reserve four units per contact. Do not contact an account twice in this batch.\n",
    "price-policy.md": "# Simulated price policy\n\nThe approved teaching price grid is 20, 25 and 30. Unit cost is 10. Amounts are fictional currency units.\n",
}
# The manifest must list exactly these inputs. A missing entry is not an unchecked file.
SOURCE_FILES = frozenset([f"data/{name}" for name in TABLES] + [f"data/documents/{name}" for name in DOCUMENTS])
# Known simulator mechanism: (no-contact churn risk, retention gain from a delivered contact).
SEGMENTS = {"high_risk": (0.65, 0.02), "saveable": (0.35, 0.18), "stable": (0.10, 0.01)}
ASSIGNMENT_PROBABILITY = 0.5
DELIVERY_PROBABILITY = 0.9
RETAINED_VALUE = 100
CONTACT_COST = 4
# Experiment rules from 09-business-machine-learning/delivery-plan.md: diagnose sample-ratio
# mismatch before reading lift; two-sided 5% test, 80% power, normal approximation.
SRM_ALPHA = 0.001
Z_ALPHA, Z_POWER = 1.96, 0.84
# Flat, checked-in reference name -> path inside an ordinary lab run.
REFERENCE_FILES = {
    "calibration.svg": "figures/calibration.svg", "pricing.svg": "figures/pricing.svg",
    "data-card.md": "reports/data-card.md", "evaluation.json": "reports/evaluation.json",
    "evaluation.md": "reports/evaluation.md", "incident-report.md": "reports/incident-report.md",
    "model-card.md": "reports/model-card.md", "model.json": "reports/model.json",
    "price-comparison.csv": "reports/price-comparison.csv", "release-manifest.json": "reports/release-manifest.json",
}


def stamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def clock(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def sigmoid(value: float) -> float:
    value = max(-35.0, min(35.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("Cannot write a table without rows")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def features_at(events: list[dict[str, Any]], as_of: str) -> dict[str, float]:
    """Immutable, deduplicated events; both occurrence and availability matter."""
    cutoff = clock(as_of)
    seen: set[str] = set()
    usable = []
    for event in events:
        if event["event_id"] in seen:
            raise ValueError("Duplicate event ID")
        seen.add(event["event_id"])
        event_time = clock(event["event_time"])
        available_at = clock(event["available_at"])
        if available_at < event_time:
            raise ValueError("An event cannot be available before it occurs")
        if cutoff - timedelta(days=30) <= event_time < cutoff and available_at <= cutoff:
            usable.append(event)
    purchases = [event for event in usable if event["kind"] == "purchase"]
    last_purchase = max((clock(event["event_time"]) for event in purchases), default=None)
    return {
        "purchases_30d": float(len(purchases)),
        "support_30d": float(sum(event["kind"] == "support" for event in usable)),
        "recency_days": (cutoff - last_purchase).total_seconds() / 86400 if last_purchase else 30.0,
    }


def generate(output: Path, seed: int = SEED) -> dict[str, Any]:
    rng = random.Random(seed)
    events: list[dict[str, Any]] = []
    snapshots: list[dict[str, Any]] = []
    outcomes: list[dict[str, Any]] = []
    customer_number = 0
    event_number = 0
    for cohort, spec in COHORTS.items():
        for day in range(spec["start"], spec["start"] + spec["days"]):
            for _ in range(spec["per_day"]):
                customer_number += 1
                customer = f"customer-{customer_number:04d}"
                as_of = ORIGIN + timedelta(days=day, hours=12)
                customer_events = []
                # Engagement differs between customers. The late and future events
                # are deliberate fixtures, not valid features at the decision time.
                for kind, count in [("purchase", rng.randrange(0, 9)), ("support", rng.randrange(0, 5))]:
                    for _ in range(count):
                        event_number += 1
                        occurred = as_of - timedelta(days=rng.randrange(1, 30), hours=rng.randrange(0, 12))
                        available = occurred + timedelta(days=rng.choice([0, 0, 0, 1, 4, 8]))
                        customer_events.append({
                            "event_id": f"event-{event_number:05d}", "customer_id": customer,
                            "event_time": stamp(occurred), "available_at": stamp(available), "kind": kind,
                        })
                for occurred, available in [
                    (as_of - timedelta(hours=1), as_of + timedelta(days=2)),
                    (as_of + timedelta(days=1), as_of + timedelta(days=1)),
                ]:
                    event_number += 1
                    customer_events.append({
                        "event_id": f"event-{event_number:05d}", "customer_id": customer,
                        "event_time": stamp(occurred), "available_at": stamp(available), "kind": "purchase",
                    })
                row = features_at(customer_events, stamp(as_of))
                events.extend(customer_events)
                snapshot_id = f"snapshot-{customer_number:04d}"
                snapshots.append({"snapshot_id": snapshot_id, "customer_id": customer,
                                  "as_of": stamp(as_of), "cohort": cohort, **row})
                probability = sigmoid(0.25 - 0.45 * row["purchases_30d"] +
                                      0.46 * row["support_30d"] + 0.045 * row["recency_days"] +
                                      (0.15 if cohort == "test" else 0.0))
                # All modelling outcomes are under NO CONTACT. Intervention data
                # below belong to a separate, disjoint randomized experiment.
                outcomes.append({
                    "snapshot_id": snapshot_id, "label_end": stamp(as_of + timedelta(days=30)),
                    "label_available_at": stamp(as_of + timedelta(days=33)),
                    "coverage_complete": 1, "churn_30d": int(rng.random() < probability),
                })
    assignments, experiment_outcomes = [], []
    for number in range(800):
        segment = list(SEGMENTS)[number % 3]
        risk, effect = SEGMENTS[segment]
        assigned = int(rng.random() < ASSIGNMENT_PROBABILITY)
        delivered = int(assigned == 1 and rng.random() < DELIVERY_PROBABILITY)
        retained = int(rng.random() < 1 - risk + delivered * effect)
        identity = f"experiment-{number:04d}"
        assignments.append({"decision_id": identity, "customer_id": f"trial-{number:04d}",
                            "segment": segment, "assigned_contact": assigned,
                            "assignment_probability": ASSIGNMENT_PROBABILITY, "delivered": delivered})
        experiment_outcomes.append({"decision_id": identity, "coverage_complete": 1, "retained": retained,
                                    "net_contribution": retained * RETAINED_VALUE - delivered * CONTACT_COST})
    data = output / "data"
    for name, rows in zip(TABLES, [events, snapshots, outcomes, assignments, experiment_outcomes]):
        write_csv(data / name, rows)
    for name, content in DOCUMENTS.items():
        path = data / "documents" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    files = sorted(path for path in data.rglob("*") if path.is_file())
    manifest = {
        "lab_version": VERSION, "seed": seed, "data_kind": "synthetic; no measured real-world impact",
        "row_grain": "one snapshot per unique modelling customer; disjoint experiment customers",
        "feature_lookback_days": 30, "outcome_horizon_days": 30, "reporting_delay_days": 3,
        "cohorts": {name: {**spec, "fit_or_evaluation_cutoff_utc": stamp(ORIGIN + timedelta(days=spec["cutoff"], hours=12))}
                    for name, spec in COHORTS.items()},
        "files": {str(path.relative_to(output)): digest(path) for path in files},
    }
    write_json(output / "manifest.json", manifest)
    return manifest


def load_rows(output: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    if manifest["lab_version"] != VERSION:
        raise ValueError("Regenerate data using this lab version")
    for name in manifest["files"]:
        if (output / name).resolve().is_relative_to(output.resolve()) is False:
            raise ValueError("Manifest path escapes output directory")
    # A deleted manifest entry would otherwise skip that file's checksum silently.
    listed = set(manifest["files"])
    if listed != SOURCE_FILES:
        missing = ", ".join(sorted(SOURCE_FILES - listed)) or "none"
        unexpected = ", ".join(sorted(listed - SOURCE_FILES)) or "none"
        raise ValueError(f"Manifest must list exactly the lab's source files (missing: {missing}; "
                         f"unexpected: {unexpected}); regenerate or document a new data version")
    for name, expected in manifest["files"].items():
        path = output / name
        if digest(path) != expected:
            raise ValueError(f"Source checksum mismatch: {name}; regenerate or document a new data version")
    events = defaultdict(list)
    for row in read_csv(output / "data/events.csv"):
        events[row["customer_id"]].append(row)
    outcome_rows = read_csv(output / "data/outcomes.csv")
    outcomes = {row["snapshot_id"]: row for row in outcome_rows}
    if len(outcomes) != len(outcome_rows):
        raise ValueError("Duplicate outcomes would violate the snapshot join grain")
    rows, ids, customers = [], set(), set()
    for row in read_csv(output / "data/snapshots.csv"):
        if row["snapshot_id"] in ids or row["customer_id"] in customers:
            raise ValueError("Each modelling customer must have one snapshot")
        ids.add(row["snapshot_id"])
        customers.add(row["customer_id"])
        expected = features_at(events[row["customer_id"]], row["as_of"])
        for feature in FEATURES:
            if not math.isclose(float(row[feature]), expected[feature], abs_tol=1e-9):
                raise ValueError(f"Point-in-time feature mismatch: {feature}")
            row[feature] = float(row[feature])
        label = outcomes[row["snapshot_id"]]
        if label["coverage_complete"] != "1":
            raise ValueError("Unknown outcome coverage must not become a negative label")
        cutoff = clock(manifest["cohorts"][row["cohort"]]["fit_or_evaluation_cutoff_utc"])
        if clock(label["label_available_at"]) > cutoff:
            raise ValueError("Immature outcome at cohort fitting/evaluation cutoff")
        if clock(label["label_end"]) <= clock(row["as_of"]):
            raise ValueError("Outcome horizon must follow the decision")
        if clock(label["label_available_at"]) < clock(label["label_end"]):
            raise ValueError("A complete fixed-horizon label cannot arrive before its horizon ends")
        row["label"] = int(label["churn_30d"])
        if row["label"] not in (0, 1):
            raise ValueError("Churn labels must be binary")
        row["label_available_at"] = label["label_available_at"]
        rows.append(row)
    if len(outcomes) != len(rows):
        raise ValueError("Outcome join must preserve the snapshot grain")
    validate_cohorts(rows)
    return rows, manifest


def validate_cohorts(rows: list[dict[str, Any]]) -> None:
    groups = {name: [row for row in rows if row["cohort"] == name] for name in COHORTS}
    if any(not group for group in groups.values()):
        raise ValueError("Every fixed cohort must contain data")
    if len({row["customer_id"] for row in rows}) != len(rows):
        raise ValueError("Customer overlap would invalidate the independent-unit design")
    for earlier, later in [("train", "calibration"), ("calibration", "test")]:
        if max(clock(row["label_available_at"]) for row in groups[earlier]) >= min(clock(row["as_of"]) for row in groups[later]):
            raise ValueError("Chronological cohorts require a mature-label gap")


def fit_logistic(vectors: list[list[float]], labels: list[int], iterations: int = 700,
                 regularization: float = 0.02) -> list[float]:
    if not vectors or len(vectors) != len(labels):
        raise ValueError("Training vectors and labels must be nonempty and aligned")
    weights = [0.0] * (len(vectors[0]) + 1)
    for _ in range(iterations):
        gradients = [0.0] * len(weights)
        for vector, label in zip(vectors, labels):
            extended = [1.0, *vector]
            # fsum is correctly rounded on every supported Python; built-in float sum
            # changed in 3.12, which would alter the last bits of the reference model.
            error = sigmoid(math.fsum(w * x for w, x in zip(weights, extended))) - label
            for index, value in enumerate(extended):
                gradients[index] += error * value
        for index in range(len(weights)):
            penalty = regularization * weights[index] if index else 0.0
            weights[index] -= 0.08 * (gradients[index] / len(vectors) + penalty)
    return weights


def fit_model(train: list[dict[str, Any]], calibration: list[dict[str, Any]]) -> dict[str, Any]:
    centers = [mean(row[name] for row in train) for name in FEATURES]
    scales = [math.sqrt(mean((row[name] - centers[i]) ** 2 for row in train)) or 1.0 for i, name in enumerate(FEATURES)]
    vectors = [[(row[name] - centers[i]) / scales[i] for i, name in enumerate(FEATURES)] for row in train]
    weights = fit_logistic(vectors, [row["label"] for row in train])
    model = {"features": list(FEATURES), "centers": centers, "scales": scales, "weights": weights,
             "baseline_probability": mean(row["label"] for row in train)}
    # A separate calibration cohort fits a sigmoid to frozen model logits.
    # This is not a guarantee that probabilities remain calibrated after shift.
    logits = [[model_logit(model, row)] for row in calibration]
    model["calibrator"] = fit_logistic(logits, [row["label"] for row in calibration], regularization=0.01)
    model["threshold"] = min(
        [step / 20 for step in range(1, 20)],
        key=lambda threshold: (decision_cost([row["label"] for row in calibration],
                                             [predict(model, row) for row in calibration], threshold), threshold),
    )
    model["baseline_threshold"] = min(
        [step / 20 for step in range(1, 20)],
        key=lambda threshold: (decision_cost([row["label"] for row in calibration],
                                             [model["baseline_probability"]] * len(calibration), threshold), threshold),
    )
    return model


def model_logit(model: dict[str, Any], row: dict[str, Any]) -> float:
    return model["weights"][0] + math.fsum(
        weight * (row[name] - center) / scale
        for name, center, scale, weight in zip(model["features"], model["centers"], model["scales"], model["weights"][1:])
    )


def predict(model: dict[str, Any], row: dict[str, Any]) -> float:
    logit = model_logit(model, row)
    if "calibrator" in model:
        intercept, slope = model["calibrator"]
        logit = intercept + slope * logit
    return sigmoid(logit)


def log_loss(label: int, probability: float) -> float:
    probability = min(1 - 1e-12, max(1e-12, probability))
    return -label * math.log(probability) - (1 - label) * math.log(1 - probability)


def confusion(labels: list[int], predictions: list[int]) -> dict[str, int]:
    if len(labels) != len(predictions) or any(value not in (0, 1) for value in [*labels, *predictions]):
        raise ValueError("Binary labels and predictions must align")
    result = {"tn": 0, "fp": 0, "fn": 0, "tp": 0}
    for label, prediction in zip(labels, predictions):
        result[{(0, 0): "tn", (0, 1): "fp", (1, 0): "fn", (1, 1): "tp"}[(label, prediction)]] += 1
    return result


def decision_cost(labels: list[int], probabilities: list[float], threshold: float) -> float:
    matrix = confusion(labels, [int(value >= threshold) for value in probabilities])
    return (matrix["fp"] * 2 + matrix["fn"] * 10) / len(labels)


def auc(labels: list[int], probabilities: list[float]) -> float | None:
    positive = [p for y, p in zip(labels, probabilities) if y]
    negative = [p for y, p in zip(labels, probabilities) if not y]
    if not positive or not negative:
        return None
    return sum((p > n) + 0.5 * (p == n) for p in positive for n in negative) / (len(positive) * len(negative))


def metrics(labels: list[int], probabilities: list[float], threshold: float) -> dict[str, Any]:
    if not labels or len(labels) != len(probabilities):
        raise ValueError("Evaluation labels and probabilities must align")
    return {"n": len(labels), "prevalence": mean(labels),
            "log_loss": mean(log_loss(y, p) for y, p in zip(labels, probabilities)),
            "brier": mean((y - p) ** 2 for y, p in zip(labels, probabilities)),
            "roc_auc": auc(labels, probabilities), "threshold": threshold,
            "cost_per_customer": decision_cost(labels, probabilities, threshold),
            "confusion": confusion(labels, [int(p >= threshold) for p in probabilities])}


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    low = math.floor(index)
    high = math.ceil(index)
    return ordered[low] + (ordered[high] - ordered[low]) * (index - low)


def paired_bootstrap(differences: list[float], seed: int = SEED, draws: int = 1000) -> dict[str, Any]:
    """Pairs stay together; one row is one independent synthetic customer."""
    if not differences or draws < 2:
        raise ValueError("A nonempty sample and at least two bootstrap draws are required")
    rng = random.Random(seed)
    estimates = [mean(rng.choices(differences, k=len(differences))) for _ in range(draws)]
    return {"mean": mean(differences), "lower_95": percentile(estimates, 0.025),
            "upper_95": percentile(estimates, 0.975), "draws": draws,
            "resampling_unit": "unique synthetic customer; paired predictions"}


def release_gate(interval: dict[str, Any], baseline: dict[str, Any], candidate: dict[str, Any]) -> str:
    """Predeclared probability-quality gate; anything short of a clear gain keeps the baseline."""
    # An uncertain gain, a worse Brier score and a regression (interval above zero) all defer.
    if interval["upper_95"] < -0.01 and candidate["brier"] <= baseline["brier"]:
        return "pass_simulated_gate"
    return "defer"


def sample_ratio_check(arm_sizes: dict[int, int], probability: float = ASSIGNMENT_PROBABILITY,
                       alpha: float = SRM_ALPHA) -> dict[str, Any]:
    """Chi-square goodness of fit of assigned arm sizes against the designed allocation."""
    total = sum(arm_sizes.values())
    if total == 0 or not 0 < probability < 1 or set(arm_sizes) - {0, 1}:
        raise ValueError("A sample-ratio check needs control/contact counts and a designed probability")
    expected = {0: total * (1 - probability), 1: total * probability}
    statistic = math.fsum((arm_sizes.get(arm, 0) - expected[arm]) ** 2 / expected[arm] for arm in (0, 1))
    # One degree of freedom: P(chi-square > x) = erfc(sqrt(x / 2)). Six significant
    # figures are ample for an alarm threshold and keep the report platform-stable.
    p_value = float(f"{math.erfc(math.sqrt(statistic / 2)):.6g}")
    observed = {str(arm): arm_sizes.get(arm, 0) for arm in (0, 1)}
    if p_value < alpha:
        raise ValueError(f"Sample ratio mismatch: {observed['0']} control vs {observed['1']} contact assignments "
                         f"against a designed {probability} allocation (chi-square p={p_value:.3g} < {alpha}). "
                         "Investigate assignment and logging before reading any effect")
    return {"observed": observed, "expected": {str(arm): value for arm, value in expected.items()},
            "chi_square": statistic, "p_value": p_value, "alarm_threshold": alpha}


def intention_to_treat(control: list[float], contact: list[float], known_effect: float) -> dict[str, Any]:
    """Assigned-arm mean difference, unequal-variance standard error and a power check."""
    if len(control) < 2 or len(contact) < 2:
        raise ValueError("Each assigned arm needs at least two observed outcomes")
    arms = [(arm, mean(arm)) for arm in (control, contact)]
    variances = [math.fsum((value - center) ** 2 for value in arm) / (len(arm) - 1) for arm, center in arms]
    difference = arms[1][1] - arms[0][1]
    error = math.sqrt(variances[0] / len(control) + variances[1] / len(contact))
    lower, upper = difference - Z_ALPHA * error, difference + Z_ALPHA * error
    pooled = ((len(control) - 1) * variances[0] + (len(contact) - 1) * variances[1]) / (len(control) + len(contact) - 2)
    # The delivery plan's sanity check: n per arm ≈ 2 × (1.96 + 0.84)^2 × variance / effect^2.
    # This run knows the simulator's effect; a real plan uses a predeclared worthwhile effect
    # and pre-treatment variance, decided before launch rather than after reading the result.
    needed = math.ceil(2 * (Z_ALPHA + Z_POWER) ** 2 * pooled / known_effect ** 2) if known_effect else None
    decision = "inconclusive" if lower <= 0 <= upper else (
        "positive_simulated_effect" if lower > 0 else "negative_simulated_effect")
    return {"estimand": "mean net contribution per assigned account, contact minus control",
            "difference": difference, "standard_error": error, "lower_95": lower, "upper_95": upper,
            "interval_method": "normal approximation, unequal arm variances",
            "minimum_detectable_effect_80_power": (Z_ALPHA + Z_POWER) * error,
            "simulator_designed_effect": known_effect, "accounts_per_arm_to_detect_designed_effect": needed,
            "decision": decision}


def judge_fixture() -> dict[str, Any]:
    # Positive means an answer is acceptable. This fixed 50-case fixture is
    # separate from churn modelling and never uses a paid/model-based judge.
    human = [1] * 30 + [0] * 20
    judge = [1] * 26 + [0] * 4 + [1] * 3 + [0] * 17
    matrix = confusion(human, judge)
    return {"positive_means": "acceptable answer", "source": "hand-constructed 50-case teaching fixture",
            "confusion": matrix, "precision": matrix["tp"] / (matrix["tp"] + matrix["fp"]),
            "recall": matrix["tp"] / (matrix["tp"] + matrix["fn"]),
            "false_acceptance_rate": matrix["fp"] / (matrix["fp"] + matrix["tn"]),
            "limitation": "Fixed fixture arithmetic, not a measured judge or evidence of general reliability"}


def choose_contacts(rows: list[dict[str, Any]], score_key: str, budget: float, contact_cost: float = 4) -> list[str]:
    if budget < 0 or contact_cost <= 0:
        raise ValueError("Budget must be nonnegative and contact cost positive")
    if len({row["customer_id"] for row in rows}) != len(rows):
        raise ValueError("Contact candidates must be unique customers")
    eligible = [row for row in rows if row.get("eligible", True) and row[score_key] > 0]
    return [row["customer_id"] for row in sorted(eligible, key=lambda row: (-row[score_key], row["customer_id"]))[:int(budget // contact_cost)]]


def business_examples(output: Path) -> dict[str, Any]:
    pricing = [{"price": price, "conversion_probability": probability,
                "unit_cost": 10, "expected_contribution_per_opportunity": (price - 10) * probability}
               for price, probability in [(20, 0.30), (25, 0.24), (30, 0.15)]]
    profiles = []
    for index, segment in enumerate(["high_risk", "high_risk", "saveable", "saveable", "stable", "stable"]):
        risk, effect = SEGMENTS[segment]
        profiles.append({"customer_id": f"example-{index + 1}", "segment": segment, "churn_risk": risk,
                         "incremental_value": effect * RETAINED_VALUE - CONTACT_COST, "eligible": True})
    risk_contacts = choose_contacts(profiles, "churn_risk", budget=8)
    value_contacts = choose_contacts(profiles, "incremental_value", budget=8)
    by_customer = {row["customer_id"]: row for row in profiles}
    # Independent experiment: assignment, delivery and outcome remain separate.
    assignments = read_csv(output / "data/assignments.csv")
    outcome_rows = read_csv(output / "data/experiment_outcomes.csv")
    outcomes = {row["decision_id"]: row for row in outcome_rows}
    decisions = {row["decision_id"] for row in assignments}
    if len(decisions) != len(assignments) or len(outcomes) != len(outcome_rows) or set(outcomes) != decisions:
        raise ValueError("Experiment outcomes must join one-to-one with unique assignments")
    arm_values = {arm: [] for arm in (0, 1)}
    delivered_by_arm = {arm: 0 for arm in (0, 1)}
    designed_effects = []
    for row in assignments:
        if row["assigned_contact"] not in ("0", "1") or float(row["assignment_probability"]) != ASSIGNMENT_PROBABILITY:
            raise ValueError("Assignment log disagrees with the designed binary allocation")
        outcome = outcomes[row["decision_id"]]
        if outcome["coverage_complete"] != "1":
            raise ValueError("Do not estimate effect by replacing missing outcomes with zeros")
        arm = int(row["assigned_contact"])
        arm_values[arm].append(float(outcome["net_contribution"]))
        delivered_by_arm[arm] += int(row["delivered"])
        # Oracle only: the simulator knows what an assignment is worth in each segment.
        effect = SEGMENTS[row["segment"]][1]
        designed_effects.append(DELIVERY_PROBABILITY * (effect * RETAINED_VALUE - CONTACT_COST))
    # Diagnose a sample-ratio mismatch before reading any lift; a failure stops the analysis.
    sample_ratio = sample_ratio_check({arm: len(values) for arm, values in arm_values.items()})
    itt = intention_to_treat(arm_values[0], arm_values[1], mean(designed_effects))
    return {
        "currency": "fictional currency units", "pricing": pricing,
        "conversion_winner": max(pricing, key=lambda row: row["conversion_probability"])["price"],
        "contribution_winner": max(pricing, key=lambda row: row["expected_contribution_per_opportunity"])["price"],
        "inventory_example": {"inventory": 10, "mean_demand_both": 10,
                              "served_deterministic_demand_10": 10, "served_half_0_half_20": 5},
        "retention": {"source": "known simulator effects; oracle illustration, not learned causal estimates",
                      "profiles": profiles, "budget": 8, "contact_cost": 4,
                      "risk_contacts": risk_contacts, "value_contacts": value_contacts,
                      "risk_expected_increment": sum(by_customer[c]["incremental_value"] for c in risk_contacts),
                      "value_expected_increment": sum(by_customer[c]["incremental_value"] for c in value_contacts)},
        "randomized_experiment": {"assignment_probability": ASSIGNMENT_PROBABILITY,
                                  "arm_sizes": {str(arm): len(values) for arm, values in arm_values.items()},
                                  "delivery_count": sum(delivered_by_arm.values()),
                                  "delivered_by_arm": {str(arm): count for arm, count in delivered_by_arm.items()},
                                  "sample_ratio_check": sample_ratio,
                                  "intention_to_treat": itt,
                                  "intent_to_treat_contribution_difference": itt["difference"],
                                  "decision": itt["decision"],
                                  "interpretation": "One simulated randomized experiment analysed by assigned arm, including failed deliveries. An interval spanning zero is inconclusive, not evidence of no effect. No real business impact is established."},
    }


class DecisionLedger:
    """Single-process teaching ledger, not a production campaign service."""

    def __init__(self, budget: int):
        if budget < 0:
            raise ValueError("Budget must be nonnegative")
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.execute("CREATE TABLE budget (remaining INTEGER NOT NULL)")
        self.db.execute("INSERT INTO budget VALUES (?)", (budget,))
        self.db.execute("CREATE TABLE decisions (decision_id TEXT PRIMARY KEY, customer_id TEXT UNIQUE NOT NULL, cost INTEGER NOT NULL, status TEXT NOT NULL)")
        self.db.commit()

    @property
    def remaining(self) -> int:
        return self.db.execute("SELECT remaining FROM budget").fetchone()[0]

    def reserve(self, decision_id: str, customer_id: str, cost: int) -> str:
        if not decision_id or not customer_id or not isinstance(cost, int) or cost <= 0:
            raise ValueError("A decision requires identity and a positive integer cost")
        with self.db:
            old = self.db.execute("SELECT * FROM decisions WHERE decision_id = ?", (decision_id,)).fetchone()
            if old:
                if old["customer_id"] != customer_id or old["cost"] != cost:
                    raise ValueError("An idempotency key cannot represent different requests")
                return old["status"]
            if self.db.execute("SELECT 1 FROM decisions WHERE customer_id = ?", (customer_id,)).fetchone():
                raise ValueError("An account cannot receive a second action in this batch")
            if self.remaining < cost:
                return "budget_exhausted"
            self.db.execute("UPDATE budget SET remaining = remaining - ?", (cost,))
            self.db.execute("INSERT INTO decisions VALUES (?, ?, ?, 'reserved')", (decision_id, customer_id, cost))
        return "reserved"

    def settle(self, decision_id: str, status: str) -> None:
        if status not in {"delivered", "unknown", "confirmed_not_delivered"}:
            raise ValueError("Unsupported execution status")
        with self.db:
            row = self.db.execute("SELECT * FROM decisions WHERE decision_id = ?", (decision_id,)).fetchone()
            if not row:
                raise ValueError("Reserve a decision before settling it")
            if row["status"] == status:
                return
            if row["status"] in {"delivered", "confirmed_not_delivered"}:
                raise ValueError("A terminal execution result cannot be silently changed")
            if status == "confirmed_not_delivered":
                self.db.execute("UPDATE budget SET remaining = remaining + ?", (row["cost"],))
            self.db.execute("UPDATE decisions SET status = ? WHERE decision_id = ?", (status, decision_id))

    def rows(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.db.execute("SELECT * FROM decisions ORDER BY decision_id")]

    def close(self) -> None:
        self.db.close()


def write_figures(output: Path, labels: list[int], probabilities: list[float], pricing: list[dict[str, Any]]) -> None:
    directory = output / "figures"
    directory.mkdir(parents=True, exist_ok=True)
    bins = []
    for lower in [step / 5 for step in range(5)]:
        selected = [(label, probability) for label, probability in zip(labels, probabilities)
                    if lower <= probability < lower + 0.2 or lower == 0.8 and probability == 1]
        if selected:
            bins.append((mean(p for _, p in selected), mean(y for y, _ in selected), len(selected)))
    circles = "".join(f'<circle cx="{70 + p * 410:.2f}" cy="{290 - y * 230:.2f}" r="6" fill="#237b67"><title>{n} synthetic customers; predicted {p:.3f}, observed {y:.3f}</title></circle>' for p, y, n in bins)
    reliability = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 360" role="img" aria-labelledby="title desc">
<title id="title">Held-out calibration on synthetic data</title><desc id="desc">Five probability bins compare mean predicted churn with observed churn. Sample sizes are small; proximity to the diagonal is not a guarantee of future calibration.</desc>
<rect width="560" height="360" fill="#faf8f2"/><g fill="#183d37" font-family="sans-serif" font-size="13">
<text x="30" y="30" font-size="18">Calibration, held-out synthetic customers</text><path d="M70 60V290H480" fill="none" stroke="#7c8983"/><path d="M70 290L480 60" fill="none" stroke="#b1b9b4" stroke-dasharray="5 5"/>
<text x="64" y="310">0</text><text x="475" y="310">1</text><text x="45" y="65">1</text><text x="45" y="295">0</text><text x="160" y="339">Mean predicted probability</text><text transform="translate(22 255) rotate(-90)">Observed churn proportion</text>{circles}</g></svg>'''
    (directory / "calibration.svg").write_text(reliability, encoding="utf-8")
    bars = "".join(f'<rect x="{95 + i * 140}" y="{280 - row["expected_contribution_per_opportunity"] * 50:.1f}" width="68" height="{row["expected_contribution_per_opportunity"] * 50:.1f}" fill="#237b67"/><text x="{129 + i * 140}" y="{268 - row["expected_contribution_per_opportunity"] * 50:.1f}" text-anchor="middle">{row["expected_contribution_per_opportunity"]:.2f}</text><text x="{129 + i * 140}" y="305" text-anchor="middle">Price {row["price"]}</text>' for i, row in enumerate(pricing))
    (directory / "pricing.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 350" role="img" aria-labelledby="title desc"><title id="title">Expected contribution at three simulated prices</title><desc id="desc">Price 20 converts 30 percent and contributes 3 per opportunity; price 25 converts 24 percent and contributes 3.6; price 30 converts 15 percent and contributes 3. The highest conversion is not the highest contribution.</desc><rect width="560" height="350" fill="#faf8f2"/><g fill="#183d37" font-family="sans-serif" font-size="14"><text x="30" y="32" font-size="18">Simulated contribution per opportunity</text><path d="M70 60V280H500" stroke="#7c8983" fill="none"/>{bars}<text x="100" y="335">Fictional units; assumed probabilities, not measured demand</text></g></svg>''', encoding="utf-8")


def evaluate(output: Path) -> dict[str, Any]:
    rows, manifest = load_rows(output)
    groups = {name: [row for row in rows if row["cohort"] == name] for name in COHORTS}
    model = fit_model(groups["train"], groups["calibration"])
    test = groups["test"]
    labels = [row["label"] for row in test]
    baseline = [model["baseline_probability"]] * len(test)
    candidate = [predict(model, row) for row in test]
    baseline_metrics = metrics(labels, baseline, model["baseline_threshold"])
    candidate_metrics = metrics(labels, candidate, model["threshold"])
    uncertainty = paired_bootstrap([log_loss(y, c) - log_loss(y, b) for y, c, b in zip(labels, candidate, baseline)])
    # This gate is declared in code before opening the test. It is not tuned
    # until a desired outcome appears. A defer result is a completed lab.
    decision = release_gate(uncertainty, baseline_metrics, candidate_metrics)
    business = business_examples(output)
    experiment = business["randomized_experiment"]
    ledger = DecisionLedger(8)
    ledger.reserve("contact-001", "example-3", 4)
    ledger.settle("contact-001", "unknown")
    ledger.reserve("contact-001", "example-3", 4)
    ledger.reserve("contact-002", "example-4", 4)
    ledger.settle("contact-002", "confirmed_not_delivered")
    execution = {"decisions": ledger.rows(), "remaining_budget": ledger.remaining,
                 "lesson": "Unknown delivery retains its reservation; a repeated request does not reserve twice."}
    ledger.close()
    result = {
        "lab_version": VERSION, "seed": manifest["seed"], "data_kind": manifest["data_kind"],
        "cohort_sizes": {name: len(group) for name, group in groups.items()},
        "baseline": baseline_metrics, "candidate": candidate_metrics,
        "paired_log_loss_difference": uncertainty,
        "prototype_decision": decision,
        "gate": "Upper paired 95% bootstrap bound on candidate-minus-baseline log loss < -0.01, and candidate Brier <= baseline Brier. No real deployment approved.",
        "experiment_decision": experiment["decision"],
        "experiment_gate": f"Sample-ratio chi-square p >= {SRM_ALPHA} before reading lift; claim a simulated contact effect only if the 95% intention-to-treat interval excludes zero, otherwise inconclusive. No real campaign approved.",
        "judge": judge_fixture(), "business": business, "execution": execution,
        "limitations": ["Entirely synthetic: predictive and causal findings do not establish real-world performance or business impact.",
                        "Fixed independent-customer cohorts; real repeated users require grouped/time-aware resampling.",
                        "One final test and predeclared gate. Changing the candidate after seeing this test requires fresh confirmatory data.",
                        "Sigmoid calibration on a separate cohort is not a guarantee after population shift.",
                        "Oracle retention effects and assumed price response are teaching assumptions, not learned causal estimates.",
                        "The randomized experiment is far smaller than its power check requires; its interval, not its point estimate, is the result."],
    }
    reports = output / "reports"
    write_json(reports / "evaluation.json", result)
    write_json(reports / "model.json", model)
    write_csv(reports / "test-predictions.csv", [
        {"snapshot_id": row["snapshot_id"], "customer_id": row["customer_id"], "label": row["label"],
         "baseline_probability": baseline[index], "candidate_probability": candidate[index]}
        for index, row in enumerate(test)
    ])
    write_csv(reports / "price-comparison.csv", business["pricing"])
    write_figures(output, labels, candidate, business["pricing"])
    release = {"release_id": f"synthetic-v{VERSION}-seed-{manifest['seed']}", "evidence_level": "simulated prototype",
               "decision": result["prototype_decision"], "experiment_decision": result["experiment_decision"],
               "source_sha256": digest(Path(__file__)),
               "data_manifest_sha256": digest(output / "manifest.json"),
               "model_sha256": digest(reports / "model.json"), "evaluation_sha256": digest(reports / "evaluation.json"),
               "feature_schema": list(FEATURES), "calibrator": "sigmoid on separate calibration cohort, bundled in model.json",
               "policy": {"threshold": model["threshold"], "false_positive_cost": 2, "false_negative_cost": 10},
               "fallback": "training-prevalence baseline; no autonomous contact or price action",
               "dependencies": "Python standard library only; record exact Python version when reproducing",
               "training_cutoff": manifest["cohorts"]["train"]["fit_or_evaluation_cutoff_utc"],
               "evaluation_report": "reports/evaluation.json", "real_world_launch_approved": False}
    write_json(reports / "release-manifest.json", release)
    write_reports(reports, result, release)
    return result


def write_reports(reports: Path, result: dict[str, Any], release: dict[str, Any], figures: str = "../figures/") -> None:
    """``figures`` is the image link prefix: a run keeps them in ../figures/, the reference beside the report."""
    baseline, candidate = result["baseline"], result["candidate"]
    interval = result["paired_log_loss_difference"]
    business = result["business"]
    experiment = business["randomized_experiment"]
    ratio, itt = experiment["sample_ratio_check"], experiment["intention_to_treat"]
    reading = {"inconclusive": "The interval includes zero, so this run cannot support a claim of benefit or harm.",
               "positive_simulated_effect": "The interval lies above zero: a simulated benefit, not a real business result.",
               "negative_simulated_effect": "The interval lies below zero: a simulated harm, not a real business result."}[itt["decision"]]
    needed = itt["accounts_per_arm_to_detect_designed_effect"]
    if needed is None:
        power = "With a designed effect of zero, no sample size can detect it."
    else:
        verdict = "underpowered for" if needed > min(experiment["arm_sizes"].values()) else "large enough for"
        power = (f"Detecting it with the book's delivery-plan\napproximation, `2 × (1.96 + 0.84)^2 × variance / effect^2`, "
                 f"needs about {needed:,} accounts per arm.\nThis experiment is {verdict} that effect.")
    report = f'''# Evaluation report — simulated reference lab

**Evidence level:** synthetic prototype. **Decision:** `{result["prototype_decision"]}`.
**Contact experiment:** `{result["experiment_decision"]}`.
It shows no real customer performance, causal benefit or production readiness.

## Frozen protocol

One unique customer per row. Cohorts in time order: 300 training, 150 calibration and
150 final-test customers. Training labels mature before calibration snapshots, and calibration
labels mature before test snapshots. Both event time and availability time limit features.
Standardisation and logistic weights use training data only. A separate calibration cohort
fits a sigmoid and picks cost thresholds for both baseline and candidate. The final cohort is
opened once, after those choices are frozen.

| Measure | Training-prevalence baseline | Calibrated logistic candidate |
| --- | ---: | ---: |
| Test customers | {baseline["n"]} | {candidate["n"]} |
| Log loss, lower is better | {baseline["log_loss"]:.6f} | {candidate["log_loss"]:.6f} |
| Brier score, lower is better | {baseline["brier"]:.6f} | {candidate["brier"]:.6f} |
| ROC AUC | {baseline["roc_auc"]:.6f} | {candidate["roc_auc"]:.6f} |
| Chosen threshold | {baseline["threshold"]:.2f} | {candidate["threshold"]:.2f} |
| FP×2 + FN×10 per customer | {baseline["cost_per_customer"]:.6f} | {candidate["cost_per_customer"]:.6f} |

Threshold-dependent costs use the listed policies. The release gate compares probability
quality only. It does not show that the candidate's action policy improves real outcomes.

Candidate-minus-baseline mean log-loss difference: **{interval["mean"]:.6f}**.
Paired percentile-bootstrap 95% interval: **[{interval["lower_95"]:.6f}, {interval["upper_95"]:.6f}]**,
using {interval["draws"]} draws, with unique customers as the independent resampling unit.
These finite-sample bootstrap estimates hold only for this simulator and cohort design.

![Held-out synthetic calibration plot. Each dot is a probability bin.]({figures}calibration.svg)

Gate, set in advance: upper interval bound below −0.01 and no worse Brier score.
A defer result stands. Do not tune on the final test until it passes.

## Judge arithmetic fixture

Positive means an acceptable answer. Human labels against a hypothetical judge on 50
hand-built cases: TP=26, FN=4, FP=3, TN=17. Precision is 26/29={26/29:.4f}.
Recall is 26/30={26/30:.4f}. False acceptance among unacceptable answers is 3/20=0.15.
This is an arithmetic fixture, not a measured model judge. For a sensitive task, three
false accepts may be too many, even when overall agreement looks good.

## Business decisions

Prices 20, 25 and 30 have assumed conversion probabilities 0.30, 0.24 and 0.15.
With unit cost 10, expected contribution per opportunity is 3.00, 3.60 and 3.00.
Price {business["conversion_winner"]} wins on conversion. Price {business["contribution_winner"]} wins on contribution.
The probabilities are simulator assumptions. Observational price correlations could not prove them.

![Expected contribution is highest at price 25 in this assumed response example.]({figures}pricing.svg)

For six hypothetical accounts and a contact budget of eight, risk ranking picks the two
high-risk accounts for expected incremental contribution **{business["retention"]["risk_expected_increment"]:.2f}**.
Known-effect ranking picks the two saveable accounts for **{business["retention"]["value_expected_increment"]:.2f}**.
These are oracle illustrations. A real policy needs identified effects and independent policy evaluation.

The separate randomised simulation assigns contact with probability {experiment["assignment_probability"]}. Failed
deliveries stay in their assigned arms (intention to treat). Assigned arms: {ratio["observed"]["0"]} control and {ratio["observed"]["1"]}
contact accounts. The {experiment["delivered_by_arm"]["1"]} contact-arm deliveries are reported separately. Sample-ratio
check before reading lift: chi-square {ratio["chi_square"]:.3f}, p = {ratio["p_value"]:.4f} against the designed
allocation. The alarm, set in advance, is p < {ratio["alarm_threshold"]}.

| Contact minus control, net contribution per assigned account | Fictional units |
| --- | ---: |
| Intention-to-treat difference | {itt["difference"]:.6f} |
| Standard error, unequal arm variances | {itt["standard_error"]:.6f} |
| Normal-approximation 95% interval | [{itt["lower_95"]:.6f}, {itt["upper_95"]:.6f}] |
| Minimum detectable effect, 80% power, two-sided 5% | {itt["minimum_detectable_effect_80_power"]:.6f} |

**Experiment decision:** `{itt["decision"]}`.
{reading}
The simulator's designed effect, known here only because the data are simulated, is
{itt["simulator_designed_effect"]:.6f} per assigned account. {power}
A real plan fixes its size before launch, from pre-treatment variance and a minimum worthwhile effect chosen upfront.

## Limitations and next experiment

The generator deliberately resembles its fitted model and uses independent synthetic customers.
Real data have measurement errors, censoring, repeated users, selection and shifting treatment effects.
Before a real pilot, document permissions and coverage, identify effects, size a prospective test
for power, check delivery and outcome instrumentation, set guardrails in advance and name an owner.
See the [full evaluation](evaluation.json), [release manifest](release-manifest.json),
[data card](data-card.md), [model card](model-card.md) and [incident rehearsal](incident-report.md).
'''
    (reports / "evaluation.md").write_text(report, encoding="utf-8")
    (reports / "data-card.md").write_text('''# Data card — synthetic retail/subscription lab

- **Origin and permission:** made by this repository's MIT-licensed code. No real people or scraped data.
- **Purpose:** practise point-in-time features, separate calibration, fair test evaluation and decisions under limits.
- **Grain:** 600 unique modelling customers, plus a separate 800-customer randomised experiment.
- **Clocks:** UTC, 30-day lookback. Only events with `event_time < as_of` and `available_at <= as_of`.
- **Outcome:** simulated 30-day churn with no contact, fully observed at 33 days. Do not zero-fill unknown coverage.
- **Partitions:** fixed train/calibration/test cohorts in time order, with mature-label gaps. Do not shuffle them for a better score.
- **Known artifacts:** each customer has one deliberately late and one future purchase. Historical features must exclude both.
- **Documents:** three fictional policy documents for a small retrieval and extraction exercise.
- **Manifest:** SHA-256 for every generated input. Evaluation requires exactly that file list, checks every hash and rebuilds every feature.
- **Experiment checks:** one outcome per assignment, no zero-filled outcomes, and a sample-ratio check before any lift is read.
- **Limitations:** deliberately simple independent units, a known response mechanism, no real consent or protected-group representation.
- **What you can conclude:** the code works on this simulator. Real-world quality and causal impact remain unknown.
''', encoding="utf-8")
    (reports / "model-card.md").write_text(f'''# Model card — calibrated logistic reference

**Purpose:** a readable churn-risk prototype on fully synthetic no-contact data.
**Inputs:** available purchases, support contacts and purchase recency over 30 days.
**Training:** 300 independent customers. Feature means/scales fit on training only. L2-regularised logistic regression.
**Calibration/decision selection:** separate 150-customer cohort. Sigmoid calibration and a threshold chosen with FP cost 2 / FN cost 10.
**Final evaluation:** 150 later customers. Log loss {candidate["log_loss"]:.6f}, Brier {candidate["brier"]:.6f}, AUC {candidate["roc_auc"]:.6f}.
**Baseline:** constant training prevalence, not final-test prevalence.
**Intended use:** teaching and reproduction. Not for real customer contact, pricing or eligibility decisions.
**Known limits:** the simulator resembles the model. One small cohort is shifted in time. No empirical fairness, censoring or deployment validation.
**Fallback:** keep the baseline and defer when evidence is too weak. Risk does not measure treatment response.
**Owner:** the learner running the prototype. A real release needs a named accountable operator.
''', encoding="utf-8")
    (reports / "incident-report.md").write_text('''# Incident rehearsal — unknown contact delivery

**Environment:** deterministic, in-memory teaching ledger. This incident was simulated.

## Trigger and observation

Reserve four units for `contact-001`. Simulate a timeout with unknown remote delivery.
Retry the same decision ID. The ledger returns its existing state and keeps the original
reservation. It must not take four more units or issue a second decision for that customer.
Reserve `contact-002`, then reconcile a confirmed non-delivery. Release only that reservation.

## Result

Initial budget: eight. One unknown reservation: four. One confirmed non-delivery refunded: four.
Final available budget: four. No duplicate decision was created. The tests for this
are in `test_ground_truth_lab.py`, and the generated execution records are in `evaluation.json`.

## Recovery boundary

This ledger makes local reservation transactions atomic. It does not call a real delivery
provider, so it cannot promise exactly-once external effects. A real service needs a durable
outbox, provider idempotency keys, acknowledgement reconciliation, access controls, backup
and restoration tests. Keep unknown deliveries reserved until you know their status.

## Follow-up

Before a pilot, test two crashes against the real provider's idempotency and status contract:
one before dispatch, one after the effect but before acknowledgement. Record detection
and recovery times from the real drill. This fixture has no measured production timings.
''', encoding="utf-8")


def export_reference(destination: Path, seed: int = SEED) -> dict[str, Any]:
    """Rebuild the checked-in reference set from a fresh run in a temporary directory.

    The reference is flat, so its report links to sibling figures. Every other byte is
    the ordinary run output, including the release manifest that pins this source file.
    """
    with tempfile.TemporaryDirectory() as folder:
        run = Path(folder)
        generate(run, seed)
        result = evaluate(run)
        destination.mkdir(parents=True, exist_ok=True)
        for name, source in REFERENCE_FILES.items():
            (destination / name).write_bytes((run / source).read_bytes())
        release = json.loads((run / "reports/release-manifest.json").read_text(encoding="utf-8"))
        write_reports(destination, result, release, figures="")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("generate", "evaluate", "all", "reference"):
        command_parser = subparsers.add_parser(command, help={"generate": "Create deterministic synthetic data", "evaluate": "Validate existing data and create evidence reports", "all": "Generate data, validate, fit and evaluate", "reference": "Rebuild the flat, checked-in reference set (default: labs/reference)"}[command])
        default = Path("labs/reference" if command == "reference" else "labs/output")
        command_parser.add_argument("--output", type=Path, default=default, help=f"Data/report directory (default: {default})")
        if command != "evaluate":
            command_parser.add_argument("--seed", type=int, default=SEED, help="Synthetic seed (default: 42)")
    args = parser.parse_args()
    try:
        if args.command in {"generate", "all"}:
            generate(args.output, args.seed)
            print(f"Generated synthetic data in {args.output}")
        if args.command in {"evaluate", "all"}:
            result = evaluate(args.output)
            print(f"Evidence report: {args.output / 'reports/evaluation.md'}")
            print(f"Simulated gate: {result['prototype_decision']}; contact experiment: {result['experiment_decision']}; no real deployment approved")
        if args.command == "reference":
            result = export_reference(args.output, args.seed)
            print(f"Reference set (seed {args.seed}) written to {args.output}; review and commit it with the source change")
            print(f"Simulated gate: {result['prototype_decision']}; contact experiment: {result['experiment_decision']}")
    except (ValueError, KeyError, FileNotFoundError) as error:
        parser.exit(2, f"Lab error: {error}\n")


if __name__ == "__main__":
    main()
