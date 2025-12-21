import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# parameters
m1 = 1.0
m2 = 1.2
k1 = 1.0
k2 = 1.5
k3 = .8
gamma1 = 0.1
gamma2 = 0.15


def equations(t, y):
    x1, v1, x2, v2 = y

    a1 = -(k1 + k3) / m1 * x1 + (k3 / m1) * x2 - gamma1 * v1
    a2 = (k3 / m2) * x1 - (k2 + k3) / m2 * x2 - gamma2 * v2

    return [v1, a1, v2, a2]


# initial conditions
y0 = [0.1, 0, -0.1, 0]  # x1, v1, x2, v2

sol = solve_ivp(equations, [0, 40], y0, max_step=0.01, dense_output=True)

t = np.linspace(0, 40, 5000)
x1, v1, x2, v2 = sol.sol(t)

plt.plot(t, x1, label="x1(t)")
plt.plot(t, x2, label="x2(t)")
plt.legend()
plt.grid()
plt.xlabel("t")
plt.ylabel("Position")
plt.show()
