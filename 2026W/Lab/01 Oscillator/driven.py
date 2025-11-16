from pathlib import Path

import matplotlib.pyplot as plt
import autograd.numpy as np
import pandas as pd
import scipy

import driven_constants
import utils
import damped


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
    return ticks - np.mean(ticks)


def amplitude_ratio_model(frequency, spring_constant, mass, natural_frequency, tau):
    under_root = (natural_frequency ** 2 - frequency ** 2) ** 2 + (frequency / tau) ** 2
    return (spring_constant / mass) * 1 / np.sqrt(under_root)


def parse_single_run(file_path: Path):
    data = pd.read_csv(utils.get_edited_driven_data_path(file_path))
    # motor_ticks = normalize_ticks(data["ticks_a"]) / driven_constants.TICKS_PER_METER
    motor_ticks = normalize_ticks(data["ticks_a"]) / driven_constants.TICKS_PER_METER
    # mass_ticks = normalize_ticks(data["ticks_b"])
    mass_ticks = data["ticks_b"] / driven_constants.TICKS_PER_METER
    time = data["time"]

    # plt.title(file_path)
    # plt.plot(time, motor_ticks, ".", label="motor ticks")
    # plt.plot(time, mass_ticks, ".", label="mass ticks")
    # plt.legend()
    # plt.grid()

    # Find motor frequency
    peak_indices, _ = scipy.signal.find_peaks(motor_ticks, distance=100)
    # plt.plot(time[peak_indices], motor_ticks[peak_indices], "^", label="Peaks")
    frequency = (2 * np.pi) / (np.average(np.diff(peak_indices * (time[1]-time[0]))))

    # plt.show()

    motor_amplitude = utils.get_amplitude(motor_ticks)
    mass_amplitude = utils.get_amplitude(mass_ticks)
    amplitude_ratio = mass_amplitude/motor_amplitude
    frequencies = np.linspace(0, driven_constants.NATURAL_FREQUENCY, len(motor_ticks))
    # ratio =
    return amplitude_ratio, frequency, motor_ticks, mass_ticks


amplitude_ratios = []
frequencies = []
file_paths = []
for file_path in Path("driven_data").iterdir():
    if file_path.suffix == ".csv":
        continue
    # path = utils.get_edited_driven_data_path(file_path)
    # print(file_path)
    parsed = parse_single_run(file_path)
    amplitude_ratios.append(parsed[0])
    frequencies.append(parsed[1])
    file_paths.append(file_path.name)
frequencies/=driven_constants.NATURAL_FREQUENCY
for x, y, label in zip(frequencies, amplitude_ratios, file_paths):
    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')  # small label
plt.plot(frequencies, amplitude_ratios,'.',)
lin = np.linspace(0, driven_constants.NATURAL_FREQUENCY*2, 2000)
plt.plot(lin/driven_constants.NATURAL_FREQUENCY, amplitude_ratio_model(lin, driven_constants.k2, driven_constants.CART_MASS, driven_constants.NATURAL_FREQUENCY, 2.72074))
plt.grid()
plt.show()
