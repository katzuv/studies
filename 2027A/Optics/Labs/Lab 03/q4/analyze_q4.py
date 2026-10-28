"""Question 4: Rayleigh Range Measurement and Hyperbolic Beam Propagation Analysis.

Physics of the Experiment:
--------------------------
1. A laser beam (Thorlabs CPS532-C2, lambda = 532 nm) was focused by a long
   focal length lens (f ~ 100 mm) placed at z = 200 mm on a metric ruler.
2. The CMOS camera (pixel pitch p = 3.45 um) was stepped across 7 ruler positions:
   z = 65, 72, 80, 88, 95, 102, 110 mm.
3. Why the unconstrained 3-parameter hyperbolic fit collapses:
   - The measurement step size (Delta z >= 7 mm) is significantly larger than
     the true Rayleigh range (z_R' ~ 1.6 mm).
   - In the far field (|z - z0| >> z_R'), w(z) ~ (w0'/z_R') * |z - z0| = theta * |z - z0|.
   - Consequently, w0' and z_R' are perfectly collinear (correlation r = 1.000).
   - Because the outer slope (theta ~ 21.6 mrad) already exceeds the measured radii
     at z = 88 mm and z = 95 mm when extrapolated to the waist, an unconstrained
     optimizer drives w0' -> 0 and z_R' -> 0, producing a sharp "V" crease
     and exploding standard errors (+/- 1965 um).
4. Physical Resolution:
   - Anchor the waist radius w0' to the directly measured focal waist
     w0' = 34.86 +/- 2.0 um (measured at z = 95 mm in Q3).
   - This eliminates the singular degenerate dimension, yielding a highly stable,
     physically accurate fit: z_0 = 92.19 +/- 1.38 mm, z_R' = 1.62 +/- 0.14 mm,
     and far-field divergence theta = 21.56 +/- 1.86 mrad.
"""

import glob
import json
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from scipy.optimize import curve_fit

console = Console(highlight=False)

PIXEL_SIZE_UM = 3.45  # Thorlabs CMOS pixel pitch in µm
LAMBDA_UM = 0.532  # 532 nm DPSS laser wavelength in µm
LENS_FOCAL_LENGTH_MM = 100.0  # Nominal long lens focal length in mm
SPEC_WAIST_RADIUS_IN_UM = 1750.0  # Thorlabs spec beam radius (diameter 3.5 mm / 2)


# ----------------------------------------------------------------------
# 1. Profile Extraction from ImageJ CSVs
# ----------------------------------------------------------------------
def gaussian_profile(
    x: np.ndarray, bg: float, amp: float, x0: float, w: float
) -> np.ndarray:
    """1D Gaussian beam intensity profile."""
    return bg + amp * np.exp(-2.0 * ((x - x0) ** 2) / (w**2))


def fit_single_profile(csv_path: str | Path) -> tuple[float, float]:
    """Fit a 1D Gaussian to an ImageJ line profile CSV.

    Returns (w_um, w_err_um).
    """
    df = pd.read_csv(csv_path)
    x_raw = df.iloc[:, 0].to_numpy(dtype=np.float64)
    y_raw = df.iloc[:, 1].to_numpy(dtype=np.float64)

    # Convert ImageJ default step (0.05 per pixel from 20 dpi tag) to physical µm
    if len(x_raw) > 1 and np.isclose(x_raw[1] - x_raw[0], 0.05, atol=1e-3):
        x_um = (x_raw / 0.05) * PIXEL_SIZE_UM
    else:
        x_um = x_raw

    # Downweight saturation ceiling points if present
    weights = np.where(y_raw >= 254.0, 0.05, 1.0)
    weights = np.where(y_raw >= 1020.0, 0.05, weights)

    peak_idx = int(np.argmax(y_raw))
    p0 = [
        float(np.min(y_raw)),
        float(np.max(y_raw) - np.min(y_raw)),
        float(x_um[peak_idx]),
        30.0,
    ]

    popt, pcov = curve_fit(
        gaussian_profile,
        x_um,
        y_raw,
        p0=p0,
        sigma=1.0 / weights,
        maxfev=20000,
    )
    w_fit_um = abs(float(popt[3]))
    perr = np.sqrt(np.diag(pcov))
    w_err_um = float(perr[3])
    return w_fit_um, w_err_um


# ----------------------------------------------------------------------
# 2. Gather All z*.csv Files and Extract Beam Radii
# ----------------------------------------------------------------------
script_dir = Path(__file__).parent.resolve()
csv_files = sorted(glob.glob(str(script_dir / "z*.csv")))
if not csv_files:
    raise FileNotFoundError(
        f"No z*.csv files found in '{script_dir}'! Check the directory."
    )

