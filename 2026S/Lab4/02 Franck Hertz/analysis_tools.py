"""
Frank-Hertz Experiment Analysis Tools.
Contains logic to parse, analyze, and plot the characteristic curve and ionization data.
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from physlab.core import set_style


def get_last_digit_error(series_str):
    """
    Calculates the instrumental error based on the last significant digit displayed.

    @param series_str: A pandas Series containing string representations of numeric values.
    @return: The instrumental error.
    """
    decimals = series_str.str.split(".").str[1].str.len().max()
    if pd.isna(decimals) or decimals == 0:
        return 1.0
    return 10.0 ** (-decimals)


def analyze_and_plot_fh_files(file_paths, output_svg="fh_characteristic_curves.svg"):
    """
    Analyzes Frank-Hertz files by discarding low-voltage noise,
    finding physical peaks, and plotting the characteristic curves.

    @param file_paths: List of paths to CSV files.
    @param output_svg: Output filename for the plot.
    @return: A summary of results including excitation energy and contact potential.
    """
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

            peak_voltages = voltage[peaks_idx]
            peak_currents = current[peaks_idx]

            has_multiple_peaks = len(peak_voltages) >= 2
            if has_multiple_peaks:
                peak_diffs = np.diff(peak_voltages)
                mean_diff = np.mean(peak_diffs)
                std_error_diff = (
                    np.std(peak_diffs, ddof=1) / np.sqrt(len(peak_diffs))
                    if len(peak_diffs) > 1
                    else v_error_inst
                )
                excitation_energy = mean_diff
                contact_potential = peak_voltages[0] - mean_diff
                np.sqrt(v_error_inst**2 + std_error_diff**2)
            else:
                (
                    excitation_energy,
                    std_error_diff,
                    contact_potential,
                    _contact_pot_error,
                ) = np.nan, np.nan, np.nan, np.nan

            results_summary[path] = {
                "heater_mA": heater,
                "excitation_energy_eV": excitation_energy,
                "excitation_energy_error_eV": std_error_diff,
                "contact_potential_V": contact_potential,
                "peaks": list(zip(peak_voltages, peak_currents, strict=False)),
            }

            clean_label = f"$I_H$ = {heater} mA, $V_R$ = {v_ret} V"
            eb = plt.errorbar(
                raw_voltage,
                raw_current,
                xerr=v_error_inst,
                yerr=i_error_inst,
                fmt=".",
                label=clean_label,
                linewidth=0.5,
                elinewidth=0.4,
                alpha=0.6,
                capsize=1,
                zorder=3,
            )

            color = eb[0].get_color()
            plt.scatter(
                peak_voltages,
                peak_currents,
                color=color,
                s=45,
                edgecolors="black",
                zorder=5,
            )

            is_260ma = "260ma" in path.name.lower() or heater == "260"
            y_offset = -25 if is_260ma else 12

            for i, (v, cur) in enumerate(
                zip(peak_voltages, peak_currents, strict=False)
            ):
                plt.annotate(
                    f"P{i + 1}\n{v:.1f}V",
                    xy=(v, cur),
                    xytext=(0, y_offset),
                    textcoords="offset points",
                    ha="center",
                    fontsize=9,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.2", fc="white", ec=color, alpha=0.8
                    ),
                    zorder=6,
                )

        except Exception as e:
            print(f"Error processing file {path}: {e}")

    set_style(
        xlabel="Accelerating Voltage $V_a$ [V]", ylabel="Collector Current $I$ [pA]"
    )
    plt.xlim(0, 31)
    plt.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor="#e5e7eb",
        framealpha=0.9,
        fontsize=14,
    )
    plt.tight_layout()
    plt.savefig(output_svg, format="svg")
    plt.close()

    return results_summary


def analyze_ionization_experiment(
    ionization_file_path,
    contact_potential_V,
    contact_pot_error_V=0.0,
    output_svg="fh_ionization_curve.svg",
):
    """
    Analyzes the ionization curve by identifying the onset of ionization above the noise floor.

    @param ionization_file_path: Path to the ionization CSV file.
    @param contact_potential_V: The previously calculated contact potential.
    @param contact_pot_error_V: Error in the contact potential.
    @param output_svg: Output filename for the plot.
    @return: Ionization findings.
    """
    ionization_file_path = Path(ionization_file_path)
    df_str = pd.read_csv(ionization_file_path, sep="\t", header=5, dtype=str)

    raw_voltage = df_str.iloc[:, 0].astype(float).to_numpy()
    raw_current = df_str.iloc[:, 1].astype(float).to_numpy()

    v_error_inst = get_last_digit_error(df_str.iloc[:, 0])
    i_error_inst = get_last_digit_error(df_str.iloc[:, 1])

    baseline_mask = (raw_voltage >= 2.0) & (raw_voltage <= 8.0)
    baseline_currents = raw_current[baseline_mask]

    if len(baseline_currents) == 0:
        baseline_currents = raw_current[: int(len(raw_current) * 0.3)]

    mean_noise = np.mean(baseline_currents)
    std_noise = np.std(baseline_currents, ddof=1)
    statistical_noise_ceiling = mean_noise + (5.0 * std_noise)

    v_start_raw = None
    for i in range(len(raw_voltage) - 4):
        if (
            raw_current[i] > statistical_noise_ceiling
            and raw_current[i + 1] > raw_current[i]
            and raw_current[i + 2] > raw_current[i + 1]
            and raw_current[i + 3] > raw_current[i + 2]
        ):
            v_start_raw = raw_voltage[i]
            break

    if v_start_raw is None:
        v_start_raw = raw_voltage[
            np.where(raw_current > statistical_noise_ceiling)[0][0]
        ]

    true_ionization_energy = v_start_raw - contact_potential_V
    total_error = np.sqrt(v_error_inst**2 + contact_pot_error_V**2)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(
        raw_voltage,
        raw_current,
        xerr=v_error_inst,
        yerr=i_error_inst,
        fmt=".",
        color="#1f77b4",
        label="Ion Current Data ($I$)",
        linewidth=0.5,
        elinewidth=0.3,
        alpha=0.5,
        capsize=1,
        zorder=2,
    )

    ax.axhline(
        y=statistical_noise_ceiling,
        color="orange",
        linestyle=":",
        label=r"5$\sigma$ Noise Floor Ceiling",
    )
    ax.axvline(
        x=v_start_raw,
        color="crimson",
        linestyle="--",
        linewidth=1.5,
        label=f"Ionization Onset ($V_a^\\circ$ = {v_start_raw:.2f} V)",
    )

    idx_closest = np.abs(raw_voltage - v_start_raw).argmin()
    ax.scatter(
        raw_voltage[idx_closest],
        raw_current[idx_closest],
        color="crimson",
        s=100,
        edgecolors="black",
        facecolors="none",
        linewidths=2,
        zorder=5,
    )

    set_style(
        ax=ax,
        xlabel="Accelerating Voltage $V_a$ [V]",
        ylabel="Collector Current $I$ [pA]",
    )
    ax.set_xlim(0, max(raw_voltage) + 1)

    results_box_text = (
        f"Experimental Metrics:\n"
        f"Raw Onset $V_a^\\circ$: {v_start_raw:.2f} V\n"
        f"Contact Shift $V_c$: {contact_potential_V:.3f} V\n"
        f"True $E_{{ion}}$: {true_ionization_energy:.3f} $\\pm$ {total_error:.3f} eV\n"
        f"Literature Values: 10.438 eV"
    )

    ax.text(
        0.03,
        0.65,
        results_box_text,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="#f8f9fa",
            edgecolor="#d1d5db",
            alpha=0.9,
        ),
    )

    ax.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor="#e5e7eb",
        framealpha=0.9,
        fontsize=14,
    )
    plt.tight_layout()
    plt.savefig(output_svg, format="svg")
    plt.close()

    return {
        "raw_ionization_onset_V": v_start_raw,
        "true_ionization_energy_eV": true_ionization_energy,
        "error_eV": total_error,
    }


if __name__ == "__main__":
    fh_files = [
        Path("data/step10_270ma.csv"),
        Path("data/step10_250ma.csv"),
        Path("data/step10_260ma.csv"),
    ]
    print("Running characteristic curve analysis...")
    results = analyze_and_plot_fh_files(fh_files)

    # We use contact potential from the first file in results for ionization
    c_pot = results[fh_files[0]]["contact_potential_V"]
    c_pot_err = results[fh_files[0]]["excitation_energy_error_eV"]
    if pd.isna(c_pot):
        c_pot = 1.112  # fallback
    if pd.isna(c_pot_err):
        c_pot_err = 0.06  # fallback

    print(
        f"Using Contact Potential {c_pot:.3f} ± {c_pot_err:.3f} V for ionization analysis."
    )
    print("Running ionization curve analysis...")
    ion_results = analyze_ionization_experiment(
        Path("data/step2_280ma.csv"),
        contact_potential_V=c_pot,
        contact_pot_error_V=c_pot_err,
    )
    print("Done. SVGs generated.")
