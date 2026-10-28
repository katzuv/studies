import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter1d
from PIL import Image
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# ==============================================================================
# 1. Experimental Parameters & Sensor Specifications
# ==============================================================================
IMAGE_PATH = "q1.tif"
PIXEL_SIZE_UM = 3.45  # 3.45 um x 3.45 um from sensor spec
WAVELENGTH_NM = 532.0  # 532 nm

# Thorlabs CPS532-C2 Spec Sheet Nominal Values
SPEC_DIAMETER_MM = 3.5  # Round beam, Ø3.5 mm (1/e^2)
SPEC_DIVERGENCE_MAX_MRAD = 0.5  # Max full-angle divergence

pixel_size_m = PIXEL_SIZE_UM * 1e-6
wavelength_m = WAVELENGTH_NM * 1e-9

# ==============================================================================
# 2. Image Loading & Line Profile Extraction
# ==============================================================================
try:
    img = Image.open(IMAGE_PATH)
except FileNotFoundError:
    console.print(
        f"[bold red]Error:[/bold red] Could not find '[yellow]{IMAGE_PATH}[/yellow]'. Check your current working directory."
    )
    exit(1)

img_arr = np.array(img, dtype=np.float64)

if img_arr.ndim == 3:
    intensity_map = img_arr[:, :, 1] if img_arr.shape[2] >= 2 else img_arr[:, :, 0]
else:
    intensity_map = img_arr

peak_y, peak_x = np.unravel_index(np.argmax(intensity_map), intensity_map.shape)

# Average across 11 rows around the peak to suppress speckle noise
half_band = 5
y_start = max(0, peak_y - half_band)
y_end = min(intensity_map.shape[0], peak_y + half_band + 1)
raw_profile = np.mean(intensity_map[y_start:y_end, :], axis=0)

# 1D smoothing along the line profile
horizontal_profile = gaussian_filter1d(raw_profile, sigma=2.0)
x_pixels = np.arange(len(horizontal_profile), dtype=np.float64)

# ==============================================================================
# 3. Normalization & Curve Fitting
# ==============================================================================
min_val = np.min(horizontal_profile)
max_val = np.max(horizontal_profile)
norm_range = max(1e-6, max_val - min_val)
norm_profile = (horizontal_profile - min_val) / norm_range


def normalized_gaussian(x, I_bg, I_0, x_0, w):
    return I_bg + I_0 * np.exp(-2.0 * ((x - x_0) ** 2) / (w**2))


p0 = [0.05, 0.9, float(peak_x), float(len(x_pixels) / 4.0)]
lower_bounds = [-0.2, 0.1, 0.0, 5.0]
upper_bounds = [0.5, 2.0, float(len(x_pixels)), float(len(x_pixels) * 3.0)]

popt_norm, _ = curve_fit(
    normalized_gaussian,
    x_pixels,
    norm_profile,
    p0=p0,
    bounds=(lower_bounds, upper_bounds),
    maxfev=20000,
)

I_bg_norm, I_0_norm, x_0_fit, w_pixels = popt_norm
w_pixels = abs(w_pixels)

I_bg_fit = min_val + I_bg_norm * norm_range
I_0_fit = I_0_norm * norm_range

# ==============================================================================
# 4. Physical Calculations & Spec Sheet Comparison
# ==============================================================================
w0_m = w_pixels * pixel_size_m
w0_mm = w0_m * 1e3
beam_diameter_mm = 2.0 * w0_mm

# Rayleigh Range: z_R = pi * w0^2 / lambda
z_R = (np.pi * (w0_m**2)) / wavelength_m

# Far-field divergence (theoretical TEM00)
theta_div_half_mrad = (wavelength_m / (np.pi * w0_m)) * 1e3
theta_div_full_mrad = 2.0 * theta_div_half_mrad

# Relative differences from Thorlabs CPS532-C2 datasheet
diameter_diff_percent = (
    (beam_diameter_mm - SPEC_DIAMETER_MM) / SPEC_DIAMETER_MM
) * 100.0

# ==============================================================================
# 5. Rich Output Display
# ==============================================================================
console.print("\n")
console.print(
    Panel.fit(
        "[bold green]Gaussian Beam Analysis & Spec Sheet Benchmark[/bold green]",
        border_style="cyan",
    )
)

table = Table(
    title="Beam Parameter Results & Datasheet Comparison",
    show_header=True,
    header_style="bold magenta",
)
table.add_column("Parameter", style="cyan", width=28)
table.add_column("Measured / Calculated", style="green", width=24)
table.add_column("Datasheet Spec", style="yellow", width=18)
table.add_column("Difference / Status", style="bold", width=22)

table.add_row("Beam Center (x0)", f"{x_0_fit:.1f} px", "—", "—")
table.add_row(
    "Beam Waist Radius (w0)",
    f"{w0_mm:.3f} mm ({w_pixels:.1f} px)",
    f"{SPEC_DIAMETER_MM / 2.0:.3f} mm",
    f"{diameter_diff_percent:+.1f}%",
)
table.add_row(
    "Beam Diameter (2*w0)",
    f"{beam_diameter_mm:.3f} mm",
    f"Ø {SPEC_DIAMETER_MM:.1f} mm",
    f"{diameter_diff_percent:+.1f}%",
)
table.add_row("Rayleigh Range (z_R)", f"{z_R:.2f} m", "—", "—")
table.add_row("Divergence Half-Angle (θ)", f"{theta_div_half_mrad:.3f} mrad", "—", "—")

div_status = (
    "[green]PASS (<= 0.5 mrad)[/green]"
    if theta_div_full_mrad <= SPEC_DIVERGENCE_MAX_MRAD
    else "[red]EXCEEDS SPEC[/red]"
)
table.add_row(
    "Full Divergence (2*θ)",
    f"{theta_div_full_mrad:.3f} mrad",
    f"<= {SPEC_DIVERGENCE_MAX_MRAD:.1f} mrad",
    div_status,
)

console.print(table)

# ==============================================================================
# 6. Plotting & Save
# ==============================================================================
x_fit = np.linspace(0, len(x_pixels) - 1, 1000)
y_fit = I_bg_fit + I_0_fit * np.exp(-2.0 * ((x_fit - x_0_fit) ** 2) / (w_pixels**2))

plt.figure(figsize=(9, 5))
plt.scatter(
    x_pixels, raw_profile, s=3, color="forestgreen", alpha=0.3, label="Raw Data Profile"
)
plt.plot(
    x_fit,
    y_fit,
    color="black",
    linewidth=2.0,
    label=f"Gaussian Fit ($w_0$ = {w0_mm:.2f} mm)",
)

e2_level = I_bg_fit + I_0_fit * np.exp(-2.0)
plt.axhline(
    e2_level, color="red", linestyle="--", alpha=0.7, label=r"$1/e^2$ Threshold"
)

plt.title(f"Horizontal Profile & Gaussian Fit (Row {peak_y})")
plt.xlabel("Pixel Index (x)")
plt.ylabel("Intensity (Raw Counts)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("gaussian_beam_fit.png", dpi=300)
plt.show()