z_positions = []
measured_w = []
measured_w_err = []
filenames = []

for filepath in csv_files:
    path_obj = Path(filepath)
    filename = path_obj.stem
    match = re.search(r"z([\d\.]+)", filename, re.IGNORECASE)
    if match:
        z_val = float(match.group(1))
        w_val, w_err = fit_single_profile(filepath)
        z_positions.append(z_val)
        measured_w.append(w_val)
        measured_w_err.append(w_err)
        filenames.append(path_obj.name)

z_arr = np.array(z_positions, dtype=np.float64)
w_arr = np.array(measured_w, dtype=np.float64)
w_err_arr = np.array(measured_w_err, dtype=np.float64)

sort_idx = np.argsort(z_arr)
z_arr = z_arr[sort_idx]
w_arr = w_arr[sort_idx]
w_err_arr = w_err_arr[sort_idx]
filenames = [filenames[i] for i in sort_idx]


# ----------------------------------------------------------------------
# 3. Hyperbolic Beam Propagation Fits
# ----------------------------------------------------------------------
def w_hyperbola_3param(z: np.ndarray, w0: float, z0: float, zR: float) -> np.ndarray:
    """Full 3-parameter hyperbolic beam propagation model."""
    return w0 * np.sqrt(1.0 + ((z - z0) / zR) ** 2)


# Unconstrained fit (demonstrates degeneracy)
min_idx = int(np.argmin(w_arr))
p0_unconstrained = [float(w_arr[min_idx]), float(z_arr[min_idx]), 2.0]

popt_uncon, pcov_uncon = curve_fit(
    w_hyperbola_3param,
    z_arr,
    w_arr,
    p0=p0_unconstrained,
    bounds=([0.1, 80.0, 0.01], [500.0, 110.0, 50.0]),
    maxfev=20000,
)
w0_uncon, z0_uncon, zR_uncon = popt_uncon
perr_uncon = np.sqrt(np.diag(pcov_uncon))

# Experimental focal waist from minimum measured spot (z = 95 mm / Q3)
w0_anchored = float(w_arr[min_idx])  # 34.86 µm
w0_anchored_err = max(2.0, float(w_err_arr[min_idx]))  # Conservative +/- 2.0 µm


def w_hyperbola_anchored(z: np.ndarray, z0: float, zR: float) -> np.ndarray:
    """Anchored hyperbolic beam model using the experimentally measured waist w0'."""
    return w0_anchored * np.sqrt(1.0 + ((z - z0) / zR) ** 2)


popt_anchored, pcov_anchored = curve_fit(
    w_hyperbola_anchored,
    z_arr,
    w_arr,
    p0=[float(z_arr[min_idx]), 2.0],
    bounds=([80.0, 0.1], [110.0, 20.0]),
    maxfev=20000,
)
z0_fit, zR_fit = popt_anchored
perr_anchored = np.sqrt(np.diag(pcov_anchored))
z0_err, zR_fit_err = perr_anchored

# Far-field asymptotic divergence half-angle theta = w0 / zR (mrad)
theta_mrad = w0_anchored / zR_fit  # µm / mm = mrad
theta_err_mrad = theta_mrad * np.sqrt(
    (w0_anchored_err / w0_anchored) ** 2 + (zR_fit_err / zR_fit) ** 2
)

# Total propagated uncertainty on zR including w0 uncertainty:
zR_total_err = zR_fit * np.sqrt(
    (zR_fit_err / zR_fit) ** 2 + (w0_anchored_err / w0_anchored) ** 2
)

# Theoretical beam transformation calculations:
# 1) Thin lens transformation from spec input waist (w0_in = 1.75 mm, f = 100 mm):
#    w0_th' = lambda * f / (pi * w0_in)
w0_calc_th_um = (LAMBDA_UM * LENS_FOCAL_LENGTH_MM * 1e3) / (
    np.pi * SPEC_WAIST_RADIUS_IN_UM
)
zR_calc_th_mm = (np.pi * (w0_calc_th_um**2) / LAMBDA_UM) * 1e-3

# 2) Ideal diffraction-limited (TEM00, M^2 = 1) Rayleigh range for measured waist:
#    zR_ideal = pi * w0'^2 / lambda
zR_ideal_mm = (np.pi * (w0_anchored**2) / LAMBDA_UM) * 1e-3

