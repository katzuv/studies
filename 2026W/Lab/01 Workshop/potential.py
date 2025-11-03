import matplotlib.pyplot as plt
import numpy as np  # math functions

C = 1
a = 1
L = 3
N = 100
coord = np.linspace(-L, L, N)  # defines coordinates
# Create x and y grid for all coordinates.
coord_x, coord_y = np.meshgrid(coord, coord)


def ln_argument(x, y, a):
    return np.abs(np.hypot(x - a, y) / a)


def get_potential(x, y, a, C):
    return -C * np.log(ln_argument(x, y, -a)) + C * ln_argument(x, y, a)


# Calculate potential at every coordinate.
potential = get_potential(coord_x, coord_y, a, C)

plt.figure()
# Make a color for every coordinate based on the potential.
plt.pcolormesh(coord_x, coord_y, potential)
plt.colorbar()

# `cmap`: color map.
plt.contour(coord_x, coord_y, potential, np.linspace(-2, 2, 10), cmap="Accent")

plt.show()
