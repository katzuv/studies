from cmath import phase
from pathlib import Path

import matplotlib.pyplot as plt
import autograd.numpy as np
import pandas as pd
import scipy
import constants
import driven_constants
import utils
import simple
from simple import ticks_err


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

def amplitude_ratio_model_cfit(frequency, spring_con_per_mass, natural_frequency, tau):
    under_root = (natural_frequency ** 2 - frequency ** 2) ** 2 + (frequency / tau) ** 2
    return spring_con_per_mass / under_root

def parse_single_run(file_path: Path):
    data = pd.read_csv(utils.get_edited_driven_data_path(file_path))
    # motor_ticks = normalize_ticks(data["ticks_a"]) / driven_constants.TICKS_PER_METER
    motor_ticks = normalize_ticks(data["ticks_a"]) / driven_constants.TICKS_PER_METER
    # mass_ticks = normalize_ticks(data["ticks_b"])
    mass_ticks = data["ticks_b"] / driven_constants.TICKS_PER_METER
    time = data["time"]

    # plt.title(file_path)
    #plt.plot(time, motor_ticks, "-", label="motor ticks" + str(file_path))
    # plt.legend()
    # plt.grid()

    # Find motor frequency
    motor_peak_indices, _ = scipy.signal.find_peaks(motor_ticks, distance=100)
    mass_peak_indices, _ = scipy.signal.find_peaks(mass_ticks, distance=100)
    # diff = np.mean(motor_peak_indices - mass_peak_indices)
    diff = (2*np.pi)/((motor_peak_indices[0] - mass_peak_indices[0])*(time[1] - time[0]))
    p = (np.average(np.diff(motor_peak_indices * (time[1] - time[0]))))
    frequency = (2 * np.pi) / p
    p_err = (time[1] - time[0]) / np.sqrt(len(np.diff(motor_peak_indices)))
    frequency_err = (2 * np.pi * p_err) / p**2
    zc = np.where(np.diff(np.sign(motor_ticks)) != 0)[0]
    t_zc = time[zc]
    period = 2 * np.mean(np.diff(t_zc))  # full period = 2 crossings
    period_err = 2 * (time[1]-time[0])/np.sqrt(len(np.diff(t_zc)))
    f = 2*np.pi / period
    f_err = period_err*2*np.pi / period**2
    # compute phases
    #plt.plot(time, mass_ticks, ".", label=str(np.round(100*f)/100))
    phi_motor_guess = np.arctan2(np.sum(motor_ticks * np.cos(2 * np.pi * f * time)),
                           np.sum(motor_ticks * np.sin(2 * np.pi * f * time)))

    phi_mass_guess = np.arctan2(np.sum(mass_ticks * np.cos(2 * np.pi * f * time)),
                          np.sum(mass_ticks * np.sin(2 * np.pi * f * time)))
    motor_amplitude_guess, motor_a_err_guess = utils.get_amplitude(motor_ticks)
    mass_amplitude_guess, mass_a_err_guess = utils.get_amplitude(mass_ticks)
    p0_ma = np.array([motor_amplitude_guess, f, phi_mass_guess])
    p0_mo = np.array([mass_amplitude_guess, f, phi_motor_guess])
    mass_parameters, popt_ma = scipy.optimize.curve_fit(simple.sine_func, time, mass_ticks, p0 = p0_ma,
                                                                      sigma = ticks_err)
    motor_parameters, popt_mo = scipy.optimize.curve_fit(simple.sine_func, time, motor_ticks, p0 = p0_mo,
                                                                        sigma = ticks_err)
    if (mass_parameters[0]<0):
        mass_parameters[0] = -mass_parameters[0]
        mass_parameters[2] = mass_parameters[2] - np.pi
    if (motor_parameters[0]<0):
        motor_parameters[0] = -motor_parameters[0]
        motor_parameters[2] = motor_parameters[2] - np.pi
    mass_parameters_err = np.sqrt(np.diag(popt_ma))
    motor_parameters_err = np.sqrt(np.diag(popt_mo))
    # phase difference in radians normalized to [0, 2pi]
    phase_diff = (mass_parameters[2] - motor_parameters[2]) % (2 * np.pi)


    #amplitude_ratio_guess= mass_amplitude_guess / motor_amplitude_guess
    #amplitude_ratio_err = np.sqrt(mass_a_err_guess**2 / motor_amplitude_guess**2 +
    #                              (mass_amplitude_guess**2)*(motor_a_err_guess**2)/motor_amplitude_guess**2)
    amplitude_ratio = mass_parameters[0]/motor_parameters[0]
    amplitude_ratio_err = np.sqrt(mass_parameters_err[0] ** 2 / motor_parameters[0] ** 2 +
                                  (mass_parameters[0] ** 2) * (motor_parameters_err[0] ** 4) / motor_parameters[0] ** 2)
    frequencies = np.linspace(0, driven_constants.NATURAL_FREQUENCY, len(motor_ticks))
    phase_diff_err = np.sqrt((mass_parameters[2]*mass_parameters_err[2]) ** 2 +
                          (motor_parameters[2]*motor_parameters_err[2]) ** 2)
    # ratio =
    return (amplitude_ratio, motor_parameters[1], -phase_diff + np.pi, motor_ticks, mass_ticks,
            motor_parameters_err[1], amplitude_ratio_err, phase_diff_err)


