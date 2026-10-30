# Resources — Chapter 9: Business machine learning

[Chapter](../README.md) &nbsp;·&nbsp; [Offers](../offer-recommendation.md) &nbsp;·&nbsp;
[Prices](../price-recommendation.md) &nbsp;·&nbsp; [Churn](../churn.md)

**Sources checked for the October 2026 revision.** The recommendations combine these sources. Each
paper or document shows a capability or result under stated assumptions, not a universally best
model. Read each source alongside its task instead of working through the list. Each guide explains
the assumptions behind the methods it recommends.

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

_Research paper · published in PNAS, 2019 · preprint linked._ Read the S/T/X learner setup and the
assumptions behind each learner's advantages. It supports comparing simple treatment-effect learners
first. It names no universal winner and does not validate treatment effects
in unrandomised CRM data.

### [EconML — Doubly robust learning](https://www.pywhy.org/EconML/spec/estimation/dr.html)

_Official implementation documentation._ Use it for categorical or multi-arm treatment estimation,
nuisance models and cross-fitting. You still need identification and overlap. Choose an estimator
and inference method suited to the treatment and data. Use known randomisation probabilities where
supported.

### [Ascarza — Retention Futility: Targeting High-Risk Customers Might Be Ineffective](https://journals.sagepub.com/doi/10.1509/jmr.16.0163)

_Journal of Marketing Research, 2018._ The field experiments separate churn risk from retention
response. The tested campaigns and populations are specific. The lesson is to measure who responds,
instead of assuming their treatment effects transfer to your company.

### [TensorFlow Recommenders — Basic retrieval](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

_Official tutorial._ A practical two-tower candidate-retrieval example. Use when catalogue scale
and interaction history justify embeddings. Retrieving movie preferences is a different goal from
deciding whether a paid incentive creates incremental profit.

