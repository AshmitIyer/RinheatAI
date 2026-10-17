from __future__ import annotations

import pandas as pd


HEALTH_STATES = [
    "NORMAL",
    "WATCH",
    "DEGRADED",
    "CRITICAL",
]


def classify_health_state(
    u_status: str,
    delta_p_status: str,
    u_change_1h: float | None = None,
    delta_p_change_1h: float | None = None,
) -> str:
    """
    Classify equipment health using thermal and hydraulic indicators.

    The logic is intentionally simple and interpretable for the prototype.

    A trend is considered meaningful only when:
    - U decreases by more than 5 units over one hour.
    - delta-P increases by more than 0.05 over one hour.

    Baseline status remains the primary indicator.
    """

    thermal_concern = u_status == "LOW"
    hydraulic_concern = delta_p_status == "HIGH"

    thermal_declining = (
        u_change_1h is not None
        and pd.notna(u_change_1h)
        and u_change_1h < -5.0
    )

    hydraulic_increasing = (
        delta_p_change_1h is not None
        and pd.notna(delta_p_change_1h)
        and delta_p_change_1h > 0.05
    )

    active_concerns = sum(
        [
            thermal_concern,
            hydraulic_concern,
            thermal_declining,
            hydraulic_increasing,
        ]
    )

    combined_degradation = (
        thermal_concern
        and hydraulic_concern
        and thermal_declining
        and hydraulic_increasing
    )

    if combined_degradation:
        return "CRITICAL"

    if active_concerns >= 2:
        return "DEGRADED"

    if active_concerns == 1:
        return "WATCH"

    return "NORMAL"


def add_health_state(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add an equipment health-state column to an engineered DataFrame.

    Required columns:
    - U_baseline_status
    - delta_p_baseline_status
    - U_change_1h
    - delta_p_change_1h
    """

    required_columns = [
        "U_baseline_status",
        "delta_p_baseline_status",
        "U_change_1h",
        "delta_p_change_1h",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    result = df.copy()

    result["health_state"] = result.apply(
        lambda row: classify_health_state(
            u_status=row["U_baseline_status"],
            delta_p_status=row["delta_p_baseline_status"],
            u_change_1h=row["U_change_1h"],
            delta_p_change_1h=row["delta_p_change_1h"],
        ),
        axis=1,
    )

    return result
