import sys
from pathlib import Path

import pandas as pd
import scipy
from matplotlib import pyplot as plt

from consts import *
import autograd.numpy as np

sys.path.append("../utils.py")
import utils


def left_model(time, tau, low_frequency, high_frequency, phi1, phi2, A, B):
    low = low_frequency * time + phi1
    high = high_frequency * time + phi2
    exp = np.exp(-time / (2 * tau))
    return exp * (A * np.cos(low) + B * np.cos(high))


def right_model(time, tau, low_frequency, high_frequency, phi1, phi2, A, B):
    low = low_frequency * time + phi1
    high = high_frequency * time + phi2
    exp = np.exp(-time / (2 * tau))
    return exp * (A * np.cos(low) - B * np.cos(high))


# def left_model_new(time, A, B):
#     low = low_frequency * time + phi1
#     high = high_frequency * time + phi2
#     exp = np.exp(-time / (2 * tau))
#     return exp * (A * np.cos(low) + B * np.cos(high))
#
#
# def right_model_new(time, A, B):
#     low = low_frequency * time + phi1
#     high = high_frequency * time + phi2
#     exp = np.exp(-time / (2 * tau))
#     return exp * (A * np.cos(low) - B * np.cos(high))


def plot_single(file_path, guesses):
    file_path = Path(file_path)
    data = pd.read_csv(utils.get_edited_driven_data_path(file_path))
    left_ticks = data["ticks_a"][0:3000] / TICKS_PER_CM
    left_ticks -= np.mean(left_ticks)
    right_ticks = data["ticks_b"][0:3000] / TICKS_PER_CM
    right_ticks -= np.mean(right_ticks)
    time = data["time"][0:3000]
    #print("frequencies_left =", np.fft.fft(left_ticks))
    #print("frequencies_right =", np.fft.fft(right_ticks))
    length_error = .5
    plt.plot(time, left_ticks, label="Left")
    plt.fill_between(time,
                     left_ticks - length_error,
                     left_ticks + length_error,
                     color='C0', alpha=0.25, label='Left error')
    plt.fill_between(time,
                     right_ticks - length_error,
                     right_ticks + length_error,
                     color='C1', alpha=0.25, label='Right error')

    plt.errorbar(time, right_ticks, label="Right")

    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude [cm]")

    print(file_path)
    lower_bounds = [-np.inf, -np.inf, -np.inf,-np.pi, -np.pi, -np.inf, -np.inf]
    upper_bounds = [np.inf, np.inf, np.inf,np.pi, np.pi, np.inf, np.inf]

    t_fit = np.linspace(time.min(), time.max(), 1000)
    lower_bounds = [-np.inf, -np.inf, -np.inf,-np.pi, -np.pi, -np.inf, -np.inf]
    upper_bounds = [np.inf, np.inf, np.inf,np.pi, np.pi, np.inf, np.inf]
    popt, pcov = scipy.optimize.curve_fit(left_model, time, left_ticks, p0=guesses, sigma=length_error, bounds=(lower_bounds, upper_bounds))
    left_model_fit = left_model(t_fit, *popt)
    plt.plot(t_fit, left_model_fit, "r-", label="Left fit")
    tau, low, high, phi1, phi2, a, b = popt
    tau_err, low_err, high_err, phi1_err, phi2_err, a_err, b_err = np.sqrt(pcov.diagonal())
    # error = utils.propagate_error(left_model, (time,tau, low, high, phi1, phi2, a, b), (0,tau_err, low_err, high_err, phi1_err, phi2_err, a_err, b_err))
    # plt.fill_between(time,
    #                  left_model_fit - error,
    #                  left_model_fit + error,
    #                  color='C0', alpha=0.25, label='Left model error')
    print(f"tau  = {tau:.5f} ± {tau_err:.5f}")
    #print(f"low  = {low:.5f} ± {low_err:.5f}")
    #print(f"high = {high:.5f} ± {high_err:.5f}")
    #print(f"a    = {a:.5f} ± {a_err:.5f}")
    #print(f"b    = {b:.5f} ± {b_err:.5f}")
    #print(f"phi1 = {phi1:.5f} ± {phi1_err:.5f}")
    #print(f"phi2 = {phi2:.5f} ± {phi2_err:.5f}")

    popt, pcov = scipy.optimize.curve_fit(right_model, time, right_ticks, p0=guesses, sigma=length_error,bounds=(lower_bounds, upper_bounds))
    t_fit = np.linspace(time.min(), time.max(), 1000)
    right_model_fit = right_model(t_fit, *popt)
    plt.plot(t_fit, right_model_fit, "g-", label="Right fit")
    tau, low, high, phi1, phi2, a, b = popt
    tau_err, low_err, high_err, phi1_err, phi2_err, a_err, b_err = np.sqrt(pcov.diagonal())
    # error = utils.propagate_error(right_model, (time, tau, low, high, phi1, phi2, a, b),
    #                               (0, tau_err, low_err, high_err, phi1_err, phi2_err, a_err, b_err))
    # plt.fill_between(time,
    #                  right_model_fit - error,
    #                  right_model_fit + error,
    #                  color='C1', alpha=0.25, label='Right model error')
    print(f"tau      = {tau:.5f} ± {tau_err:.5f}")
    #print(f"low      = {low:.5f} ± {low_err:.5f}")
    #print(f"high     = {high:.5f} ± {high_err:.5f}")
    #print(f"a        = {a:.5f} ± {a_err:.5f}")
    #print(f"b        = {b:.5f} ± {b_err:.5f}")
    #print(f"phi1     = {phi1:.5f} ± {phi1_err:.5f}")
    #print(f"phi2     = {phi2:.5f} ± {phi2_err:.5f}")

    plt.legend()
    plt.grid()
    plt.savefig(file_path.stem, format='svg')
    plt.show()


guesses = [3, 5, 8, 1, 1, 1, 1]
plot_single("Data/symmetric.txt",guesses)
plot_single("Data/anti_sym.txt", guesses)
plot_single("Data/100_0.txt",guesses)
