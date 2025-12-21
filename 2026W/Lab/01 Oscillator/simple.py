import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

import constants
import utils
from constants import NATURAL_FREQUENCY, NATURAL_FREQUENCY_ERROR

# path = utils.get_edited_data_path(Path("simple.txt"), start_index=486)
path = "simple.csv"
data = pd.read_csv("simple.csv")

ticks = data["ticks"]
time = data["time"]
ticks /= constants.TICKS_PER_METER

plt.errorbar(time, ticks * 100, yerr=constants.TICKS_PER_METER_ERROR * 100, fmt=".", label="Measurements", ecolor='gray',
         elinewidth=1, capsize=2)

amplitude = utils.get_amplitude(ticks)
peak_indices, _ = scipy.signal.find_peaks(ticks)
peaks = ticks.values[peak_indices] * 100
peak1, peak2 = peaks[0], peaks[-1]
print(f"{peak1=:.2f}, {peak2=:.2f}, {((peak1-peak2)/peak1) * 100:.2f}%")

# plt.plot(time[peak_indices], peaks, "^", label="Peaks")


def sine_func(time, amplitude, frequency, phase):
    return amplitude * np.cos(frequency * time + phase)


guess_amplitude = (np.max(ticks) - np.min(ticks)) / 2
guess_frequency = 2 * np.pi / 1
guess_phase = 0
p0 = [guess_amplitude, guess_frequency, guess_phase]

ticks_err = 1 / constants.TICKS_PER_METER
popt, pcov = scipy.optimize.curve_fit(sine_func, time, ticks, p0=p0, sigma=ticks_err)
amplitude_fit, frequency_fit, phase_fit = popt
amplitude_error, frequency_error, phase_error = np.sqrt(pcov.diagonal())

print(f"Amplitude = {amplitude_fit * 100:.2f}±{amplitude_error * 100:.5e}cm")
print(f"ω = {frequency_fit:.2f}±{frequency_error:.5e} 1/sec")
print(f"φ = {phase_fit / np.pi:.2f}±{phase_error / np.pi:.5e}π rad")

t_fit = np.linspace(time.min(), time.max(), 1000)
plt.plot(t_fit, sine_func(t_fit, *popt) * 100, "r-", label="Fit", zorder=3)

plt.legend()
plt.grid()
plt.xlabel("Time [s]")
plt.ylabel("Distance from equilibrium [cm]")
plt.savefig("simple.svg", format="svg")
plt.show()

error = (np.abs(frequency_fit - NATURAL_FREQUENCY) / NATURAL_FREQUENCY) * 100
print(f"Theory: {NATURAL_FREQUENCY}±{NATURAL_FREQUENCY_ERROR} | Error percentage of frequency from theory: {error:.2f}%")

fitted = sine_func(time, *popt)
residuals = ticks - fitted
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((ticks - np.mean(ticks)) ** 2)
r_squared = 1 - ss_res / ss_tot

print(f"R^2 = {r_squared:.6f}")
