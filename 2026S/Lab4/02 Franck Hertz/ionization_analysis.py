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

from physlab.core import set_style
from excitation_analysis import analyze_and_plot_fh_files


def get_last_digit_error(series_str):
    decimals = series_str.str.split(".").str[1].str.len().max()
    if pd.isna(decimals) or decimals == 0:
        return 1.0
    return 10.0 ** (-decimals)


def analyze_ionization_experiment(
    ionization_file_path,
    contact_potential_V,
    contact_pot_error_V=0.0,
    output_svg="fh_ionization_curve.svg",
):
    ionization_file_path = Path(ionization_file_path)
    df_str = pd.read_csv(ionization_file_path, sep="\t", header=5, dtype=str)

    raw_voltage = df_str.iloc[:, 0].astype(float).to_numpy()
    raw_current = df_str.iloc[:, 1].astype(float).to_numpy()

    # Step size dynamically found
    v_diffs = np.abs(np.diff(raw_voltage))
    step_size = np.round(np.median(v_diffs[v_diffs > 0]), 3)
    v_error_inst = step_size
    i_error_inst = get_last_digit_error(df_str.iloc[:, 1])

    # Baseline calculations
    baseline_mask = (raw_voltage >= 2.0) & (raw_voltage <= 8.0)
    baseline_currents = raw_current[baseline_mask]
    if len(baseline_currents) == 0:
        baseline_currents = raw_current[: int(len(raw_current) * 0.3)]

    mean_noise = np.mean(baseline_currents)
    std_noise = np.std(baseline_currents, ddof=1)
    mean_noise_err = std_noise / np.sqrt(len(baseline_currents))

    # Statistical ceiling for detecting the early rise
    statistical_noise_ceiling = mean_noise + (5.0 * std_noise)

    # --- מציאת נקודת העלייה הראשונית (לתצוגה ויזואלית בלבד) ---
    v_initial_rise = None
    for i in range(len(raw_voltage) - 3):
        if (
            raw_current[i] > statistical_noise_ceiling
            and raw_current[i + 1] > raw_current[i]
            and raw_current[i + 2] > raw_current[i + 1]
        ):
            v_initial_rise = raw_voltage[i]
            break

    if v_initial_rise is None:
        idx_above = np.where(raw_current > statistical_noise_ceiling)[0]
        if len(idx_above) > 0:
            v_initial_rise = raw_voltage[idx_above[0]]
        else:
            v_initial_rise = raw_voltage[0]

    # --- UPDATED: Linear Extrapolation Method (לחישוב הפיזיקלי) ---
    # 1. Calculate the discrete derivative (slope) of the current
    dI_dV = np.gradient(raw_current, raw_voltage)

    # 2. Find the steepest part of the curve (ignoring the noisy start)
    valid_indices = np.where(raw_voltage > 7.0)[0]
    if len(valid_indices) == 0:
        valid_indices = np.arange(len(raw_voltage))

    max_slope_idx = valid_indices[np.argmax(dI_dV[valid_indices])]

    # 3. Take a window of points around the steepest slope to perform a linear fit
    window_size = 2  # 2 points back, 2 points forward
    fit_start = max(0, max_slope_idx - window_size)
    fit_end = min(len(raw_voltage), max_slope_idx + window_size + 1)

    x_fit = raw_voltage[fit_start:fit_end]
    y_fit = raw_current[fit_start:fit_end]

    # Linear fit: y = mx + b
    slope, intercept = np.polyfit(x_fit, y_fit, 1)

    # 4. Find where the extrapolation line intersects the baseline noise floor
    v_onset = (mean_noise - intercept) / slope
    v_onset_err = v_error_inst  # Uncertainty remains bound by the resolution step

    # Calculate final physics
    true_ionization_energy = v_onset - contact_potential_V
    total_error = np.sqrt(v_onset_err**2 + contact_pot_error_V**2)

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the raw data
    ax.errorbar(
        raw_voltage,
        raw_current,
        xerr=v_error_inst,
        yerr=i_error_inst,
        fmt=".",
        color="#2E86AB",
        label="Ion Current Data (I)",
        markersize=4.0,
        elinewidth=1.0,
        alpha=0.9,
        capsize=2,
        zorder=2,
    )

    # הוספת קו אנכי לתחילת העלייה הראשונית
    ax.axvline(
        x=v_initial_rise,
        color="#4CAF50",
        linestyle=":",
        linewidth=2.5,
        label=f"Initial Current Rise (~{v_initial_rise:.2f} V)",
        zorder=3,
    )
    # סימון הנקודה על הגרף
    idx_initial = np.abs(raw_voltage - v_initial_rise).argmin()
    ax.scatter(
        raw_voltage[idx_initial],
        raw_current[idx_initial],
        color="#4CAF50",
        s=120,
        marker="X",
        zorder=5,
    )

    # Plot the curve fit (linear regression) from the onset to the fit region
    x_extrapolate = np.linspace(v_onset, raw_voltage[fit_end] if fit_end < len(raw_voltage) else max(raw_voltage), 100)
    y_extrapolate = slope * x_extrapolate + intercept
    ax.plot(
        x_extrapolate,
        y_extrapolate,
        color="orange",
        linestyle="-",
        linewidth=2,
        label="Linear Regression",
        zorder=3,
    )



    # Plot intersection point and onset line (The physical result)
    ax.axvline(
        x=v_onset,
        color="#C73E1D",
        linestyle="-.",
        linewidth=2.5,
        label=f"Extrapolated Onset ($V_{{a0}}$ = {v_onset:.2f} V)",
    )
    ax.scatter(
        v_onset,
        mean_noise,
        color="#C73E1D",
        s=150,
        edgecolors="white",
        linewidths=2.5,
        zorder=5,
    )

    # Highlight the points used for the fit
    ax.scatter(x_fit, y_fit, color="#FCA311", s=80, label="Fit Region", zorder=4)

    set_style(
        ax=ax,
        xlabel=r"Acceleration voltage ($V_a$) [V]",
        ylabel="Collector current [pA]",
    )
    ax.set_xlim(0, 15)

    # Set y-axis to focus on the relevant part
    ax.set_ylim(mean_noise - 5, 1000)

    ax.legend(loc="upper left", frameon=True, shadow=True, fontsize=14)
    plt.tight_layout()
    plt.savefig(output_svg, format="svg")
    plt.close()

    return {
        "fitted_ionization_onset_V": v_onset,
        "fitted_ionization_onset_error_V": v_onset_err,
        "true_ionization_energy_eV": true_ionization_energy,
        "error_eV": total_error,
        "mean_noise": mean_noise,
        "mean_noise_err": mean_noise_err,
        "std_noise": std_noise,
    }