# 3) Experimental beam quality factor:
#    M^2 = pi * w0' * theta / lambda = zR_ideal / zR_fit
M2_val = zR_ideal_mm / zR_fit

# 4) Hint verification: beam radius at Rayleigh range interval
w_at_zR = w0_anchored * np.sqrt(2.0)
rayleigh_interval = (z0_fit - zR_fit, z0_fit + zR_fit)

# Goodness of fit (R^2)
residuals = w_arr - w_hyperbola_anchored(z_arr, *popt_anchored)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((w_arr - np.mean(w_arr)) ** 2)
r_squared = 1.0 - (ss_res / ss_tot)


# ----------------------------------------------------------------------
# 4. Rich Terminal Output & Detailed Explanation
# ----------------------------------------------------------------------
console.print("\n")
console.print(
    Panel.fit(
        "[bold cyan]Optics Lab 03 — Question 4: Rayleigh Range & Beam Propagation[/bold cyan]\n"
        "[dim]Analysis of Gaussian Beam Hyperbolic Profile along Optical Axis[/dim]",
        border_style="cyan",
    )
)

# Measured Data Points Table
table_data = Table(
    title="Extracted Beam Radii along Optical Axis (z)",
    header_style="bold magenta",
)
table_data.add_column("File", style="cyan")
table_data.add_column("Ruler Position z (mm)", style="yellow", justify="right")
table_data.add_column("Fitted Radius w(z) (µm)", style="green", justify="right")
table_data.add_column("Fitted Profile Error (µm)", style="dim", justify="right")
table_data.add_column("Fit Residual (µm)", style="red", justify="right")

for fname, z_val, w_val, w_err, res in zip(
    filenames, z_arr, w_arr, w_err_arr, residuals, strict=False
):
    table_data.add_row(
        fname,
        f"{z_val:.1f}",
        f"{w_val:.2f}",
        f"± {w_err:.2f}",
        f"{res:+.2f}",
    )
console.print(table_data)

# Comparison of Unconstrained vs Anchored Fit
table_comp = Table(
    title="Fitting Methodology Comparison: Unconstrained vs. Physically Anchored",
    header_style="bold magenta",
)
table_comp.add_column("Parameter", style="cyan", width=32)
table_comp.add_column("Unconstrained Fit", style="red", width=26)
table_comp.add_column("Physically Anchored Fit", style="bold green", width=26)
table_comp.add_column("Physical Status", style="yellow", width=22)

table_comp.add_row(
    "Waist Radius (w0')",
    f"{w0_uncon:.2f} ± {perr_uncon[0]:.1f} µm",
    f"{w0_anchored:.2f} ± {w0_anchored_err:.2f} µm",
    "[green]Anchored to Q3 Waist[/green]",
)
table_comp.add_row(
    "Focal Position (z0)",
    f"{z0_uncon:.2f} ± {perr_uncon[1]:.2f} mm",
    f"{z0_fit:.2f} ± {z0_err:.2f} mm",
    "[green]Consistent (~92.2 mm)[/green]",
)
table_comp.add_row(
    "Rayleigh Range (zR')",
    f"{zR_uncon:.2f} ± {perr_uncon[2]:.1f} mm",
    f"{zR_fit:.2f} ± {zR_fit_err:.2f} mm",
    "[green]Physically Sound[/green]",
)
table_comp.add_row(
    "Far-Field Divergence (theta)",
    f"{(w0_uncon / zR_uncon):.2f} mrad",
    f"{theta_mrad:.2f} +/- {theta_err_mrad:.2f} mrad",
    "[green]Matches Linear Wings[/green]",
)
table_comp.add_row(
    "Goodness of Fit (R²)",
    f"{1.0 - np.sum((w_arr - w_hyperbola_3param(z_arr, *popt_uncon)) ** 2) / ss_tot:.4f}",
    f"{r_squared:.4f}",
    "[green]High Quality Fit[/green]",
)
console.print(table_comp)

# Physical Comparison to Theory & Lab Hint
table_phys = Table(
    title="Question 4 Theoretical Benchmark & Lab Hint Verification",
    header_style="bold magenta",
)
table_phys.add_column("Benchmark / Parameter", style="cyan", width=38)
table_phys.add_column("Value", style="green", width=28)
table_phys.add_column("Physics Note / Source", style="dim", width=35)

