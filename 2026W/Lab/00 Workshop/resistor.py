import pandas as pd
import scipy.integrate


def get_current(voltage2, resistance1):
    return voltage2 / resistance1


def get_resistor_voltage(voltage1, voltage2):
    return voltage1 - voltage2


def get_resistor_resistance(voltage, current):
    return voltage / current


def get_resistor_power(voltage, current):
    return voltage * current


def get_resistor_energy(power, time):
    return scipy.integrate.cumulative_trapezoid(power, time)


data = pd.read_csv("ohm.csv", header=1, usecols=range(3, 6))
data.time = data["Time (s)"]
data.voltage1 = data["1 (VOLT)"]
data.voltage2 = data["2 (VOLT)"]
