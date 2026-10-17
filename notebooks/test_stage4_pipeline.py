from ml.preprocessing.loader import load_sensor_data
from ml.preprocessing.validator import validate_dataframe
from ml.preprocessing.cleaner import clean_sensor_data
from ml.preprocessing.features import add_engineering_features
from ml.engineering.baseline import (
    calculate_baseline,
    add_baseline_status,
)
from ml.engineering.health_state import add_health_state


print("=== STAGE 4 END-TO-END PIPELINE TEST ===")


print("\n=== 1. LOAD ===")

df = load_sensor_data()

print(f"Rows loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")


print("\n=== 2. VALIDATE ===")

validation = validate_dataframe(df)

print(f"Validation passed: {validation['valid']}")

assert validation["valid"] is True


print("\n=== 3. CLEAN ===")

df = clean_sensor_data(df)

print(f"Rows after cleaning: {len(df)}")

assert len(df) == 17280


print("\n=== 4. ENGINEERING FEATURES ===")

df = add_engineering_features(df)

print(f"Columns after feature generation: {len(df.columns)}")

required_features = [
    "U_rolling_1h",
    "delta_p_rolling_1h",
    "U_rolling_6h",
    "delta_p_rolling_6h",
    "U_change_1h",
    "delta_p_change_1h",
    "U_change_6h",
    "delta_p_change_6h",
    "U_lag_1h",
    "delta_p_lag_1h",
    "U_lag_6h",
    "delta_p_lag_6h",
]

for column in required_features:
    assert column in df.columns


print("Required engineering features present.")


print("\n=== 5. ENGINEERING BASELINES ===")

u_baseline = calculate_baseline(df, "U")
delta_p_baseline = calculate_baseline(df, "delta_p")

print(
    f"U baseline: "
    f"{u_baseline['lower_bound']:.3f} "
    f"to "
    f"{u_baseline['upper_bound']:.3f}"
)

print(
    f"Delta-P baseline: "
    f"{delta_p_baseline['lower_bound']:.3f} "
    f"to "
    f"{delta_p_baseline['upper_bound']:.3f}"
)


print("\n=== 6. BASELINE STATUS ===")

df = add_baseline_status(
    df,
    "U",
    u_baseline,
)

df = add_baseline_status(
    df,
    "delta_p",
    delta_p_baseline,
)

assert "U_baseline_status" in df.columns
assert "delta_p_baseline_status" in df.columns

print("Baseline status columns present.")


print("\n=== 7. EQUIPMENT HEALTH STATE ===")

df = add_health_state(df)

assert "health_state" in df.columns

valid_states = {
    "NORMAL",
    "WATCH",
    "DEGRADED",
    "CRITICAL",
}

assert set(df["health_state"].dropna()).issubset(valid_states)

print("Health-state column present.")
print("\nHealth-state distribution:")
print(df["health_state"].value_counts())


print("\n=== 8. ML HANDOFF CHECK ===")

ml_excluded_columns = {
    "fouling_state",
    "cleaning_event",
    "sensor_anomaly",
}

print("Evaluation-only columns:")
for column in sorted(ml_excluded_columns):
    print(f"- {column}")

print("\nThese columns must not be used as ML input features.")

assert ml_excluded_columns.issubset(df.columns)


print("\n=== FINAL DATASET ===")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nFinal columns:")

for column in df.columns:
    print(f"- {column}")


print("\n=== STAGE 4 ASSERTIONS ===")

assert len(df) == 17280
assert len(df.columns) == 26

assert "timestamp" in df.columns
assert "U" in df.columns
assert "delta_p" in df.columns
assert "health_state" in df.columns

assert "U_baseline_status" in df.columns
assert "delta_p_baseline_status" in df.columns

print("All Stage 4 assertions passed.")

print("\n=== STAGE 4 PIPELINE TEST PASSED ===")
