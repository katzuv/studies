import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.constants import hbar

print("[INFO] Initializing parameters for potential step simulation...")
# Parameters
L = 0.01  # 1 cm = 0.01 m
m = hbar / L
x0 = -5.0  # Starts at -5.0 meters
sigma_x = 0.5  # Width of 0.5 meters (fits comfortably to the left)
sigma_k = 1 / (2 * sigma_x)
k0 = 150.0  # Centered at momentum k0 = 150.0 rad/m (speed v_g = 1.5 m/s)

# Grid for x (highly resolved to avoid spatial aliasing of the oscillations)
x_grid = np.arange(-10, 10.005, 0.005)

# Momentum grid k (we integrate over k > 0)
k_min, k_max = 120.0, 180.0
n_k = 5000
k = np.linspace(k_min, k_max, n_k)
dk = k[1] - k[0]

# Gaussian profile in k-space
phi_k = np.exp(-((k - k0) ** 2) / (4 * sigma_k**2))  # Profile for psi0(x)

# Time grid
t_grid = np.arange(0, 10.1, 0.1)


def simulate_step(V0, name):
    print(f"\n[INFO] Starting simulation for: {name} (V0 = {V0:.3e})")

    # Calculate scattering state wavefunctions psi_k(x) for each k and x
    # shape will be (n_k, len(x_grid))
    psi_k_x = np.zeros((n_k, len(x_grid)), dtype=complex)

    for i, ki in enumerate(k):
        Ei = (hbar**2 * ki**2) / (2 * m)
        if Ei < V0:
            kappa = np.sqrt(2 * m * (V0 - Ei)) / hbar
            R = (1j * ki + kappa) / (1j * ki - kappa)
            T = (2 * 1j * ki) / (1j * ki - kappa)

            # x < 0 region
            idx_left = x_grid < 0
            psi_k_x[i, idx_left] = np.exp(1j * ki * x_grid[idx_left]) + R * np.exp(
                -1j * ki * x_grid[idx_left]
            )

            # x >= 0 region
            idx_right = x_grid >= 0
            psi_k_x[i, idx_right] = T * np.exp(-kappa * x_grid[idx_right])

        else:
            kp = np.sqrt(2 * m * (Ei - V0)) / hbar
            R = (ki - kp) / (ki + kp)
            T = (2 * ki) / (ki + kp)

            # x < 0 region
            idx_left = x_grid < 0
            psi_k_x[i, idx_left] = np.exp(1j * ki * x_grid[idx_left]) + R * np.exp(
                -1j * ki * x_grid[idx_left]
            )

            # x >= 0 region
            idx_right = x_grid >= 0
            psi_k_x[i, idx_right] = T * np.exp(1j * kp * x_grid[idx_right])

    # Time evolution
    print("  Computing time evolution...")
    psi_x_t = np.zeros((len(t_grid), len(x_grid)), dtype=complex)

    for frame, t in enumerate(t_grid):
        E = (hbar**2 * k**2) / (2 * m)
        # Evolve each k component in time
        evolved_coefs = phi_k * np.exp(-1j * k * x0) * np.exp(-1j * E * t / hbar)
        # Sum over k (matrix product)
        psi_x_t[frame] = (evolved_coefs @ psi_k_x) * dk

    # Normalize psi_x_t so that peak |psi|^2 at t=0 is 1 for clean plotting
    max_density = np.max(np.abs(psi_x_t[0]) ** 2)
    psi_x_t = psi_x_t / np.sqrt(max_density)

    # Save animation
    print("  Generating and saving animation...")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")

    (line,) = ax.plot([], [], lw=2, color="#1a5fb4")
    # Draw potential step as a dashed grey vertical line at x=0
    ax.axvline(0, color="grey", linestyle="--", alpha=0.7)

    ax.set_xlim(-10, 10)
    max_y = np.max(np.abs(psi_x_t) ** 2)
    ax.set_ylim(0, max_y * 1.1)
    ax.set_xlabel("x (m)")
    ax.set_ylabel(r"$|\psi(x,t)|^2$")
    time_text = ax.text(0.05, 0.95, "", transform=ax.transAxes, verticalalignment="top")

    # Zoomed inset window around x=0 (placed in the upper-right corner but slightly lower and wider)
    axins = ax.inset_axes([0.55, 0.45, 0.4, 0.4])
    axins.set_facecolor("#ffffff")
    (line_ins_left,) = axins.plot([], [], lw=1.5, color=line.get_color())
    (line_ins_right,) = axins.plot(
        [], [], lw=2.0, color="#e6194B"
    )  # Vibrant red color for the tunneling tail
    axins.axvline(0, color="grey", linestyle="--", alpha=0.7)
    axins.set_xlim(-0.2, 0.2)
    axins.set_ylim(0, 0.25)  # Lowered y-limit to zoom in on the tail
    axins.set_title("Zoom at x=0 (Tunneling in Red)", fontsize=9)
    axins.tick_params(labelsize=7)

    # Hide the inset window initially
    axins.set_visible(False)

    def init():
        line.set_data([], [])
        line_ins_left.set_data([], [])
        line_ins_right.set_data([], [])
        time_text.set_text("")
        return line, line_ins_left, line_ins_right, time_text

    def update(frame):
        y = np.abs(psi_x_t[frame]) ** 2
        line.set_data(x_grid, y)

        t = t_grid[frame]
        # Show the zoom window only during collision (when tunneling is visible)
        if 1.5 <= t <= 5.5:
            axins.set_visible(True)
            # Split data for left (x < 0) and right (x >= 0) regions inside the inset window
            idx_ins_left = (x_grid >= -0.2) & (x_grid <= 0.0)
            idx_ins_right = (x_grid >= 0.0) & (x_grid <= 0.2)
            line_ins_left.set_data(x_grid[idx_ins_left], y[idx_ins_left])
            line_ins_right.set_data(x_grid[idx_ins_right], y[idx_ins_right])
        else:
            axins.set_visible(False)
            line_ins_left.set_data([], [])
            line_ins_right.set_data([], [])

        time_text.set_text(f"t = {t_grid[frame]:.1f} s")
        return line, line_ins_left, line_ins_right, time_text

    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{name}.gif")
    ani = FuncAnimation(fig, update, frames=len(t_grid), init_func=init, blit=False)
    ani.save(gif_path, writer="pillow", fps=10)
    plt.close(fig)
    print(f"  Saved animation to: {gif_path}")


# Run the three simulations
# Define energy unit E_unit = hbar^2 / (2 * m)
E_unit = hbar**2 / (2 * m)
# For k0 = 150.0, E0 = 22500 * E_unit
simulate_step(56250 * E_unit, "step_under_v0")  # E < V0 (V0 = 2.5 * E0)
simulate_step(4500 * E_unit, "step_over_v0")  # E > V0 (V0 = 0.2 * E0)
simulate_step(22500 * E_unit, "step_around_v0")  # E approx V0 (V0 = E0)
