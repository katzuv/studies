import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from matplotlib import pyplot as plt

from consts import *

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

def plot_single(file_path, guesses):
    file_path = Path(file_path)
    data = pd.read_csv(utils.get_edited_driven_data_path(file_path))
    left_ticks = data["ticks_a"] / TICKS_PER_CM
    left_ticks -= np.mean(left_ticks)
    right_ticks = data["ticks_b"] / TICKS_PER_CM
    right_ticks -= np.mean(right_ticks)
    time = data["time"]

    plt.plot(time, left_ticks, label="Left")
    plt.plot(time, right_ticks, label="Right")

    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude [cm]")

    print(file_path)

    ticks_err = 1 / TICKS_PER_CM
    lower_bounds = [-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, .5, .5]
    upper_bounds = [np.inf] * 7  # all others unbounded above

    t_fit = np.linspace(time.min(), time.max(), 1000)
    lower_bounds = [-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, .5, .5]
    upper_bounds = [np.inf] * 7  # all others unbounded above
    popt, pcov = scipy.optimize.curve_fit(left_model, time, left_ticks, p0=guesses, sigma=ticks_err, bounds=(lower_bounds, upper_bounds))
    plt.plot(t_fit, left_model(t_fit, *popt), "r-", label="Left fit")
    tau, low, high, a, b, phi1, phi2 = popt
    tau_err, low_err, high_err, a_err, b_err, phi1_err, phi2 = np.sqrt(pcov.diagonal())
    print(f"tau      = {tau:.5f} ± {tau_err:.5f}")
    print(f"low      = {low:.5f} ± {low_err:.5f}")
    print(f"high     = {high:.5f} ± {high_err:.5f}")
    print(f"a        = {a:.5f} ± {a_err:.5f}")
    print(f"b        = {b:.5f} ± {b_err:.5f}")
    print(f"phi1        = {phi1:.5f} ± {phi1_err:.5f}")
    print(f"phi2        = {phi2:.5f}")  # if no error provided for d

    popt, pcov = scipy.optimize.curve_fit(right_model, time, right_ticks, p0=guesses, sigma=ticks_err,bounds=(lower_bounds, upper_bounds))
    t_fit = np.linspace(time.min(), time.max(), 1000)
    plt.plot(t_fit, right_model(t_fit, *popt), "g-", label="Right fit")
    tau, low, high, a, b, phi1, phi2 = popt
    tau_err, low_err, high_err, a_err, b_err, phi1_err, phi2 = np.sqrt(pcov.diagonal())
    print(f"tau      = {tau:.5f} ± {tau_err:.5f}")
    print(f"low      = {low:.5f} ± {low_err:.5f}")
    print(f"high     = {high:.5f} ± {high_err:.5f}")
    print(f"a        = {a:.5f} ± {a_err:.5f}")
    print(f"b        = {b:.5f} ± {b_err:.5f}")
    print(f"phi1        = {phi1:.5f} ± {phi1_err:.5f}")
    print(f"phi2        = {phi2:.5f}")  # if no error provided for d

    plt.legend()
    plt.grid()
    plt.show()


plot_single("Data/symmetric.txt",[2, 1, 3, 1, 1, 1, 1])
plot_single("Data/anti_sym.txt", [2, 1, 3, 1, 1, 1, 1])
plot_single("Data/100_0.txt",[2, 1, 3, 2, 2, 2, 2])
