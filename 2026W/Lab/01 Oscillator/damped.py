from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

import constants
import utils
from simple import ticks_err
from constants import NATURAL_FREQUENCY

def damped_model(time, amplitude, tau, frequency, phase):
    return amplitude * np.exp(-time / (2 * tau)) * np.sin(frequency * time + phase)

def process_run(path: Path):
    path = utils.get_edited_data_path(path, start_index=202)

    data = pd.read_csv(path)
    ticks = data["ticks"]
    time = data["time"]

    ticks /= constants.TICKS_PER_METER

    plt.plot(time, ticks, ".", label="data")
    peak_indices, _ = scipy.signal.find_peaks(ticks)
    peaks = ticks[peak_indices]
    amplitude = round(np.mean(np.abs(peaks)) * 100, 3)
    print(f"{amplitude=}cm")


    plt.plot(time[peak_indices], peaks, "^", label="Peaks")


    guess_amplitude = (np.max(ticks) - np.min(ticks)) / 2
    guess_tau = 5
    guess_frequency = 2 * np.pi / 1
    guess_phase = np.pi / 2
    p0 = [guess_amplitude, guess_tau, guess_frequency, guess_phase]

    popt, pcov = scipy.optimize.curve_fit(damped_model, time, ticks, p0=p0, sigma = ticks_err)
    amplitude_fit, tau_fit, frequency_fit, phase_fit = popt
    amplitude_error, tau_error, frequency_error, phase_error = np.sqrt(pcov.diagonal())
    print(f"Amplitude = {amplitude_fit*100:.5f}±{amplitude_error*100:.5f}cm")
    print(f"ω = {frequency_fit:.5f}±{frequency_error:.5f} 1/s")
    print(f"τ = {tau_fit:.5f}±{tau_error:.5f} sec")
    print(f"φ = {phase_fit / np.pi:.5f}±{phase_error / np.pi:.5f}π rad")

    t_fit = np.linspace(time.min(), time.max(), 1000)
    plt.plot(t_fit, damped_model(t_fit, *popt), "r-", label="fit")

    plt.legend()
    plt.grid()
    plt.show()

    print(np.abs(frequency_fit - NATURAL_FREQUENCY) / NATURAL_FREQUENCY)

process_run(Path("damped.txt"))
