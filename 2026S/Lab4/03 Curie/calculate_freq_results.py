import json
from pathlib import Path

import numpy as np
import pandas as pd

# Load data
df = pd.read_csv("data/freq_sweep.csv")
air = df[df["Core Type"] == "VS0 (Air core)"].copy()

# Parameters
R1 = 11.80  # Primary resistance [Ohm]
L1 = 0.0057  # Primary inductance [H]

# Frequencies of interest
freqs = [100, 500, 950, 2000, 4000]

results = []
for f in freqs:
    row = air[air["Frequency (Hz)"] == f].iloc[0]
    Vp = row["CH1 (V)"]
    Vs = row["CH2 (V)"]
    ratio_meas = Vs / Vp

    # Theoretical phase shift
    omega = 2 * np.pi * f
    theta = np.arctan(omega * L1 / R1)
    phase_theory_deg = 90.0 + np.degrees(theta)

    # Theoretical ratio assuming high-frequency limit of Vs/Vp is 1.134 (empirical)
    # or using the ideal model where Vs/Vp at f -> infinity is 0.6533
    ratio_theory_ideal = 0.6533 / np.sqrt(1 + (R1 / (omega * L1)) ** 2)
    ratio_theory_empirical = 1.134 / np.sqrt(1 + (R1 / (omega * L1)) ** 2)

    results.append(
        {
            "frequency": int(f),
            "Vp": float(Vp),
            "Vs": float(Vs),
            "ratio_meas": float(ratio_meas),
            "ratio_theory_ideal": float(ratio_theory_ideal),
            "ratio_theory_empirical": float(ratio_theory_empirical),
            "phase_theory_deg": float(phase_theory_deg),
        }
    )

# Write to JSON
output_path = Path("constants/freq_results.json")
with open(output_path, "w") as f_out:
    json.dump(results, f_out, indent=2)

print("Calculation completed. Results written to constants/freq_results.json")
