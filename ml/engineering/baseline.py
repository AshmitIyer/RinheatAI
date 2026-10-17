from __future__ import annotations

import pandas as pd


def calculate_baseline(
    df: pd.DataFrame,
    column: str,
) -> dict:
    """
    Calculate a simple statistical baseline for an engineering variable.

    The baseline consists of:
    - mean
    - standard deviation
    - lower bound
    - upper bound

    The bounds are defined as mean +/- 2 standard deviations.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    values = pd.to_numeric(df[column], errors="coerce").dropna()

    if values.empty:
        raise ValueError(
            f"No valid numeric values available for '{column}'."
        )

    mean = values.mean()
    std = values.std()

    return {
        "column": column,
        "mean": mean,
        "std": std,
        "lower_bound": mean - (2 * std),
        "upper_bound": mean + (2 * std),
    }


def classify_against_baseline(
    value: float,
    baseline: dict,
) -> str:
    """
    Classify a value relative to its baseline.

    Returns:
    - NORMAL
    - LOW
    - HIGH
    """
    if value < baseline["lower_bound"]:
        return "LOW"

    if value > baseline["upper_bound"]:
        return "HIGH"

    return "NORMAL"


def add_baseline_status(
    df: pd.DataFrame,
    column: str,
    baseline: dict,
) -> pd.DataFrame:
    """
    Add a baseline-status column to the DataFrame.

    Missing values are classified as UNKNOWN.
    """
    result = df.copy()
    status_column = f"{column}_baseline_status"

    result[status_column] = result[column].apply(
        lambda value: (
            classify_against_baseline(value, baseline)
            if pd.notna(value)
            else "UNKNOWN"
        )
    )

    return result