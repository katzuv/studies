import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

data = pd.read_csv("buzzers.csv")
x1 = data["x_1 (cm)"]
amplitude = data["Amplitude"]
length = data["L (cm)"]
frequency = data["f (Hz)"]
L = 0.246


def get_amplitude(x, a, lam, phi):
    t = (np.pi / lam) * (2 * x - L) + phi / 2
    return np.abs(2 * a * np.cos(t))


params, cov = curve_fit(
    get_amplitude,
    x1,
    amplitude,
    p0=(2.8, 2.5, 0),
    bounds=([0, 0, -np.pi], [5, np.inf, np.pi]),
)
a_fit, lam_fit, phi_fit = params
print(f"a = {a_fit:.3f}, lambda = {lam_fit:.4f}, phi = {phi_fit:.3f} rad")
x_fit = np.linspace(min(x1), max(x1), 500)
y_fit = get_amplitude(x_fit, *params)

y_pred = get_amplitude(x1, *params)
Rsq = r2_score(amplitude, y_pred)
print(f"{Rsq=}")

plt.plot(x1, amplitude, ".")
plt.plot(x_fit, y_fit, "-")
plt.grid()
plt.show()

errors = np.sqrt(np.diag(cov))

a_err, lam_err, phi_err = errors

print(f"amplitude = {params[0]:.3f} ± {a_err:.3f}")
print(f"lambda = {params[1]:.3f} ± {lam_err:.3f}")
print(f"phi = {params[2]:.3f} ± {phi_err:.3f} rad")
