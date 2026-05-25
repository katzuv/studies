from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

import constants
import utils
from constants import NATURAL_FREQUENCY
from simple import ticks_err


def damped_model(time, amplitude, tau, frequency, phase):
    return amplitude * np.exp(-time / (2 * tau)) * np.sin(frequency * time + phase)

def amplitude_model(time, amplitude, tau):
    return amplitude * np.exp(-time / (2 * tau))


def process_run(path: Path):
    path = utils.get_edited_data_path(path, start_index=202)

    data = pd.read_csv(path)
    ticks = data["ticks"]
    time = data["time"]

    ticks /= constants.TICKS_PER_METER

    plt.errorbar(time, ticks * 100, yerr=constants.TICKS_PER_METER_ERROR * 100, fmt=".", label="Measurements",
                 ecolor='gray',
                 elinewidth=1, capsize=2)

    peak_indices, _ = scipy.signal.find_peaks(ticks)
    peaks = ticks[peak_indices]
    amplitude = round(np.mean(np.abs(peaks)) * 100, 3)
    print(f"{amplitude=}cm")

    # plt.plot(time[peak_indices], peaks, "^", label="Peaks")

    guess_amplitude = (np.max(ticks) - np.min(ticks)) / 2
    guess_tau = 5
    guess_frequency = 2 * np.pi / 1
    guess_phase = np.pi / 2
    p0 = [guess_amplitude, guess_tau, guess_frequency, guess_phase]

    popt, pcov = scipy.optimize.curve_fit(damped_model, time, ticks, p0=p0, sigma=ticks_err)
    amplitude_fit, tau_fit, frequency_fit, phase_fit = popt
    amplitude_error, tau_error, frequency_error, phase_error = np.sqrt(pcov.diagonal())
    print(f"Amplitude = {amplitude_fit * 100:.2f}±{amplitude_error * 100:.5e}cm")
    print(f"ω = {frequency_fit:.2f}±{frequency_error:.5e} 1/s")
    print(f"τ = {tau_fit:.2f}±{tau_error:.5e} sec")
    print(f"φ = {phase_fit / np.pi:.2f}±{phase_error / np.pi:.5e}π rad")
    plt.plot(amplitude_fit)

    t_fit = np.linspace(time.min(), time.max(), 1000)
    plt.plot(t_fit, damped_model(t_fit, *popt)*100, "r-", label="Fit", zorder=3)
    plt.plot(t_fit, amplitude_model(t_fit, -amplitude_fit, tau_fit)*100, "g-", label="Amplitude fit", zorder=0)

    plt.legend()
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Distance from equilibrium [cm]")
    plt.savefig(f"damped_{path.stem}.svg", format="svg")
    plt.show()

    print(np.abs(frequency_fit - NATURAL_FREQUENCY) / NATURAL_FREQUENCY)

    fitted = damped_model(time, *popt)
    residuals = ticks - fitted
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((ticks - np.mean(ticks)) ** 2)
    r_squared = 1 - ss_res / ss_tot
    print(f"R^2 sin = {r_squared:.9f}")

    fitted = amplitude_model(time, -amplitude_fit,tau_fit)
    residuals = ticks - fitted
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((ticks - np.mean(ticks)) ** 2)
    r_squared = 1 - ss_res / ss_tot
    print(f"R^2 exp = {r_squared:.9f}")

    theoretical_omega = np.sqrt(constants.SPRING_CONSTANT / constants.CART_MASS - (1 / (4 * tau_fit ** 2)))
    # propagated error for theoretical_omega = sqrt(K/m - 1/(4 tau^2))
    A = constants.SPRING_CONSTANT / constants.CART_MASS - (1 / (4 * tau_fit ** 2))
    sigma_K = constants.SPRING_CONSTANT_ERROR
    sigma_m = constants.MASS_ERROR
    sigma_tau = tau_error
    dA_dK = 1.0 / constants.CART_MASS
    dA_dm = -constants.SPRING_CONSTANT / (constants.CART_MASS ** 2)
    dA_dtau = 1.0 / (2 * tau_fit ** 3)
    sigma_A = np.sqrt((dA_dK * sigma_K) ** 2 + (dA_dm * sigma_m) ** 2 + (dA_dtau * sigma_tau) ** 2)
    theoretical_omega_error = 0.5 / np.sqrt(A) * sigma_A
    error = (np.abs(frequency_fit - theoretical_omega) / theoretical_omega) * 100

    print(f"Theory: {theoretical_omega}±{theoretical_omega_error} | Error percentage of frequency from theory: {error:.2f}%")


process_run(Path("damped.txt"))
