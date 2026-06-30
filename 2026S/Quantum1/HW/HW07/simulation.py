import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.constants import hbar

print("[INFO] Initializing parameters and grids...")
# Parameters
L = 0.01  # 1 cm = 0.01 m
m = hbar / L
Delta = hbar / L
p0 = hbar / L
x0 = -5 * L

# Grid for momentum p
p_min, p_max = -10 * p0, 10 * p0
n_p = 100000  # Set back to 100k to resolve high-frequency phase oscillations at later times
p = np.linspace(p_min, p_max, n_p)
dp = p[1] - p[0]
print(f"  Momentum grid: {p_min:.3e} to {p_max:.3e} with {n_p} points.")

# 4.2.2: Compute psi(0,0) with N = 1
print("[INFO] Step 4.2.2: Computing unnormalized psi(0,0)...")
psi0_p_unnormalized = np.exp(-((p - p0) ** 2) / (2 * Delta**2)) * np.exp(
    -1j * p * x0 / hbar
)
psi_0_0_unnormalized = (
    (1 / np.sqrt(2 * np.pi * hbar)) * np.sum(psi0_p_unnormalized) * dp
)
print(f"  Result -> psi(0,0) unnormalized: {psi_0_0_unnormalized}")

# 4.2.3: Compute psi(x,0) with N = 1 on grid x from -10 to 10 (meters)
x_grid = np.arange(-10, 10.1, 0.1)
print(
    "[INFO] Step 4.2.3: Computing unnormalized psi(x,0) using matrix multiplication..."
)
kernel_x = np.exp(1j * np.outer(p, x_grid) / hbar)  # shape (n_p, len(x_grid))
psi_x_0_unnormalized = (
    (1 / np.sqrt(2 * np.pi * hbar)) * (psi0_p_unnormalized @ kernel_x) * dp
)
print("  Completed computing psi(x,0) for all grid points.")

# 4.2.4: Numerically normalize to find N
print("[INFO] Step 4.2.4: Calculating normalization constant N...")
dx = x_grid[1] - x_grid[0]
norm_integral = np.sum(np.abs(psi_x_0_unnormalized) ** 2) * dx
N = 1 / np.sqrt(norm_integral)
print(f"  Result -> Normalization constant N: {N:.6e}")

# Normalized wavefunctions
psi_x_0 = N * psi_x_0_unnormalized
psi_0_0 = N * psi_0_0_unnormalized
print(f"  Result -> psi(0,0) normalized: {psi_0_0}")

# 4.2.5: Compute psi(x,t) over time grid t from 0 to 10
t_grid = np.arange(0, 10.1, 0.1)
print(
    "[INFO] Step 4.2.5: Computing time evolution psi(x,t) using matrix multiplication..."
)
phase_t = np.exp(
    -1j * np.outer(t_grid, p**2) / (2 * m * hbar)
)  # shape (len(t_grid), n_p)
psi_p_t = psi0_p_unnormalized * phase_t  # shape (len(t_grid), n_p)
psi_x_t = (
    N * (1 / np.sqrt(2 * np.pi * hbar)) * (psi_p_t @ kernel_x) * dp
)  # shape (len(t_grid), len(x_grid))
print("  Completed computing psi(x,t) for all time steps.")

# 4.2.6: Create animation of the probability density |psi(x,t)|^2
print("[INFO] Step 4.2.6: Generating and saving probability density animation...")
fig, ax = plt.subplots(figsize=(8, 5))
# Set pure white background for axes as per User Preferences
ax.set_facecolor("#ffffff")
fig.patch.set_facecolor("#ffffff")

(line,) = ax.plot([], [], lw=2, color="#1a5fb4")
ax.set_xlim(-10, 10)
max_y = np.max(np.abs(psi_x_t) ** 2)
ax.set_ylim(0, max_y * 1.1)
time_text = ax.text(0.05, 0.95, "", transform=ax.transAxes, verticalalignment="top")


def init():
    line.set_data([], [])
    time_text.set_text("")
    return line, time_text


def update(frame):
    y = np.abs(psi_x_t[frame]) ** 2
    line.set_data(x_grid, y)
    time_text.set_text(f"t = {t_grid[frame]:.1f} s")
    return line, time_text


gif_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "density_animation.gif"
)
ani = FuncAnimation(fig, update, frames=len(t_grid), init_func=init, blit=False)
ani.save(gif_path, writer="pillow", fps=10)
print(f"[INFO] Animation saved successfully to: {gif_path}")

# 4.2.7: Lorentzian Wave Packet Time Evolution and Animation
print("\n[INFO] Step 4.2.7: Initializing Lorentzian wave packet...")
Delta_lor = L
# Analytical normalization constant in position space
N_lor = np.sqrt(2 * Delta_lor / np.pi)

# Analytical momentum representation phi(p) for Lorentzian
phi_p_lor = (
    np.sqrt(Delta_lor / hbar)
    * np.exp(-1j * (p - p0) * x0 / hbar)
    * np.exp(-Delta_lor * np.abs(p - p0) / hbar)
)

# Time evolution in momentum space
print("[INFO] Step 4.2.7: Computing time evolution for Lorentzian...")
phi_p_t_lor = phi_p_lor * phase_t  # shape (len(t_grid), n_p)
psi_x_t_lor = (
    (1 / np.sqrt(2 * np.pi * hbar)) * (phi_p_t_lor @ kernel_x) * dp
)  # shape (len(t_grid), len(x_grid))
print("  Completed computing psi(x,t) for Lorentzian wave packet.")

# Create Lorentzian animation
print(
    "[INFO] Step 4.2.7: Generating and saving Lorentzian probability density animation..."
)
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.set_facecolor("#ffffff")
fig2.patch.set_facecolor("#ffffff")

(line2,) = ax2.plot([], [], lw=2, color="#e66100")
ax2.set_xlim(-10, 10)
max_y2 = np.max(np.abs(psi_x_t_lor) ** 2)
ax2.set_ylim(0, max_y2 * 1.1)
time_text2 = ax2.text(0.05, 0.95, "", transform=ax2.transAxes, verticalalignment="top")


def init2():
    line2.set_data([], [])
    time_text2.set_text("")
    return line2, time_text2


def update2(frame):
    y = np.abs(psi_x_t_lor[frame]) ** 2
    line2.set_data(x_grid, y)
    time_text2.set_text(f"t = {t_grid[frame]:.1f} s")
    return line2, time_text2


gif_path_lor = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "lorentzian_animation.gif"
)
ani2 = FuncAnimation(fig2, update2, frames=len(t_grid), init_func=init2, blit=False)
ani2.save(gif_path_lor, writer="pillow", fps=10)
print(f"[INFO] Lorentzian animation saved successfully to: {gif_path_lor}")
