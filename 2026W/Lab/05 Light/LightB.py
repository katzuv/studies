import numpy
import scipy
from matplotlib import pyplot as plt

import utils

# System parameters
INTERFEROMETER_LENGTH = 0.2
LASER_WAVELENGTH = 532e-9
TEMPERATURE = 25 + scipy.constants.zero_Celsius

PRESSURE_ERROR = 5 / 1000  # in kPa
NUMBER_ERROR = 1

i = 0


def calc_refraction(slope):
    alpha = (
        2
        * LASER_WAVELENGTH
        * scipy.constants.Boltzmann
        * scipy.constants.zero_Celsius
        * slope
        / INTERFEROMETER_LENGTH
    )
    return 1 + 0.5 * alpha * (760 * scipy.constants.mmHg / 1000) / (
        scipy.constants.Boltzmann * scipy.constants.zero_Celsius
    )


def process_gas(pressure, number, gas_name):
    pressure = pressure * scipy.constants.mmHg / 1000
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(
        pressure, number
    )
    plt.errorbar(
        pressure,
        number,
        xerr=PRESSURE_ERROR,
        yerr=NUMBER_ERROR,
        fmt=".",
        label=gas_name,
    )

    lin = numpy.linspace(0, max(pressure), 100)
    global i
    plt.plot(
        lin,
        slope * lin + intercept,
        color=f"C{i}",
        # label=f"Linear regression ({gas_name})",
    )

    i += 1

    refraction = calc_refraction(slope)
    refraction_err = utils.propagate_error(calc_refraction, (slope,), (std_err,))
    print(f"Refraction index of {gas_name}: {refraction:.8f} ± {refraction_err:.8f}")


DATA = [
    (
        (16, 71, 132, 198, 254, 312, 379, 432, 500, 557, 620, 686, 744),
        [a * 10 for a in range(13)],
        "Air",
    ),
    (
        (358, 419, 479, 540, 609, 678, 751),
        [a * 10 for a in range(7)],
        "mix (CO2 + He)",
    ),
    (
        (15, 65, 106, 139, 183, 218, 258, 300, 338, 378, 415, 456, 496, 533, 585, 628),
        [a * 10 for a in range(16)],
        "CO2",
    ),
    (
        (
            20,
            178,
            357,
            526,
            696,
        ),
        [a * 5 for a in range(5)],
        "He",
    ),
]

for pressure, number, gas_name in DATA:
    process_gas(numpy.array(pressure), numpy.array(number), gas_name)

plt.xlabel("Pressure [kPa]")
plt.ylabel("number of fringes")
plt.legend()
plt.grid()
plt.show()