The
[retrieval task API](https://www.tensorflow.org/recommenders/api_docs/python/tfrs/tasks/Retrieval)
documents accidental-hit removal and negative-sampling correction. The
[side-feature tutorial](https://www.tensorflow.org/recommenders/examples/featurization) feeds
metadata into the trained tower representations. Keep training-sampler probabilities separate from
campaign assignment probabilities, and evaluate new-item retrieval explicitly.

### [Google — Deep Neural Networks for YouTube Recommendations](https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/)

_Covington, Adams and Sargin, 2016._ Note how it separates candidate generation from ranking.
The industrial architecture is a reference for scale, not a required starting stack for a small
customer-offer table.

### Recent research to test after the baseline

These are optional comparisons, outside the 40-hour single-case project. Read the methods, how the
splits were built and the limitations before reproducing a leaderboard result.

| Paper                                                                                         | Status and date                             | Useful question                                                                | Boundary                                                                         |
| --------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| [Athey and Wager — Policy Learning with Observational Data](https://arxiv.org/abs/1702.02896) | Econometrica, 2021; revised preprint linked | Can a constrained binary decision policy improve held-out value?               | Requires identification and nuisance estimates; not a multi-arm budget solver    |
| [CausalPFN](https://arxiv.org/abs/2506.07918)                                                 | NeurIPS 2025; arXiv revised 27 October 2025 | Does a pretrained causal prior help a supported binary effect-estimation task? | Released implementation is binary; check unconfoundedness, overlap and prior fit |
| [UpliftBench](https://arxiv.org/abs/2608.00915)                                               | August 2026 preprint                        | Do ranking and cost-based policy selection agree?                              | Dataset-specific evidence; some threshold comparisons reuse evaluation data      |
| [UNIQUE](https://arxiv.org/abs/2609.23718)                                                    | September 2026 preprint                     | Does unified generative retrieval/ranking justify its serving complexity?      | Feed-engagement results do not validate paid-incentive profit                    |

### [CIPS/CDR — Ranking evaluation from deterministic slates](https://arxiv.org/abs/2603.21485)

_ICLR 2026 conference paper · March 2026 arXiv version · optional ranking research._ See the
[conference publication](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c6af791af7ef0f3e02bccef011211ca5-Abstract-Conference.html).
Study click-wise support and slate-independent
expected post-click reward before using stochastic clicks to evaluate a different ranking. Estimated
click ratios determine the bias. The paper's CDR does not get the usual doubly robust guarantee from
an accurate reward model. These assumptions do not identify incentive treatment effects.

## Pricing, elasticity and inventory

### [Fisher, Gallino and Li — Competition-Based Dynamic Pricing in Online Retailing](https://pubsonline.informs.org/doi/10.1287/mnsc.2017.2753)

_Management Science, 2018 · online publication 2017._ The method and field experiments deal with
historical-price endogeneity and randomised price variation. Read it for the design needed to link
response estimation to a price decision, instead of copying another retailer's elasticity
coefficient.

### [statsmodels — Generalized linear models](https://www.statsmodels.org/stable/glm.html)

_Official docs._ Build an inspectable demand or count baseline with a log link, a suitable family
and exposure offsets. Log price is a predictor, and the count outcome can include zeros. A
fitted price coefficient is causal only when the research design identifies it.

### [scikit-learn — Poisson regression and non-normal loss](https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html)

_Official worked example._ Learn count objectives, exposure weighting and diagnostics. The example
is an insurance application, so adapt the opportunity definition and economics for retail demand.

### [Conlon and Mortimer — Demand Estimation Under Incomplete Product Availability](https://www.nber.org/papers/w14315)

_Research working paper._ Shows why availability and substitution matter in demand estimation.
Sales recorded during stockouts are not automatically unconstrained demand. Whether you can recover
lost demand depends on the data and identification assumptions.

### [EconML — Double machine learning](https://www.pywhy.org/EconML/spec/estimation/dml.html) and [instrumental variables](https://www.pywhy.org/EconML/spec/estimation_iv.html)

_Official method documentation._ Optional depth after you write the identification design. DML needs
suitable observed confounders and model assumptions. IV needs a relevant instrument, exclusion and
its other identifying assumptions. Neither makes up for missing price exposure or an unexplained
pricing intervention.

### [Bojinov, Simchi-Levi and Zhao — Design and Analysis of Switchback Experiments](https://arxiv.org/abs/2009.00148)

_Research paper._ Optional depth for when users share inventory or a market, so randomising
individuals creates interference. Switchback periods, carryover and inference need an explicit
design. Alternating a price each day is not enough on its own.

### [Causal Foundation Models with Continuous Treatments — CCPFN](https://arxiv.org/abs/2605.15133)

_May 2026 preprint, revised July._ Optional continuous-treatment challenger. Compare supported
price-response estimates with identified classical baselines. A synthetic prior does not remove
confounding or justify extrapolating to unobserved prices.

### [Zhang, Wang and Luo — Optimal Nonparametric Dynamic Pricing with Censored Demand and Adversarial Inventory](https://arxiv.org/abs/2609.32949)

_September 2026 preprint._ Optional inventory-aware online-learning depth. Study the stationary
demand assumptions, demand-tail sharing and simulated comparisons. The learner observes inventory
but does not jointly optimise replenishment. Its revenue guarantees need care if the reward becomes
contribution.

### [Zheng and Jin — Prediction Sets for Counterfactual Decisions](https://arxiv.org/abs/2607.02206)

_Preprint submitted 2 July 2026._ Optional uncertainty-and-decision depth. Coverage for each
action separately does not automatically cover the outcome after a policy selects the action. Study
the identified, supported potential-outcome setting and the separate training, policy-learning and
calibration splits. The experiments include a held-out analysis of a randomised email dataset, not a
new live pricing trial. It is a reason to check uncertainty for the final policy, not a required
replacement for the guide's baselines.

## Churn timing and evaluation

### [scikit-survival — Introduction](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)

_Official docs._ Learn event indicators, follow-up and right censoring before turning a customer
history into a survival dataset. Avoid turning tenure into a made-up time-to-churn label.

### [scikit-survival — Evaluating survival models](https://scikit-survival.readthedocs.io/en/stable/user_guide/evaluating-survival-models.html)

_Official docs._ Use IPCW concordance, time-dependent AUC and Brier/IBS at supported horizons.
Censoring assumptions and enough reference follow-up matter. Risk scores and survival probabilities
suit different metrics.

### [Competing risks and survival calibration](https://scikit-survival.readthedocs.io/en/stable/user_guide/competing-risks.html)

_Official documentation._ Keep mutually exclusive event types and estimate cause-specific cumulative
incidence. Censoring another cause and using `1 − Kaplan–Meier` answers a different question.
[Aalen–Johansen](https://lifelines.readthedocs.io/en/latest/fitters/univariate/AalenJohansenFitter.html)
gives a nonparametric baseline. For fitted lifelines regression models, inspect
[out-of-sample censor-aware horizon calibration](https://lifelines.readthedocs.io/en/latest/lifelines.calibration.html).
That diagnostic does not accept every survival estimator.

### [scikit-survival — Random survival forests](https://scikit-survival.readthedocs.io/en/stable/user_guide/random-survival-forest.html) and [survival boosting](https://scikit-survival.readthedocs.io/en/stable/user_guide/boosting.html)

_Official docs._ Compare model families after a Cox baseline. Cox-loss boosting can fit nonlinear
feature effects while keeping a proportional-hazards structure. Name the loss and assumptions.
Calling something a tree does not remove survival assumptions.

### [SurvPFN — Towards Foundation Models for Survival Predictions](https://arxiv.org/abs/2606.04564)

_June 2026 paper · accepted to the ICML Foundation Models for Structured Data workshop._ Optional
small-data censored-survival comparison. The authors report Cox as best and no significant pairwise
model differences. Test future-cohort calibration and censoring assumptions. This is not a
longitudinal retention-policy experiment.

## Policy evaluation and operation

### [Dudík, Langford and Li — Doubly Robust Policy Evaluation and Learning](https://arxiv.org/abs/1103.4601)

_Research paper, 2011._ Read it for evaluating policies from logged actions and propensities. It
motivates IPS and DR estimators. It cannot make unsupported actions evaluable or remove hidden
confounding from arbitrary business histories.

### [Sequential and adaptive policy evaluation](https://proceedings.mlr.press/v48/jiang16.html)

_Optional method depth._ Jiang and Li (ICML 2016) separate sequential from one-step estimators.
Record histories and transitions, and check trajectory support.
[Hadad et al. (PNAS, 2021; author preprint)](https://arxiv.org/abs/1911.02768) address inference
under adaptive assignment. Logging action probabilities does not by itself justify ordinary
independent-sample intervals.

### [Lee et al. — When Offline Evaluation Misleads](https://arxiv.org/abs/2608.11560)

_August 2026 paper · arXiv reports acceptance at a KDD customer-journey workshop._ Optional
diagnostic depth for delayed rewards. Keep alignment with business action effects apart from how easy
a policy is to learn. Individual-level proxy correlation answers a different question. The
illustrative replay uses one path, delay is budgeted instead of modelled, and later deployment has
a null overall result with exploratory subgroup findings. Check cold start, logging support and
mature outcomes. This is not a universal inference recipe or evidence of profit gains for you.

### [Vowpal Wabbit — Contextual bandits](https://vowpalwabbit.org/tutorials/contextual_bandits.html)

_Official tutorial._ Optional, once a fixed policy, action-probability logs, a reward definition and
an experiment control work. Delayed business outcomes and adaptive evaluation need more than the
tutorial's immediate-reward example.

[Lancewicki et al. (ICML, 2021)](https://proceedings.mlr.press/v139/lancewicki21a.html) separate
reward-independent from reward-dependent delays. Their theoretical setting helps you check update
assumptions, but is not evidence of settled retail-profit gains. The pricing guide starts with
scheduled updates on mature cohorts.

### [Microsoft — Diagnosing sample-ratio mismatch](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)

_Practitioner research._ Use when logged experiment counts differ from the intended design.
Diagnose assignment, execution, filtering and join issues before interpreting the outcome.

### [MLflow — Model registry workflows](https://mlflow.org/docs/latest/ml/model-registry/workflow/)

_Official docs._ Reference for versions, aliases and release management once a local artifact
manifest is not enough. Version the feature contract, calibration and action policy as well
as the fitted model.

## Practice datasets: what each can prove

| Source                                                                                                                             | Good exercise                                                              | Limit                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| [Criteo corrected uplift dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/)                                      | Binary randomised-treatment/uplift methods                                 | Use the corrected release and declare sampling assumptions; no original propensity logs, coupon costs or multi-arm profit evidence |
| [GroupLens MovieLens](https://grouplens.org/datasets/movielens/)                                                                   | Retrieval, preference ranking and cold-start evaluation                    | Ratings are not randomised incentive assignments                                                                                   |
| [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)                                                         | Transaction cleaning, demand summaries and inactivity snapshots            | Purchase rows omit nonbuyer exposure, full availability and campaign assignments; no causal price/offer effect by default          |
| [IBM Telco sample documentation](https://community.ibm.com/community/user/blogs/steven-macko/2019/07/11/telco-customer-churn-1113) | Classification and leakage audit on a fictional-company sample             | Snapshot variants cannot establish a longitudinal backtest; exclude supplied churn scores/reasons and hindsight fields             |
| [UCI Iranian Churn](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset)                                                 | Small customer-table baseline comparison                                   | Do not invent scoring timestamps, event dates or retention treatment labels                                                        |
| Explicit synthetic generator                                                                                                       | Decision-time replay, known causal effects, uncertainty and failure drills | Validates the specified simulator, not a real business effect                                                                      |

Keep dataset version, checksum, licence, dictionary and limitations with your experiment. The
guides list the extra fields and evidence an operational business project needs.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
