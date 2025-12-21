import numpy as np
import scipy
from matplotlib import pyplot as plt

f = 4.15  # kHz
zamzam_x = 70.1  # initial distance [cm] +- 2 mm
dx = (
    np.array((73.1, 73.6, 74.1, 74.8, 75.5, 76.4, 77.1, 77.7, 78.5, 79.1)) - zamzam_x
)  # distance [cm] +- 2 mm
phase = np.array(
    (102, 125, 133, 166, -170, -133, -103, -79.5, -38, -13)
)  # phase shift [deg]
phase = np.radians((phase + 360) % 360)
phase_err = np.radians((3, 3, 3, 3, 3, 3, 3, 3, 3, 3))  # phase shift error [deg]
plt.figure(2)
plt.errorbar(
    dx,
    phase / (2 * np.pi),
    xerr=0.2,
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
plt.plot(dx, y, label="Linear regression")

plt.xlabel("Distance [cm]")
plt.ylabel("Phase shift [radians]")
plt.grid()
plt.legend()
plt.savefig("freq_response.svg", format="svg")
plt.show()

lam = 2 * np.pi / reg.slope
print(f"Wavelength of sound in air is {lam:.3f} cm")
v = lam * f * 10
print(f"Speed of sound in air is {v:.3f} m/s")
