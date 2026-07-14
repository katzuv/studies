import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.constants as sp
import scipy.signal as sig
from scipy.integrate import trapezoid
from scipy.optimize import curve_fit

# Standalone configuration for Bragg X-ray Spectroscopy
# Set up clean grid styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5

script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"
lif2mm_path = data_dir / "lif2mm.txt"
kbr2mm_path = data_dir / "kbr2mm.txt"
lif5mm_path = data_dir / "lif5mm.txt"

def load_data(file_path):
    if not file_path.exists():
        return None, None
    angles = []
    intensity = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("Time") or "θ" in line:
                continue
            parts = line.split()
            try:
                if len(parts) == 6:
                    # 6 columns format: Time, Impulse, U, I, Detector_angle, Crystal_angle
                    angles.append(float(parts[5]))
                    intensity.append(float(parts[1]))
                elif len(parts) >= 2:
                    # Default 2 columns format: Bragg_angle, Intensity
                    angles.append(float(parts[0]))
                    intensity.append(float(parts[1]))
            except ValueError:
                continue
    return np.array(angles), np.array(intensity)

def angle_to_energy(angle_deg, d_pm, n=1):
    hc = 1239.84193 # eV*nm
    d_nm = d_pm / 1000.0
    wavelength = (2 * d_nm * np.sin(np.radians(angle_deg))) / n
    energy_ev = hc / wavelength
    return energy_ev / 1000.0 # Convert to keV

def findtheta(E_ev, d_meters, n=1):
    E_joules = E_ev * sp.electron_volt
    lam = (sp.Planck * sp.speed_of_light) / E_joules
    sinth = (n * lam) / (2.0 * d_meters)
    if sinth > 1.0:
        return None
    return np.degrees(np.arcsin(sinth))

print("=" * 70)
print("       Bragg X-ray Spectroscopy Standalone Data Analysis ")
print("=" * 70)

# Load datasets
lif2mm_ang, lif2mm_int = load_data(lif2mm_path)
kbr2mm_ang, kbr2mm_int = load_data(kbr2mm_path)
lif5mm_ang, lif5mm_int = load_data(lif5mm_path)

if lif2mm_ang is None:
    print("Warning: lif2mm.txt not found in data/.")
if kbr2mm_ang is None:
    print("Warning: kbr2mm.txt not found in data/.")
if lif5mm_ang is None:
    print("Warning: lif5mm.txt not found in data/.")

# 1. Theoretical calculations reference table
print("\n--- 1. Theoretical Bragg Angles Reference ---")
theo_rows = []
# LiF uses Copper anode tube (Ka = 8.04 keV, Kb = 8.91 keV)
cu_lines = {"Cu K_alpha (8.040 keV)": 8040.0, "Cu K_beta (8.910 keV)": 8910.0}
for name, E in cu_lines.items():
    n = 1
    while True:
        th = findtheta(E, 201.4 * 1e-12, n)
        if th is None:
            break
        theo_rows.append({
            "Crystal": "LiF (d=201.4 pm)",
            "Emission Line": name,
            "Order (n)": n,
            "Bragg Angle (deg)": round(th, 2)
        })
        n += 1

# KBr uses Molybdenum anode tube (Ka = 17.479 keV, Kb = 19.608 keV)
mo_lines = {"Mo K_alpha (17.479 keV)": 17479.34, "Mo K_beta (19.608 keV)": 19608.3}
for name, E in mo_lines.items():
    n = 1
    while True:
        th = findtheta(E, 329.9 * 1e-12, n)
        if th is None:
            break
        theo_rows.append({
            "Crystal": "KBr (d=329.9 pm)",
            "Emission Line": name,
            "Order (n)": n,
            "Bragg Angle (deg)": round(th, 2)
        })
        n += 1

df_theo = pd.DataFrame(theo_rows)
print(df_theo.to_string(index=False))

# 2. Peak matching and zero-point alignment
print("\n--- 2. Experimental Peak Matches & Zero-Point Deviations ---")

# LiF (2mm) Matching
offsets_lif = []
lif_match_rows = []
if lif2mm_ang is not None and len(lif2mm_ang) > 0:
    box = np.ones(7) / 7.0
    smoothed = np.convolve(lif2mm_int, box, mode="same")
    peaks, _ = sig.find_peaks(smoothed, prominence=20, distance=5)
    peaks_found = [(lif2mm_ang[p], lif2mm_int[p]) for p in peaks if lif2mm_ang[p] > 5.0]

    for row in theo_rows:
        if "LiF" in row["Crystal"]:
            best = None
            min_diff = float("inf")
            for exp_a, counts in peaks_found:
                diff = abs(exp_a - row["Bragg Angle (deg)"])
                if diff < min_diff and diff < 1.0:
                    min_diff = diff
                    best = (exp_a, counts)
            if best:
                offset = best[0] - row["Bragg Angle (deg)"]
                offsets_lif.append(offset)
                lif_match_rows.append({
                    "Line": row["Emission Line"].split(" ")[1],
                    "Order (n)": row["Order (n)"],
                    "Theo Angle (deg)": row["Bragg Angle (deg)"],
                    "Exp Angle (deg)": round(best[0], 2),
                    "Offset (deg)": round(offset, 2),
                    "Intensity (cps)": int(best[1])
                })

