import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import sklearn

eps0 = scipy.constants.epsilon_0  # F/m
plate_diameter = 18e-2  # m
distance = 0.5e-3  # m

theoretical_capacitance = (
    eps0 * scipy.constants.pi * (plate_diameter**2) / (4 * distance)
)
print(f"{theoretical_capacitance=:.3e}")

resistance = 977  # Ohm
total_resistance = 38.4e3  # Ohm
theoretical_time_constant = total_resistance * theoretical_capacitance
print(f"{theoretical_time_constant=:.3e}")

capacitor_data = pd.read_csv("capacitor.csv")
capacitor_data = capacitor_data.rename(
    columns={"time (sec)": "time", "ch2": "resistor_voltage"}
)
capacitor_data.capacitor_voltage = capacitor_data.ch1 - capacitor_data.resistor_voltage
plt.plot(
    capacitor_data.time * 1e6,
    capacitor_data.capacitor_voltage,
    label="Capacitor voltage [V]",
)
plt.xlabel("Time [μs]")
plt.ylabel("Voltage [V]")
plt.legend()
plt.grid()
plt.show()


# Implementing curve fit -- finding an analytical function that closely fits the real data.
def voltage_decay(time, time_constant, initial_voltage):
    return initial_voltage * np.exp(-time / time_constant)


p_optimal, p_covariance = scipy.optimize.curve_fit(
    voltage_decay, capacitor_data.time, capacitor_data.capacitor_voltage, p0=(3e-6, 4)
)
fit_time_constant, fit_initial_voltage = p_optimal
# Get errors by calculating square roots of the standard deviations.
p_errors = np.sqrt(np.diag(p_covariance))
time_constant_err, initial_voltage_err = p_errors
print(f"Time constant: {fit_time_constant:.10f} ± {time_constant_err:.10f}")
print(f"Initial voltage: {fit_initial_voltage:.10f} ± {initial_voltage_err:.10f}")

data_from_fit = voltage_decay(
    capacitor_data.time, fit_time_constant, fit_initial_voltage
)
plt.plot(
    capacitor_data.time * 1e6,
    data_from_fit,
    label="Fit curve",
)
plt.show()

r2 = sklearn.metrics.r2_score(capacitor_data.capacitor_voltage, data_from_fit)
print(f"R² = {r2:.4f}")  # 0.99 is very high!

linear_time_range = (capacitor_data.time >= 0) & (capacitor_data.time <= 5e-5)
plt.plot(
    capacitor_data.time[linear_time_range],
    np.log(capacitor_data.capacitor_voltage[linear_time_range]),
    ".",
    label=r"$\ln(V)$",
)
