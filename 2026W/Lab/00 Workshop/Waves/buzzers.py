import numpy as np
import pandas as pd

data = pd.read_csv("buzzers.csv")
x1 = data["x1"]
amplitude = data["Amplitude"]
length = data["L (cm)"]
frequency = data["f (Hz)"]
L = 0.246


def get_amplitude(x, a, lam, phi):
    t = (np.pi / lam) * (2 * x - L) + phi / 2
    return np.abs(2 * a * np.cos(t))
