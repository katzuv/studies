from utils import propagate_error
import autograd.numpy as np

TIME_ERROR = 0.002  # ms
CYLINDER_LENGTH = 1.96  # length of the cylinder [m]


def calc_speed(len, time):
    return len / time


# Air
time_in_air = 5.65e-3  # travel time of the pulse [s]
speed_in_air = CYLINDER_LENGTH / time_in_air
speed_in_air_err = propagate_error(calc_speed, (CYLINDER_LENGTH, time_in_air,), (0.01, 0.002e-3))
print(f"v_air: {speed_in_air} m/s")

# Helium
time_in_helium = 2.024e-3  # travel time of the pulse [s]
speed_in_helium = CYLINDER_LENGTH / time_in_helium
speed_in_helium_err = propagate_error(calc_speed, (CYLINDER_LENGTH, time_in_helium,), (0.01, 0.002e-3))
print(f"v_He: {speed_in_helium} m/s")

# CO2
time_in_co2 = (7.236 + 7 + 7.005 + 7.24) / 4 / 1000  # travel time of the pulse [s]
speed_in_co2 = CYLINDER_LENGTH / time_in_co2
speed_in_co2_err = propagate_error(calc_speed, (CYLINDER_LENGTH, time_in_co2), (0.01, 0.002e-3))
print(f"v_CO2: {speed_in_co2} m/s")


header = f"{'Gas':<8}{'time (ms)':>12}{'v (m/s)':>14}{'± v (m/s)':>14}"
print(header)
print("-" * len(header))
print(f"{'Air':<8}{time_in_air*1000:12.3f}{speed_in_air:14.2f}{speed_in_air_err:14.2f}")
print(
    f"{'He':<8}{time_in_helium*1000:12.3f}{speed_in_helium:14.2f}{speed_in_helium_err:14.2f}"
)
print(f"{'CO2':<8}{time_in_co2*1000:12.3f}{speed_in_co2:14.2f}{speed_in_co2_err:14.2f}")

def theo_speed(gama, const, temp, molar_mass):
    return np.sqrt(gama * const * temp / molar_mass)

temp_1 = 23.62 + 273.15
temp_2 = 23.38 + 273.15
temp_err = 0.01

# Adiabatic index (gamma)
gama_air = 1.40
gama_helium = 1.66
gama_co2 = 1.30

gama_air_err = 0.01
gama_helium_err = 0.01
gama_co2_err = 0.01

# Universal gas constant
const = 8.314  # J/(mol·K)
const_err = 0.001

# Molar masses (kg/mol)
molar_mass_air = 0.02897      # kg/mol
molar_mass_helium = 0.0040026 # kg/mol
molar_mass_co2 = 0.04401      # kg/mol

molar_mass_air_err = 1.0e-5
molar_mass_helium_err = 1.0e-7
molar_mass_co2_err = 1.0e-5

theo_air = theo_speed(gama_air, const, temp_1, molar_mass_air)
theo_helium = theo_speed(gama_helium, const, temp_2, molar_mass_helium)
theo_co2 = theo_speed(gama_co2, const, temp_1, molar_mass_co2)

theo_air_err = propagate_error(theo_speed, (gama_air, const, temp_1, molar_mass_air), (gama_air_err, const_err, temp_err, molar_mass_air_err))
theo_helium_err = propagate_error(theo_speed, (gama_helium, const, temp_2, molar_mass_helium), (gama_helium_err, const_err, temp_err, molar_mass_helium_err))
theo_co2_err = propagate_error(theo_speed, (gama_co2, const, temp_1, molar_mass_co2), (gama_co2_err, const_err, temp_err, molar_mass_co2_err))

print(f"the theoretical speed of sound in air is {theo_air:.2f} ± {theo_air_err:.2f} [m/s]")
print(f"the theoretical speed of sound in Helium is {theo_helium:.2f} ± {theo_helium_err:.2f} [m/s]")
print(f"the theoretical speed of sound in CO2 is {theo_co2:.2f} ± {theo_co2_err:.2f} [m/s]")