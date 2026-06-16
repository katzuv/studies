import pandas as pd
import numpy as np

# Load data
df = pd.read_csv(r"c:\Users\Student\studies\2026S\Lab4\03 Curie\curie_data_invar.csv", comment="#")
max_temp_idx = df["Temp (C)"].idxmax()
max_temp = df["Temp (C)"].max()
print(f"Max Temp: {max_temp} at index {max_temp_idx}")

heating_df = df.iloc[:max_temp_idx].copy()
cooling_df = df.iloc[max_temp_idx:].copy()

print(f"Heating points: {len(heating_df)}, Temp range: {heating_df['Temp (C)'].min()} to {heating_df['Temp (C)'].max()}")
print(f"Cooling points: {len(cooling_df)}, Temp range: {cooling_df['Temp (C)'].min()} to {cooling_df['Temp (C)'].max()}")

# Let's see what the transition looks like.
# For Invar, the Curie temp is around 230 to 280 deg C.
# Let's find where RMS CH2 (V) drops significantly.
# Let's print some statistics of RMS CH2 (V) vs Temp (C) in heating.
print("\nHeating data sample around expected transition (200 to 286 C):")
h_trans = heating_df[(heating_df["Temp (C)"] >= 200) & (heating_df["Temp (C)"] <= 286)]
print(h_trans.groupby(pd.cut(h_trans["Temp (C)"], bins=10))["RMS CH2 (V)"].mean())

print("\nCooling data sample around expected transition (200 to 286 C):")
c_trans = cooling_df[(cooling_df["Temp (C)"] >= 200) & (cooling_df["Temp (C)"] <= 286)]
print(c_trans.groupby(pd.cut(c_trans["Temp (C)"], bins=10))["RMS CH2 (V)"].mean())
