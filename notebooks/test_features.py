from ml.preprocessing.loader import load_sensor_data
from ml.preprocessing.cleaner import clean_sensor_data
from ml.preprocessing.features import add_engineering_features


df = load_sensor_data()

cleaned_df = clean_sensor_data(df)

feature_df = add_engineering_features(cleaned_df)

print("=== Engineering Feature Generation ===")
print(f"Original rows: {len(df):,}")
print(f"Feature rows:  {len(feature_df):,}")
print()

print("Original columns:")
print(list(df.columns))
print()

print("New feature columns:")
new_columns = [
    column
    for column in feature_df.columns
    if column not in df.columns
]
for column in new_columns:
    print(f"  {column}")
print()

print(f"Total columns: {len(feature_df.columns)}")
print()

print("=== Feature Sample ===")
print(
    feature_df[
        [
            "timestamp",
            "U",
            "U_rolling_1h",
            "U_rolling_6h",
            "U_change_1h",
            "U_change_6h",
            "U_lag_1h",
            "delta_p",
            "delta_p_rolling_1h",
            "delta_p_change_1h",
        ]
    ].tail(10)
)