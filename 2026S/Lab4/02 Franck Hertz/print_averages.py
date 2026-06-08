import sys
from pathlib import Path

import numpy as np

# Add the project root to the path so we can import physlab
sys.path.append(str(Path(__file__).resolve().parents[2]))

from analysis_tools import analyze_and_plot_fh_files
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def main():
    console = Console()

    fh_files = [
        Path("data/step10_270ma.csv"),
        Path("data/step10_250ma.csv"),
        Path("data/step10_260ma.csv"),
    ]

    # Run analysis to get the fitted peak positions and uncertainties
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

        # Calculate spacings and errors
        spacings = []
        spacing_errors = []
        for i in range(len(peaks) - 1):
            v1, _, _, v1_err_tot, _, _ = peaks[i]
            v2, _, _, v2_err_tot, _, _ = peaks[i + 1]
            diff = v2 - v1
            diff_err = np.sqrt(v1_err_tot**2 + v2_err_tot**2)
            spacings.append(diff)
            spacing_errors.append(diff_err)

        # Calculate weighted average for this run
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

    # Calculate the overall weighted average of the averages
    weights_global = 1.0 / (np.array(run_errors) ** 2)
    global_weighted_avg = np.sum(np.array(run_averages) * weights_global) / np.sum(
        weights_global
    )
    global_weighted_avg_err = 1.0 / np.sqrt(np.sum(weights_global))

    # Literature value comparison
    lit_value = 4.90
    abs_dev = abs(global_weighted_avg - lit_value)
    rel_dev = (abs_dev / lit_value) * 100
    sigma_diff = abs_dev / global_weighted_avg_err

    summary_text = (
        f"[bold gold1]Overall Weighted Average of Averages:[/bold gold1]\n"
        f"  [bold]E_exc[/bold] = [bold green]{global_weighted_avg:.3f} +/- {global_weighted_avg_err:.3f} eV[/bold green]\n\n"
        f"[bold cyan]Comparison with Literature (4.90 eV):[/bold cyan]\n"
        f"  - Absolute Deviation: {abs_dev:.3f} eV\n"
        f"  - Relative Deviation: {rel_dev:.2f}%\n"
        f"  - Statistical Significance: {sigma_diff:.2f} sigma"
    )

    console.print(
        Panel(
            summary_text,
            title="[bold white]Final Results Summary[/bold white]",
            border_style="gold1",
        )
    )


if __name__ == "__main__":
    main()
