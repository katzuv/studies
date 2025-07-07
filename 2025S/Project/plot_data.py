# -*- coding: utf-8 -*-
"""
Created on Tue May 20 16:03:10 2025

@author: moshe
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, cumulative_trapezoid

# Constants
mu0 = 4 * np.pi * 1e-7  # Vacuum permeability (not used but good to have)
epsilon0 = 8.854e-12    # Vacuum permittivity

# Copper properties
rho_0 = 1.68e-8         # Ohm·m at 20°C
alpha = 0.00393         # 1/°C temperature coefficient
T0 = 20                 # Reference temperature in °C
T_melt = 1085           # Copper melting point (°C)
c_p = 385               # J/(kg·K), specific heat capacity
rho_cu = 8960           # kg/m³ density of copper
L_fusion = 205e3        # J/kg, latent heat of fusion

# Wire dimensions
length = 0.01           # meters
diameter = 0.1e-3       # meters
area = np.pi * (diameter / 2)**2
volume = area * length
mass = volume * rho_cu

# Initial capacitor voltage
V0 = 1000.0             # Volts

# Circuit parameters
L = 100e-9              # Inductance in H
C = 1e-6                # Capacitance in F
U0 = 0.5*C*V0**2        # total energy in J

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

CVR_RESISTANCE = 0.1
ATTENUATOR_MULTIPLIER = 20
time, cvr_voltage, trigger_voltage = np.loadtxt("wire70u_1 explotion.csv", delimiter=',', skiprows=0, usecols=[3, 4, 10]).T
current = (cvr_voltage / CVR_RESISTANCE) * ATTENUATOR_MULTIPLIER

ax1.plot(time, current, label='Current (A)', color='blue')
ax1.set_xlabel(r'Time ($\mu$s)')
ax1.set_ylabel('Current (A)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Function to compute R at a given temperature
def resistance(T):
    return rho_0 * (1 + alpha * (T - T0)) * length / area

# T_est = T0 + delta_T
P = current**2 * .212
absorbed_energy = cumulative_trapezoid(P, time, initial=0)
# Estimate temperature rise from energy
delta_T = absorbed_energy / (mass * c_p)

# Recalculate power and energy with new current
# R_time = resistance(T_est)


# Energy axis
ax2 = ax1.twinx()
ax2.plot(time, absorbed_energy, label='Energy Absorbed (J)', color='red')
# ax2.axhline(2200, color='red', linestyle='--', label='Melting Threshold')
ax2.set_ylabel('Energy (J)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Legend and titles
fig.suptitle(f'Voltage: {V0:.0f} (V)  ;  Total Energy: {U0:.2f} (J) \n C={C*1e6} ($\mu$F)  ;  L={L*1e9} (nH)  ;  Diameter={diameter*1e3} (mm)  ;  Length={length*1e3} (mm)')
fig.legend(loc='lower right', bbox_to_anchor=(0.9, 0.15))
plt.grid(True)
plt.tight_layout()
plt.show()
