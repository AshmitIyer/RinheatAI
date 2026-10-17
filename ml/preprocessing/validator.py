from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "timestamp",
    "temperature",
    "pressure",
    "flow_rate",
    "steam_flow",
    "delta_p",
    "production_load",
    "U",
]


def validate_required_columns(df: pd.DataFrame) -> list[str]:
    """Return required columns that are missing from the dataset."""
    return [column for column in REQUIRED_COLUMNS if column not in df.columns]


def check_timestamp_quality(df: pd.DataFrame) -> dict:
    """Check timestamp completeness, duplicates, ordering and gaps."""

    timestamps = pd.to_datetime(df["timestamp"], errors="coerce")

    invalid_timestamps = int(timestamps.isna().sum())
    duplicate_timestamps = int(timestamps.duplicated().sum())

    if len(timestamps) > 1:
        time_differences = timestamps.sort_values().diff().dropna()
        negative_intervals = int((time_differences < pd.Timedelta(0)).sum())
        largest_gap = time_differences.max()
    else:
        negative_intervals = 0
        largest_gap = pd.Timedelta(0)

    return {
        "invalid_timestamps": invalid_timestamps,
        "duplicate_timestamps": duplicate_timestamps,
        "negative_intervals": negative_intervals,
        "largest_gap": largest_gap,
    }


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """Return missing-value counts for each column."""
    return df.isna().sum()


def check_physical_ranges(df: pd.DataFrame) -> dict:
    """Check for physically suspicious sensor values."""

    checks = {
        "negative_pressure": int((df["pressure"] < 0).sum()),
        "negative_flow_rate": int((df["flow_rate"] < 0).sum()),
        "negative_steam_flow": int((df["steam_flow"] < 0).sum()),
        "negative_delta_p": int((df["delta_p"] < 0).sum()),
        "negative_U": int((df["U"] < 0).sum()),
    }

    return checks


def validate_dataframe(df: pd.DataFrame) -> dict:
    """Run the complete Stage 4 data-validation checks."""

    missing_columns = validate_required_columns(df)

    if missing_columns:
        return {
            "valid": False,
            "missing_columns": missing_columns,
        }

    timestamp_quality = check_timestamp_quality(df)
    missing_values = check_missing_values(df)
    physical_ranges = check_physical_ranges(df)

    has_missing_values = bool(missing_values.sum() > 0)

    has_timestamp_problems = (
        timestamp_quality["invalid_timestamps"] > 0
        or timestamp_quality["duplicate_timestamps"] > 0
        or timestamp_quality["negative_intervals"] > 0
    )

    has_physical_problems = any(
        count > 0 for count in physical_ranges.values()
    )

    return {
        "valid": not (
            has_missing_values
            or has_timestamp_problems
            or has_physical_problems
        ),
        "missing_columns": [],
        "timestamp_quality": timestamp_quality,
        "missing_values": missing_values,
        "physical_ranges": physical_ranges,
    }