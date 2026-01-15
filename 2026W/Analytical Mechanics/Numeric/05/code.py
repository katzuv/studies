import matplotlib.pyplot as plt
import numpy as np
import scipy

G = 6.674e-11
M = 1.99e30
m_mercury = 3.30e23
r0 = 6.98e10
v0 = 38.86e3
c = 3e8

a = (G * M) / (v0**2 * r0)
b = (G * M) / (c**2 * r0)

print(f"Calculated constants:\n a = {a:.5f}\n b = {b:.5e}")


def mercury_orbit(theta, y):
    w = y[0]
    dw = y[1]

    d2w = a - w + 3 * b * (w**2)
    return [dw, d2w]


y0 = [1.0, 0.0]

theta_span = (0, 200 * np.pi)
t_eval = np.linspace(0, 200 * np.pi, 10000)

sol = scipy.integrate.solve_ivp(
    mercury_orbit, theta_span, y0, t_eval=t_eval, rtol=1e-9, atol=1e-9
)

w_sol = sol.y[0]
r_sol = r0 / w_sol
theta_sol = sol.t

plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection="polar")
ax.plot(theta_sol, r_sol, linewidth=2)

ax.grid(True)

# ax.set_ylim(0, np.max(r_sol) * 1.1)

plt.legend()
plt.savefig("03.svg", format="svg")
plt.show()
