import pandas as pd
import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit

# Load ferrite data
df_f = pd.read_csv(r"c:\Users\Student\studies\2026S\Lab4\03 Curie\curie_data_ferrit.csv", comment="#")
max_temp_idx_f = df_f["Temp (C)"].idxmax()
h_df_f = df_f.iloc[:max_temp_idx_f].copy()
c_df_f = df_f.iloc[max_temp_idx_f:].copy()

# Load invar data
df_i = pd.read_csv(r"c:\Users\Student\studies\2026S\Lab4\03 Curie\curie_data_invar.csv", comment="#")
max_temp_idx_i = df_i["Temp (C)"].idxmax()
h_df_i = df_i.iloc[:max_temp_idx_i].copy()
c_df_i = df_i.iloc[max_temp_idx_i:].copy()

def erf_model(T, Tc, dT):
    return 0.5 * (1.0 - erf((T - Tc) / (dT * np.sqrt(2.0))))

# Let's fit Ferrite Heating
print("--- Ferrite Heating ---")
h_trans_f = h_df_f[(h_df_f["Temp (C)"] >= 120) & (h_df_f["Temp (C)"] <= 150)].copy()
V_raw = h_trans_f["RMS CH2 (V)"].values
V_min, V_max = V_raw.min(), V_raw.max()
V_norm = (V_raw - V_min) / (V_max - V_min)
popt, pcov = curve_fit(erf_model, h_trans_f["Temp (C)"].values, V_norm, p0=[133.0, 0.5])
print("Ferrite Heat popt:", popt)

# Let's fit Ferrite Cooling
print("--- Ferrite Cooling ---")
c_trans_f = c_df_f[(c_df_f["Temp (C)"] >= 125) & (c_df_f["Temp (C)"] <= 165)].copy()
V_raw = c_trans_f["RMS CH2 (V)"].values
V_min, V_max = V_raw.min(), V_raw.max()
V_norm = (V_raw - V_min) / (V_max - V_min)
popt, pcov = curve_fit(erf_model, c_trans_f["Temp (C)"].values, V_norm, p0=[138.0, 0.5])
print("Ferrite Cool popt:", popt)

# Let's fit Invar Heating
print("--- Invar Heating ---")
h_trans_i = h_df_i[(h_df_i["Temp (C)"] >= 220) & (h_df_i["Temp (C)"] <= 275)].copy()
V_raw = h_trans_i["RMS CH2 (V)"].values
V_min, V_max = V_raw.min(), V_raw.max()
V_norm = (V_raw - V_min) / (V_max - V_min)
popt, pcov = curve_fit(erf_model, h_trans_i["Temp (C)"].values, V_norm, p0=[246.0, 5.0])
print("Invar Heat popt:", popt)

# Let's fit Invar Cooling
print("--- Invar Cooling ---")
c_trans_i = c_df_i[(c_df_i["Temp (C)"] >= 220) & (c_df_i["Temp (C)"] <= 275)].copy()
V_raw = c_trans_i["RMS CH2 (V)"].values
V_min, V_max = V_raw.min(), V_raw.max()
V_norm = (V_raw - V_min) / (V_max - V_min)
popt, pcov = curve_fit(erf_model, c_trans_i["Temp (C)"].values, V_norm, p0=[250.0, 5.0])
print("Invar Cool popt:", popt)
