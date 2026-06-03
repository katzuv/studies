import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from analysis_tools import (
    BG_ERR,
    BG_RATE,
    fit_exponential,
    load_gm,
    subtract_bg,
)

import physlab


def parse_thickness(stem):
    """Extracts numeric thickness from filename stem."""
    match = re.search(r"^(\d+(\.\d+)?)", stem)
    return float(match.group(1)) if match else None


def find_empirical_tvl_with_err(x, y, y_err):
    """
    Finds TVL empirically using log-linear interpolation and propagates the error.
    """
    target_y = y[0] / 10.0
    target_y_err = y_err[0] / 10.0

    if target_y < np.min(y):
        print(
            "  Warning: 10% target is below the minimum measured rate. Extrapolating..."
        )

    log_y = np.log(y)
    target_log_y = np.log(target_y)

    # Calculate empirical TVL using interpolation
    tvl = np.interp(target_log_y, log_y[::-1], x[::-1])

    # Error propagation using local slope around the target
    idx_below = np.where(y <= target_y)[0]
    if len(idx_below) > 0:
        i2 = idx_below[0]
        i1 = max(0, i2 - 1)
    else:
        i2 = len(y) - 1
        i1 = len(y) - 2

    if i1 != i2 and log_y[i2] != log_y[i1]:
        dx_dlogy = (x[i2] - x[i1]) / (log_y[i2] - log_y[i1])
    else:
        dx_dlogy = 0

    # delta_x = |dx/d(ln y)| * delta(ln y)
    # delta(ln y) = delta_y / y
    relative_y_err = target_y_err / target_y if target_y != 0 else 0
    tvl_err = abs(dx_dlogy) * relative_y_err

    return tvl, tvl_err


def calc_beta_energy_flammersfeld_with_err(thickness_um, thickness_err_um):
    """
    Calculates Beta max energy using Flammersfeld equation and propagates the error.
    Returns: Energy in MeV, Energy Error in MeV.
    """
    rho_al = 2.7  # Density of Aluminum in g/cm^3

    # Convert thickness to Mass Thickness (R) in g/cm^2
    thickness_cm = thickness_um * 1e-4
    thickness_err_cm = thickness_err_um * 1e-4

    R = thickness_cm * rho_al
    R_err = thickness_err_cm * rho_al

    # Flammersfeld equation: E = 1.92 * sqrt(R^2 + 0.22*R)
    E_mev = 1.92 * np.sqrt(R**2 + 0.22 * R)

    # Error propagation: derivative of Flammersfeld eq w.r.t R
    if R > 0:
        dE_dR = 1.92 * (R + 0.11) / np.sqrt(R**2 + 0.22 * R)
        E_err = dE_dR * R_err
    else:
        E_err = 0.0

    return E_mev, E_err


