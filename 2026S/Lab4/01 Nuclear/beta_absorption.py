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


def find_empirical_tvl(x, y):
    """
    Finds TVL empirically using log-linear interpolation.
    Assumes the first point (x[0]) is the unattenuated rate.
    """
    target_y = y[0] / 10.0

    if target_y < np.min(y):
        print(
            "  Warning: 10% target is below the minimum measured rate. Extrapolating..."
        )

    log_y = np.log(y)
    target_log_y = np.log(target_y)

    tvl = np.interp(target_log_y, log_y[::-1], x[::-1])
    return tvl


def calc_beta_energy_flammersfeld(thickness_um):
    """
    Calculates Beta max energy using Flammersfeld equation.
    thickness_um: thickness in micrometers.
    Returns: Energy in MeV.
    """
    # 1. Convert thickness to Mass Thickness (R) in g/cm^2
    rho_al = 2.7  # Density of Aluminum in g/cm^3
    thickness_cm = thickness_um * 1e-4
    R = thickness_cm * rho_al

    # 2. Flammersfeld equation: E = 1.92 * sqrt(R^2 + 0.22*R)
    # Valid for E < ~3 MeV
    E_mev = 1.92 * np.sqrt(R**2 + 0.22 * R)
    return E_mev


def main():
    # 1. Background Rate
    bg_rate = BG_RATE
    bg_err = BG_ERR
    print(f"Background Rate (Manual): {bg_rate:.3f} ± {bg_err:.3f} cps")

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
        rates = []
        rates_err = []

        for file in data_dir.glob("*.tsv"):
            d = parse_thickness(file.stem)
            if d is None:
                continue

            df = load_gm(file)
            r = df["rate"].mean()
            r_e = df["rate_err"].mean()

            r_corr, r_e_corr = subtract_bg(r, r_e, bg_rate, bg_err)

            thicknesses.append(d)
            rates.append(r_corr)
            rates_err.append(r_e_corr)

        idx = np.argsort(thicknesses)
        x = np.array(thicknesses)[idx]
        y = np.array(rates)[idx]
        y_err = np.array(rates_err)[idx]

        mask = y > 0
        x_fit, y_fit, y_err_fit = x[mask], y[mask], y_err[mask]

        if len(x_fit) == 0:
            continue

        try:
            print(f"\nSource: {info['name']}")

            # Run the exponential fit for ALL sources to get statistical metrics (R^2, chi_red)
            res, fit_tlv, fit_tlv_err = fit_exponential(x_fit, y_fit, y_err_fit)

            # Calculate R-squared manually to ensure it's available
            y_pred = res.model(x_fit, *res.params)
            ss_res = np.sum((y_fit - y_pred) ** 2)
            ss_tot = np.sum((y_fit - np.mean(y_fit)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            if info["model"] == "empirical":
                # Find empirical TVL
                tlv = find_empirical_tvl(x_fit, y_fit)

                # Calculate Energy
                energy_mev = calc_beta_energy_flammersfeld(tlv)

                (line,) = plt.plot(
                    x_fit, y_fit, "o-", label=f"{info['name']} (Empirical)"
                )

                # Add label information with Energy
                label = (
                    f"{info['name']} Empirical\n"
                    f"  TVL: {tlv:.1f} μm\n"
                    f"  Energy (Est.): {energy_mev:.2f} MeV\n"
                    f"  Fit $R^2$: {r_squared:.3f}\n"
                    rf"  Fit $\chi^2_\nu$: {res.chi_red:.2f}"
                )

                plt.plot(
                    tlv, y_fit[0] / 10.0, "x", color=line.get_color(), markersize=10
                )
                plt.plot([], [], "-", color=line.get_color(), label=label)

                print(f"  TVL (Empirical): {tlv:.2f} μm")
                print(f"  Estimated Energy: {energy_mev:.2f} MeV")
                print(
                    f"  Exponential Fit Stats -> R^2: {r_squared:.3f}, Chi2_red: {res.chi_red:.3f}"
                )

            else:
                (line,) = plt.plot(x_fit, y_fit, "o", label=f"{info['name']} (Data)")
                x_range = np.linspace(0, max(x_fit), 100)

                label = (
                    f"{info['name']} Fit\n"
                    f"  TVL: {fit_tlv:.1f} ± {fit_tlv_err:.1f} μm\n"
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

                print(f"  TVL (Fit): {fit_tlv:.2f} ± {fit_tlv_err:.2f} μm")
                print(f"  R^2: {r_squared:.3f}")
                print(f"  Chi2_red: {res.chi_red:.3f}, p-value: {res.p_value:.4f}")

        except Exception as e:
            print(f"Could not process {info['name']}: {e}")

    physlab.set_style(
        plt.gca(),
        xlabel="Aluminum Thickness (μm)",
        ylabel="Corrected Count Rate (cps)",
    )

    plt.yscale("log")
    plt.legend(frameon=True, fontsize=11, loc="best")
    plt.tight_layout()

    plt.savefig("beta_absorption.svg")
    plt.show()
    print("\nGraph saved as beta_absorption.svg")


if __name__ == "__main__":
    main()
