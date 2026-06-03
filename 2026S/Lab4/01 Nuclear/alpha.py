from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from analysis_tools import BG_ERR, BG_RATE, load_gm, subtract_bg

import physlab


def main():
    # 1. Background
    bg_rate = BG_RATE
    bg_err = BG_ERR

    # Constants from the lab manual
    X_MICA = 2.0  # mg/cm^2 (Mica window areal density)
    RHO_AIR = 1.2  # mg/cm^3 (Air density)
    R_MICA = 1.4  # cm (radius of the GM window)

    # Fixed Geometry of the system
    D_TOP_SHELF_TO_WINDOW = 12.3  # mm

    # Calculate the air-equivalent thickness of the mica window in cm
    D_WINDOW_AIR_EQ = X_MICA / RHO_AIR
    print("========================================")
    print(" Alpha Radiation - System Parameters")
    print("========================================")
    print(f"Mica Window Air-Equivalent: {D_WINDOW_AIR_EQ:.3f} cm")
    print(f"Top Shelf to Window Offset: {D_TOP_SHELF_TO_WINDOW:.1f} mm")
    print(f"Background Rate: {bg_rate:.3f} ± {bg_err:.3f} cps\n")

    # 2. Define files and their distance ADDED BELOW the top shelf (in mm).
    # Applied the logical correction: alpha 1 is likely at 32 mm.
    alpha_measurements = {"alpha 1": 32.0, "alpha 2 16mm": 16.0}

    d_eff_list = []
    fluxes = []
    fluxes_err = []

    print("========================================")
    print(" Measurements & Calculations")
    print("========================================")

    for stem, d_added_mm in alpha_measurements.items():
        file_path = Path(f"{stem}.tsv")
        if not file_path.exists():
            file_path = Path(f"data/{stem}.tsv")

        if not file_path.exists():
            print(f"  [!] Warning: Could not find {stem}.tsv")
            continue

        try:
            df = load_gm(file_path)
            r = df["rate"].mean()
            r_e = df["rate_err"].mean()

            # Subtract background
            r_corr, r_e_corr = subtract_bg(r, r_e, bg_rate, bg_err)

            # Total Physical Distance in Air (cm)
            d_air_mm_total = d_added_mm + D_TOP_SHELF_TO_WINDOW
            d_air_cm = d_air_mm_total / 10.0

            # Calculate Solid Angle (Exact disk formula for close distances)
            omega = 2 * np.pi * (1 - (d_air_cm / np.sqrt(d_air_cm**2 + R_MICA**2)))

            # Convert Count Rate to Radiation Flux & Propagate Error
            flux = r_corr / omega
            flux_err = r_e_corr / omega

            # Calculate Effective Distance (D_eff) in cm
            d_eff_cm = d_air_cm + D_WINDOW_AIR_EQ

            d_eff_list.append(d_eff_cm)
            fluxes.append(flux)
            fluxes_err.append(flux_err)

            print(f"File: {stem}.tsv")
            print(f"  Added Dist (from Top Shelf): {d_added_mm:.1f} mm")
            print(f"  Total Physical Air Dist: {d_air_cm:.3f} cm")
            print(f"  Solid Angle (Exact): {omega:.3f} sr")
            print(f"  Effective Dist (D_eff): {d_eff_cm:.3f} cm")
            print(f"  Corrected Rate: {r_corr:.2f} ± {r_e_corr:.2f} cps")
            print(f"  -> Radiation Flux: {flux:.2f} ± {flux_err:.2f} cps/sr\n")

        except Exception as e:
            print(f"  [!] Error processing {stem}: {e}")

    if len(d_eff_list) < 2:
        print("\nNot enough data to plot. Please check file paths.")
        return

    # 3. Sort data by effective distance
    idx = np.argsort(d_eff_list)
    x = np.array(d_eff_list)[idx]
    y = np.array(fluxes)[idx]
    y_err = np.array(fluxes_err)[idx]

    # 4. Plotting
    plt.figure(figsize=(8, 6))

    # Plot with error bars
    plt.errorbar(
        x,
        y,
        yerr=y_err,
        fmt="o-",
        color="purple",
        markersize=8,
        linewidth=2,
        capsize=5,
        label="Alpha Source (Am-241)",
    )

    physlab.set_style(
        plt.gca(),
        xlabel="Effective Distance in Air ($D_{eff}$) [cm]",
        ylabel="Radiation Flux [cps/sr]",
    )

    plt.ylim(bottom=0)

    # Add a bit of padding to the x-axis so the 2 points are clearly visible
    plt.xlim(min(x) - 0.5, max(x) + 0.5)

    plt.legend(frameon=True, fontsize=11, loc="best")
    plt.tight_layout()
    plt.savefig("alpha_absorption_flux.svg")
    plt.show()

    print("Graph saved as alpha_absorption_flux.svg")


if __name__ == "__main__":
    main()
