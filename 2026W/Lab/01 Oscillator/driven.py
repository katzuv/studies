from pathlib import Path

import matplotlib.pyplot as plt
import autograd.numpy as np
import pandas as pd
import scipy

import constants
import utils
from constants import NATURAL_FREQUENCY


# path = utils.get_edited_data_path(Path("driven_1.txt"), start_index=239)
# # path = "damped.csv"
# data = pd.read_csv(path)
#
# ticks = data["ticks"]
# time = data["time"]
# ticks /= constants.TICKS_PER_METER
#
# plt.plot(time, ticks, ".", label="data")


def normalize_ticks(ticks):
    peak_indices, _ = scipy.signal.find_peaks(ticks)
    peak_average = np.average(ticks[peak_indices])
    valley_indices, _ = scipy.signal.find_peaks(-ticks)
    valley_average = -np.average(ticks[valley_indices])

    mid = (peak_average + valley_average) / 2
    return ticks - mid


def amplitude_ratio_model(frequency, spring_constant, mass, natural_frequency, tau):
    under_root = (natural_frequency ** 2 - frequency ** 2) ** 2 + (frequency / tau) ** 2
    return (spring_constant / mass) * 1 / np.root(under_root)


def parse_single_run(file_path: Path):
    data = pd.read_csv(utils.get_edited_driven_data_path(file_path))
    motor_ticks = normalize_ticks(data["ticks_a"])
    # mass_ticks = normalize_ticks(data["ticks_b"])
    mass_ticks = data["ticks_b"]
    time = data["time"]

    plt.title(file_path)
    plt.plot(time, motor_ticks, ".", label="motor ticks")
    plt.plot(time, mass_ticks, ".", label="mass ticks")
    plt.legend()
    plt.grid()
    plt.show()

    # Find motor frequency
    peak_indices, _ = scipy.signal.find_peaks(motor_ticks)
    frequency = (2 * np.pi) / (np.mean(np.diff(peak_indices * (time[1]-time[0]))))

    motor_amplitude = utils.get_amplitude(motor_ticks)
    mass_amplitude = utils.get_amplitude(mass_ticks)
    amplitude_ratio = mass_amplitude/motor_amplitude
    frequencies = np.linspace(0, constants.NATURAL_FREQUENCY, len(motor_ticks))
    # ratio =
    if 7.5<amplitude_ratio<8.5
    return amplitude_ratio, frequency, motor_ticks, mass_ticks


amplitude_ratios = []
frequencies = []
for file_path in Path("driven_data").iterdir():
    # break
    if file_path.suffix == ".csv":
        continue
    # path = utils.get_edited_driven_data_path(file_path)
    print(file_path)
    parsed = parse_single_run(file_path)
    amplitude_ratios.append(parsed[0])
    frequencies.append(parsed[1])

plt.plot(frequencies, amplitude_ratios,'.',)
plt.grid()
plt.show()

# peak_indices, _ = scipy.signal.find_peaks(ticks)
# peaks = ticks[peak_indices]
# amplitude = round(np.mean(np.abs(peaks)) * 100, 3)
# print(f"{amplitude=}cm")
# plt.plot(time[peak_indices], peaks, "^", label="Peaks")


# process_single_run(Path("driven_data", "4.8.txt"))