amplitude_ratios = []
amplitude_ratios_err = []
frequencies = []
diffs = []
file_paths = []
frequencies_errs = []
diffs_err = []
for file_path in Path("driven_data").iterdir():
    if (file_path.suffix == ".csv"):
        continue
    # path = utils.get_edited_driven_data_path(file_path)
    # print(file_path)
    parsed = parse_single_run(file_path)
    amplitude_ratios.append(parsed[0])
    frequencies.append(parsed[1])
    diffs.append(parsed[2])
    frequencies_errs.append(parsed[5])
    amplitude_ratios_err.append(parsed[6])
    diffs_err.append(parsed[7])
    file_paths.append(file_path.name)
frequencies = np.array(frequencies)
frequencies_errs = np.array(frequencies_errs)
for x, y, label in zip(frequencies, amplitude_ratios, file_paths):
    plt.text(x, y, label, fontsize=8, ha='right', va='bottom')  # small label

# frequency to amplitude graph
plt.errorbar(frequencies, amplitude_ratios,xerr= frequencies_errs ,yerr = amplitude_ratios_err,
             fmt = '.', label = "results")
p0_amp = np.array([driven_constants.k1 / driven_constants.CART_MASS, driven_constants.NATURAL_FREQUENCY,
                   2.72074])
amp_fit, popt_amp = scipy.optimize.curve_fit(amplitude_ratio_model_cfit, frequencies, amplitude_ratios,
                                                sigma = amplitude_ratios_err, p0 = p0_amp)
amp_fit_err = np.sqrt(np.diag(popt_amp))
lin = np.linspace(0, driven_constants.NATURAL_FREQUENCY * 2, 2000)
#plt.plot(lin,
#         amplitude_ratio_model(lin, driven_constants.k2, driven_constants.CART_MASS, driven_constants.NATURAL_FREQUENCY,
#                               2.72074), '-', label = "theoretical curve")
plt.plot(lin, amplitude_ratio_model_cfit(lin, amp_fit[0], amp_fit[1], amp_fit[2]), '--', label = "fit")
plt.grid()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude ratio [a.u.]")
plt.legend()
plt.show()

# frequency to phase graph

def phase_diff_model(motor_frequency, natural_frequency, tau):
    return np.arctan2(
        motor_frequency / tau,
        natural_frequency**2 - motor_frequency**2
    ) - np.pi

p0_diff = np.array([driven_constants.NATURAL_FREQUENCY, 2.72074])
bounds_diff = [(0, 0), (driven_constants.NATURAL_FREQUENCY*3, 2.72074*3)]
fit_diff, popt_diff = scipy.optimize.curve_fit(phase_diff_model, frequencies, diffs, sigma=diffs_err,
                                               bounds = bounds_diff)
fit_diff_err = np.sqrt(np.diag(popt_diff))
plt.errorbar(frequencies, diffs,xerr= frequencies_errs ,yerr = diffs_err, fmt = '.', label = "results")
lin = np.linspace(0, driven_constants.NATURAL_FREQUENCY * 2, 2000)
phase_diff = [phase_diff_model(freq, driven_constants.NATURAL_FREQUENCY, 2.72074) for freq in lin]
#plt.plot(lin, phase_diff, label = "theoretical graph")
plt.plot(lin, phase_diff_model(lin, driven_constants.NATURAL_FREQUENCY, fit_diff[1]), '--', label = "fit")
plt.grid()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Phase [rad]")
plt.legend()
plt.show()
tau_amp = amp_fit[2]
tau_amp_err = amp_fit_err[2]
tau_diff = fit_diff[1]
tau_diff_err = fit_diff_err[1]
NF_amp = amp_fit[1]
NF_amp_err = amp_fit_err[1]
NF_diff = fit_diff[0]
NF_diff_err = fit_diff_err[0]

print(tau_amp, tau_amp_err, tau_diff, tau_diff_err)
print(NF_amp, NF_amp_err, NF_diff, NF_diff_err, driven_constants.NATURAL_FREQUENCY)