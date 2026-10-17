# Stage 4 - ML Handoff Specification

## Purpose

This document defines the interface between Ashmit's Stage 4 data-engineering and equipment-health work and Sarthak's Stage 5 machine-learning work.

Stage 4 converts the raw synthetic sensor dataset into a validated, cleaned, feature-engineered dataset with engineering baseline indicators and an interpretable equipment health state.

The current dataset is synthetic prototype data. It is not real customer or plant data.

---

## Stage 4 Pipeline

The Stage 4 pipeline is:

Raw sensor data
-> validation
-> cleaning
-> engineering features
-> engineering baselines
-> baseline status
-> equipment health state
-> ML handoff dataset

The current end-to-end pipeline has been tested successfully.

Dataset size:

- 17,280 rows
- 26 final columns
- 5-minute sampling interval
- Synthetic data covering approximately 60 simulated days

---

## Raw Sensor / Process Inputs

The following variables represent sensor or process measurements:

- `temperature`
- `pressure`
- `flow_rate`
- `steam_flow`
- `delta_p`
- `production_load`
- `U`

These are available as candidate ML inputs.

Their use should still be evaluated according to the specific ML task.

---

## Engineering Features

Stage 4 generates the following backward-looking time-series features:

- `U_rolling_1h`
- `delta_p_rolling_1h`
- `U_rolling_6h`
- `delta_p_rolling_6h`
- `U_change_1h`
- `delta_p_change_1h`
- `U_change_6h`
- `delta_p_change_6h`
- `U_lag_1h`
- `delta_p_lag_1h`
- `U_lag_6h`
- `delta_p_lag_6h`

These features are calculated from current and historical observations.

They do not intentionally use future observations.

---

## Engineering Baseline Indicators

Stage 4 calculates statistical baselines for:

- `U`
- `delta_p`

The current prototype baseline uses:

`mean +/- 2 standard deviations`

The resulting status columns are:

- `U_baseline_status`
- `delta_p_baseline_status`

Possible status values:

- `LOW`
- `NORMAL`
- `HIGH`
- `UNKNOWN`

These are prototype engineering indicators and are not calibrated industrial operating limits.

---

## Equipment Health State

Stage 4 generates:

- `health_state`

Possible values:

- `NORMAL`
- `WATCH`
- `DEGRADED`
- `CRITICAL`

The current prototype logic combines:

- U baseline status
- Delta-P baseline status
- meaningful U deterioration over one hour
- meaningful Delta-P increase over one hour

Current prototype trend thresholds:

- U decrease greater than 5 units over one hour
- Delta-P increase greater than 0.05 over one hour

These thresholds are prototype values and must be calibrated using real equipment operating history before production use.

---

## Evaluation-Only Columns

The following columns are synthetic ground-truth or evaluation fields:

- `fouling_state`
- `cleaning_event`
- `sensor_anomaly`

These columns MUST NOT be used as ML input features.

They may be used for:

- model evaluation
- event analysis
- validation
- comparison against known synthetic conditions

Using them as model inputs would introduce target leakage or evaluation leakage.

---

## Timestamp

`timestamp` should be retained for:

- chronological ordering
- temporal train/validation/test splitting
- time-based evaluation
- plotting and analysis

It should not normally be passed directly to a model as a raw numeric feature without a deliberate modeling reason.

---

## Important Leakage Rules

Sarthak should use temporal rather than random splitting for time-series ML.

Future observations must not be used to construct features for earlier observations.

The following must remain excluded from model inputs:

- `fouling_state`
- `cleaning_event`
- `sensor_anomaly`

Stage 4's rolling and lag features are intended to use historical information only.

The current prototype baseline is calculated across the full synthetic dataset. This is acceptable for prototype exploration but would introduce future-information leakage if directly used as a real-time production baseline.

For production use, baselines should be established from an appropriate historical/reference operating period.

---

## Recommended ML Input Starting Point

A candidate starting feature set is:

### Process variables

- `temperature`
- `pressure`
- `flow_rate`
- `steam_flow`
- `delta_p`
- `production_load`
- `U`

### Engineering features

- `U_rolling_1h`
- `delta_p_rolling_1h`
- `U_rolling_6h`
- `delta_p_rolling_6h`
- `U_change_1h`
- `delta_p_change_1h`
- `U_change_6h`
- `delta_p_change_6h`
- `U_lag_1h`
- `delta_p_lag_1h`
- `U_lag_6h`
- `delta_p_lag_6h`

### Engineering status indicators

- `U_baseline_status`
- `delta_p_baseline_status`

`health_state` may be used as an engineering-derived feature for appropriate downstream tasks, but Sarthak should explicitly decide whether it belongs in each model.

---

## Current Stage 4 Validation

The following tests have passed:

### Health-state unit test

`python -m notebooks.test_health_state`

Result:

- All health-state tests passed.

### Health-state dataset integration test

`python -m notebooks.test_health_state_dataset`

Result:

- All basic assertions passed.

### Stage 4 end-to-end pipeline test

`python -m notebooks.test_stage4_pipeline`

Result:

- All Stage 4 assertions passed.
- Stage 4 pipeline test passed.

---

## Current Prototype Health Distribution

On the current synthetic dataset:

- NORMAL: 11,563 rows (66.92%)
- WATCH: 5,297 rows (30.65%)
- DEGRADED: 420 rows (2.43%)
- CRITICAL: 0 rows (0%)

This distribution is descriptive of the current synthetic dataset and health-rule prototype.

It is not a model accuracy metric and should not be interpreted as real equipment performance.

---

## Handoff to Stage 5

Sarthak can now build the ML layer on top of the Stage 4 pipeline.

Potential Stage 5 tasks include:

- anomaly detection
- fouling-risk classification
- forecasting
- model evaluation
- temporal validation
- explainability

The ML layer should preserve the separation between:

1. model inputs
2. predicted outputs
3. evaluation-only ground truth

Stage 4 is responsible for producing reliable engineering inputs and interpretable equipment-health indicators.

Stage 5 is responsible for machine-learning analytics and predictive modeling.
