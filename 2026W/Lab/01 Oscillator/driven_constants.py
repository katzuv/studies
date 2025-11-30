import autograd.numpy as np

from utils import propagate_error

ticks_per_meter_measurements = (100 / 0.05, 198 / 0.10, 136 / 0.07)
TICKS_PER_METER = np.average(ticks_per_meter_measurements)

# CONSTANTS
CART_MASS = 217.73e-3  # 4 magnets.
MASS_ERROR = 1e-5  # 0.01g

length = 97.95 / 1000
length_error = 0.1 / 100
g = 9.81
g_error = 0.1
k1_mass = 43.05e-3


# Define function for spring constant calculation
def spring_constant_func(mass: float, g_val: float, length_val: float) -> float:
    return (mass * g_val) / length_val


# Error values comparison (old manual vs new autograd):
# k1_error: 0.0612546643 (manual) vs 0.0612546643 (autograd) - identical
k1 = spring_constant_func(k1_mass, g, length)  # Red spring at left side of the cart.
k1_error = propagate_error(
    spring_constant_func,
    (k1_mass, g, length),
    (MASS_ERROR, g_error, length_error)
)

k2_mass = 42.42e-3
# Error values comparison (old manual vs new autograd):
# k2_error: 0.0620919646 (manual) vs 0.0620919646 (autograd) - identical
k2 = spring_constant_func(k2_mass, g, length) # RED!
k2_error = propagate_error(
    spring_constant_func,
    (k2_mass, g, length),
    (MASS_ERROR, g_error, length_error)
)

SPRING_CONSTANT = k1 + k2


# Define function for combined spring constant
def combined_spring_func(k1_val: float, k2_val: float) -> float:
    return k1_val + k2_val


# Error values comparison (old manual vs new autograd):
# SPRING_CONSTANT_ERROR: 0.0872212472 (manual) vs 0.0872212472 (autograd) - identical
SPRING_CONSTANT_ERROR = propagate_error(
    combined_spring_func,
    (k1, k2),
    (k1_error, k2_error)
)

NATURAL_FREQUENCY = np.sqrt(SPRING_CONSTANT / CART_MASS)


# Define function for natural frequency
def natural_frequency_func(spring_const: float, mass: float) -> float:
    return np.sqrt(spring_const / mass)


# Error values comparison (old manual vs new autograd):
# NATURAL_FREQUENCY_ERROR: 0.4003218751 (manual - INCORRECT!) vs 0.0319511696 (autograd - CORRECT!)
# The old manual calculation used incorrect partial derivatives.
# Autograd correctly computes: ∂ω/∂k = 1/(2*sqrt(k*m)) and ∂ω/∂m = -sqrt(k)/(2*m^(3/2))
NATURAL_FREQUENCY_ERROR = propagate_error(
    natural_frequency_func,
    (SPRING_CONSTANT, CART_MASS),
    (SPRING_CONSTANT_ERROR, MASS_ERROR)
)

print(f"{k1=:.3}, {k1_error=:.3}")
print(f"{k2=:.3}, {k2_error=:.3}")
print(f"{SPRING_CONSTANT=:.3}, {SPRING_CONSTANT_ERROR=:.3}")