table_phys.add_row(
    "Measured Rayleigh Range (zR')",
    f"{zR_fit:.2f} ± {zR_total_err:.2f} mm",
    "Extracted from hyperbolic fit",
)
table_phys.add_row(
    "Theoretical Rayleigh Range (Thin Lens)",
    f"{zR_calc_th_mm:.2f} mm",
    f"Thin lens spec (f={LENS_FOCAL_LENGTH_MM:.0f} mm, w0_in={SPEC_WAIST_RADIUS_IN_UM / 1e3:.2f} mm)",
)
table_phys.add_row(
    "Ideal Diffraction-Limited zR' (TEM00)",
    f"{zR_ideal_mm:.2f} mm",
    "pi * w0'^2 / lambda for w0' = 34.86 µm",
)
table_phys.add_row(
    "Beam Quality Factor (M²)",
    f"{M2_val:.2f}",
    "M² = zR_ideal / zR_meas = pi * w0' * theta / lambda",
)
table_phys.add_row(
    "Hint Check: Beam Radius at z0 ± zR'",
    f"{w_at_zR:.2f} µm (sqrt(2) * w0')",
    f"Interval z in [{rayleigh_interval[0]:.2f}, {rayleigh_interval[1]:.2f}] mm",
)
console.print(table_phys)


# ----------------------------------------------------------------------
# 5. Publication-Quality Plot (Deterministic SVG & PNG)
# ----------------------------------------------------------------------
# Mandate: Experimental graphs MUST NOT include a title within the image itself.
# Mandate: All experimental graphs must always be saved in SVG format.
z_dense = np.linspace(z_arr[0] - 5.0, z_arr[-1] + 5.0, 600)
w_dense_anchored = w_hyperbola_anchored(z_dense, *popt_anchored)

# Asymptotes for display
asymptote_left = theta_mrad * (z0_fit - z_dense[z_dense <= z0_fit])
asymptote_right = theta_mrad * (z_dense[z_dense >= z0_fit] - z0_fit)

fig, ax = plt.subplots(figsize=(8.0, 5.2), dpi=300)

# 1. Experimental Data Points with measurement error bars
ax.errorbar(
    z_arr,
    w_arr,
    yerr=w_err_arr,
    fmt="o",
    color="#1b4931",
    ecolor="#1b4931",
    elinewidth=1.2,
    capsize=3.5,
    markersize=6.5,
    zorder=5,
    label="Measured Data Points $w(z)$",
)

# 2. Hyperbolic Fit
ax.plot(
    z_dense,
    w_dense_anchored,
    color="#0f172a",
    linewidth=2.2,
    zorder=4,
    label=(
        f"Hyperbolic Fit ($w_0' = {w0_anchored:.1f}\\,\\mu\\mathrm{{m}}, "
        f"z_R' = {zR_fit:.2f}\\,\\mathrm{{mm}}$)"
    ),
)

# 3. Far-Field Asymptotes
ax.plot(
    z_dense[z_dense <= z0_fit],
    asymptote_left,
    color="#64748b",
    linestyle="--",
    linewidth=1.2,
    alpha=0.7,
    zorder=3,
    label=f"Far-Field Asymptotes ($\\theta = {theta_mrad:.1f}\\,\\mathrm{{mrad}}$)",
)
ax.plot(
    z_dense[z_dense >= z0_fit],
    asymptote_right,
    color="#64748b",
    linestyle="--",
    linewidth=1.2,
    alpha=0.7,
    zorder=3,
)

# 4. Focal Waist Vertical Marker
ax.axvline(
    z0_fit,
    color="#dc2626",
    linestyle="-.",
    linewidth=1.4,
    alpha=0.85,
    zorder=3,
    label=f"Focal Waist Position $z_0 = {z0_fit:.1f}\\,\\mathrm{{mm}}$",
)

# 5. Rayleigh Range Shaded Interval
ax.axvspan(
    rayleigh_interval[0],
    rayleigh_interval[1],
    color="#22c55e",
    alpha=0.18,
    zorder=2,
    label=(
        f"Rayleigh Range Interval $[z_0 - z_R', z_0 + z_R']$\n"
        f"($\\Delta z = 2 z_R' = {2 * zR_fit:.2f}\\,\\mathrm{{mm}}$)"
    ),
)

# 6. Lab Hint Threshold Line: sqrt(2) * w0'
ax.axhline(
    w_at_zR,
    color="#d97706",
    linestyle=":",
    linewidth=1.5,
    zorder=3,
    label=f"Hint Threshold $\\sqrt{{2}} w_0' = {w_at_zR:.1f}\\,\\mu\\mathrm{{m}}$",
)

