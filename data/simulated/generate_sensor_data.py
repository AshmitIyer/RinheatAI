from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42

START_DATE = "2026-01-01"
DAYS = 60
SAMPLING_MINUTES = 5

OUTPUT_PATH = Path("data/simulated/rinheat_sensor_data_v2.csv")

rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# TIME AXIS
# ============================================================

timestamps = pd.date_range(
    start=START_DATE,
    periods=int(DAYS * 24 * 60 / SAMPLING_MINUTES),
    freq=f"{SAMPLING_MINUTES}min",
)

n = len(timestamps)

hours = np.asarray(
    timestamps.hour + timestamps.minute / 60.0,
    dtype=float,
)

day_number = np.asarray(
    (timestamps - timestamps[0]).total_seconds() / (24 * 3600),
    dtype=float,
)

# ============================================================
# OPERATING CONDITIONS
# ============================================================

# Daily operating cycle.
daily_cycle = np.sin(
    2 * np.pi * (hours - 5) / 24
)

# Slower multi-day operating variation.
weekly_cycle = np.sin(
    2 * np.pi * day_number / 8.5
)

# Medium-frequency operational variation.
medium_cycle = np.sin(
    2 * np.pi * day_number / 2.7 + 0.8
)


# ------------------------------------------------------------
# Production load
# ------------------------------------------------------------

production_load = (
    0.77
    + 0.095 * daily_cycle
    + 0.035 * weekly_cycle
    + 0.025 * medium_cycle
    + rng.normal(0, 0.012, n)
)

# Occasional operating-regime changes.
regime_changes = {
    8: 0.035,
    18: -0.045,
    29: 0.055,
    41: -0.030,
    51: 0.040,
}

for change_day, offset in regime_changes.items():
    production_load += np.where(day_number >= change_day, offset, 0)

production_load = np.clip(
    production_load,
    0.55,
    0.97,
)


# ============================================================
# BASE PROCESS VARIABLES
# ============================================================

# Temperature responds to load plus slow environmental variation.
temperature = (
    144.0
    + 3.0 * (production_load - 0.75)
    + 1.7 * daily_cycle
    + 0.7 * weekly_cycle
    + rng.normal(0, 0.45, n)
)

# Pressure has weaker dependence on load.
pressure = (
    2.25
    + 0.20 * (production_load - 0.70)
    + 0.025 * weekly_cycle
    + rng.normal(0, 0.018, n)
)

# Base flow responds strongly to production load.
flow_rate = (
    80.0
    + 12.0 * (production_load - 0.70)
    + 0.8 * daily_cycle
    + rng.normal(0, 0.65, n)
)

flow_rate = np.clip(
    flow_rate,
    70,
    90,
)


# ============================================================
# IRREGULAR CLEANING EVENTS
# ============================================================

# Cleaning intervals are deliberately irregular.
candidate_cleaning_days = np.array([
    4.2,
    10.8,
    17.1,
    25.6,
    34.0,
    43.7,
    52.4,
])

cleaning_indices = []

for cleaning_day in candidate_cleaning_days:

    idx = int(
        cleaning_day * 24 * 60 / SAMPLING_MINUTES
    )

    if 0 <= idx < n:
        cleaning_indices.append(idx)


cleaning_indices = np.array(
    cleaning_indices,
    dtype=int,
)


# ============================================================
# FOULING DYNAMICS
# ============================================================

fouling_state = np.zeros(n)

current_fouling = 0.0

# Different fouling rates for different operating periods.
base_fouling_rates = [
    0.00032,
    0.00048,
    0.00038,
    0.00055,
    0.00042,
    0.00050,
    0.00035,
    0.00046,
]

cleaning_effectiveness = [
    0.94,
    0.78,
    0.90,
    0.84,
    0.68,
    0.93,
    0.80,
]

cleaning_event = np.zeros(n, dtype=int)

cleaning_number = 0

