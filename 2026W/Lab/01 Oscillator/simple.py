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

plt.plot(time, ticks, ".", label="data")

amplitude = utils.get_amplitude(ticks)
peak_indices, _ = scipy.signal.find_peaks(ticks)
peaks = ticks[peak_indices]
plt.plot(time[peak_indices], peaks, "^", label="Peaks")


def sine_func(time, amplitude, frequency, phase):
    return amplitude * np.cos(frequency * time + phase)


guess_amplitude = (np.max(ticks) - np.min(ticks)) / 2
guess_frequency = 2 * np.pi / 1
guess_phase = 0
p0 = [guess_amplitude, guess_frequency, guess_phase]

ticks_err = 1/constants.TICKS_PER_METER
popt, pcov = scipy.optimize.curve_fit(sine_func, time, ticks, p0=p0, sigma = ticks_err)
amplitude_fit, frequency_fit, phase_fit = popt
amplitude_error, frequency_error, phase_error = np.sqrt(pcov.diagonal())

print(f"Amplitude = {amplitude_fit * 100:.5f}±{amplitude_error * 100:.5f}cm")
print(f"ω = {frequency_fit:.5f}±{frequency_error:.5f} 1/sec")
print(f"φ = {phase_fit / np.pi:.5f}±{phase_error / np.pi:.5f}π rad")

t_fit = np.linspace(time.min(), time.max(), 1000)
plt.plot(t_fit, sine_func(t_fit, *popt), "r-", label="fit")

plt.legend()
plt.grid()
plt.show()

error = (np.abs(frequency_fit - NATURAL_FREQUENCY) / NATURAL_FREQUENCY) * 100
print(f"Error percentage of frequency from theory: {NATURAL_FREQUENCY_ERROR:.5f}%")
