import pandas as pd
import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit

# Load data
df = pd.read_csv(r"c:\Users\Student\studies\2026S\Lab4\03 Curie\curie_data_invar.csv", comment="#")
max_temp_idx = df["Temp (C)"].idxmax()
heating_df = df.iloc[:max_temp_idx].copy()
cooling_df = df.iloc[max_temp_idx:].copy()

def erf_slope_model(T, a, b, Tc, dT, c):
    return a + b * erf((T - Tc) / dT) + c * (T - Tc)

# Newton cooling model
def cooling_model(t, T_env, T0, k):
    return T_env + (T0 - T_env) * np.exp(-k * t)

print("--- Heating Fit ---")
for t_min, t_max in [(215, 275), (220, 270), (220, 275), (220, 280)]:
    h_trans = heating_df[(heating_df["Temp (C)"] >= t_min) & (heating_df["Temp (C)"] <= t_max)]
    T_val = h_trans["Temp (C)"].values
    V_val = h_trans["RMS CH2 (V)"].values
    try:
        popt, pcov = curve_fit(erf_slope_model, T_val, V_val, p0=[2.285, -0.315, 248.0, 5.0, -0.001])
        print(f"Heating ({t_min} to {t_max} C): Tc = {popt[2]:.3f} +- {np.sqrt(pcov[2, 2]):.3f}, dT = {popt[3]:.3f}, c = {popt[4]:.5f}")
    except Exception as e:
        print(f"Heating ({t_min} to {t_max} C) failed: {e}")

print("\n--- Cooling Fit ---")
for t_min, t_max in [(215, 275), (220, 270), (220, 275), (220, 280), (225, 275)]:
    c_trans = cooling_df[(cooling_df["Temp (C)"] >= t_min) & (cooling_df["Temp (C)"] <= t_max)]
    T_val = c_trans["Temp (C)"].values
    V_val = c_trans["RMS CH2 (V)"].values
    try:
        popt, pcov = curve_fit(erf_slope_model, T_val, V_val, p0=[2.285, -0.315, 248.0, 5.0, -0.001])
        print(f"Cooling ({t_min} to {t_max} C): Tc = {popt[2]:.3f} +- {np.sqrt(pcov[2, 2]):.3f}, dT = {popt[3]:.3f}, c = {popt[4]:.5f}")
    except Exception as e:
        print(f"Cooling ({t_min} to {t_max} C) failed: {e}")

print("\n--- Cooling Curve Newton Fit ---")
times = pd.to_datetime(cooling_df["DateTime"], format="%d/%m/%Y %H:%M:%S")
t_s = (times - times.min()).dt.total_seconds().values
T_s = cooling_df["Temp (C)"].values
try:
    popt, pcov = curve_fit(cooling_model, t_s, T_s, p0=[24.0, 286.0, 0.001])
    print(f"Newton Cooling: T_env = {popt[0]:.3f}, T0 = {popt[1]:.3f}, k = {popt[2]:.6f} +- {np.sqrt(pcov[2, 2]):.6f}")
except Exception as e:
    print(f"Newton Cooling failed: {e}")
