# The Ground Truth reference lab

A small, complete project accompanies the book. Synthetic subscription data becomes historical
features, a calibrated churn model, an independent evaluation and a constrained decision exercise.
It runs locally on **Python 3.10 or later**, using only the standard library. It makes no network
requests and needs no API key, GPU, private customer data or package installation.

Every customer, policy document, intervention and result is **simulated**. The lab shows
implementation and reasoning, not real-world model quality or business impact.

## Run it

From the repository root:

```bash
python3 labs/ground_truth_lab.py all --output labs/output
python3 -m unittest discover -s labs/tests -p 'test_*.py' -v
```

The first command takes a few seconds on an ordinary laptop. When it finishes, open
`labs/output/reports/evaluation.md`. It reports two separate decisions:

- **Model gate.** On this simulator the calibrated candidate passes for seed 42 and for every seed
  from 1 to 20, because the generator deliberately resembles the fitted model. `defer` appears when
  the evidence is weaker. To see it, set the three outcome coefficients in `generate` to zero.
  `ReleaseGateTests` builds the defer and regression paths directly.
- **Contact experiment.** For seed 42 the intention-to-treat interval includes zero, so the result
  is `inconclusive`.

Each of these outcomes is a valid, completed experiment. Keep it and explain it, rather than
changing the test protocol until a score you like appears.

The two stages can also run separately:

```bash
python3 labs/ground_truth_lab.py generate --output labs/output --seed 42
python3 labs/ground_truth_lab.py evaluate --output labs/output
python3 labs/ground_truth_lab.py --help
```

