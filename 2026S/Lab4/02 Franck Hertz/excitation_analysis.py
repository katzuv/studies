import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Add the project root to the path so we can import physlab
sys.path.append(str(Path(__file__).resolve().parents[2]))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from physlab.core import physics_fit, set_style


def get_last_digit_error(series_str):
    decimals = series_str.str.split(".").str[1].str.len().max()
    if pd.isna(decimals) or decimals == 0:
        return 1.0
    return 10.0 ** (-decimals)


def parabola(x, a, x0, y0):
    return a * (x - x0) ** 2 + y0


def analyze_and_plot_fh_files(
    file_paths, output_svg="fh_characteristic_curves.svg", verbose=True
):
    plt.figure(figsize=(11, 6))
    results_summary = {}

    for path in file_paths:
        path = Path(path)
        try:
            lines = path.read_text().splitlines()
            metadata_text = "\n".join(lines[:5])
            v_ret_match = re.search(r"Vr\(V\)=\s*([\d.]+)", metadata_text)
            v_ret = v_ret_match.group(1) if v_ret_match else "1.5"

            heater_match = re.search(
                r"Cathode Heater Current \(mA\) =\s*([\d.]+)", metadata_text
            )
            heater = heater_match.group(1) if heater_match else "Unknown"

            df_str = pd.read_csv(path, sep="\t", header=5, dtype=str)
            raw_voltage = df_str.iloc[:, 0].astype(float).to_numpy()
            raw_current = df_str.iloc[:, 1].astype(float).to_numpy()

            v_error_inst = get_last_digit_error(df_str.iloc[:, 0])
            i_error_inst = get_last_digit_error(df_str.iloc[:, 1])

            valid_mask = raw_voltage >= 5.0
            voltage = raw_voltage[valid_mask]
            current = raw_current[valid_mask]

            if len(voltage) == 0:
                continue

            min_sample_distance = int(3.5 / np.abs(np.diff(raw_voltage)).min())
            peaks_idx, _ = find_peaks(
                current,
                distance=min_sample_distance,
                prominence=np.ptp(current) * 0.03,
                width=5,
            )

            if len(peaks_idx) < 1:
                plt.errorbar(
                    raw_voltage,
                    raw_current,
                    xerr=v_error_inst,
                    yerr=i_error_inst,
                    fmt=".",
                    alpha=0.2,
                    linewidth=0.5,
                    elinewidth=0.5,
                )
                continue

            w = 7
            fitted_peak_voltages = []
            fitted_peak_currents = []
            fitted_peak_errors = []
            peak_chi_reds = []
            peak_dofs = []

            for idx in peaks_idx:
                start_idx = max(0, idx - w)
                end_idx = min(len(voltage) - 1, idx + w)

                x_fit = voltage[start_idx : end_idx + 1]
                y_fit = current[start_idx : end_idx + 1]
                y_err = np.full_like(y_fit, i_error_inst)

                x0_guess = voltage[idx]
                y0_guess = current[idx]
                a_guess = -5.0

                try:
                    res = physics_fit(
                        parabola,
                        x_fit,
                        y_fit,
                        y_err,
                        p0=[a_guess, x0_guess, y0_guess],
                    )
                    a_fit, x0_fit, y0_fit = res.params
                    a_err, x0_err, y0_err = res.errors
                    fitted_peak_voltages.append(x0_fit)
                    fitted_peak_currents.append(y0_fit)
                    fitted_peak_errors.append(x0_err)
                    peak_chi_reds.append(res.chi_red)
                    peak_dofs.append(res.dof)
                except Exception:
                    fitted_peak_voltages.append(voltage[idx])
                    fitted_peak_currents.append(current[idx])
                    fitted_peak_errors.append(v_error_inst)
                    peak_chi_reds.append(np.nan)
                    peak_dofs.append(0)

            peak_voltages = np.array(fitted_peak_voltages)
            peak_currents = np.array(fitted_peak_currents)
            peak_fit_errors = np.array(fitted_peak_errors)
            peak_total_errors = np.sqrt(peak_fit_errors**2 + v_error_inst**2)

            has_multiple_peaks = len(peak_voltages) >= 2
            if has_multiple_peaks:
                peak_diffs = np.diff(peak_voltages)
                n_diffs = len(peak_diffs)
                excitation_energy = np.mean(peak_diffs)
                excitation_energy_error = (
                    np.sqrt(peak_total_errors[-1] ** 2 + peak_total_errors[0] ** 2)
                    / n_diffs
                )
                contact_potential = peak_voltages[0] - excitation_energy
                contact_pot_error = np.sqrt(
                    (len(peak_voltages) / n_diffs) ** 2 * peak_total_errors[0] ** 2
                    + (1.0 / n_diffs) ** 2 * peak_total_errors[-1] ** 2
                )
            else:
                excitation_energy = np.nan
                excitation_energy_error = np.nan
                contact_potential = np.nan
                contact_pot_error = np.nan
                peak_diffs = []

            results_summary[path] = {
                "heater_mA": heater,
                "v_ret_V": v_ret,
                "excitation_energy_eV": excitation_energy,
                "excitation_energy_error_eV": excitation_energy_error,
                "contact_potential_V": contact_potential,
                "contact_potential_error_V": contact_pot_error,
                "peaks": list(
                    zip(
                        peak_voltages,
                        peak_currents,
                        peak_fit_errors,
                        peak_total_errors,
                        peak_chi_reds,
                        peak_dofs,
                        strict=True,
                    )
                ),
                "peak_diffs": peak_diffs,
                "v_error_inst": v_error_inst,
                "i_error_inst": i_error_inst,
            }

            clean_label = f"IH = {heater} mA, VR = {v_ret} V"
            eb = plt.errorbar(
                raw_voltage,
                raw_current,
                xerr=v_error_inst,
                yerr=i_error_inst,
                fmt="-",
                label=clean_label,
                linewidth=2.0,
                elinewidth=0.8,
                alpha=0.85,
                capsize=2,
                zorder=3,
            )

            color = eb[0].get_color()
            plt.scatter(
                peak_voltages,
                peak_currents,
                color=color,
                s=80,
                edgecolors="white",
                linewidths=1.5,
                zorder=5,
            )

            is_260ma = "260ma" in path.name.lower() or heater == "260"
            y_offset = -25 if is_260ma else 12

            for v, cur, _, _, _, _ in results_summary[path]["peaks"]:
                plt.annotate(
                    f"{v:.2f}V",
                    xy=(v, cur),
                    xytext=(0, y_offset),
                    textcoords="offset points",
                    ha="center",
                    fontsize=9,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        fc="#ffffff",
                        ec=color,
                        alpha=0.9,
                        linewidth=1.2,
                    ),
                    zorder=6,
                )

        except Exception as e:
            print(f"Error processing file {path}: {e}")

    set_style(xlabel="Accelerating Voltage Va [V]", ylabel="Collector Current I [pA]")
    plt.xlim(0, 31)
    plt.legend(
        loc="upper left",
        frameon=True,
        facecolor="#ffffff",
        edgecolor="#d1d5db",
        framealpha=0.95,
        fontsize=14,
        shadow=True,
    )
    plt.tight_layout()
    plt.savefig(output_svg, format="svg")
    plt.close()

    return results_summary


