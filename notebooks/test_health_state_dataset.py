from ml.preprocessing.loader import load_sensor_data
from ml.preprocessing.cleaner import clean_sensor_data
from ml.preprocessing.features import add_engineering_features
from ml.engineering.baseline import (
    calculate_baseline,
    add_baseline_status,
)
from ml.engineering.health_state import add_health_state


print("=== Loading Data ===")

df = load_sensor_data()

print(f"Rows loaded: {len(df)}")


print("\n=== Cleaning Data ===")

df = clean_sensor_data(df)

print(f"Rows after cleaning: {len(df)}")


print("\n=== Engineering Features ===")

df = add_engineering_features(df)

print(f"Columns after feature generation: {len(df.columns)}")


print("\n=== Calculating Baselines ===")

u_baseline = calculate_baseline(df, "U")
delta_p_baseline = calculate_baseline(df, "delta_p")

print(f"U lower bound: {u_baseline['lower_bound']:.3f}")
print(f"U upper bound: {u_baseline['upper_bound']:.3f}")

print(f"Delta-P lower bound: {delta_p_baseline['lower_bound']:.3f}")
print(f"Delta-P upper bound: {delta_p_baseline['upper_bound']:.3f}")


print("\n=== Adding Baseline Status ===")

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


print("\n=== Adding Health State ===")

df = add_health_state(df)


print("\n=== Health State Counts ===")

print(df["health_state"].value_counts())


print("\n=== Health State Percentages ===")

print(
    (df["health_state"].value_counts(normalize=True) * 100)
    .round(2)
)


print("\n=== Sample ===")

print(
    df[
        [
            "timestamp",
            "U",
            "U_baseline_status",
            "U_change_1h",
            "delta_p",
            "delta_p_baseline_status",
            "delta_p_change_1h",
            "health_state",
        ]
    ].tail(20)
)


print("\n=== Basic Assertions ===")

assert len(df) == 17280
assert "health_state" in df.columns

valid_states = {
    "NORMAL",
    "WATCH",
    "DEGRADED",
    "CRITICAL",
}

assert set(df["health_state"].dropna()).issubset(valid_states)

print("All basic assertions passed.")
