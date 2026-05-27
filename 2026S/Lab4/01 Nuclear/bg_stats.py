from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from analysis_tools import load_gm
from scipy.stats import norm, poisson

import physlab


def main():
    # 1. Load Data
    data_path = Path("data/bg.tsv")
    df = load_gm(data_path)
    counts = df["Counts"]

    # 2. Calculate Statistics
    m = len(counts)
    k1 = np.mean(counts)
    k2 = np.var(counts, ddof=1)
    k3 = np.sum((counts - k1) ** 3) / (m - 1)

    print(f"Results for {m} runs:")
    print(f"k1 (Mean):     {k1:.3f}")
    print(f"k2 (Variance): {k2:.3f}")
    print(f"k3 (Skewness): {k3:.3f}")
    print(f"Ratio k2/k1:   {k2 / k1:.3f}")

    # 3. Create Histogram Data
    bins = np.arange(counts.min(), counts.max() + 2) - 0.5
    hist, bin_edges = np.histogram(counts, bins=bins, density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # 4. Theoretical Distributions
    x_theory = np.arange(0, counts.max() + 2)
    y_poisson = poisson.pmf(x_theory, k1)
    y_gaussian = norm.pdf(x_theory, k1, np.sqrt(k2))

    # 5. Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot experimental histogram
    ax.bar(
        bin_centers,
        hist,
        width=0.8,
        alpha=0.4,
        color="gray",
        label="Experimental Data",
        edgecolor="black",
    )

    # Plot theoretical curves
    ax.plot(
        x_theory,
        y_poisson,
        "o--",
        color="blue",
        label=f"Poisson (λ={k1:.2f})",
        markersize=4,
    )
    ax.plot(
        x_theory,
        y_gaussian,
        "-",
        color="red",
        label=f"Gaussian (μ={k1:.2f}, σ²={k2:.2f})",
        linewidth=2,
    )

    # Styling using physlab utility
    physlab.set_style(
        ax,
        title="Background Radiation Statistics (Poisson vs Gaussian)",
        xlabel="Counts per Second (cps)",
        ylabel="Probability Density",
    )

    ax.legend(frameon=True)

    # Add text box with cumulants
    stats_text = (
        f"$k_1$ (mean) = {k1:.2f}\n$k_2$ (var)  = {k2:.2f}\n$k_3$ (skew) = {k3:.2f}"
    )
    ax.text(
        0.95,
        0.75,
        stats_text,
        transform=ax.transAxes,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
    )

    plt.tight_layout()
    plt.savefig("bg_statistics.svg")
    print("Graph saved as bg_statistics.svg")


if __name__ == "__main__":
    main()
