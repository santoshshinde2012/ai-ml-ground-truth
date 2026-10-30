# Delivering a business ML system end to end

[Chapter 9](README.md) &nbsp;·&nbsp; [Offers](offer-recommendation.md) &nbsp;·&nbsp;
[Prices](price-recommendation.md) &nbsp;·&nbsp; [Churn](churn.md)

All three cases share this plan. It turns the research into a reproducible prototype and a
reviewable production proposal. Work through the gates that apply to you, and complete the live
experiment gate only after a real experiment has run. The 15 shared hours assume a small project
reusing the [Chapter 6](../06-production/README.md) deployment work.

Use the [causal primer](causal-primer.md) to write the estimand before you choose a policy
estimator. The [reference lab](../labs/README.md) is a prepared starting point. Its synthetic data
lets you inspect the mechanics, but cannot show a live business effect or replace the integration
work these gates ask for.

**In this plan:** [Decision brief](#1-define-the-decision-and-economics) &nbsp;·&nbsp;
[Data contract](#2-create-the-data-and-label-contract) &nbsp;·&nbsp;
[Policy evidence](#4-evaluate-an-action-policy-honestly) &nbsp;·&nbsp;
[Experiment](#5-design-the-experiment-before-launch) &nbsp;·&nbsp;
[Delivery](#6-deliver-and-log-the-decision) &nbsp;·&nbsp;
[Completion](#8-package-the-project-and-check-completion)

## 1. Define the decision and economics

Write a one-page brief before choosing a model:

| Field             | Record                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| Decision          | Customer/item, decision time, eligible actions, and default/no-action option                     |
| Owner and cadence | Who uses the output, batch vs session/API, and when an action can take effect                    |
| Outcome           | Exact event definition, attribution/measurement horizon and reporting delay                      |
| Economics         | Contribution after fulfilment, subsidy, contact, returns and service costs; currency and horizon |
| Constraints       | Inventory, minimum margin, subsidy/contact budget, fatigue and applicable customer policy        |
| Evidence          | Randomised assignments or identification assumptions; historical support for actions             |
| Success           | Minimum useful effect and uncertainty; service, spend and customer guardrails                    |
| Fallback          | Existing approved policy when features, evidence or serving are inadequate                       |

Measure contribution instead of revenue, and retained value instead of churn risk. If cost or
treatment data is missing, state the narrower predictive question you can answer and collect the
missing data.

## 2. Create the data and label contract

Store timestamps in UTC and keep the local calendar that business features need. Define the unique
snapshot key. Use customer IDs as join keys, and as features only for a deliberate reason. For
each snapshot at `as_of`, record the feature lookback, latest allowed availability time, label
window, label completion time and training cutoff.

For fixed-horizon targets, require `label_available_at <= training_cutoff` and verified outcome
coverage through `label_end` at fitting time. Apply any documented reporting allowance too. A
passed calendar horizon is not enough when the outcome feed is late or missing.

For [survival targets](churn.md#6-when-to-use-survival-analysis), keep the event indicator and
observed event or censoring time instead. Use only records available at the training cutoff and a
verified observation limit. Partial follow-up can stay under the censoring assumptions, but an
unfinished horizon is not a negative fixed-horizon label. Document the supported evaluation horizons
and the censoring/reference-sample protocol.

An example historical aggregation, assuming `available_at` is when an event became usable and each
event has an immutable ID:

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

This is a query pattern, not a complete feature system. Deduplicate upstream and check timezone
types and join cardinality. Version corrections instead of overwriting history with today's values.
A margin finalised later needs its own availability and version record. Use the same definitions for
replay and serving. Retrieval tools still leave you to check what “available” means
([Feast point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)).

For experiments, keep eligible opportunities even when no action was delivered. Keep assignment,
delivery and outcome in separate tables. Assignment defines the main analysis group, and delivery
explains implementation failures. Report the main result on everyone assigned, not only redeemers,
buyers, contacted responders or other groups selected after treatment.

## 3. Train, compare and freeze a release

Compare the business-as-usual rule, a simple statistical baseline and one challenger. Use your
guide's split and keep all tuning and preprocessing out of the final test. When rows depend on
each other, report uncertainty at the customer, market or time-block level that matches the
decision. Evaluate both the model and the policy built from it.

Save a release manifest like this, with real values instead of placeholders:

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
calibrator and policy together. Changing a threshold or budget counts as a policy release.

## 4. Evaluate an action policy honestly

Report predictive metrics separately from causal and policy results. An offline comparison of people
who did and did not get a discount can mostly reflect how the old team chose them. If randomised
logged actions support the target policy, evaluate that frozen policy on held-out assignments. For a
frozen deterministic target policy on a discrete action set, an inverse-propensity estimate is:

```text
estimated_value(policy) = mean(
    I[logged_action == policy(context)] * net_outcome / logging_probability
)
```

For a stochastic target policy, replace the indicator with the target probability of
the logged action, given the same context and feasible set.

The logging probability is the chance of that action under the **actual** assignment policy, given
context and candidate eligibility. It is not the model's confidence. Inspect overlap, extreme weights
and effective sample size, since a deterministic old policy cannot evaluate actions it never tried.
State the uncertainty and any clipping bias. Doubly robust estimation can reduce some errors, but it
cannot repair missing action support or arbitrary unobserved confounding
([Dudík, Langford and Li, 2011](https://arxiv.org/abs/1103.4601)).

Here `net_outcome` is the observed, mature net contribution after actual costs for every eligible
assignment unit, including no purchase and no offer. A contacted nonbuyer can have negative
contribution. It is measured, not a predicted score or a baseline-subtracted uplift. The
formula evaluates an assignment policy when `logged_action` records assignment. Keep that original
assignment for intention-to-treat after human overrides or delivery failures. Executed actions need
their own justified propensities, so do not reuse the original probability for an override chosen
in an unknown way. Constraints applied **before** the random draw belong in the known assignment
mechanism. A delivery failure after the draw is a separate record, not a reason to invent a new
randomised probability.

**For combined actions, log the joint assignment mechanism.** An action can be a tuple of offer,
price and retention choice, each with its no-change option. Its propensity is the probability of
that tuple under the coordinator, given eligible candidates and pre-decision inventory, budget,
contact history and other assignment state. Multiplying three marginal probabilities is valid
only when the design makes the choices conditionally independent, which mutually exclusive or
budget-sharing choices usually are not. For staged random draws, use the recorded conditional
probability at each stage, given earlier choices. Their product is the tuple probability. Keep the
coordinator version and assignment history to reproduce it.

This estimate covers one contextual decision over the stated outcome horizon. It does not identify
a sequential campaign policy, where contacts change later eligibility or prices use up shared
inventory. That needs a design that handles sequences and interference, or a prospective experiment
of the whole policy. Conditioning on recorded stock and budget cannot show a new policy's effect on
their future distribution, and a chain of probabilities for one compound action cannot evaluate a
policy over time. Sequential off-policy methods need supported decision histories, correct
assignment probabilities and a suitable dependence model.
[Jiang and Li's ICML 2016 paper](https://proceedings.mlr.press/v48/jiang16.html) develops a
sequential doubly robust estimator under its stated trajectory assumptions. When allocations
interact across customers, start with a controlled test of the whole coordinator.

If assignment probabilities adapt as results come in, keep their value at each draw and use
inference valid for that adaptive design. Ordinary independent-row intervals can fail even with
known probabilities. [Hadad et al., 2021 (author preprint)](https://arxiv.org/abs/1911.02768)
studies policy-evaluation inference for adaptive experiments. Check its conditions, because
logging propensities alone is not enough.

For continuous prices, this discrete formula applies only to a deliberately logged, finite price
grid. A new continuous-price policy needs density-based or structural methods with more assumptions.
Prefer a bounded randomised experiment to unsupported extrapolation. Uplift ranking scores alone
cannot show net business value.

## 5. Design the experiment before launch

Write the hypothesis, control policy, target population, primary outcome, minimum detectable
effect, power and sample-size assumptions, assignment unit, duration and stopping rule. Use
pre-treatment variance estimates and allow for repeat observations, clustering, delayed labels and
attrition. Count independent assignment units, because rows are not automatically independent. A
retention test needs its full outcome horizon, and a pricing test needs mature returns and costs.

**A power sanity check.** For two equal independent arms, a continuous outcome and a fixed
two-sided 5% test with 80% power (the chance of detecting the minimum effect), a normal
approximation gives:

```text
n_per_arm ≈ 2 × (1.96 + 0.84)^2 × outcome_variance / minimum_effect^2
```

With an invented contribution standard deviation of ₹200 per eligible account and a minimum
useful mean difference of ₹5, this is about **25,088 accounts per arm**. Halving the effect needs
roughly four times as many accounts. This is a planning illustration, not a campaign-size rule.
Heavy tails, unequal arms, multiple comparisons, covariate adjustment, attrition and clustered
assignment change the calculation. Use design-based simulation or a suitable power method with
representative pre-treatment data. Pricing market-days and repeat contacts are not independent
accounts. Allow time for outcomes to mature after the last assignment.

Keep assignments stable where repeat exposure matters. If inventory, household sharing or market
competition cause interference, consider cluster randomisation or a switchback design (switching
units between arms over time), with its own carryover assumptions. Prespecify important segment
checks and multiplicity handling. For ongoing peeking, use a valid sequential method. A daily
dashboard does not turn fixed-horizon intervals into valid stopping rules.

Where feasible, run an A/A test (both groups treated alike) or a replay to check
instrumentation. Reconcile assignment with delivery and outcome joins, and diagnose sample-ratio
mismatch before reading lift. Microsoft documents the
[pre-experiment design practices](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/)
and
[SRM checks](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/).
Use intention-to-treat as the main analysis, report actual delivery separately and explain any
extra estimand.

Analysis by assignment still needs defensible outcomes. Report follow-up completeness by arm and
recover missing outcomes where possible. Keep unreachable accounts in, and leave unknown margins
missing instead of zero. Predeclare justified missing-data, censoring and sensitivity methods. If
treatment affects whose outcome you observe, randomisation alone cannot prevent bias
([Lee's sample-selection analysis](https://www.nber.org/papers/w11721)). Separate a verified
zero-purchase outcome from an unobserved one, and postpone the impact claim when evidence is thin.

For high-variance outcomes, a predeclared covariate adjustment such as CUPED can improve precision.
Use only covariates available **before assignment**, not purchases or engagement that treatment
affects. [June 2026 CUPED research](https://arxiv.org/abs/2606.18750) examines adjustment and
valid variance estimation. Cross-fit learned adjustments where required, and keep the assignment and
clustering structure in inference. Check coverage in an A/A simulation, and update the power
calculation with justified variance estimates instead of assuming a fixed reduction.

Compare against the current business policy, not only a deliberately weak model. Look for a
meaningful contribution result with acceptable guardrails, since a significant click-rate gain is a
different claim. Investigate missing telemetry and immature labels before interpreting any
result.

Decide how results generalise before expanding the pilot. An experiment among eligible existing
customers in one region shows an effect for that population and period. In a new population,
compare eligibility, action support, baseline outcomes, costs and delivery capacity. If those change
much, replicate in stages: a larger model cannot make a transportability claim valid. Keep a
control or run a new valid experiment when expanding the action policy.

## 6. Deliver and log the decision

Start with batch scoring for daily campaigns or retention queues. Use an API only when a decision
needs current session or inventory context. Both paths need schema validation, authorisation,
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

Keep late outcomes in their own table, joined by stable keys. Store scores and reason codes needed
for debugging, with restricted access and retention periods. Keep customer secrets out of general
request logs. At execution, recheck inventory, contact fatigue and campaign and price validity.
Reserve budget transactionally before delivery. Retries must never send duplicate incentives or
apply a price change twice.

Release a reservation only after confirming the benefit was finally not delivered or issued.
Reconcile uncertain timeouts so an issued benefit keeps its reservation. Log assignment, proposed
action, executed action and override mechanism separately, marking unknown execution propensities.

When evidence is missing, return the currently allowed baseline with a reason. If even that baseline
is invalid, return `review_required` and execute nothing. A new action chosen by
extrapolation makes an unreliable fallback. Rehearse stale features, empty candidates, exhausted
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

Record baseline levels and set alert limits from business tolerance and observed variability.
Tutorial thresholds are placeholders. Keep a suitable holdout or control so the model is not
credited with changes in the world. Monitor subgroup performance and allocation against the
project's customer policy.

Retrain on a documented schedule or justified trigger after checking the data. Compare the
challenger on recent mature cohorts and a stable benchmark, then shadow or canary it. Update
calibration and policy evaluation with the exact released model. Roll back the whole compatible
release or switch to the baseline, and keep the incident records.

## 8. Package the project and check completion

Below is a **target layout for the project you build**. You create these artifacts yourself:

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

Document commands that create data, train, evaluate, replay decisions and start serving from a
clean environment. A notebook can explore, but the delivered pipeline must run without manual cell
ordering. Use synthetic examples for restricted data and state how they were generated.

| Gate             | Evidence required                                                                        | Completion level                         |
| ---------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------- |
| Problem and data | Signed-off brief, schemas, clocks, mature labels or valid censoring records, allowed use | Prototype                                |
| Model            | Same-split baseline comparison, honest holdout and uncertainty                           | Prototype                                |
| Policy           | Constraints, support/identification limits, no-action baseline and evaluation            | Prototype                                |
| Engineering      | Reproducible commands, snapshot replay, execution logs and fallback rehearsal            | Prototype                                |
| Launch readiness | Experiment protocol, owners, shadow results and stop/rollback criteria                   | Ready for a controlled pilot             |
| Measured value   | Executed valid assignments, mature outcomes, effect intervals and guardrails             | Evidence for a business rollout decision |

An inconclusive or negative experiment is a completed analysis. Explain the result and keep the
baseline when the evidence does not justify replacing it. End to end means the loop reaches a
defensible decision, which may be to collect more data.

---

[Back to Chapter 9](README.md) &nbsp;·&nbsp; [Resources](resources/README.md)
