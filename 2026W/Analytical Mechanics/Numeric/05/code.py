import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

G = 6.674e-11
M = 1.99e30
r0 = 6.98e10
v0 = 38.86e3
c = 3e8

a_real = (G * M) / (v0**2 * r0)
b_real = (G * M) / (c**2 * r0)

print(f"Calculated a: {a_real:.4f}")
print(f"Calculated b: {b_real:.4e}")


def orbit_ode(theta, y, a, b):
    w = y[0]
    dw = y[1]
    d2w = a - w + 3 * b * (w**2)
    return [dw, d2w]


def solve_and_plot(filename, a_val, b_val, theta_max, title, color="tab:blue"):
    y0 = [1.0, 0.0]

    t_eval = np.linspace(0, theta_max, 10000)

    sol = solve_ivp(
        lambda t, y: orbit_ode(t, y, a_val, b_val),
        (0, theta_max),
        y0,
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    theta = sol.t
    w = sol.y[0]
    r_norm = 1.0 / w

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, projection="polar")

    lw = 2.0 if theta_max < 30 else 1.0

    ax.plot(theta, r_norm, color=color, linewidth=lw)
    ax.set_title(title, pad=20)

    ax.set_yticklabels([])
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(filename, format="svg")
    plt.close()
    print(f"Saved {filename}")


solve_and_plot(
    "03.svg",
    a_real,
    b_real,
    200 * np.pi,
    f"Mercury Orbit (Real parameters)\nb={b_real:.1e}",
)

solve_and_plot(
    "04.svg",
    a_real,
    0.01,
    20 * np.pi,
    "Mercury Orbit (Precession)\nb=0.01",
    color="tab:orange",
)

solve_and_plot(
    "05.svg", a_real, 0.1, 2 * np.pi, "Mercury Orbit (Decay)\nb=0.1", color="tab:red"
)