`generate` overwrites the lab's named data files in the chosen output directory. Use a
dedicated directory, keep earlier results when comparing experiments, and keep your own data
elsewhere. Before using existing data, `evaluate` checks that the manifest lists exactly the lab's
source files, with matching hashes (see [Checks that stop a run](#checks-that-stop-a-run)). Record
the exact Python version when comparing numeric results, since the last floating-point bit can
differ across platforms. Fixed-seed data and numeric results reproduce within one supported
environment.

## What exists when you finish

```text
output/
  manifest.json                # source hashes, seed, cohort clocks and data contract
  data/
    events.csv                 # event time and first-available time
    snapshots.csv              # one historical row per unique customer
    outcomes.csv               # horizon, availability and verified coverage
    assignments.csv            # separate randomized intervention population
    experiment_outcomes.csv    # includes nonbuyers and delivery failures
    documents/                 # three fictional policies for retrieval/extraction practice
  reports/
    model.json                 # train-only scaling, coefficients, calibrator, thresholds
    test-predictions.csv       # paired baseline/candidate probabilities
    evaluation.json            # full machine-readable evidence
    evaluation.md              # explained results and decision
    price-comparison.csv       # assumed response and contribution
    release-manifest.json      # hashes of source, data, model and evaluation
    data-card.md
    model-card.md
    incident-report.md
  figures/
    calibration.svg
    pricing.svg
```

Small, checked-in [reference results](reference/evaluation.md) show the kind of output the command
creates. They are examples from the seed-42 simulator, not claims about a deployed product. Rerun
the command to get a release manifest that matches the source you used. The reference uses a flat
layout, and one command rebuilds it (see
[Regenerate the checked-in reference](#regenerate-the-checked-in-reference)).

Read the filled-in [evaluation](reference/evaluation.md), [data card](reference/data-card.md),
[model card](reference/model-card.md) and [incident rehearsal](reference/incident-report.md).
The same lab command draws the calibration and pricing figures in the evaluation report.

## Follow the project through the book

The lab covers Chapters 2 and 3 in depth. For the other chapters it gives a smaller starting
point, and the table says how small.

| Chapter | What the lab provides | Independent work |
| --- | --- | --- |
| [Data foundations](../02-data-foundations/README.md) | **Exercised in full:** events with occurrence and availability clocks, point-in-time snapshots, matured outcomes with coverage, manifest checks and a data card | Rebuild the historical features and explain each excluded event |
| [Core ML](../03-core-machine-learning/README.md) | **Exercised in full:** chronological cohorts, train-only fitting, separate calibration, paired test predictions, a bootstrap interval and a predeclared gate | Add one challenger without opening or tuning on the final test |
| [Deep learning](../04-deep-learning/README.md) | **Optional extension only.** The lab trains no network; its generated `snapshots.csv` features, labels and fixed cohorts can feed one | Train a small network on the lab's tabular features as a separate experiment; keep the logistic comparator, the split contract and the untouched final test |
| [Language models](../05-language-models/README.md) | **A small bridge:** three fictional policy documents and a judge arithmetic fixture; no model is called | Write retrieval/extraction cases before using an optional model; include unsupported questions |
| [Production](../06-production/README.md) | **A local rehearsal:** release manifest, checksum refusal and an in-memory idempotent ledger; no service, container, monitoring or deployment | Reproduce a release, tamper with a source, explain the refusal and exercise fallback |
| [Business ML](../09-business-machine-learning/README.md) | **Worked arithmetic and one simulated experiment:** assumed price response, an oracle risk-versus-value ranking, and a randomised test with a sample-ratio check, intention-to-treat interval and power check | Distinguish predictive evidence, oracle assumptions and randomised outcomes; explain why the experiment is inconclusive |

The lab has no LLM and no neural-network trainer. Its documents and fixtures are a low-cost bridge
into those chapters' independent exercises. A hosted-model experiment needs its own
permission, budget, model version and evaluation record.

## Read the implementation in this order

1. **`features_at`:** include an event only if it happened within the historical window and was
   usable by the decision time. Every synthetic customer has a late event and a future event that
   must be excluded. The boundary rules for both clocks are deliberate.
2. **`generate` and `load_rows`:** 300 training customers, 150 calibration customers and 150 final
   test customers. Cohorts are chronological and separate. Labels mature before each
   relevant cutoff, and each cohort's labels mature before the next cohort's decisions.
3. **`fit_model`:** feature means, scales and logistic weights use training data only. A
   separate cohort fits sigmoid calibration and picks thresholds with false-positive cost 2 and
   false-negative cost 10. A sigmoid fit cannot promise calibration after a population shift.
4. **`evaluate`:** compare a training-prevalence baseline with the frozen challenger. Bootstrap
   the paired log-loss differences per customer. The gate, `release_gate`, is fixed in advance and
   needs an upper 95% bound below −0.01 and no worse Brier score. An uncertain gain, a worse Brier
   score and a regression all defer. This is a simulated-prototype gate, not launch approval.
5. **`judge_fixture`:** calculate precision, recall and false acceptance from a hand-built 50-case
   confusion matrix. These numbers teach denominators. They do not measure a real judge.
6. **`business_examples`:** see why conversion, risk, value and contribution answer different
   questions. Price response and individual treatment effects are known simulator assumptions.
   For the randomised experiment, `sample_ratio_check` runs before `intention_to_treat`, which
   reports the assigned-arm difference with its standard error, 95% interval and power check.
7. **`DecisionLedger`:** reserve a fixed contact budget atomically, reject conflicting retries, keep
   a reservation while delivery is unknown, and refund only confirmed nondelivery. The local ledger
   cannot promise exactly-once external effects or replace a durable production outbox.

## Checks that stop a run

`evaluate` refuses to report rather than quietly producing a number. Each refusal exits with status
2 and a `Lab error:` message, and the tests cover each one.

| Check | Fails when |
| --- | --- |
| Lab version | `manifest.json` was written by a different lab version |
| Manifest coverage | the manifest omits a source file, lists an unexpected one, or names a path outside the output directory |
| Checksums | a listed file's SHA-256 differs from the manifest |
| Point-in-time rebuild | a snapshot feature differs from its rebuild using only events available at `as_of` |
| Join grain | a customer has two snapshots, or an outcome is duplicated or unmatched |
| Label maturity and coverage | an outcome is immature at its cohort cutoff, or its coverage is unknown |
| Cohort gap | an earlier cohort's labels mature after a later cohort's first decision |
| Experiment join | an assignment lacks exactly one outcome, an outcome would be zero-filled, or the log disagrees with the designed allocation |
| Sample ratio | a chi-square goodness-of-fit test of arm sizes against the designed 0.5 allocation gives p < 0.001 |

Two decisions are reported rather than raised: the model gate (`pass_simulated_gate` or
`defer`) and the contact experiment (`inconclusive` when the 95% intention-to-treat interval
includes zero, otherwise a simulated positive or negative effect). The experiment section also
reports the minimum detectable effect at 80% power and the sample size needed for the simulator's
designed effect, using the power approximation in section 5 of the
[delivery plan](../09-business-machine-learning/delivery-plan.md).

## Worked decisions

**Price:** a product costs 10. At prices 20, 25 and 30, assumed conversion is 0.30, 0.24 and 0.15.
Expected contribution per opportunity is `(price − cost) × conversion`: 3.00, 3.60 and 3.00.
Conversion peaks at 20, but contribution peaks at 25. Those response probabilities require
identification in a real pricing problem.

**Retention:** a high-risk segment has churn risk 0.65 but a contact only increases retention by
0.02. At retained contribution 100 and contact cost 4, its expected incremental value is −2.
A saveable segment has risk 0.35 and a retention effect of 0.18, giving +14. A budget of eight
funds two contacts. Risk ranking gives −4, and known-effect ranking gives +28. These are
oracle illustrations, not estimates the churn classifier learned.

**Inventory:** demand fixed at 10, and demand equally likely to be 0 or 20, both have mean 10.
With stock 10, expected served demand is 10 in the first case and 5 in the second. Using
`min(mean demand, stock)` ignores the spread of demand, which the second case needs.

## Exercises, hints and explained answers

### 1. A purchase happened yesterday but arrived tomorrow

Should it enter today's historical features? Explain both clocks before running the code.

<details><summary>Hint</summary>

Which query could the deployed service actually have answered at the decision time?

</details>

<details><summary>Explained answer</summary>

No. Its event time is in the past, but it became available after the decision. Including it
would make a historical replay better informed than the real service. See
`HistoricalFeatureTests.test_event_and_availability_clocks_both_apply` in
[`tests/test_ground_truth_lab.py`](tests/test_ground_truth_lab.py).

</details>

### 2. The challenger passes the synthetic gate

What can you claim, and what evidence is still missing?

<details><summary>Hint</summary>

Separate the implementation, this generator, the deployment population and a causal intervention.

</details>

<details><summary>Explained answer</summary>

The frozen candidate passes the probability-quality gate, set in advance, on one synthetic test
cohort. The implementation is reproducible under its stated assumptions. Nothing here shows real
population performance, fairness, operational readiness or retention benefit. A real model needs
representative, independent evidence. A contact policy needs identified effects and a valid policy
experiment. Repeated tuning against this test turns it into development data.

</details>

### 3. A contact request timed out

You reserved four units. Can you refund now and send a new decision ID?

<details><summary>Hint</summary>

The remote system may have completed the action before the timeout.

</details>

<details><summary>Explained answer</summary>

Keep the reservation and reuse the same idempotency key while reconciling what happened.
Refund only after confirmed nondelivery. A different ID may create a duplicate effect. This lab
enforces the reservation rules locally. For the stronger external guarantee, a real provider must
support deduplication or status reconciliation.

</details>

### 4. Turn the policy corpus into an evaluation set

Before choosing an LLM, write six questions: two answered directly, two that need correct number
extraction and two unsupported by the documents. Specify expected source spans and an abstention
rule. A deterministic mock response is enough to test your evaluation code.

<details><summary>One possible answer</summary>

Ask about the return period, the allowed price grid, the unit cost and the per-contact
reservation. Ask unsupported questions about international shipping and real customer
eligibility. The first four must cite the matching fictional document and preserve the numbers.
The last two must say the supplied documents do not answer them. A plausible unsupported answer
is a failure.

</details>

## Evidence boundaries

This reference is deliberately easy to inspect. The generator resembles the fitted model, which
real projects rarely do. It assumes independent customers, fully observed outcomes and fixed
cohorts. The separate experiment randomises assignment at probability 0.5 and keeps failed
deliveries in their assigned arm. For seed 42 its intention-to-treat difference is about −0.2
units, with a 95% interval of about −6.9 to +6.4. The result is inconclusive even though the
simulator's designed effect is about +2.7 units per assigned account. About 400 accounts per arm
cannot detect an effect that small. The power approximation asks for roughly 4,900. With some other
seeds the interval excludes zero. Those estimates, roughly 7 to 11 units, overstate the designed
effect, because only large observed differences clear an underpowered test. The lab makes no
rollout claim from any of them.

With repeated customers, changing policies, missing outcomes, limited inventory or spillovers,
adapt the design and uncertainty method before reading results. Keep a no-action baseline, report
negative findings, and gather better data when yours cannot support a decision.

## Regenerate the checked-in reference

`labs/reference/` holds the seed-42 output in a flat layout. The report and its two figures sit side
by side, so its image links are `calibration.svg` and `pricing.svg` rather than `../figures/...`.
The website publishes the folder unchanged. Edit those files only by regenerating them.
From the repository root, rebuild all ten with:

```bash
python3 labs/ground_truth_lab.py reference
```

The command runs `generate` and `evaluate` in a temporary directory and writes the reference set to
`labs/reference/` (`--output` and `--seed` default to that folder and 42). Every other byte matches
an ordinary run. `release-manifest.json` records the SHA-256 of `ground_truth_lab.py`, so any edit
to the script, even a comment, changes the reference. `ReferenceTests` runs the command into a
temporary folder and checks for the same file names and identical bytes. When it fails, regenerate,
review the diff and commit the script and reference together.

Sums use `math.fsum`, which is correctly rounded on every supported Python, so the numbers do not
depend on the Python minor version. A platform's math library could still differ in the last digit.
If the reference test fails only on a new platform, report it instead of regenerating.
