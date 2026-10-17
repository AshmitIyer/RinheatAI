from ml.preprocessing.loader import load_sensor_data
from ml.preprocessing.cleaner import clean_sensor_data
from ml.preprocessing.features import add_engineering_features
from ml.engineering.baseline import (
    calculate_baseline,
    add_baseline_status,
)


df = load_sensor_data()

cleaned_df = clean_sensor_data(df)

feature_df = add_engineering_features(cleaned_df)

# Calculate baselines.
u_baseline = calculate_baseline(feature_df, "U")
delta_p_baseline = calculate_baseline(feature_df, "delta_p")

print("=== U Baseline ===")
for key, value in u_baseline.items():
    print(f"{key}: {value}")

print()

print("=== Delta-P Baseline ===")
for key, value in delta_p_baseline.items():
    print(f"{key}: {value}")

print()

# Add baseline status.
result_df = add_baseline_status(
    feature_df,
    "U",
    u_baseline,
)

result_df = add_baseline_status(
    result_df,
    "delta_p",
    delta_p_baseline,
)

print("=== Baseline Status Counts ===")
print()
print("U:")
print(result_df["U_baseline_status"].value_counts())

print()
print("Delta-P:")
print(result_df["delta_p_baseline_status"].value_counts())

print()

print("=== Sample ===")
print(
    result_df[
        [
            "timestamp",
            "U",
            "U_baseline_status",
            "delta_p",
            "delta_p_baseline_status",
        ]
    ].tail(10)
)