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
