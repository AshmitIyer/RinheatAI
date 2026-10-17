from ml.preprocessing.loader import load_sensor_data
from ml.preprocessing.cleaner import clean_sensor_data


df = load_sensor_data()

print("=== Before Cleaning ===")
print(f"Rows: {len(df):,}")
print(f"Duplicate timestamps: {df['timestamp'].duplicated().sum()}")
print(f"Missing timestamps: {df['timestamp'].isna().sum()}")
print()

cleaned_df = clean_sensor_data(df)

print("=== After Cleaning ===")
print(f"Rows: {len(cleaned_df):,}")
print(f"Duplicate timestamps: {cleaned_df['timestamp'].duplicated().sum()}")
print(f"Missing timestamps: {cleaned_df['timestamp'].isna().sum()}")
print()

time_differences = cleaned_df["timestamp"].diff().dropna()

print("=== Time-Series Check ===")
print(f"Smallest interval: {time_differences.min()}")
print(f"Largest interval: {time_differences.max()}")
print(f"Median interval: {time_differences.median()}")
print()

print("First timestamp:")
print(cleaned_df["timestamp"].iloc[0])

print("Last timestamp:")
print(cleaned_df["timestamp"].iloc[-1])