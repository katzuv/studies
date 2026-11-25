import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# --- 1. Experimental Data ---
samples = [
    {"name": "Water", "c": 0.000, "sc": 0.0005, "theta": 309.00, "color": "#1f77b4", "rich_style": "cyan", "offset": (10, -10)},
    {"name": "Green", "c": 0.250, "sc": 0.001, "theta": 327.75, "color": "#2ca02c", "rich_style": "green", "offset": (10, -10)},
    {"name": "Orange", "c": 0.494, "sc": 0.001, "theta": 345.00, "color": "#ff7f0e", "rich_style": "dark_orange", "offset": (10, -10)},
    {"name": "Red", "c": 0.743, "sc": 0.003, "theta": 184.25 + 180.0, "color": "#d62728", "rich_style": "red", "offset": (-10, 10)},
]

c = np.array([s["c"] for s in samples])
sigma_c = np.array([s["sc"] for s in samples])
theta = np.array([s["theta"] for s in samples])
theta_0 = samples[0]["theta"]
alpha = theta - theta_0

SIGMA_DIAL = 0.5
sigma_alpha = np.full_like(alpha, np.hypot(SIGMA_DIAL, SIGMA_DIAL))

# --- 2. Optical Path Length d [dm] ---
L_total_mm = 96.18
recess1_mm, std_r1 = 2.551111, 0.02285
recess2_mm, std_r2 = 2.512222, 0.03489
windows_mm = 2 * 1.45

d_mm = L_total_mm - recess1_mm - recess2_mm - windows_mm
sigma_d_mm = np.sqrt(0.02**2 + std_r1**2 + std_r2**2 + 0.02**2)

d_dm = d_mm / 100.0
sigma_d_dm = sigma_d_mm / 100.0


# --- 3. Weighted Linear Fit (Effective-Variance ODR via curve_fit) ---
def linear_model(x: np.ndarray, m: float, b: float) -> np.ndarray:
    return m * x + b


slope_est = 74.0
for _ in range(10):
    sigma_eff = np.hypot(sigma_alpha, slope_est * sigma_c)
    popt, pcov = curve_fit(
        linear_model,
        c,
        alpha,
        p0=[slope_est, 0.0],
        sigma=sigma_eff,
        absolute_sigma=True,
    )
    slope_est = popt[0]

slope, intercept = popt
sigma_slope, sigma_intercept = np.sqrt(np.diag(pcov))
dof = len(c) - len(popt)
chi2_red = np.sum(((alpha - linear_model(c, *popt)) / sigma_eff) ** 2) / dof

# --- 4. Specific Optical Activity [alpha] = slope / d ---
spec_rot = slope / d_dm
sigma_spec_rot = spec_rot * np.hypot(sigma_slope / slope, sigma_d_dm / d_dm)

# --- 5. Rich Console Output ---
console.print()
data_table = Table(
    title="Polarimetry Measurements — Sucrose Solutions",
    box=box.ROUNDED,
    header_style="bold bright_white",
)
data_table.add_column("Solution", style="bold")
data_table.add_column("Conc. c [g/mL]", justify="right")
data_table.add_column("Dial θ [deg]", justify="right")
data_table.add_column("Rotation α [deg]", justify="right")

for s, ai, sai in zip(samples, alpha, sigma_alpha):
    raw_theta = s["theta"] - 180.0 if s["name"] == "Red" else s["theta"]
    theta_str = f"{raw_theta:.2f}° (364.25°)" if s["name"] == "Red" else f"{raw_theta:.2f}°"
    data_table.add_row(
        f"[{s['rich_style']}]● {s['name']}[/]",
        f"{s['c']:.3f} ± {s['sc']:.4f}" if s["name"] == "Water" else f"{s['c']:.3f} ± {s['sc']:.3f}",
        theta_str,
        f"+{ai:.2f} ± {sai:.2f}°" if ai > 0 else f"{ai:.2f} ± {sai:.2f}°",
    )

console.print(data_table)

