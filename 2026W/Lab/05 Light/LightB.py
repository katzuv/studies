import numpy
import scipy
from matplotlib import pyplot as plt
import utils

# System parameters
INTERFEROMETER_LENGTH = 0.24
LENGTH_ERROR = 5 / 1000
LASER_WAVELENGTH = 532e-9
TEMPERATURE = 25 + scipy.constants.zero_Celsius
TEMPERATURE_ERROR = 1  # in Kelvin

PRESSURE_ERROR = 1 * scipy.constants.mmHg / 1000  # in kPa
NUMBER_ERROR = 1

i = 0


# --- NEW FUNCTION START ---
def print_statistical_analysis(gas_name, measured_val, measured_err, lit_val):
    """
    Performs a statistical comparison between measured and literature values
    based on the 'Comparison Test' in the Data Analysis Booklet.
    """
    print(f"\n--- Analysis for {gas_name} ---")
    print(f"Measured n:   {measured_val:.8f} ± {measured_err:.8e}")

    if lit_val is None:
        print("Literature n: Not available for comparison.")
        return

    print(f"Literature n: {lit_val:.8f}")

    # Calculate Z-Score (Distance in Standard Deviations)
    # This quantifies the difference in terms of your error margins.
    diff = abs(measured_val - lit_val)
    z_score = diff / measured_err

    print(f"Difference:   {diff:.8e}")
    print(f"Z-Score:      {z_score:.2f}σ")
    # Calculate error relative to the refractivity (n-1)
    refractivity_lit = lit_val - 1
    print(f"Percentage error on (n-1): {diff / refractivity_lit:.2%}")

    # Decision Rule: 95% Confidence Interval corresponds to approx 2 sigma [cite: 297]
    if z_score < 2.0:
        print(
            "CONCLUSION:   CONSISTENT. The literature value is within the 95% Confidence Interval."
        )
        print(
            "              (The difference is statistically insignificant [cite: 310])"
        )
    else:
        print("CONCLUSION:   SIGNIFICANT DEVIATION (>2σ).")
        print(
            "              (The values are distinct; systematic error likely [cite: 311])"
        )


# --- NEW FUNCTION END ---


def calc_refraction(slope, temperature, interferometer_length):
    alpha = (
        2
        * LASER_WAVELENGTH
        * scipy.constants.Boltzmann
        * temperature
        * slope
        / interferometer_length
    )
    return 1 + 0.5 * alpha * (760 * scipy.constants.mmHg / 1000) / (
        scipy.constants.Boltzmann * temperature
    )


def process_gas(pressure, number, gas_name, lit_val):  # <--- Updated arguments
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
    )

    i += 1

    refraction = calc_refraction(slope, TEMPERATURE, INTERFEROMETER_LENGTH)
    refraction_err = utils.propagate_error(
        calc_refraction,
        (slope, TEMPERATURE, INTERFEROMETER_LENGTH),
        (std_err, TEMPERATURE_ERROR, LENGTH_ERROR),
    )

    # --- REPLACED OLD PRINT WITH NEW ANALYSIS ---
    print_statistical_analysis(gas_name, refraction, refraction_err, lit_val)
    print(f"R²: {r_value:.4f}")


# --- UPDATED DATA WITH LITERATURE VALUES ---
DATA = [
    (
        (16, 71, 132, 198, 254, 312, 379, 432, 500, 557, 620, 686, 744),
        [a * 10 for a in range(13)],
        "Air",
        1.0002926,  # Literature Value
    ),
    (
        (358, 419, 479, 540, 609, 678, 751),
        [a * 10 for a in range(7)],
        "Mix (CO2 + He)",
        None,  # No Literature Value
    ),
    (
        (15, 65, 106, 139, 183, 218, 258, 300, 338, 378, 415, 456, 496, 533, 585, 628),
        [a * 10 for a in range(16)],
        "CO2",
        1.00045,  # Literature Value
    ),
    (
        (20, 178, 357, 526, 696),
        [a * 5 for a in range(5)],
        "He",
        1.000036,  # Literature Value
    ),
]

# --- UPDATED LOOP ---
for pressure, number, gas_name, lit_val in DATA:
    process_gas(numpy.array(pressure), numpy.array(number), gas_name, lit_val)

plt.xlabel("Pressure [kPa]")
plt.ylabel("number of fringes")
plt.legend()
plt.grid()
plt.savefig("graph.svg", format="svg")
plt.show()
