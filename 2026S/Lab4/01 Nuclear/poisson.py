from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from analysis_tools import BG_ERR, BG_RATE, load_gm
from scipy.stats import norm, poisson

import physlab


def main():
    # 1. Load Data
    data_path = Path("data/dan_stats2.tsv")
    df = load_gm(data_path)
    # The data is counts in 1 second, so cps = counts.
    raw_counts = df["Counts"]

    # 2. Subtract Background
    # Corrected counts (cps) = raw - BG_RATE
    counts = raw_counts - BG_RATE
    m = len(counts)

    # 3. Calculate Statistics
    k1 = np.mean(counts)
    k2 = np.var(counts, ddof=1)
    k3 = np.sum((counts - k1) ** 3) / (m - 1)

    # Theoretical Errors (sigma) for Poisson process with mean lambda
    # We assume the underlying process is Poisson.
    # Note: Subtracting a constant BG doesn't change the variance or skewness of the sample,
    # but the Poisson *expectation* lambda is now the corrected mean.
    lam = k1
    err_k1 = np.sqrt((lam + BG_RATE) / m) # k1 error is based on raw count statistics
    err_k2 = (lam + BG_RATE) * np.sqrt(2 / m)
    err_k3 = (lam + BG_RATE) * np.sqrt(15 * (lam + BG_RATE) / m)

    print(f"Results for {m} runs (Background Corrected, BG={BG_RATE} cps):")
    print("Poisson Cumulants vs Theoretical Noise (sigma):")
    print(f"  K1 (Mean):     {k1:.3f} ± {err_k1:.3f}")
    print(
        f"  K2 (Variance): {k2:.3f} ± {err_k2:.3f} ({(k2 - k1) / k1 * 100:+.1f}% vs K1)"
    )
    print(
        f"  K3 (Skewness): {k3:.3f} ± {err_k3:.3f} ({(k3 - k1) / k1 * 100:+.1f}% vs K1)"
    )
    print("\nGaussian Parameters:")
    print(f"  mu:      {k1:.3f}")
    print(f"  sigma^2: {k2:.3f}")
    print(f"  sigma:   {np.sqrt(k2):.3f}")

    # 4. Create Histogram Data
    # We bin the CORRECTED counts.
    bins = np.arange(counts.min(), counts.max() + 2) - 0.5
    hist, bin_edges = np.histogram(counts, bins=bins, density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # 5. Theoretical Distributions
    # For corrected counts, the distribution is shifted by BG_RATE.
    # Poisson is discrete, so we use integers for the PMF.
    x_theory = np.arange(raw_counts.min(), raw_counts.max() + 2)
    y_poisson = poisson.pmf(x_theory, k1 + BG_RATE)
    y_gaussian = norm.pdf(x_theory - BG_RATE, k1, np.sqrt(k2))

    # 6. Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    errors = np.sqrt(hist / m)

    ax.bar(
        bin_centers,
        hist,
        width=0.8,
        alpha=0.3,
        color="gray",
        label="Corrected Experimental Data",
        edgecolor="black",
        linewidth=0.5,
    )

    ax.errorbar(
        bin_centers,
        hist,
        yerr=errors,
        fmt="k.",
        capsize=3,
        label=r"Measurement Error ($\sqrt{N}/M$)",
    )

    ax.plot(
        x_theory - BG_RATE,
        y_poisson,
        "o--",
        color="blue",
        label=f"Poisson (λ={k1+BG_RATE:.2f}, shifted)",
        markersize=4,
    )
    ax.plot(
        x_theory - BG_RATE,
        y_gaussian,
        "-",
        color="red",
        label=f"Gaussian (μ={k1:.2f}, σ²={k2:.2f})",
        linewidth=2,
    )

    # Styling using physlab utility
    physlab.set_style(
        ax,
        xlabel="Counts per Second (cps)",
        ylabel="Probability Density",
    )

    ax.legend(frameon=True, fontsize=14, loc="upper right")

    # Add text box with cumulants
    stats_text = (
        f"$K_1$ (mean) = {k1:.2f} ± {err_k1:.2f}\n"
        f"$K_2$ (var)  = {k2:.2f} ± {err_k2:.2f}\n"
        f"$K_3$ (skew) = {k3:.2f} ± {err_k3:.2f}"
    )
    ax.text(
        0.95,
        0.5,
        stats_text,
        transform=ax.transAxes,
        verticalalignment="center",
        horizontalalignment="right",
        fontsize=14,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
    )


    plt.tight_layout()
    plt.savefig("poisson_statistics.svg")
    print("Graph saved as poisson_statistics.svg")


if __name__ == "__main__":
    main()
