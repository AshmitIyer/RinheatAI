from ml.preprocessing.loader import load_sensor_data

df = load_sensor_data()

print(df.head())

print()
print(df.dtypes)

print()
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print()
print(f"Start: {df['timestamp'].min()}")
print(f"End:   {df['timestamp'].max()}")