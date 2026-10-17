from __future__ import annotations

import pandas as pd


def add_engineering_features(df: pd.DataFrame) -> pd.DataFrame:
    """
Add engineering and time-series features to cleaned sensor data.

The original columns are preserved.

Features include:
- rolling averages for U and delta_p
- rate of change for U and delta_p
- lagged U and delta_p
"""

    features = df.copy()

    # Make sure the data is in chronological order.
    features = features.sort_values("timestamp").reset_index(drop=True)

    # ---------------------------------------------------------
    # Rolling averages
    # ---------------------------------------------------------

    # 12 samples = 1 hour for 5-minute data.
    features["U_rolling_1h"] = (
        features["U"]
        .rolling(window=12, min_periods=1)
        .mean()
    )

    features["delta_p_rolling_1h"] = (
        features["delta_p"]
        .rolling(window=12, min_periods=1)
        .mean()
    )

    # 72 samples = 6 hours for 5-minute data.
    features["U_rolling_6h"] = (
        features["U"]
        .rolling(window=72, min_periods=1)
        .mean()
    )

    features["delta_p_rolling_6h"] = (
        features["delta_p"]
        .rolling(window=72, min_periods=1)
        .mean()
    )

    # ---------------------------------------------------------
    # Rate of change
    # ---------------------------------------------------------

    # Change over one hour.
    features["U_change_1h"] = features["U"].diff(12)
    features["delta_p_change_1h"] = features["delta_p"].diff(12)

    # Change over six hours.
    features["U_change_6h"] = features["U"].diff(72)
    features["delta_p_change_6h"] = features["delta_p"].diff(72)

    # ---------------------------------------------------------
    # Lag features
    # ---------------------------------------------------------

    # Previous-hour values.
    features["U_lag_1h"] = features["U"].shift(12)
    features["delta_p_lag_1h"] = features["delta_p"].shift(12)

    # Previous six-hour values.
    features["U_lag_6h"] = features["U"].shift(72)
    features["delta_p_lag_6h"] = features["delta_p"].shift(72)



    return features