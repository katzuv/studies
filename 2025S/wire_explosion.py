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
diameter = 0.11e-3      # meters
area = np.pi * (diameter / 2)**2
volume = area * length
mass = volume * rho_cu

# Initial capacitor voltage
V0 = 1000.0             # Volts

# Circuit parameters
L = 100e-9              # Inductance in H
C = 1e-6                # Capacitance in F
U0 = 0.5*C*V0**2        # total energy in J

# Time span
t_span = (0, 0.01e-3)
t_eval = np.linspace(*t_span, 10000)

# Function to compute R at a given temperature
def resistance(T):
    return rho_0 * (1 + alpha * (T - T0)) * length / area

# RLC ODE System: dI/dt = (V_C - IR) / L, dV_C/dt = -I / C
def rlc_system(t, y, temp_func):
    I, V_C = y
    T = temp_func(t)
    R = resistance(T)
    dI_dt = (V_C - I * R) / L
    dV_C_dt = -I / C
    return [dI_dt, dV_C_dt]

# First run: assume room temperature to get initial current profile
sol = solve_ivp(lambda t, y: rlc_system(t, y, lambda t: T0), t_span, [0, V0], t_eval=t_eval)
I = sol.y[0]
V_C = sol.y[1]
t = sol.t

# Compute instantaneous power and cumulative energy
P = I**2 * resistance(T0)
E = cumulative_trapezoid(P, t, initial=0)

# Estimate temperature rise from energy
delta_T = E / (mass * c_p)
T_est = T0 + delta_T

# Recalculate resistance with changing T
def T_interp(ti):
    return np.interp(ti, t, T_est)

# Second run: solve again with updated temperature
sol2 = solve_ivp(lambda t, y: rlc_system(t, y, T_interp), t_span, [0, V0], t_eval=t_eval)
I2 = sol2.y[0]
V_C2 = sol2.y[1]

# Recalculate power and energy with new current
R_time = resistance(T_est)
P2 = I2**2 * R_time
E2 = cumulative_trapezoid(P2, t, initial=0)

# Threshold energy to melt wire
E_melt = mass * c_p * (T_melt - T0) + mass * L_fusion

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(t * 1e6, I2, label='Current (A)', color='blue')
ax1.set_xlabel(r'Time ($\mu$s)')
ax1.set_ylabel('Current (A)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Energy axis
ax2 = ax1.twinx()
ax2.plot(t * 1e6, E2, label='Energy Absorbed (J)', color='red')
ax2.axhline(E_melt, color='red', linestyle='--', label='Melting Threshold')
ax2.set_ylabel('Energy (J)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Legend and titles
fig.suptitle(f'Voltage: {V0:.0f} (V)  ;  Total Energy: {U0:.2f} (J) \n C={C*1e6} ($\\mu$F)  ;  L={L*1e9} (nH)  ;  Diameter={diameter*1e3} (mm)  ;  Length={length*1e3} (mm)  ;  Diameter={diameter*1e3} (mm)')
fig.legend(loc='lower right', bbox_to_anchor=(0.9, 0.15))
plt.grid(True)
plt.tight_layout()
plt.show()