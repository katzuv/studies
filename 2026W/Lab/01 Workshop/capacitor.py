import scipy

eps0 = scipy.constants.epsilon_0  # F/m
plate_diameter = 18e-2  # m
distance = 0.5e-3  # m

theoretical_capacitance = (
    eps0 * scipy.constants.pi * (plate_diameter**2) / (4 * distance)
)
print(f"{theoretical_capacitance=:.3e}")
