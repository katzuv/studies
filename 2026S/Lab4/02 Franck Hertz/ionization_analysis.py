import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add the project root to the path so we can import physlab
sys.path.append(str(Path(__file__).resolve().parents[2]))

from excitation_analysis import analyze_and_plot_fh_files, get_last_digit_error
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from physlab.core import physics_fit, set_style


def quadratic_threshold(V, b, V_i, I_offset):
    return np.where(V_i < V, b * (V - V_i) ** 2 + I_offset, I_offset)


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

    v_error_inst = get_last_digit_error(df_str.iloc[:, 0])
    i_error_inst = get_last_digit_error(df_str.iloc[:, 1])

    # Baseline noise analysis
    baseline_mask = (raw_voltage >= 2.0) & (raw_voltage <= 8.0)
    baseline_currents = raw_current[baseline_mask]

    if len(baseline_currents) == 0:
        baseline_currents = raw_current[: int(len(raw_current) * 0.3)]

    mean_noise = np.mean(baseline_currents)
    std_noise = np.std(baseline_currents, ddof=1)
    mean_noise_err = std_noise / np.sqrt(len(baseline_currents))
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

    # Perform quadratic threshold fit (5.0 to 11.5 V)
    mask = (raw_voltage >= 5.0) & (raw_voltage <= 11.5)
    x_fit = raw_voltage[mask]
    y_fit = raw_current[mask]
    y_err = np.full_like(y_fit, i_error_inst)

    try:
        res = physics_fit(
            quadratic_threshold,
            x_fit,
            y_fit,
            y_err,
            p0=[10.0, v_start_raw, mean_noise],
        )
        b_fit, vi_fit, ioff_fit = res.params
        b_err, vi_err, ioff_err = res.errors
        chi_red_ion = res.chi_red
        dof_ion = res.dof
        v_onset = vi_fit
        v_onset_err = np.sqrt(vi_err**2 + v_error_inst**2)
    except Exception as e:
        print(f"Error in quadratic threshold fit: {e}")
        v_onset = v_start_raw
        v_onset_err = v_error_inst
        chi_red_ion = np.nan
        dof_ion = 0
        b_fit, vi_fit, ioff_fit = np.nan, np.nan, np.nan
        b_err, vi_err, ioff_err = np.nan, np.nan, np.nan

    true_ionization_energy = v_onset - contact_potential_V
    total_error = np.sqrt(v_onset_err**2 + contact_pot_error_V**2)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(
        raw_voltage,
        raw_current,
        xerr=v_error_inst,
        yerr=i_error_inst,
        fmt="-",
        color="#2E86AB",
        label="Ion Current Data (I)",
        linewidth=2.5,
        elinewidth=1.0,
        alpha=0.9,
        capsize=2,
        zorder=2,
    )

    ax.fill_between(
        raw_voltage,
        mean_noise - 5.0 * std_noise,
        statistical_noise_ceiling,
        color="#F18F01",
        alpha=0.15,
        zorder=1,
    )

    ax.axhline(
        y=statistical_noise_ceiling,
        color="#F18F01",
        linestyle="--",
        linewidth=2.0,
        label="5sigma Noise Floor Ceiling",
    )

    if not np.isnan(vi_fit):
        v_plot = np.linspace(5.0, 11.5, 200)
        i_plot = quadratic_threshold(v_plot, b_fit, vi_fit, ioff_fit)
        ax.plot(
            v_plot,
            i_plot,
            color="#A23B72",
            linestyle="--",
            linewidth=2.0,
            label="Quadratic Threshold Fit",
            zorder=3,
        )

    ax.axvline(
        x=v_onset,
        color="#C73E1D",
        linestyle="-.",
        linewidth=2.5,
        label=f"Ionization Onset (Va0 = {v_onset:.3f} V)",
    )

    idx_closest = np.abs(raw_voltage - v_onset).argmin()
    ax.scatter(
        raw_voltage[idx_closest],
        raw_current[idx_closest],
        color="#C73E1D",
        s=150,
        edgecolors="white",
        linewidths=2.5,
        zorder=5,
    )

    set_style(
        ax=ax,
        xlabel="Accelerating Voltage Va [V]",
        ylabel="Collector Current I [pA]",
    )
    ax.set_xlim(0, max(raw_voltage) + 1)

    # Note: Keep label details minimal inside graph, text in report is preferred
    results_box_text = (
        f"Experimental Metrics:\n"
        f"Fitted Onset Va0: {v_onset:.3f} ± {v_onset_err:.3f} V\n"
        f"Contact Shift Vc: {contact_potential_V:.3f} ± {contact_pot_error_V:.3f} V\n"
        f"True E_ion: {true_ionization_energy:.3f} ± {total_error:.3f} eV\n"
        f"Literature: 10.438 eV"
    )

    ax.text(
        0.08,
        0.58,
        results_box_text,
        transform=ax.transAxes,
        fontsize=13,
        verticalalignment="top",
        linespacing=1.8,
        bbox=dict(
            boxstyle="round,pad=1.3",
            facecolor="#ffffff",
            edgecolor="#C73E1D",
            linewidth=1.5,
            alpha=0.95,
        ),
    )

    ax.legend(
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

    return {
        "fitted_ionization_onset_V": v_onset,
        "fitted_ionization_onset_error_V": v_onset_err,
        "true_ionization_energy_eV": true_ionization_energy,
        "error_eV": total_error,
        "chi_red": chi_red_ion,
        "dof": dof_ion,
        "b_fit": b_fit,
        "b_err": b_err,
        "ioff_fit": ioff_fit,
        "ioff_err": ioff_err,
        "mean_noise": mean_noise,
        "mean_noise_err": mean_noise_err,
        "std_noise": std_noise,
    }


def main():
    console = Console()
    base_dir = Path(__file__).resolve().parent

    # Get contact potential from Part 1 files to keep consistency
    fh_files = [
        base_dir / "data/step10_270ma.csv",
        base_dir / "data/step10_250ma.csv",
        base_dir / "data/step10_260ma.csv",
    ]

    console.print(
        Panel.fit(
            "[bold yellow]*** FRANCK-HERTZ EXPERIMENT - PART 2: IONIZATION POTENTIAL ANALYSIS ***[/bold yellow]\n"
            "[dim]Physical quadratic threshold model fitting to detect ionization onset[/dim]",
            border_style="bold gold1",
            padding=(1, 4),
            title="[bold green]Technion Physics Lab 4[/bold green]",
        )
    )

    # Compute contact potential dynamically
    results = analyze_and_plot_fh_files(
        fh_files, output_svg=base_dir / "fh_characteristic_curves.svg", verbose=False
    )

    # We compute the overall weighted average of contact potentials across the three runs
    run_contact_pots = []
    run_contact_pot_errors = []
    for _path, res in results.items():
        peaks = res["peaks"]
        spacings = []
        spacing_errors = []
        for i in range(len(peaks) - 1):
            v1, _, v1_err_tot = peaks[i]
            v2, _, v2_err_tot = peaks[i + 1]
            diff = v2 - v1
            diff_err = np.sqrt(v1_err_tot**2 + v2_err_tot**2)
            spacings.append(diff)
            spacing_errors.append(diff_err)

        weights = 1.0 / (np.array(spacing_errors) ** 2)
        weighted_avg = np.sum(np.array(spacings) * weights) / np.sum(weights)

        v1_val, _, v1_err_tot = peaks[0]
        contact_pot = v1_val - weighted_avg

        c1 = 1.0 + weights[0] / np.sum(weights)
        c2 = -(weights[0] - weights[1]) / np.sum(weights)
        c3 = -(weights[1] - weights[2]) / np.sum(weights)
        c4 = -(weights[2] - weights[3]) / np.sum(weights)
        c5 = -weights[3] / np.sum(weights)

        c_coeffs = np.array([c1, c2, c3, c4, c5])
        peak_errs = np.array([p[2] for p in peaks])
        contact_pot_err = np.sqrt(np.sum((c_coeffs * peak_errs) ** 2))

        run_contact_pots.append(contact_pot)
        run_contact_pot_errors.append(contact_pot_err)

    weights_cp = 1.0 / (np.array(run_contact_pot_errors) ** 2)
    c_pot = np.sum(np.array(run_contact_pots) * weights_cp) / np.sum(weights_cp)
    c_pot_err = 1.0 / np.sqrt(np.sum(weights_cp))

    # Analyze ionization experiment
    ion_results = analyze_ionization_experiment(
        base_dir / "data/step2_280ma.csv",
        contact_potential_V=c_pot,
        contact_pot_error_V=c_pot_err,
        output_svg=base_dir / "fh_ionization_curve.svg",
    )

    # Display baseline parameters
    noise_table = Table(
        title="\n[bold cyan]1. Baseline Noise Analysis[/bold cyan]",
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
    noise_table.add_row(
        "5-sigma noise ceiling",
        f"{(ion_results['mean_noise'] + 5 * ion_results['std_noise']):.3f}",
    )
    console.print(noise_table)

    # Display fit parameters
    fit_table = Table(
        title="[bold cyan]2. Quadratic Threshold Fit Summary[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )
    fit_table.add_column("Parameter", style="dim")
    fit_table.add_column("Fitted Value", justify="right", style="cyan")
    fit_table.add_row(
        "Scale factor b",
        f"{ion_results['b_fit']:.3f} ± {ion_results['b_err']:.3f} pA/V^2",
    )
    fit_table.add_row(
        "Baseline offset I_offset",
        f"{ion_results['ioff_fit']:.3f} ± {ion_results['ioff_err']:.3f} pA",
    )
    fit_table.add_row(
        "Fitted Onset Vi",
        f"{ion_results['fitted_ionization_onset_V']:.3f} ± {ion_results['fitted_ionization_onset_error_V']:.3f} V",
    )
    fit_table.add_row(
        "Reduced Chi-squared (DoF)",
        f"{ion_results['chi_red']:.2f} (DoF = {ion_results['dof']})",
    )
    console.print(fit_table)

    # Final Comparison
    e_ion = ion_results["true_ionization_energy_eV"]
    e_ion_err = ion_results["error_eV"]
    lit_val = 10.438
    abs_dev = abs(e_ion - lit_val)
    rel_dev = (abs_dev / lit_val) * 100
    sigma_diff = abs_dev / e_ion_err

    summary_text = (
        f"[bold gold1]Experimental Ionization Metrics:[/bold gold1]\n"
        f"  - Fitted Onset Voltage Vi = {ion_results['fitted_ionization_onset_V']:.3f} ± {ion_results['fitted_ionization_onset_error_V']:.3f} V\n"
        f"  - Contact potential shift Vc = {c_pot:.3f} ± {c_pot_err:.3f} V\n"
        f"  - True Ionization Energy E_ion = [bold green]{e_ion:.3f} ± {e_ion_err:.3f} eV[/bold green]\n\n"
        f"[bold cyan]Comparison with Literature (10.438 eV):[/bold cyan]\n"
        f"  - Absolute Deviation: {abs_dev:.3f} eV\n"
        f"  - Relative Deviation: {rel_dev:.2f}%\n"
        f"  - Statistical Significance: {sigma_diff:.2f} sigma"
    )
    console.print(
        Panel(
            summary_text,
            title="[bold white]Part 2 Results Summary[/bold white]",
            border_style="gold1",
        )
    )


if __name__ == "__main__":
    main()