summary_text = (
    f"[bold]Optical Path Length (d):[/bold] {d_mm:.2f} ± {sigma_d_mm:.2f} mm  "
    f"([cyan]{d_dm:.4f} ± {sigma_d_dm:.4f} dm[/cyan])\n"
    f"[bold]Linear Fit α(c):[/bold]        α = ({slope:.2f} ± {sigma_slope:.2f})·c + "
    f"({intercept:.2f} ± {sigma_intercept:.2f}) deg\n"
    f"[bold]Goodness of Fit:[/bold]        χ²_ν = [green]{chi2_red:.3f}[/green] (dof = {dof})\n"
    f"[bold]Specific Activity [α]:[/bold]  [bold yellow]+{spec_rot:.2f} ± {sigma_spec_rot:.2f} deg·mL/(g·dm)[/bold yellow]  "
    f"[bold green](Dextrorotary, +)[/bold green]"
)
console.print(Panel(summary_text, title="Q3.2 Fit & Optical Activity Results", border_style="bright_blue", box=box.ROUNDED))

# --- 6. Plot ---
c_grid = np.linspace(-0.03, 0.80, 300)
alpha_fit = linear_model(c_grid, *popt)
sigma_band = np.sqrt((c_grid**2) * pcov[0, 0] + pcov[1, 1] + 2 * c_grid * pcov[0, 1])

fig, ax = plt.subplots(figsize=(7.5, 5.0))

ax.fill_between(
    c_grid,
    alpha_fit - sigma_band,
    alpha_fit + sigma_band,
    color="#4a5568",
    alpha=0.14,
    label=r"$1\sigma$ Fit Confidence Band",
)
ax.plot(
    c_grid,
    alpha_fit,
    "-",
    color="#2d3748",
    linewidth=1.8,
    zorder=3,
    label=(
        rf"Weighted Fit: $\alpha = ({slope:.2f} \pm {sigma_slope:.2f})c "
        rf"+ ({intercept:.2f} \pm {sigma_intercept:.2f})$"
        f"\n"
        rf"$[\alpha] = +{spec_rot:.1f} \pm {sigma_spec_rot:.1f}\ \mathrm{{deg\cdot mL/(g\cdot dm)}}$ "
        rf"($\chi^2_\nu = {chi2_red:.2f}$)"
    ),
)

# Plot each sample with its matching color & styled badge label
for s, ai, sai in zip(samples, alpha, sigma_alpha):
    ax.errorbar(
        s["c"],
        ai,
        xerr=s["sc"],
        yerr=sai,
        fmt="o",
        color=s["color"],
        ecolor=s["color"],
        elinewidth=1.4,
        capsize=3.5,
        markersize=7,
        markeredgecolor="white",
        markeredgewidth=0.8,
        zorder=5,
    )
    ha = "right" if s["name"] == "Red" else "left"
    va = "bottom" if s["name"] == "Red" else "top"
    ax.annotate(
        f"{s['name']} ({s['c']:.3f} g/mL)",
        (s["c"], ai),
        textcoords="offset points",
        xytext=s["offset"],
        ha=ha,
        va=va,
        fontsize=9,
        fontweight="bold",
        color=s["color"],
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor=s["color"],
            alpha=0.92,
            linewidth=1.1,
        ),
        zorder=6,
    )

ax.axhline(0, color="gray", linewidth=0.8, alpha=0.45)
ax.axvline(0, color="gray", linewidth=0.8, alpha=0.45)
ax.set_title("Optical Rotation Angle vs. Sucrose Concentration", fontsize=13, fontweight="bold", pad=10)
ax.set_xlabel(r"Sucrose Concentration $c$ [g/mL]", fontsize=11)
ax.set_ylabel(r"Optical Rotation $\alpha$ [deg]", fontsize=11)
ax.set_xlim(-0.04, 0.81)
ax.set_ylim(-4.5, 62)
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.95)

plt.tight_layout()
plt.savefig("q3_optical_activity.svg", format="svg", bbox_inches="tight")
console.print("[bold green]✓ Saved[/bold green] [underline]q3_optical_activity.svg[/underline]\n")
plt.show()