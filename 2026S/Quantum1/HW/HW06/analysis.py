import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.constants as const
from scipy.optimize import curve_fit

from physlab.core import export_constants, set_style

# 1. Load the data
df = pd.read_csv("atom_distributions.csv")


# 2. Define the Gaussian fit function (centered at the origin)
def gaussian(x, A, delta):
    return A * np.exp(-(x**2) / (delta**2))


times = ["t2_us", "t4_us", "t6_us", "t8_us"]
labels = [
    r"$t = 2\ \mathrm{\mu s}$",
    r"$t = 4\ \mathrm{\mu s}$",
    r"$t = 6\ \mathrm{\mu s}$",
    r"$t = 8\ \mathrm{\mu s}$",
]
markers = ["o", "s", "^", "D"]

# --- FIGURE 1: Raw Data Only (For 4.א) ---
fig1, ax1 = plt.subplots(figsize=(8, 6))
for col, label, marker in zip(times, labels, markers, strict=True):
    ax1.scatter(df["bin"], df[col], label=label, marker=marker, s=40, alpha=0.85)

set_style(
    ax=ax1,
    xlabel=r"Position $x\ [\mathrm{\mu m}]$",
    ylabel="Probability",
    grid=True,
)
ax1.legend(frameon=True, fontsize=12, loc="upper right")
plt.figure(fig1.number)
plt.tight_layout()
plt.savefig("distributions.svg", format="svg", bbox_inches="tight")
plt.close(fig1)

# --- FIGURE 2: Raw Data + Fits (For 4.ב) ---
fig2, ax2 = plt.subplots(figsize=(8, 6))
constants_data = []
x_dense = np.linspace(-10, 10, 500)

for i, (col, label, marker) in enumerate(zip(times, labels, markers, strict=True)):
    x_data = df["bin"].values
    y_data = df[col].values

    # Initial guess
    p0 = [np.max(y_data), 1.0]

    # Perform fit
    popt, _ = curve_fit(gaussian, x_data, y_data, p0=p0)
    A_fit, delta_fit = popt

    # Store fit results for export (no errors)
    time_val = (i + 1) * 2
    constants_data.append(
        {
            "hebrew_name": f"רוחב חבילת הגלים בזמן t={time_val} מיקרו-שניות",
            "english_name": f"Wave packet width at t={time_val} us",
            "hebrew_var": f"דלתא_{time_val}",
            "english_var": f"delta_{time_val}",
            "symbol": rf"\Delta({time_val}\ \mathrm{{\mu s}})",
            "value": float(delta_fit),
            "error": None,
            "units": "",
            "fmt_spec": ".4f",
        }
    )

    # Plot raw scatter data
    scatter = ax2.scatter(x_data, y_data, label=label, marker=marker, s=40, alpha=0.85)
    color = scatter.get_facecolor()[0]

    # Plot continuous fitted Gaussian curve
    ax2.plot(
        x_dense,
        gaussian(x_dense, A_fit, delta_fit),
        color=color,
        linestyle="-",
        linewidth=1.5,
        alpha=0.9,
    )

set_style(
    ax=ax2,
    xlabel=r"Position $x\ [\mathrm{\mu m}]$",
    ylabel="Probability",
    grid=True,
)
ax2.legend(frameon=True, fontsize=12, loc="upper right")
plt.figure(fig2.number)
plt.tight_layout()
plt.savefig("distributions_fit.svg", format="svg", bbox_inches="tight")
plt.close(fig2)

# --- FIGURE 3: Width Spreading and Linear Fit (For 4.ד) ---
fig3, ax3 = plt.subplots(figsize=(8, 6))

t_points = np.array([2.0, 4.0, 6.0, 8.0])
delta_points = np.array([c["value"] for c in constants_data])


def linear_model(t, a, b):
    return a * t + b


# Perform unweighted linear fit
popt_lin, _ = curve_fit(linear_model, t_points, delta_points)
a_fit, b_fit = popt_lin

# Convert slope to SI units: 1 um/us = 1 m/s
# So slope in m/s is exactly a_fit.

hbar = const.hbar
amu = 1.660538921e-27  # atomic mass unit in kg
delta0 = 0.07e-6  # initial width in meters

# Formula: m = hbar / (a * delta0) --> Leads to Lithium-7
m_li = hbar / (a_fit * delta0)
m_li_amu = m_li / amu

# Add linear fit results to constants_data (no errors)
constants_data.append(
    {
        "hebrew_name": "שיפוע גרף התרחבות חבילת הגלים",
        "english_name": "Slope of wave packet width vs time",
        "hebrew_var": "שיפוע",
        "english_var": "slope",
        "symbol": "a",
        "value": float(a_fit),
        "error": None,
        "units": '"μm/μs"',
        "fmt_spec": ".4f",
    }
)

constants_data.append(
    {
        "hebrew_name": "חיתוך גרף התרחבות חבילת הגלים",
        "english_name": "Intercept of wave packet width vs time",
        "hebrew_var": "חיתוך",
        "english_var": "intercept",
        "symbol": "b",
        "value": float(b_fit),
        "error": None,
        "units": '"μm"',
        "fmt_spec": ".4f",
    }
)

# Add Mass constants (no errors)
constants_data.append(
    {
        "hebrew_name": "מסת האטום (קג)",
        "english_name": "Atomic mass (kg)",
        "hebrew_var": "מסה_קג",
        "english_var": "mass_kg",
        "symbol": "m",
        "value": float(m_li),
        "error": None,
        "units": '"kg"',
        "fmt_spec": ".4e",
    }
)
constants_data.append(
    {
        "hebrew_name": "מסת האטום (אמו)",
        "english_name": "Atomic mass (amu)",
        "hebrew_var": "מסה_אמו",
        "english_var": "mass_amu",
        "symbol": "m",
        "value": float(m_li_amu),
        "error": None,
        "units": '"u"',
        "fmt_spec": ".2f",
    }
)

# Plot data points
ax3.plot(
    t_points,
    delta_points,
    "o",
    color="#A23B72",
    label="Fitted widths " + r"$\Delta(t)$",
    markersize=6,
)

# Plot fitted line
t_dense = np.linspace(1.5, 8.5, 100)
ax3.plot(
    t_dense,
    linear_model(t_dense, a_fit, b_fit),
    color="#2E86AB",
    linestyle="--",
    linewidth=1.8,
    label=rf"Linear Fit: $\Delta(t) = {a_fit:.4f} t + {b_fit:.4f}$",
)

set_style(
    ax=ax3,
    xlabel=r"Time $t\ [\mathrm{\mu s}]$",
    ylabel=r"Width $\Delta\ [\mathrm{\mu m}]$",
    grid=True,
)
ax3.legend(frameon=True, fontsize=11, loc="upper left")
plt.figure(fig3.number)
plt.tight_layout()
plt.savefig("width_fit.svg", format="svg", bbox_inches="tight")
plt.close(fig3)

print("Saved distributions.svg, distributions_fit.svg, and width_fit.svg successfully.")

# Export constants to JSON and Typst files
export_constants(constants_data, ".")
print("Exported constants successfully.")