print("\nLiF (2mm) Peak Alignment:")
if lif_match_rows:
    df_match_lif = pd.DataFrame(lif_match_rows)
    print(df_match_lif.to_string(index=False))
    print(f"Average LiF Goniometer Zero-Point Shift (Delta theta_B): {np.mean(offsets_lif):+.2f} deg")
else:
    print("No matches found.")

# KBr (2mm) Matching
offsets_kbr = []
kbr_match_rows = []
if kbr2mm_ang is not None and len(kbr2mm_ang) > 0:
    peaks, _ = sig.find_peaks(kbr2mm_int, prominence=25, distance=4)
    peaks_found = [(kbr2mm_ang[p], kbr2mm_int[p]) for p in peaks if kbr2mm_ang[p] > 5.0]

    for row in theo_rows:
        if "KBr" in row["Crystal"]:
            best = None
            min_diff = float("inf")
            for exp_a, counts in peaks_found:
                diff = abs(exp_a - row["Bragg Angle (deg)"])
                if diff < min_diff and diff < 1.5:
                    min_diff = diff
                    best = (exp_a, counts)
            if best:
                offset = best[0] - row["Bragg Angle (deg)"]
                offsets_kbr.append(offset)
                kbr_match_rows.append({
                    "Line": row["Emission Line"].split(" ")[1],
                    "Order (n)": row["Order (n)"],
                    "Theo Angle (deg)": row["Bragg Angle (deg)"],
                    "Exp Angle (deg)": round(best[0], 2),
                    "Offset (deg)": round(offset, 2),
                    "Intensity (cps)": int(best[1])
                })

print("\nKBr (2mm) Peak Alignment:")
if kbr_match_rows:
    df_match_kbr = pd.DataFrame(kbr_match_rows)
    print(df_match_kbr.to_string(index=False))
    print(f"Average KBr Goniometer Zero-Point Shift (Delta theta_B): {np.mean(offsets_kbr):+.2f} deg")
else:
    print("No matches found.")