for i in range(n):

    # --------------------------------------------------------
    # Cleaning event
    # --------------------------------------------------------

    if i in cleaning_indices:

        cleaning_event[i] = 1

        effectiveness = cleaning_effectiveness[
            min(
                cleaning_number,
                len(cleaning_effectiveness) - 1,
            )
        ]

        current_fouling *= (1.0 - effectiveness)

        cleaning_number += 1

    # --------------------------------------------------------
    # Fouling accumulation
    # --------------------------------------------------------

    load_factor = (
        0.65
        + 1.15 * production_load[i]
    )

    temperature_factor = (
        1.0
        + 0.025 * max(
            temperature[i] - 145.0,
            0,
        )
    )

    process_factor = (
        0.90
        + 0.20
        * (
            0.5
            + 0.5
            * np.sin(
                2 * np.pi
                * day_number[i]
                / 11.0
            )
        )
    )

    regime_index = min(
        int(day_number[i] // 7),
        len(base_fouling_rates) - 1,
    )

    fouling_rate = (
        base_fouling_rates[regime_index]
        * load_factor
        * temperature_factor
        * process_factor
    )

    # Natural saturation:
    # accumulation slows as fouling becomes severe.
    saturation_factor = (
        max(
            1.0 - current_fouling,
            0.02,
        )
        ** 1.5
    )

    fouling_rate *= saturation_factor

    # Small stochastic variation.
    fouling_rate *= rng.lognormal(
        mean=0,
        sigma=0.08,
    )

    current_fouling += fouling_rate

    # Very high safety bound only.
    current_fouling = min(
        current_fouling,
        0.98,
    )

    fouling_state[i] = current_fouling


# ============================================================
# HEAT TRANSFER PERFORMANCE: U
# ============================================================

# Base equipment performance.
base_U = 880.0

fouling_effect = (
    175.0 * fouling_state
    + 35.0 * (fouling_state ** 2)
)

# Load changes apparent heat-transfer performance.
load_effect = (
    35.0 * (production_load - 0.75)
)

# Temperature and pressure contribute smaller effects.
temperature_effect = (
    4.0 * (temperature - 144.0)
)

pressure_effect = (
    18.0 * (pressure - 2.25)
)

# Slow equipment health variation.
health_drift = (
    -0.025 * day_number
)

# Measurement/process noise.
U_noise = rng.normal(
    0,
    4.0,
    n,
)

U = (
    base_U
    - fouling_effect
    + load_effect
    + temperature_effect
    + pressure_effect
    + health_drift
    + U_noise
)

# Equipment cannot exceed reasonable bounds.
U = np.clip(
    U,
    600,
    900,
)


# ============================================================
# DIFFERENTIAL PRESSURE
# ============================================================

delta_p = (
    0.72
    + 0.58 * fouling_state
    + 0.0040 * (flow_rate - 80.0)
    + 0.060 * (production_load - 0.75)
    + 0.035 * weekly_cycle
    + rng.normal(0, 0.025, n)
)

delta_p = np.clip(
    delta_p,
    0.55,
    1.55,
)


# ============================================================
# STEAM FLOW
# ============================================================

# Steam demand rises with load and, to a lesser extent,
# with fouling because degraded heat transfer requires
# more process effort.
steam_flow = (
    29.5
    + 8.0 * production_load
    + 1.5 * fouling_state
    + 0.8 * daily_cycle
    + 0.5 * weekly_cycle
    + rng.normal(0, 0.30, n)
)

steam_flow = np.clip(
    steam_flow,
    31,
    40,
)


# ============================================================
# SENSOR ANOMALIES
# ============================================================

sensor_anomaly = np.zeros(n, dtype=int)

# Sparse anomaly points.
num_anomalies = int(n * 0.008)

anomaly_indices = rng.choice(
    n,
    size=num_anomalies,
    replace=False,
)

sensor_anomaly[anomaly_indices] = 1


# Apply different types of anomalies.
for idx in anomaly_indices:

    anomaly_type = rng.choice(
        ["temperature", "pressure", "flow", "U"],
        p=[0.30, 0.20, 0.25, 0.25],
    )

    if anomaly_type == "temperature":
        temperature[idx] += rng.choice(
            [-1, 1]
        ) * rng.uniform(4, 8)

    elif anomaly_type == "pressure":
        pressure[idx] += rng.choice(
            [-1, 1]
        ) * rng.uniform(0.15, 0.30)

    elif anomaly_type == "flow":
        flow_rate[idx] += rng.choice(
            [-1, 1]
        ) * rng.uniform(5, 10)

    elif anomaly_type == "U":
        U[idx] += rng.choice(
            [-1, 1]
        ) * rng.uniform(25, 55)


# ============================================================
# SENSOR DRIFT
# ============================================================

# Very small long-term sensor bias.
temperature_drift = (
    0.025 * day_number
)

pressure_drift = (
    -0.0008 * day_number
)

flow_drift = (
    0.015 * day_number
)

temperature += temperature_drift
pressure += pressure_drift
flow_rate += flow_drift


# ============================================================
# BUILD DATAFRAME
# ============================================================

df = pd.DataFrame(
    {
        "timestamp": timestamps,
        "temperature": temperature,
        "pressure": pressure,
        "flow_rate": flow_rate,
        "steam_flow": steam_flow,
        "delta_p": delta_p,
        "production_load": production_load,
        "U": U,
        "fouling_state": fouling_state,
        "cleaning_event": cleaning_event,
        "sensor_anomaly": sensor_anomaly,
    }
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

df.to_csv(
    OUTPUT_PATH,
    index=False,
)


# ============================================================
# SUMMARY
# ============================================================

print("=" * 60)
print("RINHEAT SENSOR SIMULATOR V2")
print("=" * 60)

print(f"Rows:              {len(df):,}")
print(f"Duration:          {DAYS} days")
print(f"Sampling:          {SAMPLING_MINUTES} minutes")
print(f"Columns:           {len(df.columns)}")

print()
print(f"Cleaning events:   {df['cleaning_event'].sum()}")
print(f"Sensor anomalies:  {df['sensor_anomaly'].sum()}")

print()
print("Fouling state:")
print(f"  Min:             {df['fouling_state'].min():.3f}")
print(f"  Max:             {df['fouling_state'].max():.3f}")

print()
print("Heat-transfer coefficient U:")
print(f"  Min:             {df['U'].min():.2f}")
print(f"  Max:             {df['U'].max():.2f}")
print(f"  Mean:            {df['U'].mean():.2f}")

print()
print("Differential pressure:")
print(f"  Min:             {df['delta_p'].min():.3f}")
print(f"  Max:             {df['delta_p'].max():.3f}")

print()
print("Production load:")
print(f"  Min:             {df['production_load'].min():.3f}")
print(f"  Max:             {df['production_load'].max():.3f}")

print()
print("Output:")
print(f"  {OUTPUT_PATH}")

print("=" * 60)