# Rinheat AI — Stage 5 Analytics + ML Report

**Dataset:** synthetic prototype sensor data; not real plant data.

- Stage 4 handoff rows: 17,280
- Stage 4 handoff columns: 26
- Predictor count: 21
- Fouling thresholds learned from training data: 0.375442201754, 0.583942114062

## Fouling Risk Classification

- Test accuracy: 0.9772
- Test balanced accuracy: 0.9677
- Test macro F1: 0.9728

## Sensor Anomaly Detection

- Test precision: 0.0000
- Test recall: 0.0000
- Test F1: 0.0000
- Test ROC-AUC: 0.7118659914296845

## Six-Hour-Ahead U Forecasting

### Random Forest

- Test MAE: 15.7789
- Test RMSE: 29.4775
- Test R²: 0.37757612121675166

### Persistence baseline

- Test MAE: 14.9422
- Test RMSE: 24.0329
- Test R²: 0.5862687645235543

## Leakage safeguards

- Chronological train/validation/test splits were used.
- Fouling thresholds were estimated from training-period values only.
- `fouling_state`, `cleaning_event`, `sensor_anomaly`, `health_state`, and `timestamp` were not predictors.
- Stage 4 baseline-status columns use the prototype Stage 4 baseline logic; full-history baselines require redesign before real-time production use.
- All source data are synthetic. Metrics are prototype evaluation results, not evidence of real-world plant performance.
