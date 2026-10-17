from __future__ import annotations

import pandas as pd


def clean_sensor_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean validated sensor time-series data.

    Cleaning steps:
    - Copy the input DataFrame so the original is not modified.
    - Convert timestamp to datetime.
    - Sort rows chronologically.
    - Remove exact duplicate timestamps, keeping the first record.
    - Return the cleaned DataFrame.
    """

    cleaned = df.copy()

    # Ensure timestamps are datetime values.
    cleaned["timestamp"] = pd.to_datetime(
        cleaned["timestamp"],
        errors="coerce",
    )

    # Remove rows where timestamp could not be interpreted.
    cleaned = cleaned.dropna(subset=["timestamp"])

    # Sort chronologically.
    cleaned = cleaned.sort_values("timestamp")

    # Remove duplicate timestamps.
    cleaned = cleaned.drop_duplicates(
        subset=["timestamp"],
        keep="first",
    )

    # Reset the row index after cleaning.
    cleaned = cleaned.reset_index(drop=True)

    return cleaned