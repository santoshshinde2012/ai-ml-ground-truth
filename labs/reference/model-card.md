# Model card — calibrated logistic reference

**Purpose:** a readable churn-risk prototype on fully synthetic no-contact data.
**Inputs:** available purchases, support contacts and purchase recency over 30 days.
**Training:** 300 independent customers; feature means/scales fit on training only; L2-regularized logistic regression.
**Calibration/decision selection:** separate 150-customer cohort; sigmoid calibration and a threshold selected under FP cost 2 / FN cost 10.
**Final evaluation:** 150 later customers; log loss 0.495936, Brier 0.169020, AUC 0.837216.
**Baseline:** constant training prevalence, not final-test prevalence.
**Intended use:** teaching and reproduction. No actual customer contact, pricing or eligibility decision.
**Known limits:** simulator resembles the model; a small temporally shifted cohort; no empirical fairness, censoring or deployment validation.
**Fallback:** preserve baseline and defer when evidence is insufficient. Risk does not measure treatment response.
**Owner:** the learner running the prototype; a real release requires a named accountable operator.
