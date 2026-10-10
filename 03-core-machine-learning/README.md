# Chapter 3: Core machine learning

**Weeks 6–13 &nbsp;·&nbsp; about 80 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** This chapter teaches you to train a model honestly: split the data so the
score means something, pick a metric that maps to a real cost, compare against a simple baseline,
and explain the result. The same discipline carries straight into evaluating language models later.
You finish with a model served behind an API.

**Use your Chapter 2 dataset.** Same repo or a fork — the story should connect.

**In this chapter:** [Plan](#your-eight-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your eight-week plan

About ten hours a week. Follow the rows; do not skip the baseline or the README.

| Week | Focus                   | Do this                                                                                                  | Done when                                                    |
| ---- | ----------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 6    | Problem + split         | Define prediction target; choose split (random / time / group); justify in writing                       | Split documented in README                                   |
| 7    | Baseline + leakage      | Prior-probability baseline (`DummyClassifier`); deliberate preprocessing leakage, then fix with Pipeline | Before/after scores in README                                |
| 8    | Logistic regression     | ISL or scikit-learn MOOC; metric tied to cost                                                            | Improves on baseline or explains why to retain it            |
| 9    | Trees                   | Random forest + one boosted tree; SHAP on one wrong prediction                                           | Quality, calibration, runtime/memory and latency comparison  |
| 10   | Calibration + threshold | Reliability plot on held-out data; tune decision on validation costs                                     | Can explain probability and threshold separately             |
| 11   | API                     | FastAPI `/predict`; Pydantic validation; valid-request and invalid-request tests                         | Served predictions match saved bundle; bad input returns 422 |
| 12   | Polish                  | Confidence intervals; "what failed" section; load-test note                                              | README is the deliverable                                    |
| 13   | Buffer                  | Re-build one model from empty file; rehearse interview story on leakage                                  | Can rebuild without tutorial                                 |

The table uses classification as its example. For a numeric target, use `DummyRegressor`,
regularised linear regression, `RandomForestRegressor` and a boosted regressor. Replace the
classification threshold exercise with error/interval analysis and a cost-based decision rule. The
same split, holdout and API requirements apply. A justified negative result completes the
comparison; do not search for a misleading split just to beat the baseline.

In the existing uv project, start with `uv add scikit-learn`. Add the selected boosted-tree and SHAP
packages when you reach Week 9, using their official installation guidance and committing the
updated lock. Keep one boosted candidate; installing three libraries is not a model comparison.

---

## Is this still worth eight weeks in 2026?

Yes: the skills here support both tabular business decisions and generative systems. A more capable
pretrained model still needs a deployment-matched test, a baseline, an appropriate metric and a
cost-aware decision. The split and leakage discipline carries into
[Chapter 5](../05-language-models/README.md), although agent evaluation also needs task-specific
tests for tools, safety and interaction.

Eight weeks, then, rather than six months.

## What you will be able to do

Take an unfamiliar dataset, choose a validation scheme and defend it, choose a metric and tie it to
a real cost, compare to a simple baseline, and explain in writing why each model helped or did not.

## What to learn

**The learning problem.** A model maps inputs to outputs, and a loss measures its errors. Many
models optimise differentiable parameters with gradient-based methods; trees learn partitions and
linear regression can also use a direct solver. Learn regularisation, bias and variance, and the
optimisation method used by each candidate rather than assuming every model trains like a
transformer.

Learning curves are the most practically useful idea here and the most often skipped. Plotting
training and validation score against training-set size helps diagnose whether more representative
data or a different model might help. It is evidence to test, not a unique diagnosis: label noise,
distribution shift and changing population composition can produce similar patterns. Preserve time
or group structure while building the curves.

**Validation, which is where the real care goes.** Your validation score estimates performance under
its sampling and deployment assumptions. Information unavailable at the simulated training or
prediction time can invalidate that estimate without raising an error. Leakage often makes scores
optimistic; an honest holdout still cannot promise performance after an untested change.

Three families to know:

| Kind                      | What happens                                                                                                                          | Guard                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Preprocessing leakage** | You fit a scaler, imputer or target encoder on the whole dataset before splitting, so every fold has seen the test set's statistics   | Put all preprocessing inside a `Pipeline`, so cross-validation refits it per fold |
| **Temporal leakage**      | You use information that did not exist at prediction time. Random K-fold on time-ordered data trains on Thursday to predict Wednesday | `TimeSeriesSplit`, or rolling-origin backtesting                                  |
| **Group leakage**         | Related rows cross folds when you claim performance on unseen entities                                                                | `GroupKFold` or `StratifiedGroupKFold` for that deployment question               |

Two questions, asked before you choose a splitter, prevent most of this: **does a row's identity
repeat, and does time matter?**

Match the split to deployment. Predicting next month's activity for existing customers can
legitimately reuse those customers' earlier histories; also evaluate unseen customers if that is
part of the launch. A time split and a group split answer different questions, and sometimes you
need both. Exclude immature training labels: if a label needs 30 days plus seven days of reporting
delay, those 37 days must have elapsed by the simulated training cutoff. A fixed row-count gap in
`TimeSeriesSplit` does not by itself enforce a calendar-based label window.

Keep separate training, model-selection, calibration/decision-selection and final test data, or use
carefully designed out-of-fold estimates. Refitting a model can change its calibration; evaluate the
exact model and calibrator you will serve. All early stopping, feature selection, resampling and
hyperparameter tuning belong inside the training procedure. The final test is opened after the
choices are frozen.

Label maturity and observation are separate checks. A 30-day window can end with a missing source
record; do not treat that as a negative or silently evaluate only successfully matched outcomes.
Report coverage by time and cohort, and state which population the score represents. A duration
target with incomplete follow-up needs a censoring-aware design, as explained in
[Chapter 2](../02-data-foundations/README.md#what-to-learn).

A pipeline is necessary but does not choose the correct time/group semantics for every component.
For example,
[scikit-learn's TargetEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html)
uses cross-fitting in `fit_transform`; calling `fit(...).transform(...)` on the same training rows
does not do the same thing. Default internal folds are random. Since 1.9, grouped splitters can be
supplied with metadata routing, but every row must appear in a validation fold exactly once. An
ordinary forward-only `TimeSeriesSplit` does not satisfy that rule; chronological encodings need an
explicit past-only design or a different encoder. Never let a training row's own or future label
enter its feature encoding.

Repeatedly choosing the best score over many models and configurations also overfits validation. Use
a fixed tuning budget and untouched test, or deployment-matched nested validation when you need to
estimate the entire selection procedure. Compare models on the same rows and horizon; record
version, seed, search budget and failed runs. The
[nested-CV example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html)
explains the selection bias; its random-fold example needs adaptation for time or groups.

**Metrics, which are decisions in disguise.** On a dataset with 1% positives, a model that always
predicts "no" scores 99% accuracy. A metric is a claim about what it costs to be wrong, and choosing
one is a business decision you are making on someone's behalf, usually by leaving it at the default.

Use
[`DummyClassifier(strategy="prior")`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html)
as the probability baseline: it estimates class frequencies from training labels and predicts the
majority class. Unlike `strategy="most_frequent"`, its probabilities are not forced to zero and one,
making it a useful log-loss/Brier comparator. Also report the simplest actual action policy, such as
always taking no action, under your stated costs. A probability baseline and an action baseline
answer different questions.

Worth knowing well: precision and recall and when each dominates. ROC-AUC measures ranking, but can
coexist with poor precision when positives are rare. Report average precision or a clearly defined
PR-AUC, positive prevalence, and precision/recall at your team's actual capacity. PR metrics also
depend on prevalence; they are not automatically comparable across datasets.

**Probability and action are separate.** A score of 0.8 should correspond to about 80% positives
among similar scored cases. Inspect a reliability diagram and log loss or Brier score; those losses
also reflect discrimination, so neither alone proves calibration. Fit sigmoid or isotonic
calibration on independent, representative data and recheck it by cohort. Small calibration samples
make flexible isotonic fits unstable. Calibration in last month's sample does not guarantee
calibration after prevalence, eligibility or data collection changes.
[scikit-learn's calibration guide](https://scikit-learn.org/stable/modules/calibration.html)
explains the methods. Choose thresholds on validation data, using costs and capacity, and then
evaluate once on untouched test data; see the
[threshold tuning guide](https://scikit-learn.org/stable/modules/classification_threshold.html).

Class weighting, oversampling and undersampling can change a classifier's probability scale. Fit any
sampler only within training folds. Keep calibration, decision selection and final evaluation
representative of deployment prevalence, or document justified sampling weights. A balanced test set
answers a different question; see
[imbalanced-learn's leakage examples](https://imbalanced-learn.org/stable/common_pitfalls.html).
Cost-weighted scores are not automatically raw event probabilities. Check their calibration before
applying a cost-derived probability threshold; using costs in training does not remove that check.

Calibration has its own split semantics.
[`CalibratedClassifierCV`](https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html)
defaults to stratified folds for classification, which do not enforce your time or entity boundary.
A simple route is a fitted pipeline wrapped in `FrozenEstimator`, calibrated on a disjoint,
representative set that follows the same deployment split. Keep threshold-selection and final test
data separate. For cross-fitted calibration, verify the API's fold requirements and class support;
do not assume that any time splitter works with every ensemble setting.

**A tiny threshold example.** Suppose false negatives cost ten times false positives — you miss a
fraud case ten times worse than you flag an honest transaction. With calibrated probabilities, zero
cost for correct classifications and no capacity constraint, expected loss is minimized at
`C_FP / (C_FP + C_FN) = 1 / 11`, about 0.091. Precision and recall at that threshold must be
measured from validation data; the cost ratio does not determine them. Capacity limits or costs that
vary by case require a richer decision rule. On 1% positives, "always no" still scores 99% accuracy,
which illustrates why accuracy alone is inadequate.

**Tree models.** Gradient-boosted trees are a strong practical candidate for many tabular problems.
Compare them against a simple model on your actual split. Learn what bagging and boosting each buy
you, and what `max_depth`, `min_child_weight`, `subsample`, `colsample_bytree` and early stopping
actually do to bias and variance. XGBoost, LightGBM and CatBoost are alternatives for this week's
single boosted candidate; CatBoost is convenient for many categorical fields, while LightGBM can be
efficient on large tables. Measure those benefits on your data and hardware.

Also learn interpretability: permutation importance and why it misleads under correlated features,
partial dependence, and SHAP, which attributes a single prediction to the features that drove it.
Feature attributions describe a model's prediction, not the effect of changing a customer's
behaviour. A SHAP plot alone does not establish causality, fairness or suitability for a
consequential decision. Compare simpler interpretable models when explanation is a requirement;
scikit-learn's
[causal interpretation example](https://scikit-learn.org/stable/auto_examples/inspection/plot_causal_interpretation.html)
shows why predictive explanations can mislead about interventions.

**What changed in tabular modelling in 2026.** Pretrained tabular models are serious challengers,
especially on the small/medium IID benchmark settings where rows are independently sampled. The June
[BeyondArena preprint](https://arxiv.org/abs/2606.30410) evaluated 142 datasets including time,
group and scale challenges; it tested then-current versions, including TabPFN-2.6. The September
[TabPFN-3.5 report](https://arxiv.org/abs/2609.17895) claims the overall core lead, yet reports that
tuned/ensembled MLPs still lead its full grouped, temporal and large slices. Its group-ID protocol
differs from the original, and headline family rankings combine different variants, including hosted
Thinking and the released checkpoint. Neither result establishes a universal winner for one fixed
model or serving budget.

| Your setting                                               | Candidates and decision                                                                                                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| First learning project or limited CPU budget               | Dummy and regularised linear/logistic baseline, then one forest and boosted tree. Complete honest validation before adding models.                                  |
| Small/medium labelled table with feasible inference budget | Optionally compare a current TabPFN or TabICLv2 checkpoint against the completed boosted baseline. Keep calibration and test labels out of its training context.    |
| Large/wide data, repeated entities or future deployment    | Compare feasible boosted trees and, when warranted, an MLP or foundation model using the actual group/time split. Measure memory, batch and single-request latency. |
| Explanation, licensing or operational constraints dominate | Include a simpler interpretable candidate and check the specific code, weight and service licences. Benchmark score is only one selection criterion.                |

These models use labelled training rows as inference context; pretrained inference does not mean
learning from no data or serving at zero cost. Pin checkpoint and package versions, time the full
preprocessing/context/inference path and preserve context provenance. As of this review,
[TabPFN's code and newer weights have different terms](https://github.com/PriorLabs/TabPFN),
including noncommercial weight restrictions; [TabICLv2](https://github.com/soda-inria/tabicl) is
another candidate with permissive distribution. Verify the chosen checkpoint's terms before a public
or commercial deployment. This comparison is an optional Week 13 experiment, not extra required
weeks.

Also test sensitivity to the labelled context's class balance. The
[ICML 2026 DistPFN paper](https://proceedings.mlr.press/v306/lee26aw.html) reports accuracy and
calibration gains under controlled resampling for TabPFN-v2, LoCalPFN and TabICL. That is evidence
to check training-prior sensitivity, not proof that posterior adjustment fixes arbitrary feature
drift or improves TabPFN-3.5. Label-shift corrections assume stable feature distributions within
each class; representative held-out calibration remains the starting point.

**Regression and forecasting.** For a numeric target, compare a constant or seasonal baseline,
regularised linear regression and a boosted regressor. Report MAE in business units, inspect errors
by segment, and use quantile/prediction intervals when uncertainty changes the decision. MAPE is
undefined at zero and unstable near zero; choose scaled or absolute errors deliberately.
[Forecasting: Principles and Practice](https://otexts.com/fpp3/accuracy.html) explains the
tradeoffs. For demand over time, compare seasonal-naive, exponential-smoothing or ARIMA baselines
with a lag-feature tree. Backtest at several rolling origins and the actual forecast horizon;
compute lags and rolling statistics using only past data. Start with the
[scikit-learn lagged-features example](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html).
Match feature updates to serving: rolling one-step forecasts may use observations received between
predictions, but a 24-hour forecast issued now cannot use tomorrow's realised demand in later lags.
For fixed-origin multi-step forecasts, recursively feed predicted values or train direct
horizon-specific models using only origin-available inputs. Report error by horizon, as in the
[forecast cross-validation example](https://otexts.com/fpp3/tscv.html). A forecast at today's price
does not identify demand at an untested price.

For a forecasting project, an optional challenger can be
[Chronos-2](https://arxiv.org/abs/2510.15821) or
[TimesFM 3](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/).
Their current interfaces support multivariate/covariate-informed forecasts; check the selected
checkpoint's frequency, context and horizon limits. Future covariates must actually be known at the
forecast origin: a scheduled holiday is different from tomorrow's realised weather or sales. Compare
business error and interval coverage at the same rolling origins, including holidays, stockouts and
regime changes; model-reported benchmark wins do not replace this check.
[TimesFM 3's downloadable weights have noncommercial/nonproduction terms](https://github.com/google-research/timesfm)
distinct from its code and hosted commercial offering. Keep seasonal/statistical baselines even when
a foundation model wins.

**Clustering and anomaly detection, when the question calls for them.** Use scaled K-means as a
segmentation baseline, PCA for exploring correlated features, and Isolation Forest as an anomaly
candidate. Check segment stability and business usefulness; a silhouette score alone does not
validate a customer strategy. Review anomalies with labelled examples and measure precision at the
review budget. These are optional extensions, not reasons to postpone your supervised project.

**Intervals that match your data.** Report a paired model comparison on the same test cases. For
repeated customers, bootstrap customers rather than individual rows; for serial dependence use
appropriate time blocks. Fold standard deviation is not a confidence interval for future deployment.
Freeze the comparison plan before the final test and report the sample size and dependence
assumptions.

Prediction intervals and confidence intervals answer different questions: uncertainty about an
individual future outcome versus uncertainty about a measured model comparison. As optional depth,
[split conformal prediction](https://arxiv.org/abs/2107.07511) wraps a model using separate
calibration residuals. Its usual guarantee is marginal coverage under exchangeability, not a
guarantee for each customer or arbitrary temporal drift. Report interval width and observed coverage
by horizon/cohort; neither quantile forecasts nor conformal intervals create causal evidence.

**From prediction to intervention.** Offer recommendation, pricing and retention ask what changes
when you take an action. Randomized treatment data or a defensible causal identification design is
needed for that claim. The data and model recipes are in
[Chapter 9](../09-business-machine-learning/README.md). A churn classifier, sales regressor or click
ranker can be a useful baseline without being evidence that a campaign increases profit.

**The maths, paid for as you go.** This is the most argued-about part of any AI roadmap, so here is
my reading of it, plainly.

The people who teach the hands-on courses are unusually consistent: fast.ai's own prerequisites page
says high-school maths is sufficient, Karpathy's course asks for "intro-level math (e.g. derivative,
gaussian)", and Parr and Howard tell readers to come to their matrix-calculus paper only **after**
they are already training networks. The failure I see most often is not under-preparing but
over-preparing: committing to a long linear algebra course before writing any model, and stalling
around month three with nothing built.

The minimum is small enough to name:

- **Linear algebra:** vectors, matrices and tensors; shapes and axes; matrix multiplication and why
  shapes must line up; transpose; dot product as similarity; broadcasting; a matrix as a
  transformation, and matrix products as composition. Eigenvectors, SVD, rank, norms and
  orthogonality can wait a few weeks.
- **Calculus:** the derivative as sensitivity; partial derivatives; the gradient; **the chain
  rule**, which carries more weight than anything else here; recognising a Jacobian; and gradient
  descent. Integrals, Hessians and hand-derived matrix calculus can wait, or may never come up.
- **Probability and statistics:** random variables, expectation and variance, independence,
  conditional probability, Bayes' rule, the Gaussian, Bernoulli and categorical distributions,
  likelihood and maximum likelihood, log-probabilities, and cross-entropy as a loss.

That is perhaps twenty to forty hours of honest study rather than a semester. Classical hypothesis
testing is deliberately down-weighted here; it matters a great deal for experimentation work, which
is covered in the [Data Scientist branch of Chapter 7](../07-specialisation/README.md).

The counter-argument deserves respect too. People who take the code-first route and never come back
to the maths tend to plateau at the point where they need to read a paper, debug an unusual loss, or
design an architecture. The bill arrives either way. Paying it here, once you have something
concrete to attach it to, tends to go better.

## Resources

All 43 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

Choose one main textbook or course and selected reference sections. Full-resource reading estimates
are alternatives, not a sum to fit inside 80 hours. Use the maths as needed and the buffer week for
one optional research comparison after the required project is complete.

The ones to begin with:

- [An Introduction to Statistical Learning (ISLP — Python edition)](https://www.statlearning.com/) —
  Gareth James, Daniela Witten, Trevor Hastie & Robert Tibshirani, with Jonathan Taylor. A free
  book; select sections within this chapter's 80 hours rather than requiring the full 60–90-hour
  reading estimate.
- [scikit-learn: Common Pitfalls and Recommended Practices](https://scikit-learn.org/stable/common_pitfalls.html)
  — scikit-learn core developers. Free documentation, 2–3 hours. Read it in week 7, before the
  leakage exercise.
- [Approaching (Almost) Any Machine Learning Problem](https://github.com/abhishekkrthakur/approachingalmost)
  — Abhishek Thakur. A free book, 20–30 hours.
- [Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/) — Christoph
  Molnar. A free book, 12–18 hours; the SHAP and permutation-importance chapters first.

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

Return a model version with predictions, validate feature names/types/units, and define behavior for
missing or unknown categories. Serve the tested preprocessing/model/calibration bundle; do not
retrain or fit a scaler inside a request. For Week 11, add the API and testing dependencies:

```bash
uv add "fastapi[standard]"
uv add --dev pytest httpx
uv run --locked pytest
```

Follow the official [request-body](https://fastapi.tiangolo.com/tutorial/body/) and
[testing](https://fastapi.tiangolo.com/tutorial/testing/) guides. Test a valid request against the
saved bundle's prediction in a fresh process, including the probability or numeric prediction, model
version and selected decision rule. Also test a malformed request and your specified handling of
missing/unknown inputs. Retain the training environment's dependency versions when loading a Python
model artifact; cross-version scikit-learn loading is unsupported, as the
[persistence guide](https://scikit-learn.org/stable/model_persistence.html) explains. Document
measured latency, memory and CPU fallback; follow Chapter 6 for production operations.

**The Week 7 leakage exercise:** deliberately fit preprocessing on the full dataset, record the
score, then move its fitting inside a `Pipeline` and repeat on the same split. Report the actual
difference, even if it is small; this particular leak does not guarantee a large score change.
Availability-time and group errors require separate data/split corrections, so do not claim that a
pipeline fixes every kind of leakage.

## Before you move on

- Given a dataset description, you can choose a split and a metric and defend both in a minute.
- You can explain the costs and derive your classification threshold or numeric action rule out
  loud.
- You can explain what SHAP computes, and one thing it does not tell you.
- You can call your endpoint, match a valid prediction to the saved bundle and show it rejecting a
  malformed request.
- You can explain which decisions your predictions support and which require an experiment.
- Your comparison states the actual split, model/checkpoint versions and compute constraints; the
  served bundle reproduces the tested predictions.
- You can explain how missing outcomes or altered class balance could change the reported score,
  probability scale and action threshold.

## A few things worth knowing

- **Start with ISL rather than ESL.** They share authors and the titles are similar, but _Elements
  of Statistical Learning_ is a graduate statistics text. People often start there, stop at chapter
  three, and conclude they are not a maths person. They usually are; it was the wrong book.
- **If you want Strang's linear algebra**, MIT 18.065 is the machine-learning-facing course. 18.06
  is excellent and spends its first month on material you will not use here.
- **Kaggle is a good gym and a weak portfolio.** Competitions give fast, honest feedback on
  validation design, which is genuinely valuable. They also remove problem framing, data sourcing
  and metric choice, which are three of the harder parts of the job.

---

[Previous: Data foundations](../02-data-foundations/README.md) &nbsp;·&nbsp;
[Next: Deep learning](../04-deep-learning/README.md)
