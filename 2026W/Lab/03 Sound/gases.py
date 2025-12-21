from utils import propagate_error

TIME_ERROR = 0.002  # ms
CYLINDER_LENGTH = 1.96  # length of the cylinder [m]


def calc_speed(time):
    return CYLINDER_LENGTH / time


# Air
time_in_air = 5.65e-3  # travel time of the pulse [s]
speed_in_air = CYLINDER_LENGTH / time_in_air
speed_in_air_err = propagate_error(calc_speed, (time_in_air,), (0.002,))
print(f"v_air: {speed_in_air} m/s")

# Helium
time_in_helium = 2.024e-3  # travel time of the pulse [s]
speed_in_helium = CYLINDER_LENGTH / time_in_helium
speed_in_helium_err = propagate_error(calc_speed, (time_in_helium,), (0.002,))
print(f"v_He: {speed_in_helium} m/s")

# CO2
time_in_co2 = (7.236 + 7 + 7.005 + 7.24) / 4 / 1000  # travel time of the pulse [s]
speed_in_co2 = CYLINDER_LENGTH / time_in_co2
speed_in_co2_err = propagate_error(calc_speed, (time_in_co2,), (0.002,))
print(f"v_CO2: {speed_in_co2} m/s")


header = f"{'Gas':<8}{'time (ms)':>12}{'v (m/s)':>14}{'± v (m/s)':>14}"
print(header)
print("-" * len(header))
print(f"{'Air':<8}{time_in_air*1000:12.3f}{speed_in_air:14.2f}{speed_in_air_err:14.2f}")
print(
    f"{'He':<8}{time_in_helium*1000:12.3f}{speed_in_helium:14.2f}{speed_in_helium_err:14.2f}"
)
print(f"{'CO2':<8}{time_in_co2*1000:12.3f}{speed_in_co2:14.2f}{speed_in_co2_err:14.2f}")