def main():
    # 1. Background Rate
    bg_rate = BG_RATE
    bg_err = BG_ERR
    print(f"Background Rate (Manual): {bg_rate:.3f} ± {bg_err:.3f} cps")

    # 2. Solid Angle Calculation (from Lab Manual Eq. 6)
    r_mica = 1.4  # cm
    d_source = 2.0  # cm
    omega = np.pi * (r_mica**2) / (d_source**2)
    print(f"Solid Angle (Omega): {omega:.3f} sr")

    sources = {
        "tl": {"name": "Thallium-204", "model": "empirical"},
        "sr": {"name": "Strontium-90", "model": "empirical"},
        "co": {"name": "Cobalt-60", "model": "exponential"},
    }

    plt.figure(figsize=(11, 8))

    for code, info in sources.items():
        data_dir = Path(f"data/{code}")
        if not data_dir.exists():
            continue

        thicknesses = []
        fluxes = []
        fluxes_err = []

        for file in data_dir.glob("*.tsv"):
            d = parse_thickness(file.stem)
            if d is None:
                continue

            df = load_gm(file)
            r = df["rate"].mean()
            r_e = df["rate_err"].mean()

            # Subtract background
            r_corr, r_e_corr = subtract_bg(r, r_e, bg_rate, bg_err)

            # Convert Count Rate to Radiation Flux (Eq. 6)
            flux = r_corr / omega
            flux_err = r_e_corr / omega

            thicknesses.append(d)
            fluxes.append(flux)
            fluxes_err.append(flux_err)

        idx = np.argsort(thicknesses)
        x = np.array(thicknesses)[idx]
        y = np.array(fluxes)[idx]
        y_err = np.array(fluxes_err)[idx]

        mask = y > 0
        x_fit, y_fit, y_err_fit = x[mask], y[mask], y_err[mask]

        if len(x_fit) == 0:
            continue

        try:
            # Run the exponential fit for ALL sources to get statistical metrics
            res, fit_tlv, fit_tlv_err = fit_exponential(x_fit, y_fit, y_err_fit)

            # Calculate R-squared manually to ensure it's available
            y_pred = res.model(x_fit, *res.params)
            ss_res = np.sum((y_fit - y_pred) ** 2)
            ss_tot = np.sum((y_fit - np.mean(y_fit)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            if info["model"] == "empirical":
                # Find empirical TVL with error propagation
                tlv, tlv_err = find_empirical_tvl_with_err(x_fit, y_fit, y_err_fit)

                # Calculate Energy with error propagation
                energy_mev, energy_err = calc_beta_energy_flammersfeld_with_err(
                    tlv, tlv_err
                )

                (line,) = plt.plot(
                    x_fit, y_fit, "o-", label=f"{info['name']} (Empirical)"
                )

                # Clean legend label: No TVL, only statistical metrics
                label = (
                    f"{info['name']} Empirical\n"
                    f"  Fit $R^2$: {r_squared:.3f}\n"
                    rf"  Fit $\chi^2_\nu$: {res.chi_red:.2f}"
                )

                plt.plot(
                    tlv, y_fit[0] / 10.0, "x", color=line.get_color(), markersize=10
                )
                plt.plot([], [], "-", color=line.get_color(), label=label)

                # Print clean, distinct blocks of information for each source
                print("\n========================================")
                print(f" Source: {info['name']}")
                print("========================================")
                print(f"  Calculated TVL: {tlv:.2f} ± {tlv_err:.2f} μm")
                print(f"  Calculated Energy: {energy_mev:.2f} ± {energy_err:.2f} MeV")
                print(
                    f"  Exponential Fit Stats -> R^2: {r_squared:.3f}, Chi2_red: {res.chi_red:.3f}"
                )

            else:
                (line,) = plt.plot(x_fit, y_fit, "o", label=f"{info['name']} (Data)")
                x_range = np.linspace(0, max(x_fit), 100)

                # Clean legend label for the fit model
                label = (
                    f"{info['name']} Fit\n"
                    f"  $R^2$: {r_squared:.3f}\n"
                    rf"  $\chi^2_\nu$: {res.chi_red:.2f}"
                )

                plt.plot(
                    x_range,
                    res.model(x_range, *res.params),
                    "--",
                    color=line.get_color(),
                    label=label,
                )

                print("\n========================================")
                print(f" Source: {info['name']}")
                print("========================================")
                print(f"  TVL (Fit): {fit_tlv:.2f} ± {fit_tlv_err:.2f} μm")
                print(f"  R^2: {r_squared:.3f}")
                print(f"  Chi2_red: {res.chi_red:.3f}, p-value: {res.p_value:.4f}")

        except Exception as e:
            print(f"Could not process {info['name']}: {e}")

    physlab.set_style(
        plt.gca(),
        xlabel="Aluminum Thickness (μm)",
        ylabel="Radiation Flux (cps/sr)",
    )

    plt.yscale("log")
    plt.legend(frameon=True, fontsize=11, loc="best")
    plt.tight_layout()

    plt.savefig("beta_absorption.svg")
    plt.show()
    print("\nGraph saved as beta_absorption.svg")


if __name__ == "__main__":
    main()