def main():
    console = Console()

    fh_files = [
        Path("data/step10_270ma.csv"),
        Path("data/step10_250ma.csv"),
        Path("data/step10_260ma.csv"),
    ]

    console.print(
        Panel(
            "[bold cyan]Running Part 1: Excitation Energy Analysis[/bold cyan]",
            border_style="cyan",
        )
    )

    # Run peak fitting & plotting
    results = analyze_and_plot_fh_files(fh_files)

    table = Table(
        title="[bold cyan]Franck-Hertz Run Spacings & Weighted Averages[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Run (Heater)", style="dim")
    table.add_column("Spacings (dV) [V]", justify="right")
    table.add_column("Weighted Average [V]", justify="right", style="bold green")

    run_averages = []
    run_errors = []

    for _path, res in results.items():
        heater = res["heater_mA"]
        peaks = res["peaks"]

        spacings = []
        spacing_errors = []
        for i in range(len(peaks) - 1):
            v1, _, _, v1_err_tot, _, _ = peaks[i]
            v2, _, _, v2_err_tot, _, _ = peaks[i + 1]
            diff = v2 - v1
            diff_err = np.sqrt(v1_err_tot**2 + v2_err_tot**2)
            spacings.append(diff)
            spacing_errors.append(diff_err)

        weights = 1.0 / (np.array(spacing_errors) ** 2)
        weighted_avg = np.sum(np.array(spacings) * weights) / np.sum(weights)
        weighted_avg_err = 1.0 / np.sqrt(np.sum(weights))

        run_averages.append(weighted_avg)
        run_errors.append(weighted_avg_err)

        spacings_str = ", ".join(
            f"{s:.2f} +/- {se:.3f}" for s, se in zip(spacings, spacing_errors, strict=False)
        )
        table.add_row(
            f"{heater} mA",
            spacings_str,
            f"{weighted_avg:.3f} +/- {weighted_avg_err:.3f}",
        )

    console.print(table)

    # Calculate overall weighted average of the averages
    weights_global = 1.0 / (np.array(run_errors) ** 2)
    global_weighted_avg = np.sum(np.array(run_averages) * weights_global) / np.sum(
        weights_global
    )
    global_weighted_avg_err = 1.0 / np.sqrt(np.sum(weights_global))

    # Lit comparison
    lit_value = 4.90
    abs_dev = abs(global_weighted_avg - lit_value)
    rel_dev = (abs_dev / lit_value) * 100
    sigma_diff = abs_dev / global_weighted_avg_err

    summary_text = (
        f"[bold gold1]Overall Weighted Average of Averages:[/bold gold1]\n"
        f"  E_exc = [bold green]{global_weighted_avg:.3f} +/- {global_weighted_avg_err:.3f} eV[/bold green]\n\n"
        f"[bold cyan]Comparison with Literature (4.90 eV):[/bold cyan]\n"
        f"  - Absolute Deviation: {abs_dev:.3f} eV\n"
        f"  - Relative Deviation: {rel_dev:.2f}%\n"
        f"  - Statistical Significance: {sigma_diff:.2f} sigma"
    )

    console.print(
        Panel(
            summary_text,
            title="[bold white]Part 1 Results Summary[/bold white]",
            border_style="gold1",
        )
    )


if __name__ == "__main__":
    main()
