import sys

import numpy as np

sys.path.append("../utils.py")
import utils

LEFT_CART_MASS = 222.55e-3  # 5 magnets.
RIGHT_CART_MASS = 223.93e-3  # 5 magnets.
MASS_ERROR = 1e-5  # 0.01g

length = 9.8 / 100
length_error = 0.1 / 100
g = 9.81
g_error = 0.1
k1_mass = 42.15e-3
k2_mass = 42.85e-3
k3_mass = 42.70e-3

def spring_constant(mass, gravity, length_diff):
    return (mass * gravity) / length_diff

K1_CONSTANT = spring_constant(k1_mass, g, length)
K2_CONSTANT = spring_constant(k2_mass, g, length)
K3_CONSTANT = spring_constant(k3_mass, g, length)
K1_ERROR = utils.propagate_error(spring_constant, (k1_mass, g, length), (MASS_ERROR, g_error, length_error))
K2_ERROR = utils.propagate_error(spring_constant, (k2_mass, g, length), (MASS_ERROR, g_error, length_error))
K3_ERROR = utils.propagate_error(spring_constant, (k3_mass, g, length), (MASS_ERROR, g_error, length_error))
K_AVG = (K1_CONSTANT+K2_CONSTANT+K3_CONSTANT)/3
K_AVG_ERROR = (K1_ERROR+K2_ERROR+K3_ERROR)/3
print(K1_CONSTANT, K2_CONSTANT, K3_CONSTANT)
print(K1_ERROR, K2_ERROR, K3_ERROR)
print(K_AVG, K_AVG_ERROR)

ticks_per_meter_measurements = (178 / 0.09, 100 / 0.05, 140 / 0.07)
TICKS_PER_CM = np.average(ticks_per_meter_measurements) / 100
TICKS_PER_CM_ERROR = np.average(ticks_per_meter_measurements) / 100