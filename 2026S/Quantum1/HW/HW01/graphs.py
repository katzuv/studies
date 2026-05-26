import matplotlib.pyplot as plt
import numpy as np


# The mathematical function you derived, now with the 1/sqrt(2pi) constant
def f_hat(w, tau, w0):
    peak_right = 1 / (1 + (w - w0) ** 2 * tau**2)
    peak_left = 1 / (1 + (w + w0) ** 2 * tau**2)
    constant = 1 / np.sqrt(2 * np.pi)
    return constant * (peak_left + peak_right)


# Set up the frequency axis
omega = np.linspace(-15, 15, 1000)

# --- Graph 1: Varying omega_0 (Shifting) ---
plt.figure(figsize=(10, 6))
tau_fixed = 1.0
w0_values = [0.0, 2.0, 5.0, 8.0]

for w0 in w0_values:
    y = f_hat(omega, tau_fixed, w0)
    plt.plot(omega, y, lw=2.5, label=rf"$\omega_0 = {w0}$")

# plt.title(fr"Effect of Frequency Shift ($\omega_0$) with constant $\tau={tau_fixed}$", fontsize=16, pad=15)
plt.xlabel(r"Frequency ($\omega$)", fontsize=14)
plt.ylabel(r"Amplitude $\hat{f}(\omega)$", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Save and close
plt.savefig("varying_w0.svg", format="svg")
plt.show()
plt.close()

# --- Graph 2: Varying tau (Width) ---
plt.figure(figsize=(10, 6))
w0_fixed = 6.0
tau_values = [0.5, 1.0, 2.0, 5.0]

for tau in tau_values:
    y = f_hat(omega, tau, w0_fixed)
    plt.plot(omega, y, lw=2.5, label=rf"$\tau = {tau}$")

# plt.title(fr"Effect of Width Parameter ($\tau$) with constant $\omega_0={w0_fixed}$", fontsize=16, pad=15)
plt.xlabel(r"Frequency ($\omega$)", fontsize=14)
plt.ylabel(r"Amplitude $\hat{f}(\omega)$", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Save and close
plt.savefig("varying_tau.svg", format="svg")
plt.show()
plt.close()

# --- Graph 3: Standalone Single Version ---
plt.figure(figsize=(10, 6))
w0_single = 5.0
tau_single = 1.0

y_single = f_hat(omega, tau_single, w0_single)
plt.plot(
    omega,
    y_single,
    lw=2.5,
    color="#2ca02c",
    label=rf"$\omega_0 = {w0_single}, \tau = {tau_single}$",
)

# plt.title(r"Fourier Transform: $\hat{f}(\omega)$", fontsize=16, pad=15)
plt.xlabel(r"Frequency ($\omega$)", fontsize=14)
plt.ylabel(r"Amplitude $\hat{f}(\omega)$", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Save and close
plt.savefig("single_version.svg", format="svg")
plt.show()
plt.close()

print("Graphs successfully generated and saved.")
