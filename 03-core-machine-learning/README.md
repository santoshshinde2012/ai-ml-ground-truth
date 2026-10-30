# Chapter 3: Core machine learning

**Weeks 6–13 &nbsp;·&nbsp; about 80 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** This chapter teaches you to train a model carefully. Split the data so the
score means something, pick a metric tied to a real cost, compare against a simple baseline, and
explain the result. The same habits carry straight into evaluating language models later. You
finish with a model served behind an API.

**Use your Chapter 2 dataset.** Same repo or a fork — the story should connect. Review the holdout
you set aside when choosing what to predict, and keep it fixed after seeing outcomes.

**In this chapter:** [Plan](#your-eight-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your eight-week plan

About ten hours a week. Follow the rows in order, including the baseline and the README.

| Week | Focus                   | Do this                                                                                                  | Done when                                                    |
| ---- | ----------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 6    | Problem + split         | Recheck the target and reserved split (random / time / group). Justify it before fitting                | README records the split and earlier exploration             |
| 7    | Baseline + leakage      | Prior-probability baseline (`DummyClassifier`). Leak preprocessing on purpose, then fix it with Pipeline | Before/after scores in README                                |
| 8    | Logistic regression     | ISL or scikit-learn MOOC. Pick a metric tied to cost                                                     | Beats the baseline, or explains why to keep the baseline     |
| 9    | Trees                   | Random forest + one boosted tree. SHAP on one wrong prediction                                           | Quality, calibration, runtime/memory and latency compared    |
| 10   | Calibration + threshold | Reliability plot on held-out data. Tune the decision on validation costs                                 | Can explain probability and threshold separately             |
| 11   | API                     | FastAPI `/predict` with Pydantic validation. Test a valid and an invalid request                         | Served predictions match saved bundle. Bad input returns 422 |
| 12   | Polish                  | Confidence intervals, a "what failed" section and a load-test note                                       | README is the deliverable                                    |
| 13   | Buffer                  | Rebuild one model from an empty file. Practise your leakage story for interviews                         | Can rebuild without a tutorial                               |

The table uses **binary classification** as its first-project example. For a numeric target, use
`DummyRegressor`, regularised linear regression, `RandomForestRegressor` and a boosted regressor.
Swap the threshold exercise for error/interval analysis and a cost-based decision rule. The same
split, holdout and API requirements apply. A well-explained negative result completes the
comparison. Avoid searching for a misleading split just to beat the baseline.

For a first multiclass project, compare a class-prior baseline. Report a confusion matrix and
per-class precision/recall alongside the aggregate you chose. A binary cost threshold does not carry
over to several classes. Define the cost of each action/outcome pair and choose the lowest expected
cost using suitable probabilities. Multilabel tasks also need their own label-level decision and
evaluation design. Leave them for later if the basic workflow is new.

In your uv project, start with `uv add scikit-learn`. In Week 9, add the boosted-tree and SHAP
packages you chose, following their official install guides, and commit the updated lock. Keep one
boosted candidate. Installing three libraries is not a model comparison.

---

## Is this still worth eight weeks in 2026?

Yes. The skills here support both tabular business decisions and generative systems. A more capable
pretrained model still needs a deployment-matched test, a baseline, a suitable metric and a
cost-aware decision. The split and leakage habits carry into
[Chapter 5](../05-language-models/README.md), though agent evaluation also needs its own tests for
tools, safety and interaction.

Eight weeks, then, rather than six months.

## What you will be able to do

Take an unfamiliar dataset, choose a validation scheme and defend it, choose a metric and tie it to
a real cost, compare to a simple baseline, and explain in writing why each model helped or did not.

## What to learn

### Worked lesson: a probability is not an action

Four made-up development cases have predicted event probabilities `[0.1, 0.4, 0.7, 0.9]` and true
labels `[0, 1, 0, 1]`. A false positive costs 2 units and a false negative costs 8. Assume correct
decisions have zero cost and there is no capacity limit.

At threshold 0.5, the last two cases are positive: one false positive and one false negative cost
`2 + 8 = 10`. At threshold 0.2, the last three are positive: one false positive costs 2. The model
has not changed. The action policy has.

With calibrated probabilities and these costs, compare the cost of acting, `2 × (1 - p)`, with the
cost of not acting, `8 × p`. Acting is cheaper when `p > 2 / (2 + 8) = 0.2`. Set a rule for ties.
This assumes the error costs describe the decision. It cannot show a treatment benefit from a
churn-risk score.

```python
probabilities = [0.1, 0.4, 0.7, 0.9]
labels = [0, 1, 0, 1]

def observed_cost(threshold, false_positive_cost=2, false_negative_cost=8):
    return sum(false_positive_cost if p >= threshold and y == 0 else
               false_negative_cost if p < threshold and y == 1 else 0
               for p, y in zip(probabilities, labels))

assert observed_cost(0.5) == 10
assert observed_cost(0.2) == 2
```

**Try it yourself.** Swap the costs: false positives cost 8 and false negatives cost 2. Work out
the threshold and its observed cost. Is a four-case table enough to show calibration?

<details>
<summary>Hint and explained answer</summary>

Compare `8 × (1 - p)` with `2 × p`. The threshold is 0.8. Only the 0.9 case is positive, so the
0.4 case is a false negative and the total observed cost is 2. Four cases cannot show reliable
calibration or a lower cost in production. Set the rule on development data. Then evaluate the
frozen model, calibrator and policy on independent data, with suitable uncertainty.

</details>

The [reference lab](../labs/README.md) has a reproducible baseline comparison. Write down your
expected result before running it, and explain any difference from what you see.

### Core concepts and practical failure modes

On a first pass, focus on the split, baseline, pipeline, metric and decision. The dated benchmark,
advanced uncertainty and causal sections below are optional depth after that baseline works.

**The learning problem.** A model maps inputs to outputs, and a loss measures its errors. Many
models optimise differentiable parameters with gradient-based methods. Trees learn partitions, and
linear regression can also use a direct solver. Learn regularisation, bias and variance, and how
each candidate is optimised. Not every model trains like a transformer.

Learning curves are the most practically useful idea here and the most often skipped. Plotting
training and validation score against training-set size helps you judge whether more representative
data or a different model might help. Treat it as a clue to test, not a firm diagnosis. Label noise,
distribution shift and a changing population mix can produce similar patterns. Keep time or group
structure while building the curves.

**Validation, which is where the real care goes.** Your validation score estimates performance under
its sampling and deployment assumptions. Information not available at the simulated training or
prediction time can quietly invalidate it. Leakage often makes scores look too good, and even a
clean holdout cannot promise performance after an untested change.

Three families to know:

| Kind                      | What happens                                                                                                                          | Guard                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Preprocessing leakage** | You fit a scaler, imputer or target encoder on the whole dataset before splitting, so every fold has seen the test set's statistics   | Put all preprocessing inside a `Pipeline`, so cross-validation refits it per fold |
| **Temporal leakage**      | You use information that did not exist at prediction time. Random K-fold on time-ordered data trains on Thursday to predict Wednesday | `TimeSeriesSplit`, or rolling-origin backtesting                                  |
| **Group leakage**         | Rows from the same entity land on both sides of the split, while you claim performance on unseen entities                            | `GroupKFold` or `StratifiedGroupKFold` for that deployment question               |

Two questions, asked before you choose a splitter, prevent most of this: **does a row's identity
repeat, and does time matter?**

Match the split to deployment. Predicting next month's activity for existing customers can fairly
reuse their earlier histories. If the launch includes new customers, also evaluate on unseen ones.
A time split and a group split answer different questions, and sometimes you need both. Leave out
immature training labels. If a label needs 30 days plus seven days of reporting delay, those 37 days
must have passed by the simulated training cutoff. A fixed row-count gap in `TimeSeriesSplit` does
not by itself enforce a calendar-based label window.

Keep separate training, model-selection, calibration/decision-selection and final test data, or
use carefully designed out-of-fold estimates. Refitting a model can change its calibration, so
evaluate the exact model and calibrator you will serve. Early stopping, feature selection,
resampling and hyperparameter tuning all belong inside the training procedure. Open the final test
only after the choices are frozen.

Label maturity and observation are separate checks. A 30-day window can end with the source record
missing. Keep that out of the negatives, and avoid quietly scoring only the matched outcomes. Report
coverage by time and cohort, and say which population the score represents. A duration target with
incomplete follow-up needs a censoring-aware design, as
[Chapter 2](../02-data-foundations/README.md#what-to-learn) explains.

A pipeline is necessary, but it does not choose the right time or group handling for every
component. For example,
[scikit-learn's TargetEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html)
uses cross-fitting in `fit_transform`. Calling `fit(...).transform(...)` on the same training rows
does something different. Default internal folds are random. Since 1.9 you can pass grouped
splitters through metadata routing, but every row must appear in a validation fold exactly once. An
ordinary forward-only `TimeSeriesSplit` breaks that rule. Time-ordered encodings need an explicit
past-only design or a different encoder. Keep a training row's own and future labels out of its
feature encoding.

Repeatedly picking the best score across many models and settings also overfits validation. Use a
fixed tuning budget and an untouched test. To estimate the whole selection procedure, use
deployment-matched nested validation. Compare models on the same rows and horizon, and record
version, seed, search budget and failed runs. The
[nested-CV example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html)
explains the selection bias, but its random folds need adapting for time or groups.

**Metrics, which are decisions in disguise.** On a dataset with 1% positives, a model that always
predicts "no" scores 99% accuracy. A metric is a claim about what it costs to be wrong, and choosing
one is a business decision you are making on someone's behalf, usually by leaving it at the default.

Use
[`DummyClassifier(strategy="prior")`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)
as the probability baseline. It estimates class frequencies from training labels and predicts
the majority class. Unlike `strategy="most_frequent"`, its probabilities are not forced to zero and
one, so it is a useful log-loss/Brier comparator. Also report the simplest real action policy under
your stated costs, such as always taking no action. A probability baseline and an action baseline
answer different questions.

Learn precision and recall well, and when each matters more. ROC-AUC measures ranking, but can
coexist with poor precision when positives are rare. Report average precision or a clearly defined
PR-AUC, positive prevalence, and precision/recall at your team's real capacity. PR metrics also
depend on prevalence, so they are not directly comparable across datasets.

**Probability and action are separate.** A score of 0.8 should mean about 80% positives among
similar scored cases. Check a reliability diagram and log loss or Brier score. Those losses also
reflect discrimination, so neither alone proves calibration. Fit sigmoid or isotonic calibration on
independent, representative data and recheck it by cohort. Small calibration samples make flexible
isotonic fits unstable. Calibration on last month's sample does not guarantee calibration after
prevalence, eligibility or data collection changes.
[scikit-learn's calibration guide](https://scikit-learn.org/stable/modules/calibration.html)
explains the methods. Choose thresholds on validation data using costs and capacity, then evaluate
once on untouched test data. See the
[threshold tuning guide](https://scikit-learn.org/stable/modules/classification_threshold.html).

Class weighting, oversampling and undersampling can change a classifier's probability scale. Fit any
sampler inside training folds only. Keep calibration, decision selection and final evaluation at
deployment prevalence, or document justified sampling weights. A balanced test set answers a
different question, as
[imbalanced-learn's leakage examples](https://imbalanced-learn.org/stable/common_pitfalls.html)
show. Cost-weighted scores are not automatically raw event probabilities. Check their calibration
before applying a cost-derived probability threshold, even if you used costs in training.

Calibration needs the same care with splits.
[`CalibratedClassifierCV`](https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html)
defaults to stratified folds for classification, which ignore your time or entity boundary. A
simple route: wrap a fitted pipeline in `FrozenEstimator` and calibrate it on a separate,
representative set that follows the same deployment split. Keep threshold-selection and final test
data apart. For cross-fitted calibration, check the API's fold requirements and class support, and
confirm your time splitter works with your ensemble setting.

**A tiny threshold example.** Suppose false negatives cost ten times false positives — missing a
fraud case is ten times worse than flagging an honest transaction. With calibrated probabilities,
zero cost for correct classifications and no capacity limit, expected loss is minimised at
`C_FP / (C_FP + C_FN) = 1 / 11`, about 0.091. Measure precision and recall at that threshold on
validation data, since the cost ratio does not determine them. Capacity limits or case-varying costs
need a richer decision rule. On 1% positives, "always no" still scores 99% accuracy, which shows why
accuracy alone is not enough.

**Tree models.** Gradient-boosted trees are a strong practical candidate for many tabular problems.
Compare them against a simple model on your actual split. Learn what bagging and boosting each buy
you, and what `max_depth`, `min_child_weight`, `subsample`, `colsample_bytree` and early stopping
actually do to bias and variance. XGBoost, LightGBM and CatBoost are alternatives for this week's
single boosted candidate. CatBoost is convenient for many categorical fields, and LightGBM can be
efficient on large tables. Measure those benefits on your data and hardware.

Also learn interpretability: permutation importance and why it misleads under correlated features,
partial dependence, and SHAP, which attributes a single prediction to the features that drove it.
Feature attributions describe a model's prediction, not the effect of changing a customer's
behaviour. A SHAP plot alone cannot show causality, fairness or fitness for a high-stakes decision.
When explanation is a requirement, compare simpler interpretable models. scikit-learn's [causal
interpretation
example](https://scikit-learn.org/stable/auto_examples/inspection/plot_causal_interpretation.html)
shows why predictive explanations can mislead about interventions.

<details>
<summary>Optional research: tabular model comparisons in 2026</summary>

Pretrained tabular models are serious challengers, especially in small/medium IID benchmark
settings, where rows are sampled independently. The June [BeyondArena
preprint](https://arxiv.org/abs/2606.30410) evaluated 142 datasets, including time, group and scale
challenges. It tested then-current versions, including TabPFN-2.6. The September [TabPFN-3.5
report](https://arxiv.org/abs/2609.17895) claims the overall core lead, yet reports that
tuned/ensembled MLPs still lead its full grouped, temporal and large slices. Its group-ID protocol
differs from the original, and headline family rankings combine different variants, including hosted
Thinking and the released checkpoint. Neither result names a universal winner for one fixed model or
serving budget.

| Your setting                                               | Candidates and decision                                                                                                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| First learning project or limited CPU budget               | Dummy and regularised linear/logistic baseline, then one forest and boosted tree. Finish careful validation before adding models.                                   |
| Small/medium labelled table with feasible inference budget | Optionally compare a current TabPFN or TabICLv2 checkpoint against the completed boosted baseline. Keep calibration and test labels out of its training context.    |
| Large/wide data, repeated entities or future deployment    | Compare feasible boosted trees and, when it makes sense, an MLP or foundation model on the actual group/time split. Measure memory, batch and single-request latency. |
| Explanation, licensing or operational constraints dominate | Include a simpler interpretable candidate and check the specific code, weight and service licences. Benchmark score is only one reason to choose.                  |

These models use labelled training rows as inference context. Pretrained inference still needs your
data, and serving still costs something. Pin checkpoint and package versions, time the full
preprocessing/context/inference path and record where the context came from. As of this review,
[TabPFN's code and newer weights have different terms](https://github.com/PriorLabs/TabPFN),
including noncommercial weight restrictions. [TabICLv2](https://github.com/soda-inria/tabicl) is
another candidate with permissive distribution. Check the chosen checkpoint's terms before a public
or commercial deployment. This comparison is an optional Week 13 experiment, not extra required
weeks.

Also test sensitivity to the labelled context's class balance. The
[ICML 2026 DistPFN paper](https://proceedings.mlr.press/v306/lee26aw.html) reports accuracy and
calibration gains under controlled resampling for TabPFN-v2, LoCalPFN and TabICL. That is a reason
to check training-prior sensitivity, not proof that posterior adjustment fixes arbitrary feature
drift or improves TabPFN-3.5. Label-shift corrections assume stable feature distributions within
each class. Representative held-out calibration is still the starting point.

</details>

**Regression and forecasting.** For a numeric target, compare a constant or seasonal baseline,
regularised linear regression and a boosted regressor. Report MAE in business units, look at errors
by segment, and use quantile/prediction intervals when uncertainty changes the decision. MAPE is
undefined at zero and unstable near zero, so choose scaled or absolute errors on purpose.
[Forecasting: Principles and Practice](https://otexts.com/fpp3/accuracy.html) explains the
tradeoffs. For demand over time, compare seasonal-naive, exponential-smoothing or ARIMA baselines
with a lag-feature tree. Backtest at several rolling origins and at the real forecast horizon.
Compute lags and rolling statistics from past data only. Start with the
[scikit-learn lagged-features example](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html).

Update features the way serving will. Rolling one-step forecasts may use observations that arrive
between predictions. A 24-hour forecast issued now cannot use tomorrow's realised demand in later
lags. For fixed-origin multi-step forecasts, recursively feed back predicted values, or train direct
per-horizon models on origin-available inputs only. Report error by horizon, as in the [forecast
cross-validation example](https://otexts.com/fpp3/tscv.html). A forecast at today's price cannot
tell you demand at an untested price.

For a forecasting project, an optional challenger can be
[Chronos-2](https://arxiv.org/abs/2510.15821) or
[TimesFM 3](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/).
Their current interfaces support multivariate/covariate-informed forecasts. Check the chosen
checkpoint's frequency, context and horizon limits. Future covariates must really be known at the
forecast origin. A scheduled holiday is, but tomorrow's realised weather or sales are not. Compare
business error and interval coverage at the same rolling origins, including holidays, stockouts and
regime changes. The model's own benchmark wins do not replace this check.
[TimesFM 3's downloadable weights have noncommercial/nonproduction terms](https://github.com/google-research/timesfm)
separate from its code and hosted commercial offering. Keep seasonal/statistical baselines even when
a foundation model wins.

**Clustering and anomaly detection, when the question calls for them.** Use scaled K-means as a
segmentation baseline, PCA for exploring correlated features, and Isolation Forest as an anomaly
candidate. Check segment stability and business usefulness. A silhouette score alone does not
validate a customer strategy. Review anomalies against labelled examples and measure precision at
the review budget. These are optional extensions. Your supervised project comes first.

**Intervals that match your data.** Compare models in pairs on the same test cases. When customers
repeat, bootstrap customers rather than rows. For serial dependence, use suitable time blocks. Fold
standard deviation is not a confidence interval for future deployment. Freeze the comparison plan
before the final test, and report the sample size and dependence assumptions.

Prediction intervals and confidence intervals answer different questions. The first covers one
future outcome, the second a measured model comparison. As optional depth,
[split conformal prediction](https://arxiv.org/abs/2107.07511) wraps a model using separate
calibration residuals. Its usual guarantee is marginal coverage under exchangeability: an average
over cases, not a promise for each customer or under arbitrary temporal drift. Report interval
width and observed coverage by horizon/cohort. Neither quantile forecasts nor conformal intervals
give causal evidence.

**From prediction to intervention.** Offer recommendation, pricing and retention ask what changes
when you take an action. That claim needs randomised treatment data or a causal identification
design you can defend. [Chapter 9](../09-business-machine-learning/README.md) has the data and model
recipes. A churn classifier, sales regressor or click ranker can be a useful baseline without
showing that a campaign increases profit.

**The maths, paid for as you go.** This is the most argued-about part of any AI roadmap, so here is
my reading of it, plainly.

The people who teach the hands-on courses agree to an unusual degree. fast.ai's own prerequisites
page says high-school maths is enough. Karpathy's course asks for "intro-level math (e.g.
derivative, gaussian)". Parr and Howard tell readers to come to their matrix-calculus paper only
**after** they are already training networks. The failure I see most often is over-preparing, not
under-preparing: committing to a long linear algebra course before writing any model, and stalling
around month three with nothing built.

The minimum is small enough to name:

- **Linear algebra:** vectors, matrices and tensors. Shapes and axes. Matrix multiplication and why
  shapes must line up. Transpose, dot product as similarity, broadcasting. A matrix as a
  transformation, and matrix products as composition. Eigenvectors, SVD, rank, norms and
  orthogonality can wait a few weeks.
- **Calculus:** the derivative as sensitivity, partial derivatives and the gradient. **The chain
  rule**, which carries more weight than anything else here. Recognising a Jacobian, and gradient
  descent. Integrals, Hessians and hand-derived matrix calculus can wait, or may never come up.
- **Probability and statistics:** random variables, expectation and variance, independence,
  conditional probability, Bayes' rule, the Gaussian, Bernoulli and categorical distributions,
  likelihood and maximum likelihood, log-probabilities, and cross-entropy as a loss.

That is perhaps twenty to forty hours of focused study rather than a semester. Classical hypothesis
testing gets less weight here on purpose. It matters a great deal for experimentation work, which
the [Data Scientist branch of Chapter 7](../07-specialisation/README.md) covers.

The counter-argument deserves respect too. People who take the code-first route and never come back
to the maths tend to plateau at the point where they need to read a paper, debug an unusual loss, or
design an architecture. The bill arrives either way. Paying it here, once you have something
concrete to attach it to, tends to go better.

## Resources

All 43 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

Choose one main textbook or course, plus selected reference sections. Full-resource reading
estimates are alternatives, not a total to fit inside 80 hours. Pick up the maths as you need it.
Once the required project is complete, use the buffer week for one optional research comparison.

The ones to begin with:

- [An Introduction to Statistical Learning (ISLP — Python edition)](https://www.statlearning.com/) —
  Gareth James, Daniela Witten, Trevor Hastie & Robert Tibshirani, with Jonathan Taylor. A free
  book. Pick sections that fit this chapter's 80 hours, rather than the full 60–90-hour reading
  estimate.
- [scikit-learn: Common Pitfalls and Recommended Practices](https://scikit-learn.org/stable/common_pitfalls.html)
  — scikit-learn core developers. Free documentation, 2–3 hours. Read it in week 7, before the
  leakage exercise.
- [Approaching (Almost) Any Machine Learning Problem](https://github.com/abhishekkrthakur/approachingalmost)
  — Abhishek Thakur. A free book, 20–30 hours.
- [Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/) — Christoph
  Molnar. A free book, 12–18 hours. Start with the SHAP and permutation-importance chapters.

## What to build

**A model behind an API.** Take your [Chapter 2](../02-data-foundations/README.md) dataset and
complete the loop:

1. A split you chose deliberately and justified in writing
2. All preprocessing inside a `Pipeline`
3. A simple baseline, then a linear/logistic model, a random forest and a boosted tree for the
   target type
4. A metric tied to a stated cost, reported with confidence intervals
5. A classification threshold or regression decision rule taken from the stated costs and
   constraints
6. SHAP explanations, including a misclassified case or a large-error regression case
7. A FastAPI endpoint with schema validation, and tests for both code and data
8. A reliability plot or regression error analysis, an untouched test comparison, and documented
   label maturity, outcome coverage and calibration/decision-selection splits
9. A versioned model/preprocessor/calibrator bundle with dependency and data provenance, plus a
   fresh-process API check

The README is the deliverable. Include a table of every model and what it bought you, a section on
what did not work, and a section on known failures. Those last two are unusual in a junior portfolio
and they do a lot of quiet good.

Return a model version with predictions, validate feature names/types/units, and define behaviour
for missing or unknown categories. Serve the preprocessing/model/calibration bundle you tested, and
keep retraining and scaler fitting out of the request. For Week 11, add the API and testing
dependencies:

```bash
uv add "fastapi[standard]"
uv add --dev pytest httpx
uv run --locked pytest
```

Follow the official [request-body](https://fastapi.tiangolo.com/tutorial/body/) and
[testing](https://fastapi.tiangolo.com/tutorial/testing/) guides. In a fresh process, test a valid
request against the saved bundle's prediction, including the probability or numeric prediction,
model version and chosen decision rule. Also test a malformed request and your chosen handling of
missing/unknown inputs. Load a Python model artifact with the training environment's dependency
versions. Loading across scikit-learn versions is unsupported, as the
[persistence guide](https://scikit-learn.org/stable/model_persistence.html) explains. Document
measured latency, memory and CPU fallback. Chapter 6 covers production operations.

**The Week 7 leakage exercise:** fit preprocessing on the full dataset on purpose and record the
score. Then move the fitting inside a `Pipeline` and repeat on the same split. Report the real
difference, even if it is small, since this leak does not always change the score much.
Availability-time and group errors need their own data or split fixes. A pipeline fixes this kind
of leakage, not every kind.

**Handoff to Chapter 4.** Commit the split definition, feature pipeline and every model's results.
[Chapter 4](../04-deep-learning/README.md) can train a small network on these same features and
compare it with these numbers on the same rows. Keep the split fixed and the test untouched.

## Before you move on

- Given a dataset description, you can choose a split and a metric and defend both in a minute.
- You can explain the costs and derive your classification threshold or numeric action rule out
  loud.
- You can explain what SHAP computes, and one thing it does not tell you.
- You can call your endpoint, match a valid prediction to the saved bundle and show it rejecting a
  malformed request.
- You can explain which decisions your predictions support and which need an experiment.
- Your comparison states the actual split, model/checkpoint versions and compute limits. The served
  bundle reproduces the tested predictions.
- You can explain how missing outcomes or a changed class balance could change the reported score,
  probability scale and action threshold.

## A few things worth knowing

- **Start with ISL rather than ESL.** They share authors and the titles are similar, but _Elements
  of Statistical Learning_ is a graduate statistics text. People often start there, stop at chapter
  three, and conclude they are not a maths person. They usually are. It was the wrong book.
- **If you want Strang's linear algebra**, MIT 18.065 is the machine-learning-facing course. 18.06
  is excellent and spends its first month on material you will not use here.
- **Kaggle is a good gym and a weak portfolio.** Competitions give fast, honest feedback on
  validation design, which is genuinely valuable. They also remove problem framing, data sourcing
  and metric choice, which are three of the harder parts of the job.

---

[Previous: Data foundations](../02-data-foundations/README.md) &nbsp;·&nbsp;
[Next: Deep learning](../04-deep-learning/README.md)
