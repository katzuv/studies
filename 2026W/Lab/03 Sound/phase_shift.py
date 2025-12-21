import numpy as np
import scipy
from matplotlib import pyplot as plt

from utils import propagate_error

f = 4.15 * 1000  # kHz
zamzam_x = 70.1  # initial distance [cm] +- 2 mm
dx = (
    np.array((73.1, 73.6, 74.1, 74.8, 75.5, 76.4, 77.1, 77.7, 78.5, 79.1)) - zamzam_x
) / 100  # distance [cm] +- 2 mm
phase = np.array(
    (102, 125, 133, 166, -170, -133, -103, -79.5, -38, -13)
)  # phase shift [deg]
phase = np.radians((phase + 360) % 360)
phase_err = np.radians((3, 3, 3, 3, 3, 3, 3, 3, 3, 3))  # phase shift error [deg]
plt.figure(2)
plt.errorbar(
    dx,
    phase / (2 * np.pi),
    xerr=0.2 / 100,
    yerr=phase_err / (2 * np.pi),
    fmt=".",
    label="Measurements",
)

# Linear regression
reg = scipy.stats.linregress(dx, phase)
y = reg.slope * dx + reg.intercept
r = reg.rvalue
r2 = r**2
print(f"r = {r:.3f}, R² = {r2:.3f}")
plt.plot(dx, y / (2 * np.pi), label="Linear regression")

plt.xlabel("Distance [cm]")
plt.ylabel("Phase shift [pi radians]")
plt.grid()
plt.legend()
plt.savefig("freq_response.svg", format="svg")
plt.show()


def lam_func(slope):
    return 2 * np.pi / slope


lam = 2 * np.pi / reg.slope
lam_err = propagate_error(lam_func, (reg.slope,), (reg.stderr,))
print(f"Wavelength of sound in air is {lam:.3f} ± {lam_err:.3f} cm")


def v_func(lambd, freq):
    return lambd * freq


v = v_func(lam, f)
v_err = propagate_error(v_func, (lam, f), (lam_err, 17.82))
print(f"Speed of sound in air is {v:.3f} ± {v_err:.3f} m/s")
