# Delivering a business ML system end to end

[Chapter 9](README.md) &nbsp;·&nbsp; [Offers](offer-recommendation.md) &nbsp;·&nbsp;
[Prices](price-recommendation.md) &nbsp;·&nbsp; [Churn](churn.md)

This plan is shared by all three cases. It turns the model research into a reproducible prototype
and a reviewable production proposal. Implement the relevant gates; complete the live experiment
gate only when a real experiment has run. The 15 shared hours assume a small project and reuse of
the [Chapter 6](../06-production/README.md) deployment work.

**In this plan:** [Decision brief](#1-define-the-decision-and-economics) &nbsp;·&nbsp;
[Data contract](#2-create-the-data-and-label-contract) &nbsp;·&nbsp;
[Policy evidence](#4-evaluate-an-action-policy-honestly) &nbsp;·&nbsp;
[Experiment](#5-design-the-experiment-before-launch) &nbsp;·&nbsp;
[Delivery](#6-deliver-and-log-the-decision) &nbsp;·&nbsp;
[Completion](#8-package-the-project-and-check-completion)

## 1. Define the decision and economics

Write a one-page brief before selecting a model:

| Field             | Record                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| Decision          | Customer/item, decision time, eligible actions, and default/no-action option                     |
| Owner and cadence | Who uses the output, batch vs session/API, and when an action can take effect                    |
| Outcome           | Exact event definition, attribution/measurement horizon and reporting delay                      |
| Economics         | Contribution after fulfilment, subsidy, contact, returns and service costs; currency and horizon |
| Constraints       | Inventory, minimum margin, subsidy/contact budget, fatigue and applicable customer policy        |
| Evidence          | Randomized assignments or identification assumptions; historical support for actions             |
| Success           | Minimum useful effect and uncertainty; service, spend and customer guardrails                    |
| Fallback          | Existing approved policy when features, evidence or serving are inadequate                       |

Do not substitute revenue for contribution or churn risk for retained value. If cost or treatment
data is missing, state the narrower predictive question you can answer and collect the missing data.

## 2. Create the data and label contract

Use UTC in stored timestamps; preserve the local calendar needed for business features. Specify the
unique snapshot key and keep customer IDs as join keys unless an ID feature is intentionally
justified. For each snapshot at `as_of`, record feature lookback, maximum permissible availability
time, label window, label completion time and training cutoff.

For fixed-horizon targets, require `label_available_at <= training_cutoff` and verified outcome
coverage through `label_end` at fitting time. Apply any documented reporting allowance as well. A
passed calendar horizon alone does not establish completeness when the outcome feed is delayed or
missing.

For [survival targets](churn.md#6-when-to-use-survival-analysis), retain the event indicator and
observed event/censoring duration instead. Use only records available at the training cutoff and a
verified observation limit. Partial follow-up can be retained under the censoring assumptions; an
unfinished horizon is not a negative fixed-horizon label. Document the supported evaluation horizons
and censoring/reference-sample protocol.

An illustrative historical aggregation, assuming `available_at` means first usability and each event
has an immutable ID:

```sql
SELECT s.customer_id, s.as_of,
       COUNT(e.event_id) AS purchases_30d,
       COALESCE(SUM(e.net_contribution), 0) AS contribution_30d
FROM snapshots AS s
LEFT JOIN purchase_events AS e
  ON e.customer_id = s.customer_id
 AND e.event_time >= s.as_of - INTERVAL '30 days'
 AND e.event_time < s.as_of
 AND e.available_at <= s.as_of
GROUP BY s.customer_id, s.as_of;
```

This is a query pattern, not a complete feature system. Deduplicate upstream, validate timezone
types and join cardinality, and version corrections instead of replacing historical values with
today's truth. If a margin was finalized later, it needs its own availability/version record. Use
the same definitions for replay and serving; historical retrieval tools still require you to verify
availability semantics
([Feast point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)).

For experiments, retain eligible opportunities even when no action was delivered. Keep assignment,
exposure/delivery and outcome in separate tables: assignment is the primary analysis group, while
delivery explains implementation failures. Do not restrict the main result to redeemers, buyers,
contacted responders or other groups selected after treatment.

## 3. Train, compare and freeze a release

Compare the business-as-usual rule, a simple statistical baseline and one challenger. Use the split
in the selected guide, keeping all tuning and preprocessing out of the final test. With dependent
rows, report uncertainty at the customer, market or time-block level relevant to the decision.
Evaluate both model quality and the policy derived from the model.

Save a release manifest like this, using actual values instead of placeholders:

```yaml
release_id: example-2026-10-08-001
code_commit: <commit>
data_snapshot: <immutable-source-version>
feature_query_version: <version>
training_cutoff_utc: <timestamp>
label_contract: <version>
feature_schema: <version>
model_artifact: <path-and-checksum>
calibrator_artifact: <path-or-null>
policy_config: <version>
experiment_config: <version-or-null>
dependency_lock: <lockfile-checksum>
evaluation_report: <path>
approved_actions: <versioned-action-set>
fallback_policy: <version>
```

This manifest is enough for a first project.
[MLflow's model registry](https://mlflow.org/docs/latest/ml/model-registry/workflow/) adds lifecycle
management when a team needs it. A deployment must load the matching feature schema, model,
calibrator and policy together; changing a threshold or budget is a policy release.

## 4. Evaluate an action policy honestly

Report predictive metrics separately from causal/policy evidence. An offline comparison of people
who did and did not receive a discount can be dominated by how the old team selected them. If
randomized logged actions support the target policy, evaluate that frozen policy on held-out
assignments. For a frozen deterministic target policy on a discrete action set, an
inverse-propensity estimate is:

```text
estimated_value(policy) = mean(
    I[logged_action == policy(context)] * net_outcome / logging_probability
)
```

For a stochastic target policy, replace the indicator with the target probability of the logged
action, conditional on the same context and feasible set.

The logging probability is the probability of that action under the **actual** assignment policy,
conditional on context and candidate eligibility. It is not the model's confidence. Inspect overlap,
extreme weights and effective sample size; a deterministic old policy cannot evaluate actions it
never tried. Specify uncertainty and any clipping bias. Doubly robust estimation can reduce some
estimation errors, but cannot repair missing action support or arbitrary unobserved confounding
([Dudík, Langford and Li, 2011](https://arxiv.org/abs/1103.4601)).

Here `net_outcome` is observed mature net contribution for every eligible assignment unit, including
no purchase and no offer, after actual costs. A contacted nonbuyer can have negative contribution.
It is not a predicted score or an already baseline-subtracted uplift quantity. This formula
evaluates an assignment policy when `logged_action` records assignment. Preserve that original
assignment for intention-to-treat after human overrides or delivery failures. Evaluation of actual
executed actions needs their own justified propensities; do not attach the original assignment
probability to an override whose selection mechanism is unknown. Constraints applied **before** the
random draw belong in the known assignment mechanism; a delivery failure after the draw is a
different record, not permission to invent a new randomized probability.

**For combined actions, log the joint assignment mechanism.** An action can be a tuple of offer,
price and retention choice, including their no-change options. Its propensity is the probability of
that tuple under the coordinator, conditional on eligible candidates and pre-decision inventory,
budget, contact history and other assignment state. Multiplying three marginal probabilities is
valid only when the design makes the choices conditionally independent. Mutually exclusive or
budget-coupled choices usually are not. For staged random draws, use the recorded conditional
probability at each stage, including earlier choices; their product gives the tuple probability.
Keep the coordinator version and assignment history needed to reproduce it.

This is a one-decision contextual policy estimate for the stated outcome horizon. It does not
automatically identify a sequential campaign policy when contacts change later eligibility or prices
deplete shared inventory. Those claims need a sequential/interference-aware design or a prospective
experiment of the whole policy. Conditioning on recorded stock and budget does not by itself
evaluate a new policy's effect on their future distribution. A chain of conditional probabilities
for one compound action is also not a longitudinal policy evaluator. Sequential off-policy methods
require supported decision histories, correctly specified assignment probabilities and an
appropriate dependence model;
[Jiang and Li's ICML 2016 paper](https://proceedings.mlr.press/v48/jiang16.html) develops a
sequential doubly robust estimator under its stated trajectory assumptions. Use a controlled test of
the whole coordinator as the first practical route when allocations interact across customers.

If assignment probabilities adapt to accumulating results, retain their values at each draw and use
inference valid for that adaptive design. Ordinary independent-row intervals can fail even with
known probabilities. [Hadad et al., 2021 (author preprint)](https://arxiv.org/abs/1911.02768)
studies policy-evaluation inference for adaptive experiments; its conditions must be checked rather
than treating propensity logging as sufficient.

For continuous prices, this discrete formula applies only when you deliberately use a logged finite
price grid; a new continuous-price policy needs suitable density-based or structural methods with
additional assumptions. Prefer a bounded randomized experiment over unsupported extrapolation.
Uplift ranking scores alone do not establish net business value.

## 5. Design the experiment before launch

Write the hypothesis, control policy, target population, primary outcome, minimum detectable effect,
power/sample-size assumptions, assignment unit, duration and stopping rule. Use pre-treatment
variance estimates and account for repeat observations, clustering, delayed labels and attrition.
Count independent assignment units; rows are not automatically independent samples. A retention test
needs its full outcome horizon and a pricing test needs mature returns/costs.

**A power sanity check.** For two equally sized independent arms, a continuous outcome and a fixed
two-sided 5% test with 80% power, a normal approximation gives:

```text
n_per_arm ≈ 2 × (1.96 + 0.84)^2 × outcome_variance / minimum_effect^2
```

With an invented per-eligible-account contribution standard deviation of ₹200 and a minimum useful
mean difference of ₹5, this is about **25,088 accounts per arm**. Halving the effect requires
roughly four times as many accounts. This is a planning illustration, not a campaign-size rule:
heavy tails, unequal arms, multiple comparisons, covariate adjustment, attrition and clustered
assignment change the calculation. Use design-based simulation or a suitable power method with
representative pre-treatment data. Pricing market-days and repeat contacts are not independent
accounts. Count the outcome-maturation delay after the last assignment when planning the calendar.

Keep assignments stable where repeat exposure matters. If inventory, household sharing or market
competition create interference, consider cluster randomization or a switchback design with its own
carryover assumptions. Prespecify important segment checks and multiplicity treatment. For ongoing
peeking, use a valid sequential method; ordinary fixed-horizon intervals do not become valid
stopping rules just because the dashboard updates daily.

Run an A/A or replay instrumentation check where feasible, reconcile assignment to delivery and
outcome joins, and diagnose sample-ratio mismatch before reading lift. Microsoft documents the
[pre-experiment design practices](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/)
and
[SRM checks](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).
Use intention-to-treat as the primary randomized analysis, report actual delivery separately, and
explain any additional estimand.

Assignment analysis still needs defensible outcome observation. Report follow-up completeness by
assigned arm; retrieve missing outcomes where possible. Do not exclude unreachable accounts or
replace unknown margin with zero. Predeclare justified missing-data/censoring methods and
sensitivity analyses; treatment-dependent observation can bias a comparison despite randomization
([Lee's sample-selection analysis](https://www.nber.org/papers/w11721)). Distinguish a verified
zero-purchase outcome from an unobserved one, and postpone the impact claim when the evidence is
insufficient.

For higher-variance outcomes, a predeclared covariate adjustment such as CUPED can improve
precision. Use covariates available **before assignment**, never treatment-affected purchases or
engagement. [June 2026 CUPED research](https://arxiv.org/abs/2606.18750) examines adjustment and
valid variance estimation. Cross-fit learned adjustments where required; preserve the
assignment/clustering structure in inference. Validate coverage in an A/A simulation and update the
power calculation with justified variance estimates rather than assuming a fixed percentage
reduction.

Compare against the current business policy, not just an intentionally weak model. Require a
meaningful contribution result and acceptable guardrails; a statistically significant click-rate
gain is not the same business claim. Investigate missing telemetry and immature labels before
interpreting a negative or positive result.

Decide how results generalize before expanding the pilot. An experiment among eligible existing
customers in one region establishes an effect for that population and period. Compare eligibility,
action support, baseline outcomes, costs and delivery capacity in a new population. Use a staged
replication when those change materially; a larger model does not make a transportability claim
valid. Preserve a control or a new valid experiment when expanding the action policy.

## 6. Deliver and log the decision

Start with batch scoring for daily campaigns or retention queues. Prefer an API only for a decision
that needs current session or inventory context. Both paths need schema validation, authorization,
deterministic eligibility checks, freshness limits, deadlines and fallbacks.

The decision record should contain:

| Field group | Required contents                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| Identity    | `decision_id`, pseudonymous entity key, `as_of`, experiment/assignment key                                           |
| Inputs      | Feature snapshot/query version, source freshness, relevant price/inventory/cost state                                |
| Candidates  | Eligible action set, constraints and exclusion reasons                                                               |
| Decision    | Selected action, default action, estimated value and uncertainty/support status                                      |
| Versions    | Model, calibration, policy and experiment configuration                                                              |
| Assignment  | Assigned arm/action tuple, actual joint or stage-conditional propensities, coordinator version/history when relevant |
| Execution   | Delivery status/time, idempotency key, override/fallback reason                                                      |
| Outcomes    | Mature outcome reference, horizon, net cost/contribution and observation completeness                                |

Keep asynchronous outcomes in their own table joined by stable keys. Store scores and reason codes
needed for debugging, with restricted access and retention periods; do not put customer secrets in
general request logs. At execution, recheck inventory, contact fatigue and campaign/price validity.
Reserve budget transactionally before delivery. Retries must not send duplicate incentives or apply
a price change twice.

Release a reservation only after confirmed terminal nondelivery/non-issuance; retain and reconcile
uncertain timeouts so an issued benefit does not become unreserved. Log assignment, proposed action,
executed action and override mechanism separately, marking unknown execution propensities.

For unavailable evidence, return the currently permitted baseline with a reason. If even that
baseline is invalid, return `review_required` and execute nothing. A novel action chosen by
extrapolation is not a reliable fallback. Rehearse stale features, empty candidates, exhausted
budget, missing inventory, invalid input, timeout and duplicated delivery.

## 7. Monitor the service, policy and outcomes

Use a small dashboard with an owner and a response for each alert:

| Layer    | Watch                                                                              | Example response                                          |
| -------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Data     | Freshness, availability violations, joins, missingness and label completeness      | Repair upstream job; suspend affected decisions           |
| Model    | Mature-cohort calibration, capacity metrics or demand errors; supported population | Diagnose drift; recalibrate or evaluate challenger        |
| Policy   | No-action/fallback rates, constraints, budget, price movement, fatigue             | Revert policy configuration or stop rollout               |
| Service  | p95 latency, timeout/error rate, duplicate deliveries, cost per decision           | Route to baseline and repair serving                      |
| Business | Experiment contribution, returns, opt-outs, complaints and retention horizon       | Check telemetry and stop according to declared guardrails |

Record baseline levels and select alert limits from business tolerance and observed variability.
Tutorial thresholds are placeholders. Keep an appropriate holdout/control so changes in the world
are not automatically credited to the model. Monitor subgroup performance and allocation against the
customer policy established for the project.

Retrain on a documented schedule or a justified trigger after checking the data. Compare the
challenger on recent mature cohorts and a stable benchmark, then shadow/canary it. Update the
calibration and policy evaluation with the exact released model. Roll back the complete compatible
release or switch to the baseline; retain the incident evidence.

## 8. Package the project and check completion

The following is a **target layout for the project you build**, not a claim that these artifacts
already exist in this book:

```text
business-ml-project/
  README.md                 # question, result, evidence level and limits
  pyproject.toml, uv.lock
  contracts/                # input, label, cost and policy definitions
  src/                      # extraction, features, train, score, decide, feedback
  configs/                  # approved actions, budgets and release config
  tests/                    # meaningful data, policy and delivery checks
  reports/                  # model/policy comparisons and experiment memo
  artifacts/                # versioned manifests; large/private files excluded from Git
  operations/               # dashboard specification, rollout and rollback runbook
```

Document commands that create data, train, evaluate, replay decisions and start serving from a clean
environment. A notebook can explore; the delivered pipeline must run without manual cell ordering.
Use synthetic examples for restricted data and disclose their generating assumptions.

| Gate             | Evidence required                                                                        | Completion level                         |
| ---------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------- |
| Problem and data | Signed-off brief, schemas, clocks, mature labels or valid censoring records, allowed use | Prototype                                |
| Model            | Same-split baseline comparison, honest holdout and uncertainty                           | Prototype                                |
| Policy           | Constraints, support/identification limits, no-action baseline and evaluation            | Prototype                                |
| Engineering      | Reproducible commands, snapshot replay, execution logs and fallback rehearsal            | Prototype                                |
| Launch readiness | Experiment protocol, owners, shadow results and stop/rollback criteria                   | Ready for a controlled pilot             |
| Measured value   | Executed valid assignments, mature outcomes, effect intervals and guardrails             | Evidence for a business rollout decision |

An inconclusive or negative experiment is a completed analysis. Explain the result and retain the
baseline when the evidence does not justify replacement. End to end means the loop reaches a
defensible decision, including the decision to collect more data.

---

[Back to Chapter 9](README.md) &nbsp;·&nbsp; [Resources](resources/README.md)
