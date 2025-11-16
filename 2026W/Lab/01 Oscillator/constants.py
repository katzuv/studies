import autograd.numpy as np

from utils import propagate_error

ticks_per_meter_measurements = (178 / 0.09, 100 / 0.05, 140 / 0.07)
TICKS_PER_METER = np.average(ticks_per_meter_measurements)

# CONSTANTS
CART_MASS = 217.88e-3  # 4 magnets.
MASS_ERROR = 1e-5  # 0.01g

length = 9.8 / 100
length_error = 0.1 / 100
g = 9.81
g_error = 0.1
k1_mass = 42.42e-3


# Define function for spring constant calculation
def spring_constant_func(mass, g_val, length_val):
    return (mass * g_val) / length_val


k1 = spring_constant_func(k1_mass, g, length)  # Red spring at left side of the cart.
k1_error = propagate_error(
    spring_constant_func,
    (k1_mass, g, length),
    (MASS_ERROR, g_error, length_error)
)

k2_mass = 43e-3
k2 = spring_constant_func(k2_mass, g, length)
k2_error = propagate_error(
    spring_constant_func,
    (k2_mass, g, length),
    (MASS_ERROR, g_error, length_error)
)

SPRING_CONSTANT = k1 + k2


# Define function for combined spring constant
def combined_spring_func(k1_val, k2_val):
    return k1_val + k2_val


SPRING_CONSTANT_ERROR = propagate_error(
    combined_spring_func,
    (k1, k2),
    (k1_error, k2_error)
)

NATURAL_FREQUENCY = np.sqrt(SPRING_CONSTANT / CART_MASS)


# Define function for natural frequency
def natural_frequency_func(spring_const, mass):
    return np.sqrt(spring_const / mass)


NATURAL_FREQUENCY_ERROR = propagate_error(
    natural_frequency_func,
    (SPRING_CONSTANT, CART_MASS),
    (SPRING_CONSTANT_ERROR, MASS_ERROR)
)
