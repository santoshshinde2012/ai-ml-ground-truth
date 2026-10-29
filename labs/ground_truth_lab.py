#!/usr/bin/env python3
"""A reproducible, synthetic reference lab. Python standard library only.

No customer data, network access, trained foundation model, or paid API is used.
Run ``python3 labs/ground_truth_lab.py all --output labs/output``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Any

VERSION = "1.0.0"
SEED = 42
FEATURES = ("purchases_30d", "support_30d", "recency_days")
ORIGIN = datetime(2025, 1, 1, tzinfo=timezone.utc)
COHORTS = {
    "train": {"start": 0, "days": 30, "per_day": 10, "cutoff": 63},
    "calibration": {"start": 65, "days": 15, "per_day": 10, "cutoff": 119},
    "test": {"start": 120, "days": 15, "per_day": 10, "cutoff": 175},
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
        segment = ["high_risk", "saveable", "stable"][number % 3]
        risk, effect = {"high_risk": (0.65, 0.02), "saveable": (0.35, 0.18), "stable": (0.10, 0.01)}[segment]
        assigned = int(rng.random() < 0.5)
        delivered = int(assigned == 1 and rng.random() < 0.9)
        retained = int(rng.random() < 1 - risk + delivered * effect)
        identity = f"experiment-{number:04d}"
        assignments.append({"decision_id": identity, "customer_id": f"trial-{number:04d}",
                            "segment": segment, "assigned_contact": assigned,
                            "assignment_probability": 0.5, "delivered": delivered})
        experiment_outcomes.append({"decision_id": identity, "coverage_complete": 1,
                                    "retained": retained, "net_contribution": retained * 100 - delivered * 4})
    data = output / "data"
    for name, rows in [("events.csv", events), ("snapshots.csv", snapshots), ("outcomes.csv", outcomes),
                       ("assignments.csv", assignments), ("experiment_outcomes.csv", experiment_outcomes)]:
        write_csv(data / name, rows)
    documents = {
        "returns-policy.md": "# Simulated returns policy\n\nProducts may be returned within 30 days. This is fictional teaching material.\n",
        "contact-policy.md": "# Simulated contact policy\n\nContact only eligible consenting accounts. Reserve four units per contact. Do not contact an account twice in this batch.\n",
        "price-policy.md": "# Simulated price policy\n\nThe approved teaching price grid is 20, 25 and 30. Unit cost is 10. Amounts are fictional currency units.\n",
    }
    for name, content in documents.items():
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
    for name, expected in manifest["files"].items():
        path = output / name
        if path.resolve().is_relative_to(output.resolve()) is False:
            raise ValueError("Manifest path escapes output directory")
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
            error = sigmoid(sum(w * x for w, x in zip(weights, extended))) - label
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
    return model["weights"][0] + sum(
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
        risk, effect = {"high_risk": (0.65, 0.02), "saveable": (0.35, 0.18), "stable": (0.10, 0.01)}[segment]
        profiles.append({"customer_id": f"example-{index + 1}", "segment": segment,
                         "churn_risk": risk, "incremental_value": effect * 100 - 4, "eligible": True})
    risk_contacts = choose_contacts(profiles, "churn_risk", budget=8)
    value_contacts = choose_contacts(profiles, "incremental_value", budget=8)
    by_customer = {row["customer_id"]: row for row in profiles}
    # Independent experiment: assignment, delivery and outcome remain separate.
    assignments = read_csv(output / "data/assignments.csv")
    outcomes = {row["decision_id"]: row for row in read_csv(output / "data/experiment_outcomes.csv")}
    arm_values = {arm: [] for arm in (0, 1)}
    delivery_count = 0
    for row in assignments:
        outcome = outcomes[row["decision_id"]]
        if outcome["coverage_complete"] != "1":
            raise ValueError("Do not estimate effect by replacing missing outcomes with zeros")
        arm_values[int(row["assigned_contact"])].append(float(outcome["net_contribution"]))
        delivery_count += int(row["delivered"])
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
        "randomized_experiment": {"assignment_probability": 0.5,
                                  "arm_sizes": {str(arm): len(values) for arm, values in arm_values.items()},
                                  "delivery_count": delivery_count,
                                  "intent_to_treat_contribution_difference": mean(arm_values[1]) - mean(arm_values[0]),
                                  "interpretation": "One simulated randomized experiment; includes failed deliveries in their assigned arm. No real business impact is established."},
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
    passed = uncertainty["upper_95"] < -0.01 and candidate_metrics["brier"] <= baseline_metrics["brier"]
    business = business_examples(output)
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
        "prototype_decision": "pass_simulated_gate" if passed else "defer",
        "gate": "Upper paired 95% bootstrap bound on candidate-minus-baseline log loss < -0.01, and candidate Brier <= baseline Brier. No real deployment approved.",
        "judge": judge_fixture(), "business": business, "execution": execution,
        "limitations": ["Entirely synthetic: predictive and causal findings do not establish real-world performance or business impact.",
                        "Fixed independent-customer cohorts; real repeated users require grouped/time-aware resampling.",
                        "One final test and predeclared gate. Changing the candidate after seeing this test requires fresh confirmatory data.",
                        "Sigmoid calibration on a separate cohort is not a guarantee after population shift.",
                        "Oracle retention effects and assumed price response are teaching assumptions, not learned causal estimates."],
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
               "decision": result["prototype_decision"], "source_sha256": digest(Path(__file__)),
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


def write_reports(reports: Path, result: dict[str, Any], release: dict[str, Any]) -> None:
    baseline, candidate = result["baseline"], result["candidate"]
    interval = result["paired_log_loss_difference"]
    business = result["business"]
    report = f'''# Evaluation report — simulated reference lab

**Evidence level:** synthetic prototype. **Decision:** `{result["prototype_decision"]}`.
No real customer performance, causal benefit or production readiness is established.

## Frozen protocol

One unique customer per row. Chronological cohorts: 300 training, 150 calibration and
150 final-test customers. Training labels mature before calibration snapshots; calibration
labels mature before test snapshots. Both event time and availability time restrict features.
Train-only standardization and logistic weights; a separate calibration cohort fits a sigmoid
and selects cost thresholds for both baseline and candidate. The final cohort is opened once
after those choices are frozen.

| Measure | Training-prevalence baseline | Calibrated logistic candidate |
| --- | ---: | ---: |
| Test customers | {baseline["n"]} | {candidate["n"]} |
| Log loss, lower is better | {baseline["log_loss"]:.6f} | {candidate["log_loss"]:.6f} |
| Brier score, lower is better | {baseline["brier"]:.6f} | {candidate["brier"]:.6f} |
| ROC AUC | {baseline["roc_auc"]:.6f} | {candidate["roc_auc"]:.6f} |
| Chosen threshold | {baseline["threshold"]:.2f} | {candidate["threshold"]:.2f} |
| FP×2 + FN×10 per customer | {baseline["cost_per_customer"]:.6f} | {candidate["cost_per_customer"]:.6f} |

Threshold-dependent costs use the listed policies. The release gate compares probability
quality; it does not establish that the candidate action policy improves real outcomes.

Candidate-minus-baseline mean log-loss difference: **{interval["mean"]:.6f}**.
Paired percentile-bootstrap 95% interval: **[{interval["lower_95"]:.6f}, {interval["upper_95"]:.6f}]**,
using {interval["draws"]} draws and unique customers as the independent resampling unit.
These are finite-sample bootstrap estimates, conditional on this simulator and cohort design.

![Held-out synthetic calibration plot; each dot is a probability bin.](../figures/calibration.svg)

Predeclared gate: upper interval bound below −0.01 and no worse Brier score.
Retain a defer result; do not tune on the final test until it passes.

## Judge arithmetic fixture

Positive means an acceptable answer. Human labels versus a hypothetical judge on 50
hand-constructed cases: TP=26, FN=4, FP=3, TN=17. Precision is 26/29={26/29:.4f};
recall is 26/30={26/30:.4f}; false acceptance among unacceptable answers is 3/20=0.15.
This is an arithmetic fixture, not a measured model judge. Three false accepts may be
unacceptable for a sensitive task even when aggregate agreement looks good.

## Business decisions

Prices 20, 25 and 30 have assumed conversion probabilities 0.30, 0.24 and 0.15.
With unit cost 10, expected contribution per opportunity is 3.00, 3.60 and 3.00.
Price {business["conversion_winner"]} wins conversion; price {business["contribution_winner"]} wins contribution.
The probabilities are simulator assumptions. Observational price correlations would not establish them.

![Expected contribution is highest at price 25 in this assumed response example.](../figures/pricing.svg)

For six hypothetical accounts and a contact budget of eight, risk ranking selects the two
high-risk accounts for expected incremental contribution **{business["retention"]["risk_expected_increment"]:.2f}**.
Known-effect ranking selects the two saveable accounts for **{business["retention"]["value_expected_increment"]:.2f}**.
These are oracle illustrations. A real policy needs identified effects and independent policy evaluation.

The separate randomized simulation keeps failed deliveries in their assigned arms.
Its realized intention-to-treat contribution difference is
**{business["randomized_experiment"]["intent_to_treat_contribution_difference"]:.6f}** fictional units.
A single realized difference without an uncertainty analysis does not establish a useful effect.

## Limitations and next experiment

The generator deliberately resembles its fitted model and uses independent synthetic customers.
Real data have measurement errors, censoring, repeated users, selection and shifting treatment effects.
Before a real pilot: document permissions and coverage, identify effects, power a prospective test,
verify delivery and outcome instrumentation, predeclare guardrails and obtain operational ownership.
Inspect the [full evaluation](evaluation.json), [release manifest](release-manifest.json),
[data card](data-card.md), [model card](model-card.md) and [incident rehearsal](incident-report.md).
'''
    (reports / "evaluation.md").write_text(report, encoding="utf-8")
    (reports / "data-card.md").write_text('''# Data card — synthetic retail/subscription lab

- **Origin and permission:** generated by this repository's MIT-licensed code; no real people or scraped data.
- **Purpose:** learn point-in-time features, separate calibration, honest test evaluation and constrained decisions.
- **Grain:** 600 unique modelling customers; separate 800-customer randomized experiment.
- **Clocks:** UTC, 30-day lookback; only events with `event_time < as_of` and `available_at <= as_of`.
- **Outcome:** simulated 30-day churn under no contact; fully observed at 33 days. Unknown coverage must never be zero-filled.
- **Partitions:** fixed chronological train/calibration/test cohorts with mature-label gaps; never shuffle them for a better score.
- **Known artifacts:** every customer has a deliberately late and a future purchase that historical features must exclude.
- **Documents:** three fictional policy documents for a small retrieval/extraction exercise.
- **Manifest:** SHA-256 for every generated input; evaluation checks those hashes and rebuilds every feature.
- **Limitations:** intentionally simplified independent units, known response mechanism, no real consent or protected-group representation.
- **Permitted conclusion:** the implementation works on this simulator. Real-world quality and causal impact remain unknown.
''', encoding="utf-8")
    (reports / "model-card.md").write_text(f'''# Model card — calibrated logistic reference

**Purpose:** a readable churn-risk prototype on fully synthetic no-contact data.
**Inputs:** available purchases, support contacts and purchase recency over 30 days.
**Training:** 300 independent customers; feature means/scales fit on training only; L2-regularized logistic regression.
**Calibration/decision selection:** separate 150-customer cohort; sigmoid calibration and a threshold selected under FP cost 2 / FN cost 10.
**Final evaluation:** 150 later customers; log loss {candidate["log_loss"]:.6f}, Brier {candidate["brier"]:.6f}, AUC {candidate["roc_auc"]:.6f}.
**Baseline:** constant training prevalence, not final-test prevalence.
**Intended use:** teaching and reproduction. No actual customer contact, pricing or eligibility decision.
**Known limits:** simulator resembles the model; a small temporally shifted cohort; no empirical fairness, censoring or deployment validation.
**Fallback:** preserve baseline and defer when evidence is insufficient. Risk does not measure treatment response.
**Owner:** the learner running the prototype; a real release requires a named accountable operator.
''', encoding="utf-8")
    (reports / "incident-report.md").write_text('''# Incident rehearsal — unknown contact delivery

**Environment:** deterministic, in-memory teaching ledger. This incident was simulated.

## Trigger and observation

Reserve four units for `contact-001`. Simulate a timeout with unknown remote delivery.
Retry the same decision ID. The ledger returns its existing state and retains the original
reservation. It must not debit four more units or issue a second decision for that customer.
Reserve `contact-002`, then reconcile a confirmed nondelivery; release only that reservation.

## Result

Initial budget: eight. One unknown reservation: four. One confirmed nondelivery refunded: four.
Final available budget: four. No duplicate decision was created. The executable assertions
are in `test_ground_truth_lab.py`; the generated execution records are in `evaluation.json`.

## Recovery boundary

This ledger makes local reservation transactions atomic. It does not call a real delivery
provider and does not promise exactly-once external effects. A real service needs a durable
outbox, provider idempotency keys, acknowledgement reconciliation, access controls, backup
and restoration tests. Keep unknown deliveries reserved until their status is established.

## Follow-up

Before a pilot, test crash-before-dispatch and crash-after-effect-before-acknowledgement
against the real provider's idempotency and status contract. Record detection and recovery
durations from the real drill; this fixture supplies no measured production timings.
''', encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("generate", "evaluate", "all"):
        command_parser = subparsers.add_parser(command, help={"generate": "Create deterministic synthetic data", "evaluate": "Validate existing data and create evidence reports", "all": "Generate data, validate, fit and evaluate"}[command])
        command_parser.add_argument("--output", type=Path, default=Path("labs/output"), help="Data/report directory (default: labs/output)")
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
            print(f"Simulated gate: {result['prototype_decision']}; no real deployment approved")
    except (ValueError, KeyError, FileNotFoundError) as error:
        parser.exit(2, f"Lab error: {error}\n")


if __name__ == "__main__":
    main()
