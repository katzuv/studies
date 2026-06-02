import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from analysis_tools import (
    BG_ERR,
    BG_RATE,
    fit_exponential,
    fit_linear_tvl,
    load_gm,
    subtract_bg,
)

import physlab


def parse_thickness(stem):
    """
    Extracts thickness in micrometers (um) from filename stem.
    Examples: '160' -> 160, '1.02mm ...' -> 1020
    """
    match = re.search(r"^(\d+(\.\d+)?)", stem)
    if not match:
        return None

    val = float(match.group(1))
    if "mm" in stem.lower():
        val *= 1000
    return val


def main():
    # 1. Calculate Background Rate
    bg_df = load_gm(Path("data/bg.tsv"))
    bg_rate = bg_df["rate"].mean()
    bg_err = bg_df["rate"].std() / np.sqrt(len(bg_df))
    print(f"Background Rate: {bg_rate:.3f} +/- {bg_err:.3f} cps")

    # Sources and their appropriate physical models
    # Tl and Sr are Beta sources (Linear), Co is a Gamma source (Exponential)
    sources = {
        "tl": {"name": "Thallium-204", "model": "linear"},
        "sr": {"name": "Strontium-90", "model": "linear"},
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
            if "fake" in file.name:
                continue

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

        try:
            if info["model"] == "linear":
                res, tlv, tlv_err = fit_linear_tvl(x_fit, y_fit, y_err_fit)
            else:
                res, tlv, tlv_err = fit_exponential(x_fit, y_fit, y_err_fit)

            (line,) = plt.plot(x, y, "o", label=f"{info['name']} (Data)")
            x_range = np.linspace(0, max(x), 100)

            # Prepare legend label with Chi2_red
            label = (
                f"{info['name']} {info['model'].capitalize()} Fit\n"
                f"  TLV: {tlv:.1f} ± {tlv_err:.1f} um\n"
                f"  $\chi^2_\\nu$: {res.chi_red:.2f}"
            )

            plt.plot(
                x_range,
                res.model(x_range, *res.params),
                "--",
                color=line.get_color(),
                label=label,
            )

            print(f"\nSource: {info['name']}")
            print(f"  TLV: {tlv:.2f} +/- {tlv_err:.2f} um")
            print(f"  Chi2_red: {res.chi_red:.3f}, p-value: {res.p_value:.4f}")

        except Exception as e:
            print(f"Could not fit {info['name']}: {e}")

    physlab.set_style(
        plt.gca(),
        xlabel="Aluminum Thickness (um)",
        ylabel="Corrected Count Rate (cps)",
    )

    plt.yscale("log")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("beta_absorption_final.svg")
    print("\nGraph saved as beta_absorption_final.svg")


if __name__ == "__main__":
    main()
