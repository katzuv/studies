import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter1d
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# ==============================================================================
# 1. Experimental Parameters & Sensor Specifications
# ==============================================================================
CSV_PATH = 'imagej_1_2.csv'
WAVELENGTH_NM = 532.0          # Laser wavelength (green DPSS)

# Thorlabs CPS532-C2 Datasheet Specs
SPEC_DIAMETER_MM = 3.5         # Round beam, Ø3.5 mm (1/e^2)
SPEC_DIVERGENCE_MAX_MRAD = 0.5 # Max full-angle divergence

wavelength_m = WAVELENGTH_NM * 1e-9

# ==============================================================================
# 2. Load CSV Profile from ImageJ
# ==============================================================================
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    console.print(f"[bold red]Error:[/bold red] Could not find '[yellow]{CSV_PATH}[/yellow]'.")
    exit(1)

# Detect column names automatically (handles 'Distance_(microns)', 'Gray_Value', etc.)
dist_col = [c for c in df.columns if 'dist' in c.lower() or 'x' in c.lower()][0]
gray_col = [c for c in df.columns if 'gray' in c.lower() or 'val' in c.lower() or 'y' in c.lower()][0]

dist_um = df[dist_col].to_numpy(dtype=np.float64)
raw_profile = df[gray_col].to_numpy(dtype=np.float64)

# Smooth profile to prevent local speckle noise from trapping the fit
smooth_profile = gaussian_filter1d(raw_profile, sigma=25.0)

# ==============================================================================
# 3. Normalized Gaussian Fit: I(x) = I_bg + I_0 * exp( -2*(x - x0)^2 / w^2 )
# ==============================================================================
min_val = np.min(smooth_profile)
max_val = np.max(smooth_profile)
norm_range = max(1e-6, max_val - min_val)
norm_profile = (smooth_profile - min_val) / norm_range

def gaussian_beam(x, I_bg, I_0, x_0, w):
    return I_bg + I_0 * np.exp(-2.0 * ((x - x_0) ** 2) / (w ** 2))

# Peak estimate in microns
peak_idx = np.argmax(smooth_profile)
x0_initial = dist_um[peak_idx]
w_initial = (dist_um[-1] - dist_um[0]) / 4.0

p0 = [0.05, 0.95, x0_initial, w_initial]
lower_bounds = [-0.2, 0.1, dist_um[0], 200.0]        # Minimum width: 200 um
upper_bounds = [0.5, 1.5, dist_um[-1], (dist_um[-1] - dist_um[0]) * 2.0]

popt_norm, _ = curve_fit(
    gaussian_beam,
    dist_um,
    norm_profile,
    p0=p0,
    bounds=(lower_bounds, upper_bounds),
    maxfev=20000
)

I_bg_norm, I_0_norm, x0_um_fit, w0_um = popt_norm
w0_um = abs(w0_um)

# Rescale fitted values back to original counts
I_bg_fit = min_val + I_bg_norm * norm_range
I_0_fit = I_0_norm * norm_range

# ==============================================================================
# 4. Physical Calculations
# ==============================================================================
w0_mm = w0_um * 1e-3
w0_m = w0_um * 1e-6
beam_diameter_mm = 2.0 * w0_mm

# Rayleigh Range: z_R = pi * w0^2 / lambda
z_R = (np.pi * (w0_m ** 2)) / wavelength_m

# Theoretical far-field divergence (TEM00)
theta_div_half_mrad = (wavelength_m / (np.pi * w0_m)) * 1e3
theta_div_full_mrad = 2.0 * theta_div_half_mrad

# Comparison against Thorlabs spec sheet
diameter_diff_percent = ((beam_diameter_mm - SPEC_DIAMETER_MM) / SPEC_DIAMETER_MM) * 100.0

# ==============================================================================
# 5. Rich Console Output
# ==============================================================================
console.print("\n")
console.print(Panel.fit("[bold green]Gaussian Beam Analysis (ImageJ Profile)[/bold green]", border_style="cyan"))

table = Table(title="Beam Parameter Results & Datasheet Comparison", show_header=True, header_style="bold magenta")
table.add_column("Parameter", style="cyan", width=28)
table.add_column("Measured / Calculated", style="green", width=24)
table.add_column("Datasheet Spec", style="yellow", width=18)
table.add_column("Difference / Status", style="bold", width=22)

table.add_row(
    "Beam Center (x0)",
    f"{x0_um_fit:.1f} µm",
    "—",
    "—"
)
table.add_row(
    "Beam Waist Radius (w0)",
    f"{w0_mm:.3f} mm ({w0_um:.1f} µm)",
    f"{SPEC_DIAMETER_MM / 2.0:.3f} mm",
    f"{diameter_diff_percent:+.1f}%"
)
table.add_row(
    "Beam Diameter (2*w0)",
    f"{beam_diameter_mm:.3f} mm",
    f"Ø {SPEC_DIAMETER_MM:.1f} mm",
    f"{diameter_diff_percent:+.1f}%"
)
table.add_row(
    "Rayleigh Range (z_R)",
    f"{z_R:.2f} m",
    "—",
    "—"
)
table.add_row(
    "Divergence Half-Angle (θ)",
    f"{theta_div_half_mrad:.3f} mrad",
    "—",
    "—"
)

div_status = "[green]PASS (<= 0.5 mrad)[/green]" if theta_div_full_mrad <= SPEC_DIVERGENCE_MAX_MRAD else "[red]EXCEEDS SPEC[/red]"
table.add_row(
    "Full Divergence (2*θ)",
    f"{theta_div_full_mrad:.3f} mrad",
    f"<= {SPEC_DIVERGENCE_MAX_MRAD:.1f} mrad",
    div_status
)

console.print(table)

# ==============================================================================
# 6. Plotting & Save Figure
# ==============================================================================
x_fit_um = np.linspace(dist_um[0], dist_um[-1], 1000)
y_fit = I_bg_fit + I_0_fit * np.exp(-2.0 * ((x_fit_um - x0_um_fit) ** 2) / (w0_um ** 2))

plt.figure(figsize=(9, 5))
plt.scatter(dist_um, raw_profile, s=2, color='forestgreen', alpha=0.3, label='ImageJ Raw Profile')
plt.plot(dist_um, smooth_profile, color='limegreen', linewidth=1.2, alpha=0.7, label='Smoothed Profile')
plt.plot(x_fit_um, y_fit, color='black', linewidth=2.0, label=f'Gaussian Fit ($w_0$ = {w0_mm:.2f} mm)')

e2_level = I_bg_fit + I_0_fit * np.exp(-2.0)
plt.axhline(e2_level, color='red', linestyle='--', alpha=0.7, label=r'$1/e^2$ Threshold')

plt.title('Gaussian Beam Profile Along Line (ImageJ)')
plt.xlabel('Distance along Line (µm)')
plt.ylabel('Gray Value')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('gaussian_profile_fit.png', dpi=300)
plt.show()