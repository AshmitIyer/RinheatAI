import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = "data/simulated/rinheat_sensor_data_v2.csv"

df = pd.read_csv(DATA_PATH)

df["timestamp"] = pd.to_datetime(df["timestamp"])


# ============================================================
# 1. U + FOULING
# ============================================================

fig, ax1 = plt.subplots(figsize=(14, 5))

ax1.plot(
    df["timestamp"],
    df["U"],
    label="Heat-transfer coefficient U",
)

ax1.set_xlabel("Time")
ax1.set_ylabel("U")

ax2 = ax1.twinx()

ax2.plot(
    df["timestamp"],
    df["fouling_state"],
    label="Fouling state",
    alpha=0.7,
)

ax2.set_ylabel("Fouling state")

plt.title(
    "Synthetic Equipment Performance and Fouling"
)

plt.tight_layout()

plt.show()


# ============================================================
# 2. DIFFERENTIAL PRESSURE
# ============================================================

plt.figure(figsize=(14, 5))

plt.plot(
    df["timestamp"],
    df["delta_p"],
)

plt.xlabel("Time")
plt.ylabel("Differential Pressure")

plt.title(
    "Differential Pressure Over Time"
)

plt.tight_layout()

plt.show()


# ============================================================
# 3. STEAM FLOW
# ============================================================

plt.figure(figsize=(14, 5))

plt.plot(
    df["timestamp"],
    df["steam_flow"],
)

plt.xlabel("Time")
plt.ylabel("Steam Flow")

plt.title(
    "Steam Flow Over Time"
)

plt.tight_layout()

plt.show()


# ============================================================
# 4. PRODUCTION LOAD
# ============================================================

plt.figure(figsize=(14, 5))

plt.plot(
    df["timestamp"],
    df["production_load"],
)

plt.xlabel("Time")
plt.ylabel("Production Load")

plt.title(
    "Production Load Over Time"
)

plt.tight_layout()

plt.show()


# ============================================================
# 5. TEMPERATURE
# ============================================================

plt.figure(figsize=(14, 5))

plt.plot(
    df["timestamp"],
    df["temperature"],
)

plt.xlabel("Time")
plt.ylabel("Temperature")

plt.title(
    "Temperature Over Time"
)

plt.tight_layout()

plt.show()