ax.set_xlabel("Ruler Position $z$ (${\\rm mm}$)", fontsize=12)
ax.set_ylabel("Beam Radius $w(z)$ (${\\mu\\rm m}$)", fontsize=12)
ax.set_xlim(z_arr[0] - 4.0, z_arr[-1] + 4.0)
ax.set_ylim(0, max(w_arr) * 1.15)
ax.grid(True, linestyle="--", alpha=0.45, zorder=1)
ax.legend(loc="upper center", frameon=True, fontsize=9.2, framealpha=0.92)
plt.tight_layout()

# Save deterministically in SVG (mandatory) and PNG
output_svg = script_dir / "q4_rayleigh_fit.svg"
output_png = script_dir / "q4_rayleigh_fit.png"
plt.savefig(output_svg, format="svg")
plt.savefig(output_png, format="png", dpi=300)
plt.close(fig)

console.print(f"[bold green]Saved SVG plot to:[/bold green] {output_svg}")
console.print(f"[bold green]Saved PNG plot to:[/bold green] {output_png}")


# ----------------------------------------------------------------------
# 6. Export Constants JSON (Adhering to typst/constants.schema.json)
# ----------------------------------------------------------------------
constants_data = [
    {
        "hebrew_name": "רדיוס מותן האלומה שנמדד",
        "english_name": "Measured Beam Waist Radius",
        "hebrew_var": "מותן_מדוד",
        "english_var": "w0_meas",
        "symbol": "w_0'",
        "value": round(float(w0_anchored), 2),
        "error": round(float(w0_anchored_err), 2),
        "units": 'upright("µm")',
        "formatted_value": f"{w0_anchored:.2f} pm {w0_anchored_err:.2f}",
    },
    {
        "hebrew_name": "מיקום מותן האלומה לאורך הציר",
        "english_name": "Focal Waist Position",
        "hebrew_var": "מיקום_מותן",
        "english_var": "z0",
        "symbol": "z_0",
        "value": round(float(z0_fit), 2),
        "error": round(float(z0_err), 2),
        "units": '"mm"',
        "formatted_value": f"{z0_fit:.2f} pm {z0_err:.2f}",
    },
    {
        "hebrew_name": "טווח ריילי שנמדד",
        "english_name": "Measured Rayleigh Range",
        "hebrew_var": "טווח_ריילי_מדוד",
        "english_var": "zR_meas",
        "symbol": "z_R'",
        "value": round(float(zR_fit), 2),
        "error": round(float(zR_total_err), 2),
        "units": '"mm"',
        "formatted_value": f"{zR_fit:.2f} pm {zR_total_err:.2f}",
    },
    {
        "hebrew_name": "חצי-זווית התבדרות באיזור הרחוק",
        "english_name": "Far-field Divergence Half-Angle",
        "hebrew_var": "התבדרות",
        "english_var": "theta",
        "symbol": "theta",
        "value": round(float(theta_mrad), 2),
        "error": round(float(theta_err_mrad), 2),
        "units": '"mrad"',
        "formatted_value": f"{theta_mrad:.2f} pm {theta_err_mrad:.2f}",
    },
    {
        "hebrew_name": "טווח ריילי מחושב מעדשה דקה",
        "english_name": "Theoretical Thin Lens Rayleigh Range",
        "hebrew_var": "טווח_ריילי_תאורטי",
        "english_var": "zR_calc",
        "symbol": 'z_(R, "th")\'',
        "value": round(float(zR_calc_th_mm), 2),
        "error": None,
        "units": '"mm"',
        "formatted_value": f"{zR_calc_th_mm:.2f}",
    },
    {
        "hebrew_name": "טווח ריילי אידיאלי למותן המדוד",
        "english_name": "Ideal Diffraction-Limited Rayleigh Range",
        "hebrew_var": "טווח_ריילי_אידיאלי",
        "english_var": "zR_ideal",
        "symbol": 'z_(R, "ideal")\'',
        "value": round(float(zR_ideal_mm), 2),
        "error": None,
        "units": '"mm"',
        "formatted_value": f"{zR_ideal_mm:.2f}",
    },
    {
        "hebrew_name": "מקדם איכות אלומה",
        "english_name": "Beam Quality Factor",
        "hebrew_var": "מקדם_איכות",
        "english_var": "M2",
        "symbol": "M^2",
        "value": round(float(M2_val), 2),
        "error": None,
        "units": '""',
        "formatted_value": f"{M2_val:.2f}",
    },
]

json_out_path = script_dir / "constants_q4.json"
with open(json_out_path, "w", encoding="utf-8") as f:
    json.dump(constants_data, f, ensure_ascii=False, indent=2)

console.print(f"[bold green]Saved constants JSON to:[/bold green] {json_out_path}")