def main():
    console = Console()
    base_dir = Path(__file__).resolve().parent

    fh_files = [
        base_dir / "data/step10_270ma.csv",
        base_dir / "data/step10_250ma.csv",
        base_dir / "data/step10_260ma.csv",
    ]

    console.print(
        Panel.fit(
            "[bold yellow]*** FRANCK-HERTZ EXPERIMENT - PART 2: IONIZATION POTENTIAL ANALYSIS ***[/bold yellow]\n"
            "[dim]Linear extrapolation of maximum slope to baseline noise floor[/dim]",
            border_style="bold gold1",
            padding=(1, 4),
            title="[bold green]Technion Physics Lab 4[/bold green]",
        )
    )

    results = analyze_and_plot_fh_files(
        fh_files, output_svg=base_dir / "fh_characteristic_curves.svg", verbose=False
    )

    run_contact_pots = []
    run_contact_pot_errors = []
    for _path, res in results.items():
        peaks = res["peaks"]
        if len(peaks) < 2:
            continue
        v_first, _, v_err_first = peaks[0]
        v_last, _, v_err_last = peaks[-1]
        n_spacings = len(peaks) - 1
        exc_energy = (v_last - v_first) / n_spacings
        contact_pot = v_first - exc_energy
        c_first, c_last = len(peaks) / n_spacings, 1.0 / n_spacings
        contact_pot_err = np.sqrt(
            (c_first * v_err_first) ** 2 + (c_last * v_err_last) ** 2
        )
        run_contact_pots.append(contact_pot)
        run_contact_pot_errors.append(contact_pot_err)

    weights_cp = 1.0 / (np.array(run_contact_pot_errors) ** 2)
    c_pot = np.sum(np.array(run_contact_pots) * weights_cp) / np.sum(weights_cp)
    c_pot_err = 1.0 / np.sqrt(np.sum(weights_cp))

    ion_results = analyze_ionization_experiment(
        base_dir / "data/step2_280ma.csv",
        contact_potential_V=c_pot,
        contact_pot_error_V=c_pot_err,
        output_svg=base_dir / "fh_ionization_curve.svg",
    )

    noise_table = Table(
        title="\n[bold cyan]Baseline Noise Analysis[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )
    noise_table.add_column("Metric", style="dim")
    noise_table.add_column("Value [pA]", justify="right", style="green")
    noise_table.add_row(
        "Mean baseline noise",
        f"{ion_results['mean_noise']:.3f} ± {ion_results['mean_noise_err']:.3f}",
    )
    noise_table.add_row("Std. dev. baseline noise", f"{ion_results['std_noise']:.3f}")
    console.print(noise_table)

    e_ion = ion_results["true_ionization_energy_eV"]
    e_ion_err = ion_results["error_eV"]
    lit_val = 10.438
    abs_dev = abs(e_ion - lit_val)
    rel_dev = (abs_dev / lit_val) * 100
    sigma_diff = abs_dev / e_ion_err

    summary_text = (
        f"[bold gold1]Experimental Ionization Metrics (Extrapolation Method):[/bold gold1]\n"
        f"  - Extrapolated Onset Vi = {ion_results['fitted_ionization_onset_V']:.3f} ± {ion_results['fitted_ionization_onset_error_V']:.3f} V\n"
        f"  - Contact potential shift Vc = {c_pot:.3f} ± {c_pot_err:.3f} V\n"
        f"  - True Ionization Energy E_ion = [bold green]{e_ion:.3f} ± {e_ion_err:.3f} eV[/bold green]\n\n"
        f"[bold cyan]Comparison with Literature (10.438 eV):[/bold cyan]\n"
        f"  - Absolute Deviation: {abs_dev:.3f} eV\n"
        f"  - Relative Deviation: {rel_dev:.2f}%\n"
        f"  - Statistical Significance: {sigma_diff:.2f} sigma"
    )
    console.print(
        Panel.fit(
            summary_text,
            title="[bold white]Part 2 Results Summary[/bold white]",
            border_style="gold1",
        )
    )


if __name__ == "__main__":
    main()
