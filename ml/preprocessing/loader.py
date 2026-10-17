from __future__ import annotations

from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_DATA_PATH = Path(
    "data/simulated/rinheat_sensor_data_v2.csv"
)


# ============================================================
# DATA LOADING
# ============================================================

def load_sensor_data(
    data_path: str | Path = DEFAULT_DATA_PATH,
) -> pd.DataFrame:
    """
    Load Rinheat sensor data from a CSV file.

    Parameters
    ----------
    data_path:
        Path to the CSV file containing sensor data.

    Returns
    -------
    pd.DataFrame
        Sensor data with timestamp converted to datetime
        and rows sorted chronologically.
    """

    data_path = Path(data_path)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Sensor data file not found: {data_path}"
        )

    df = pd.read_csv(data_path)

    if "timestamp" not in df.columns:
        raise ValueError(
            "Input data must contain a 'timestamp' column."
        )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )

    if df["timestamp"].isna().any():
        raise ValueError(
            "One or more timestamp values could not be "
            "converted to datetime."
        )

    df = df.sort_values("timestamp").reset_index(drop=True)

    return df