# 3. Peak Fitting (Gaussian fit of Cu Ka and Kb first-order peaks)
print("\n--- 3. Gaussian Peak Fitting (LiF 2mm) ---")
if lif2mm_ang is not None and len(lif2mm_ang) > 0:
    def double_gaussian_with_bg(x, amp_a, ctr_a, sig_a, amp_b, ctr_b, sig_b, bg_slope, bg_inter):
        gauss_a = amp_a * np.exp(-0.5 * ((x - ctr_a) / sig_a) ** 2)
        gauss_b = amp_b * np.exp(-0.5 * ((x - ctr_b) / sig_b) ** 2)
        bg = bg_slope * x + bg_inter
        return gauss_a + gauss_b + bg

    fit_mask = (lif2mm_ang >= 18.5) & (lif2mm_ang <= 24.5)
    x_fit = lif2mm_ang[fit_mask]
    y_fit = lif2mm_int[fit_mask]
    y_err = np.sqrt(np.clip(y_fit, 1.0, None))

    p0 = [max(y_fit), 22.4, 0.15, max(y_fit)/4.0, 20.1, 0.15, 0.0, min(y_fit)]

    try:
        popt, pcov = curve_fit(double_gaussian_with_bg, x_fit, y_fit, p0=p0, sigma=y_err, absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))

        ctr_ka, ctr_kb = popt[1], popt[4]
        err_ka, err_kb = perr[1], perr[4]

        # Convert angles to keV
        E_ka = 1239.84193 / (2 * 0.2014 * np.sin(np.radians(ctr_ka)))
        E_kb = 1239.84193 / (2 * 0.2014 * np.sin(np.radians(ctr_kb)))

        def get_de(theta, d_theta):
            theta_rad = np.radians(theta)
            d_theta_rad = np.radians(d_theta)
            deriv = -1239.84193 * np.cos(theta_rad) / (2 * 0.2014 * (np.sin(theta_rad)**2))
            return abs(deriv) * d_theta_rad

        E_ka_err = get_de(ctr_ka, err_ka)
        E_kb_err = get_de(ctr_kb, err_kb)

        print(f"Cu K_alpha Centroid: {ctr_ka:.3f} deg +/- {err_ka:.3f} deg")
        print(f"Cu K_beta Centroid:  {ctr_kb:.3f} deg +/- {err_kb:.3f} deg")
        print(f"Fitted Cu K_alpha Energy: {E_ka/1000.0:.3f} +/- {E_ka_err/1000.0:.3f} keV")
        print(f"Fitted Cu K_beta Energy:  {E_kb/1000.0:.3f} +/- {E_kb_err/1000.0:.3f} keV")

        # Save fitted constants to data/constants.json
        constants_data = {
            "Copper K-alpha Energy": {
                "value": E_ka / 1000.0,
                "error": E_ka_err / 1000.0,
                "units": "keV"
            },
            "Copper K-beta Energy": {
                "value": E_kb / 1000.0,
                "error": E_kb_err / 1000.0,
                "units": "keV"
            }
        }
        with open(data_dir / "constants.json", "w", encoding="utf-8") as f:
            json.dump(constants_data, f, indent=4)
        print("Fitted energy results exported to data/constants.json.")

        # Plot fitting panel
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.errorbar(x_fit, y_fit, yerr=y_err, fmt="o", color="#333333", markersize=3, label="Data", alpha=0.6)
        x_dense = np.linspace(18.5, 24.5, 300)
        ax.plot(x_dense, double_gaussian_with_bg(x_dense, *popt), color="#C73E1D", linewidth=2.0, label="Fit")
        ax.plot(x_dense, popt[6] * x_dense + popt[7], color="#A23B72", linestyle=":", label="Background")
        ax.set_xlabel(r"Bragg Angle $\theta_B$ ($^\circ$)")
        ax.set_ylabel("Intensity (cps)")
        ax.legend()
        plt.tight_layout()
        fig.savefig(data_dir / "peak_fit.svg")
        plt.close(fig)

    except Exception as e:
        print(f"Gaussian peak fitting failed: {str(e)}")

# 4. Generate SVG Plots
print("\n--- 4. Generating and Saving SVG Plots ---")

def plot_experiment(ang, idx_ang, label, color, E_label, E_color, d_pm, peaks_x, lines_def, filename_ang, filename_eng):
    if ang is None:
        return
    # Angle Plot (Log scale)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ang, idx_ang, label=f"{label} Data", color=color)
    ax.set_yscale("log")
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel(r"Bragg Angle $\theta_B$ ($^\circ$)")
    ax.set_ylabel("Intensity (log cps)")

    # Peak markers
    matched_x = [row["Exp Angle (deg)"] for row in peaks_x]
    matched_y = [row["Intensity (cps)"] for row in peaks_x]
    if matched_x:
        ax.scatter(matched_x, matched_y, color="#C73E1D", marker="x", s=60, zorder=5, label="Matched Peaks")
        for x, y in zip(matched_x, matched_y, strict=False):
            ax.text(x + 0.5, y * 1.1, f"{x:.2f}°", color="#C73E1D", fontsize=9, fontweight="bold")
            ax.axvline(x, color="#C73E1D", linestyle=":", alpha=0.5)

    ax.legend()
    plt.tight_layout()
    fig.savefig(data_dir / filename_ang)
    plt.close(fig)

    # Energy Plot (Linear scale)
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    energies = angle_to_energy(ang[ang > 3.0], d_pm, n=1)
    ax2.plot(energies, idx_ang[ang > 3.0], label=f"{label} Data", color=E_color)
    ax2.set_xlabel("Energy (keV)")
    ax2.set_ylabel("Intensity (cps)")
    ax2.set_xlim(3.0, 25.0)

    if matched_x:
        matched_e = angle_to_energy(np.array(matched_x), d_pm, n=1)
        ax2.scatter(matched_e, matched_y, color="#C73E1D", marker="x", s=60, zorder=5, label="Matched Peaks")
        for e, y, row in zip(matched_e, matched_y, peaks_x, strict=False):
            lbl = r"$K_\alpha$" if "alpha" in row["Line"].lower() else r"$K_\beta$"
            ax2.text(e + 0.2, y * 1.05, f"{lbl} (n={row['Order (n)']})\n{e:.2f} keV", color="#C73E1D", fontsize=9, fontweight="bold")
            ax2.axvline(e, color="#C73E1D", linestyle=":", alpha=0.5)

    ax2.legend()
    plt.tight_layout()
    fig2.savefig(data_dir / filename_eng)
    plt.close(fig2)

