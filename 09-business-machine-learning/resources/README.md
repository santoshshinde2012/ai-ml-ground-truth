# Resources — Chapter 9: Business machine learning

[Chapter](../README.md) &nbsp;·&nbsp; [Offers](../offer-recommendation.md) &nbsp;·&nbsp;
[Prices](../price-recommendation.md) &nbsp;·&nbsp; [Churn](../churn.md)

**Sources checked for the October 2026 revision.** The recommendations synthesize the sources;
papers and documentation establish capabilities or results under particular assumptions, not a
universally best model. Read the source next to the task you are doing, rather than completing this
list end to end. Each guide explains the assumptions behind the methods it recommends.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp;
[Offer recommendation and retention effects](#offer-recommendation-and-retention-effects)
&nbsp;·&nbsp; [Pricing, elasticity and inventory](#pricing-elasticity-and-inventory) &nbsp;·&nbsp;
[Churn timing and evaluation](#churn-timing-and-evaluation) &nbsp;·&nbsp;
[Policy evaluation and operation](#policy-evaluation-and-operation) &nbsp;·&nbsp;
[Practice datasets: what each can prove](#practice-datasets-what-each-can-prove)

## Start here

| Resource                                                                                                                                              | Type                  | Use it for                                              | Keep in mind                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [CatBoost categorical features](https://catboost.ai/docs/en/features/categorical-features)                                                            | Official docs         | Mixed categorical customer/offer baselines              | Its feature handling does not repair temporal leakage or confounding             |
| [LightGBM advanced topics](https://lightgbm.readthedocs.io/en/stable/Advanced-Topics.html)                                                            | Official docs         | Categorical handling, LambdaRank and position bias      | A ranker needs meaningful query groups and labels                                |
| [Probability calibration](https://scikit-learn.org/stable/modules/calibration.html)                                                                   | Official docs         | Reliability plots and independent calibration           | Proper scoring losses also reflect discrimination; refitting changes the mapping |
| [Feast point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)                                                      | Official docs         | Replaying historical features                           | Verify availability timestamps and historical corrections in your implementation |
| [Microsoft pre-experiment practices](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/) | Practitioner research | Hypothesis, assignment, metrics and power before launch | Your assignment unit and outcome horizon determine the design                    |

## Offer recommendation and retention effects

### [Künzel et al. — Meta-learners for estimating heterogeneous treatment effects](https://arxiv.org/abs/1706.03461)

_Research paper · published in PNAS, 2019; preprint linked._ Read the S/T/X learner setup and the
assumptions behind their different advantages. This supports comparing simple treatment-effect
learners before escalating. It does not establish a universal winner or validate treatment effects
in unrandomized CRM data.

### [EconML — Doubly robust learning](https://www.pywhy.org/EconML/spec/estimation/dr.html)

_Official implementation documentation._ Use for categorical/multi-arm treatment estimation,
nuisance models and cross-fitting. Identification and overlap remain necessary. Choose an
estimator/inference path suited to the treatment and data structure; known randomization
probabilities should be used where the implementation supports them.

### [Ascarza — Retention Futility: Targeting High-Risk Customers Might Be Ineffective](https://journals.sagepub.com/doi/10.1509/jmr.16.0163)

_Journal of Marketing Research, 2018._ The field experiments motivate the separation of churn risk
from retention response. The tested campaigns and populations are specific: the lesson is to measure
responsiveness, not to assume their treatment effects transfer to your company.

### [TensorFlow Recommenders — Basic retrieval](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

_Official tutorial._ A practical two-tower candidate-retrieval example. Use when catalog scale and
interaction history justify embeddings. Movie preference retrieval is a different objective from
deciding whether a paid incentive creates incremental profit.

The
[retrieval task API](https://www.tensorflow.org/recommenders/api_docs/python/tfrs/tasks/Retrieval)
documents accidental-hit removal and negative-sampling correction. The
[side-feature tutorial](https://www.tensorflow.org/recommenders/examples/featurization) connects
metadata to trained tower representations. Keep training-sampler probabilities separate from
campaign assignment probabilities, and evaluate new-item retrieval explicitly.

### [Google — Deep Neural Networks for YouTube Recommendations](https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/)

_Covington, Adams and Sargin, 2016._ Read the separation of candidate generation and ranking. The
industrial architecture is a reference for scale, not a required starting stack for a small
customer-offer table.

### Recent research to test after the baseline

These are optional comparisons, not additional requirements for the 40-hour single-case project.
Read the methods, split construction and limitations before reproducing a leaderboard result.

| Paper                                                                                         | Status and date                             | Useful question                                                                | Boundary                                                                         |
| --------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| [Athey and Wager — Policy Learning with Observational Data](https://arxiv.org/abs/1702.02896) | Econometrica, 2021; revised preprint linked | Can a constrained binary decision policy improve held-out value?               | Requires identification and nuisance estimates; not a multi-arm budget solver    |
| [CausalPFN](https://arxiv.org/abs/2506.07918)                                                 | NeurIPS 2025; arXiv revised October         | Does a pretrained causal prior help a supported binary effect-estimation task? | Released implementation is binary; check unconfoundedness, overlap and prior fit |
| [UpliftBench](https://arxiv.org/abs/2608.00915)                                               | August 2026 preprint                        | Do ranking and cost-based policy selection agree?                              | Dataset-specific evidence; some threshold comparisons reuse evaluation data      |
| [UNIQUE](https://arxiv.org/abs/2609.23718)                                                    | September 2026 preprint                     | Does unified generative retrieval/ranking justify its serving complexity?      | Feed-engagement results do not validate paid-incentive profit                    |

### [CIPS/CDR — Ranking evaluation from deterministic slates](https://arxiv.org/abs/2603.21485)

_March 2026 preprint; optional ranking research._ Study click-wise support and slate-independent
expected post-click reward before using stochastic clicks to evaluate a different ranking. Estimated
click ratios determine bias; the paper's CDR does not gain the usual doubly robust guarantee from an
accurate reward model. These assumptions do not identify incentive treatment effects.

## Pricing, elasticity and inventory

### [Fisher, Gallino and Li — Competition-Based Dynamic Pricing in Online Retailing](https://pubsonline.informs.org/doi/10.1287/mnsc.2017.2753)

_Management Science, 2018; online publication 2017._ The methodology and field experiments address
historical-price endogeneity and randomized price variation. Read it for the design requirements
connecting response estimation to a price decision, rather than copying an elasticity coefficient
from another retailer.

### [statsmodels — Generalized linear models](https://www.statsmodels.org/stable/glm.html)

_Official docs._ Use to build an inspectable demand/count baseline with a log link, appropriate
family and exposure offsets. Log price is a predictor; the count outcome can include zeros. A fitted
price coefficient is causal only when the research design identifies it.

### [scikit-learn — Poisson regression and non-normal loss](https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html)

_Official worked example._ Learn count objectives, exposure weighting and diagnostics. The example
is an insurance application, so adapt the opportunity definition and economics for retail demand.

### [Conlon and Mortimer — Demand Estimation Under Incomplete Product Availability](https://www.nber.org/papers/w14315)

_Research working paper._ Use to understand why availability and substitution matter in demand
estimation. Recorded sales during stockouts are not automatically unconstrained demand; whether lost
demand can be recovered depends on the data and identification assumptions.

### [EconML — Double machine learning](https://www.pywhy.org/EconML/spec/estimation/dml.html) and [instrumental variables](https://www.pywhy.org/EconML/spec/estimation_iv.html)

_Official method documentation._ Optional depth after the identification design is written. DML
needs appropriate observed confounders and model assumptions; IV needs a relevant instrument,
exclusion and its other identifying assumptions. Neither is a substitute for missing price exposure
or an unexplained pricing intervention.

### [Bojinov, Simchi-Levi and Zhao — Design and Analysis of Switchback Experiments](https://arxiv.org/abs/2009.00148)

_Research paper._ Optional depth for settings where users share inventory or a market and individual
randomization creates interference. Switchback periods, carryover and inference require an explicit
design; alternating a price each day is not sufficient by itself.

### [Causal Foundation Models with Continuous Treatments — CCPFN](https://arxiv.org/abs/2605.15133)

_May 2026 preprint, revised July._ Optional continuous-treatment challenger. Compare supported
price-response estimation against identified classical baselines; synthetic-prior learning does not
remove confounding or justify extrapolation to unobserved prices.

### [Zhang, Wang and Luo — Optimal Nonparametric Dynamic Pricing with Censored Demand and Adversarial Inventory](https://arxiv.org/abs/2609.32949)

_September 2026 preprint._ Optional inventory-aware online-learning depth. Study the stationary
demand assumptions, demand-tail sharing and simulated comparisons. The learner observes inventory;
it does not jointly optimize replenishment, and revenue guarantees require care when changing the
reward to contribution.

### [Zheng and Jin — Prediction Sets for Counterfactual Decisions](https://arxiv.org/abs/2607.02206)

_Preprint submitted 2 July 2026._ Optional uncertainty-and-decision depth. Separate coverage for
each action does not automatically cover the outcome after a policy selects the action. Study the
identified, supported potential-outcome setting and separate training, policy-learning and
calibration splits. The experiments include a held-out analysis of a randomized email dataset, not a
new live pricing trial. This motivates checking uncertainty for the final policy; it does not make
the proposed procedure a required replacement for the guide's baselines.

## Churn timing and evaluation

### [scikit-survival — Introduction](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)

_Official docs._ Learn event indicators, follow-up and right censoring before turning a customer
history into a survival dataset. Tenure is not a manufactured time-to-churn label.

### [scikit-survival — Evaluating survival models](https://scikit-survival.readthedocs.io/en/stable/user_guide/evaluating-survival-models.html)

_Official docs._ Use IPCW concordance, time-dependent AUC and Brier/IBS at supported horizons.
Censoring assumptions and adequate reference follow-up matter; risk scores and survival
probabilities serve different metrics.

### [Competing risks and survival calibration](https://scikit-survival.readthedocs.io/en/stable/user_guide/competing-risks.html)

_Official documentation._ Preserve mutually exclusive event types and estimate cause-specific
cumulative incidence; censoring another cause and using `1 − Kaplan–Meier` answers a different
question.
[Aalen–Johansen](https://lifelines.readthedocs.io/en/latest/fitters/univariate/AalenJohansenFitter.html)
provides a nonparametric baseline. For fitted lifelines regression models, inspect
[out-of-sample censor-aware horizon calibration](https://lifelines.readthedocs.io/en/latest/lifelines.calibration.html);
that diagnostic does not accept every survival estimator.

### [scikit-survival — Random survival forests](https://scikit-survival.readthedocs.io/en/stable/user_guide/random-survival-forest.html) and [survival boosting](https://scikit-survival.readthedocs.io/en/stable/user_guide/boosting.html)

_Official docs._ Compare model families after a Cox baseline. Cox-loss boosting can fit nonlinear
feature effects while retaining a proportional-hazards structure. Name the loss and assumptions;
calling something a tree does not remove survival assumptions.

### [SurvPFN — Towards Foundation Models for Survival Predictions](https://arxiv.org/abs/2606.04564)

_June 2026 paper; accepted to the ICML Foundation Models for Structured Data workshop._ Optional
small-data censored-survival comparison. The authors report Cox as best and no significant pairwise
model differences. Test future-cohort calibration and censoring assumptions; this is not a
longitudinal retention-policy experiment.

## Policy evaluation and operation

### [Dudík, Langford and Li — Doubly Robust Policy Evaluation and Learning](https://arxiv.org/abs/1103.4601)

_Research paper, 2011._ Read for evaluating policies with logged actions and propensities. It
motivates IPS/DR estimators; it does not make unsupported actions evaluable or eliminate hidden
confounding in arbitrary business histories.

### [Sequential and adaptive policy evaluation](https://proceedings.mlr.press/v48/jiang16.html)

_Optional method depth._ Jiang and Li (ICML 2016) distinguish sequential from one-step estimators;
record histories/transitions and check trajectory support.
[Hadad et al. (PNAS, 2021; author preprint)](https://arxiv.org/abs/1911.02768) address inference
under adaptive assignment. Ordinary independent-sample intervals are not justified simply because
action probabilities were logged.

### [Lee et al. — When Offline Evaluation Misleads](https://arxiv.org/abs/2608.11560)

_August 2026 paper; arXiv reports acceptance at a KDD customer-journey workshop._ Optional
diagnostic depth for delayed rewards. Separate alignment with business action effects from ease of
learning a policy: individual-level proxy correlation answers a different question. The illustrative
replay uses one path, delay is budgeted rather than modeled, and later deployment has a null overall
result with exploratory subgroup findings. Check cold start, logging support and mature outcomes;
this is not a universal inference recipe or evidence of profit gains for your campaigns.

### [Vowpal Wabbit — Contextual bandits](https://vowpalwabbit.org/tutorials/contextual_bandits.html)

_Official tutorial._ Optional after a fixed policy, action-probability logs, reward definition and
an experiment control work. Delayed business outcomes and adaptive evaluation need more than the
immediate-reward tutorial example.

[Lancewicki et al. (ICML, 2021)](https://proceedings.mlr.press/v139/lancewicki21a.html) distinguish
reward-independent from reward-dependent delays. Their theoretical setting is useful for checking
update assumptions, not evidence of settled retail-profit gains. The pricing guide starts with
scheduled updates on mature cohorts.

### [Microsoft — Diagnosing sample-ratio mismatch](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)

_Practitioner research._ Use when logged experiment counts differ from the intended design. Diagnose
assignment, execution, filtering and join issues before interpreting the outcome.

### [MLflow — Model registry workflows](https://mlflow.org/docs/latest/ml/model-registry/workflow/)

_Official docs._ Reference for versions, aliases and release management after a local artifact
manifest becomes insufficient. Version the feature contract, calibration and action policy as well
as the fitted model.

## Practice datasets: what each can prove

| Source                                                                                                                             | Good exercise                                                              | Limit                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| [Criteo corrected uplift dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/)                                      | Binary randomized-treatment/uplift methods                                 | Use the corrected release and declare sampling assumptions; no original propensity logs, coupon costs or multi-arm profit evidence |
| [GroupLens MovieLens](https://grouplens.org/datasets/movielens/)                                                                   | Retrieval, preference ranking and cold-start evaluation                    | Ratings are not randomized incentive assignments                                                                                   |
| [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)                                                         | Transaction cleaning, demand summaries and inactivity snapshots            | Purchase rows omit nonbuyer exposure, full availability and campaign assignments; no causal price/offer effect by default          |
| [IBM Telco sample documentation](https://community.ibm.com/community/user/blogs/steven-macko/2019/07/11/telco-customer-churn-1113) | Classification and leakage audit on a fictional-company sample             | Snapshot variants cannot establish a longitudinal backtest; exclude supplied churn scores/reasons and hindsight fields             |
| [UCI Iranian Churn](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset)                                                 | Small customer-table baseline comparison                                   | Do not invent scoring timestamps, event dates or retention treatment labels                                                        |
| Explicit synthetic generator                                                                                                       | Decision-time replay, known causal effects, uncertainty and failure drills | Validates the specified simulator, not a real business effect                                                                      |

Keep dataset version/checksum, licence, dictionary and limitations with your experiment. The guides
specify what extra fields and evidence an operational business project needs.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
