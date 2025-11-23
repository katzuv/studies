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
    motor_peak_indices, _ = scipy.signal.find_peaks(motor_ticks, distance=100)
    mass_peak_indices, _ = scipy.signal.find_peaks(mass_ticks, distance=100)
    # diff = np.mean(motor_peak_indices - mass_peak_indices)
    diff = (2*np.pi)/((motor_peak_indices[0] - mass_peak_indices[0])*(time[1] - time[0]))
    # plt.plot(time[motor_peak_indices], motor_ticks[motor_peak_indices], "^", label="Peaks")
    p = (np.average(np.diff(motor_peak_indices * (time[1] - time[0]))))
    frequency = (2 * np.pi) / p
    p_err = (time[1] - time[0]) / np.sqrt(len(np.diff(motor_peak_indices)))
    frequency_err = (2 * np.pi * p_err) / p**2
    zc = np.where(np.diff(np.sign(motor_ticks)) != 0)[0]
    t_zc = time[zc]
    period = 2 * np.mean(np.diff(t_zc))  # full period = 2 crossings
    period_err = 2 * (time[1]-time[0])/np.sqrt(len(np.diff(t_zc)))
    f = 1 / period
    f_err = period_err / period**2
    # compute phases
    phi_motor = np.arctan2(np.sum(motor_ticks * np.cos(2 * np.pi * f * time)),
                           np.sum(motor_ticks * np.sin(2 * np.pi * f * time)))

    phi_mass = np.arctan2(np.sum(mass_ticks * np.cos(2 * np.pi * f * time)),
                          np.sum(mass_ticks * np.sin(2 * np.pi * f * time)))

    # phase difference in radians normalized to [0, 2pi]
    phase_diff = (phi_mass - phi_motor) % (2 * np.pi)

    # plt.show()

    motor_amplitude = utils.get_amplitude(motor_ticks)
    mass_amplitude = utils.get_amplitude(mass_ticks)
    amplitude_ratio = mass_amplitude / motor_amplitude
    frequencies = np.linspace(0, driven_constants.NATURAL_FREQUENCY, len(motor_ticks))
    # ratio =
    return amplitude_ratio, frequency, -phase_diff + np.pi, motor_ticks, mass_ticks, frequency_err


amplitude_ratios = []
frequencies = []
diffs = []
file_paths = []
frequencies_errs = []
for file_path in Path("driven_data").iterdir():
    if file_path.suffix == ".csv":
        continue
    # path = utils.get_edited_driven_data_path(file_path)
    # print(file_path)
    parsed = parse_single_run(file_path)
    amplitude_ratios.append(parsed[0])
    frequencies.append(parsed[1])
    diffs.append(parsed[2])
    frequencies_errs.append(parsed[5])
    file_paths.append(file_path.name)
frequencies_errs = np.sqrt((frequencies_errs**2)/(driven_constants.NATURAL_FREQUENCY**2) +
                           ((frequencies/driven_constants.NATURAL_FREQUENCY)**2)*
                           driven_constants.NATURAL_FREQUENCY_ERROR**2)
frequencies /= driven_constants.NATURAL_FREQUENCY
for x, y, label in zip(frequencies, amplitude_ratios, file_paths):
    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')  # small label
plt.plot(frequencies, amplitude_ratios, '.', )
lin = np.linspace(0, driven_constants.NATURAL_FREQUENCY * 2, 2000)
plt.plot(lin / driven_constants.NATURAL_FREQUENCY,
         amplitude_ratio_model(lin, driven_constants.k2, driven_constants.CART_MASS, driven_constants.NATURAL_FREQUENCY,
                               2.72074))
plt.grid()
plt.show()


def phase_diff_model(motor_frequency, natural_frequency, tau):
    denominator = tau * (natural_frequency ** 2 - motor_frequency ** 2)
    a = np.arctan(-motor_frequency / denominator)
    if motor_frequency < natural_frequency:
        a += np.pi
    return -a

plt.plot(frequencies, diffs, '.', )
lin = np.linspace(0, driven_constants.NATURAL_FREQUENCY * 2, 2000)
phase_diff = [phase_diff_model(freq, driven_constants.NATURAL_FREQUENCY, 2.72074) for freq in lin]
plt.plot(lin / driven_constants.NATURAL_FREQUENCY, phase_diff)
plt.grid()
plt.show()