# Generate plots for all three scans
plot_experiment(lif2mm_ang, lif2mm_int, "LiF (2mm)", "#2E86AB", "LiF (2mm)", "#A23B72", 201.4, lif_match_rows, cu_lines, "spectrum_vs_angle.svg", "spectrum_vs_energy.svg")
plot_experiment(kbr2mm_ang, kbr2mm_int, "KBr (2mm)", "#F18F01", "KBr (2mm)", "#C73E1D", 329.9, kbr_match_rows, mo_lines, "kbr_spectrum_vs_angle.svg", "kbr_spectrum_vs_energy.svg")

# Match peaks for LiF 5mm and plot
lif5mm_match_rows = []
if lif5mm_ang is not None and len(lif5mm_ang) > 0:
    box = np.ones(7) / 7.0
    smoothed = np.convolve(lif5mm_int, box, mode="same")
    peaks, _ = sig.find_peaks(smoothed, prominence=20, distance=5)
    peaks_found = [(lif5mm_ang[p], lif5mm_int[p]) for p in peaks if lif5mm_ang[p] > 5.0]

    for row in theo_rows:
        if "LiF" in row["Crystal"]:
            best = None
            min_diff = float("inf")
            for exp_a, counts in peaks_found:
                diff = abs(exp_a - row["Bragg Angle (deg)"])
                if diff < min_diff and diff < 1.0:
                    min_diff = diff
                    best = (exp_a, counts)
            if best:
                offset = best[0] - row["Bragg Angle (deg)"]
                lif5mm_match_rows.append({
                    "Line": row["Emission Line"].split(" ")[1],
                    "Order (n)": row["Order (n)"],
                    "Theo Angle (deg)": row["Bragg Angle (deg)"],
                    "Exp Angle (deg)": round(best[0], 2),
                    "Offset (deg)": round(offset, 2),
                    "Intensity (cps)": int(best[1])
                })

plot_experiment(lif5mm_ang, lif5mm_int, "LiF (5mm)", "#2E86AB", "LiF (5mm)", "#A23B72", 201.4, lif5mm_match_rows, cu_lines, "lif5mm_spectrum_vs_angle.svg", "lif5mm_spectrum_vs_energy.svg")

# 5. Diaphragm Comparison (2mm vs 5mm)
if lif2mm_ang is not None and lif5mm_ang is not None:
    fig, ax = plt.subplots(figsize=(8, 5))
    mask_2mm = (lif2mm_ang > 18.0) & (lif2mm_ang < 25.0)
    mask_5mm = (lif5mm_ang > 18.0) & (lif5mm_ang < 25.0)

    y_2mm_norm = lif2mm_int[mask_2mm] / trapezoid(lif2mm_int[mask_2mm], lif2mm_ang[mask_2mm])
    y_5mm_norm = lif5mm_int[mask_5mm] / trapezoid(lif5mm_int[mask_5mm], lif5mm_ang[mask_5mm])

    ax.plot(lif2mm_ang[mask_2mm], y_2mm_norm, label="2mm Diaphragm", color="#2E86AB")
    ax.plot(lif5mm_ang[mask_5mm], y_5mm_norm, label="5mm Diaphragm", color="#A23B72")
    ax.set_xlabel(r"Bragg Angle $\theta_B$ ($^\circ$)")
    ax.set_ylabel("Normalized Intensity")
    ax.legend()
    plt.tight_layout()
    fig.savefig(data_dir / "collimator_comparison.svg")
    plt.close(fig)

# 6. Crystal Comparison (LiF vs KBr)
if lif2mm_ang is not None and kbr2mm_ang is not None:
    fig, ax = plt.subplots(figsize=(8, 5))
    lif_e = angle_to_energy(lif2mm_ang[lif2mm_ang > 3.0], 201.4, n=1)
    lif_y = lif2mm_int[lif2mm_ang > 3.0]
    kbr_e = angle_to_energy(kbr2mm_ang[kbr2mm_ang > 3.0], 329.9, n=1)
    kbr_y = kbr2mm_int[kbr2mm_ang > 3.0]

    ax.plot(lif_e, lif_y, label="LiF (200) - d=201.4 pm", color="#2E86AB")
    ax.plot(kbr_e, kbr_y, label="KBr (200) - d=329.9 pm", color="#F18F01")
    ax.axvline(13.47, color="#C73E1D", linestyle="--", alpha=0.8, label="Br K-edge: 13.47 keV")
    ax.set_xlabel("Energy (keV)")
    ax.set_ylabel("Intensity (cps)")
    ax.legend()
    plt.tight_layout()
    fig.savefig(data_dir / "crystal_comparison.svg")
    plt.close(fig)

print("All standalone analysis outputs and graphs updated.")
print("=" * 70)
