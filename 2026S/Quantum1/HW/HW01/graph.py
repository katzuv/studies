import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# 1. Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
omega = np.linspace(-15, 15, 1000)
(line,) = ax.plot([], [], lw=2.5, color="#1f77b4")

# Formatting the plot
ax.set_xlim(-10, 10)
ax.set_ylim(0, 2.2)
ax.set_title("Fourier Transform: Modulated Exponential", fontsize=16, pad=15)
ax.set_xlabel(r"Frequency ($\omega$)", fontsize=14)
ax.set_ylabel(r"Amplitude $\tilde{f}(\omega)$", fontsize=14)
ax.grid(True, linestyle="--", alpha=0.6)

# Text box to show the live parameter values
text_box = ax.text(
    0.05,
    0.85,
    "",
    transform=ax.transAxes,
    fontsize=14,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="lightgoldenrodyellow",
        alpha=0.8,
        edgecolor="gray",
    ),
)


# 2. The mathematical function you derived
def f_hat(w, tau, w0):
    peak_right = 1 / (1 + (w - w0) ** 2 * tau**2)
    peak_left = 1 / (1 + (w + w0) ** 2 * tau**2)
    return peak_left + peak_right


# 3. Animation Logic - Now slower and with a break
total_frames = 400


def init():
    line.set_data([], [])
    text_box.set_text("")
    return line, text_box


def animate(i):
    # Phase 1: Move omega_0 from 0 to 5 smoothly (Slower)
    if i < 100:
        w0 = 5.0 * (i / 100.0)
        tau = 1.0

    # Phase 1.5: The Break! Pause for a second to observe the shift
    elif i < 150:
        w0 = 5.0
        tau = 1.0

    # Phase 2: Increase tau from 1 to 5 (Skinny/Narrow Peaks)
    elif i < 250:
        w0 = 5.0
        progress = (i - 150) / 100.0
        tau = 1.0 + progress * 4.0

    # Phase 3: Decrease tau from 5 down to 0.2 (Fat/Wide Peaks)
    elif i < 350:
        w0 = 5.0
        progress = (i - 250) / 100.0
        tau = 5.0 - progress * 4.8

    # Phase 4: Return tau back to 1.0 to loop smoothly
    else:
        w0 = 5.0
        progress = (i - 350) / 50.0
        tau = 0.2 + progress * 0.8

    # Calculate y values and update plot
    y = f_hat(omega, tau, w0)
    line.set_data(omega, y)

    # Update the text box with live variables
    text_box.set_text(
        rf"$\omega_0$ (Shift) = {w0:.2f}" + "\n" + rf"$\tau$ (Width) = {tau:.2f}"
    )

    return line, text_box


# Create the animation (interval=40 makes playback slightly slower)
ani = animation.FuncAnimation(
    fig, animate, init_func=init, frames=total_frames, interval=40, blit=True
)

plt.tight_layout()
plt.show()
