# Evaluation report — simulated reference lab

**Evidence level:** synthetic prototype. **Decision:** `pass_simulated_gate`.
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
| Test customers | 150 | 150 |
| Log loss, lower is better | 0.695751 | 0.495936 |
| Brier score, lower is better | 0.251300 | 0.169020 |
| ROC AUC | 0.500000 | 0.837216 |
| Chosen threshold | 0.05 | 0.15 |
| FP×2 + FN×10 per customer | 0.986667 | 0.760000 |

Threshold-dependent costs use the listed policies. The release gate compares probability
quality; it does not establish that the candidate action policy improves real outcomes.

Candidate-minus-baseline mean log-loss difference: **-0.199816**.
Paired percentile-bootstrap 95% interval: **[-0.289922, -0.115393]**,
using 1000 draws and unique customers as the independent resampling unit.
These are finite-sample bootstrap estimates, conditional on this simulator and cohort design.

![Held-out synthetic calibration plot; each dot is a probability bin.](calibration.svg)

Predeclared gate: upper interval bound below −0.01 and no worse Brier score.
Retain a defer result; do not tune on the final test until it passes.

## Judge arithmetic fixture

Positive means an acceptable answer. Human labels versus a hypothetical judge on 50
hand-constructed cases: TP=26, FN=4, FP=3, TN=17. Precision is 26/29=0.8966;
recall is 26/30=0.8667; false acceptance among unacceptable answers is 3/20=0.15.
This is an arithmetic fixture, not a measured model judge. Three false accepts may be
unacceptable for a sensitive task even when aggregate agreement looks good.

## Business decisions

Prices 20, 25 and 30 have assumed conversion probabilities 0.30, 0.24 and 0.15.
With unit cost 10, expected contribution per opportunity is 3.00, 3.60 and 3.00.
Price 20 wins conversion; price 25 wins contribution.
The probabilities are simulator assumptions. Observational price correlations would not establish them.

![Expected contribution is highest at price 25 in this assumed response example.](pricing.svg)

For six hypothetical accounts and a contact budget of eight, risk ranking selects the two
high-risk accounts for expected incremental contribution **-4.00**.
Known-effect ranking selects the two saveable accounts for **28.00**.
These are oracle illustrations. A real policy needs identified effects and independent policy evaluation.

The separate randomized simulation keeps failed deliveries in their assigned arms.
Its realized intention-to-treat contribution difference is
**-0.219427** fictional units.
A single realized difference without an uncertainty analysis does not establish a useful effect.

## Limitations and next experiment

The generator deliberately resembles its fitted model and uses independent synthetic customers.
Real data have measurement errors, censoring, repeated users, selection and shifting treatment effects.
Before a real pilot: document permissions and coverage, identify effects, power a prospective test,
verify delivery and outcome instrumentation, predeclare guardrails and obtain operational ownership.
Inspect the [full evaluation](evaluation.json), [release manifest](release-manifest.json),
[data card](data-card.md), [model card](model-card.md) and [incident rehearsal](incident-report.md).
