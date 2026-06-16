import pandas as pd
import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit

# Load data
df = pd.read_csv(r"c:\Users\Student\studies\2026S\Lab4\03 Curie\curie_data_ferrit.csv", comment="#")
max_temp_idx = df["Temp (C)"].idxmax()
heating_df = df.iloc[:max_idx].copy() if 'max_idx' in locals() else df.iloc[:max_temp_idx].copy()
cooling_df = df.iloc[max_temp_idx:].copy()

def erf_model(T, a, b, Tc, dT):
    return a + b * erf((T - Tc) / dT)

def erf_slope_model(T, a, b, Tc, dT, c):
    return a + b * erf((T - Tc) / dT) + c * (T - Tc)

# Let's test ranges for cooling fit (simple erf)
for temp_max in [145, 150, 155, 160, 165, 170]:
    c_trans = cooling_df[(cooling_df["Temp (C)"] >= 125) & (cooling_df["Temp (C)"] <= temp_max)]
    T_val = c_trans["Temp (C)"].values
    V_val = c_trans["RMS CH2 (V)"].values
    try:
        popt, pcov = curve_fit(erf_model, T_val, V_val, p0=[2.14, -0.17, 138.0, 3.0])
        print(f"Cooling (125 to {temp_max} C) Simple Erf: Tc = {popt[2]:.3f} +- {np.sqrt(pcov[2, 2]):.3f}, dT = {popt[3]:.3f}")
    except Exception as e:
        print(f"Cooling (125 to {temp_max} C) failed: {e}")

# Let's test ranges for cooling fit with slope
print("\n--- Cooling with Slope ---")
for temp_max in [150, 155, 160, 165, 170]:
    c_trans = cooling_df[(cooling_df["Temp (C)"] >= 125) & (cooling_df["Temp (C)"] <= temp_max)]
    T_val = c_trans["Temp (C)"].values
    V_val = c_trans["RMS CH2 (V)"].values
    try:
        popt, pcov = curve_fit(erf_slope_model, T_val, V_val, p0=[2.14, -0.17, 138.0, 3.0, -0.001])
        print(f"Cooling (125 to {temp_max} C) Slope Erf: Tc = {popt[2]:.3f} +- {np.sqrt(pcov[2, 2]):.3f}, dT = {popt[3]:.3f}, c = {popt[4]:.5f}")
    except Exception as e:
        print(f"Cooling (125 to {temp_max} C) failed: {e}")

# Let's test ranges for heating fit (simple erf)
print("\n--- Heating Simple Erf ---")
for temp_max in [145, 150, 155, 160]:
    h_trans = heating_df[(heating_df["Temp (C)"] >= 120) & (heating_df["Temp (C)"] <= temp_max)]
    T_val = h_trans["Temp (C)"].values
    V_val = h_trans["RMS CH2 (V)"].values
    try:
        popt, pcov = curve_fit(erf_model, T_val, V_val, p0=[2.15, -0.15, 133.0, 2.0])
        print(f"Heating (120 to {temp_max} C) Simple Erf: Tc = {popt[2]:.3f} +- {np.sqrt(pcov[2, 2]):.3f}, dT = {popt[3]:.3f}")
    except Exception as e:
        print(f"Heating (120 to {temp_max} C) failed: {e}")
