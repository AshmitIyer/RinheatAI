from ml.preprocessing.loader import load_sensor_data
from ml.preprocessing.validator import validate_dataframe


df = load_sensor_data()

results = validate_dataframe(df)

print("=== Rinheat Data Validation ===")
print(f"Overall valid: {results['valid']}")
print()

print("Missing columns:")
print(results["missing_columns"])
print()

print("Timestamp quality:")
for key, value in results["timestamp_quality"].items():
    print(f"  {key}: {value}")
print()

print("Missing values:")
print(results["missing_values"])
print()

print("Physical range checks:")
for key, value in results["physical_ranges"].items():
    print(f"  {key}: {value}")