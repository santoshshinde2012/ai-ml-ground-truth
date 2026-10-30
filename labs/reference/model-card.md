# Model card — calibrated logistic reference

**Purpose:** a readable churn-risk prototype on fully synthetic no-contact data.
**Inputs:** available purchases, support contacts and purchase recency over 30 days.
**Training:** 300 independent customers. Feature means/scales fit on training only. L2-regularised logistic regression.
**Calibration/decision selection:** separate 150-customer cohort. Sigmoid calibration and a threshold chosen with FP cost 2 / FN cost 10.
**Final evaluation:** 150 later customers. Log loss 0.495936, Brier 0.169020, AUC 0.837216.
**Baseline:** constant training prevalence, not final-test prevalence.
**Intended use:** teaching and reproduction. Not for real customer contact, pricing or eligibility decisions.
**Known limits:** the simulator resembles the model. One small cohort is shifted in time. No empirical fairness, censoring or deployment validation.
**Fallback:** keep the baseline and defer when evidence is too weak. Risk does not measure treatment response.
**Owner:** the learner running the prototype. A real release needs a named accountable operator.
