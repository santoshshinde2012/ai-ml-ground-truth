# Data card — synthetic retail/subscription lab

- **Origin and permission:** made by this repository's MIT-licensed code. No real people or scraped data.
- **Purpose:** practise point-in-time features, separate calibration, fair test evaluation and decisions under limits.
- **Grain:** 600 unique modelling customers, plus a separate 800-customer randomised experiment.
- **Clocks:** UTC, 30-day lookback. Only events with `event_time < as_of` and `available_at <= as_of`.
- **Outcome:** simulated 30-day churn with no contact, fully observed at 33 days. Do not zero-fill unknown coverage.
- **Partitions:** fixed train/calibration/test cohorts in time order, with mature-label gaps. Do not shuffle them for a better score.
- **Known artifacts:** each customer has one deliberately late and one future purchase. Historical features must exclude both.
- **Documents:** three fictional policy documents for a small retrieval and extraction exercise.
- **Manifest:** SHA-256 for every generated input. Evaluation requires exactly that file list, checks every hash and rebuilds every feature.
- **Experiment checks:** one outcome per assignment, no zero-filled outcomes, and a sample-ratio check before any lift is read.
- **Limitations:** deliberately simple independent units, a known response mechanism, no real consent or protected-group representation.
- **What you can conclude:** the code works on this simulator. Real-world quality and causal impact remain unknown.
