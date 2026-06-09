from collections import namedtuple
from collections.abc import Callable, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from autograd import grad
from scipy import stats
from scipy.optimize import curve_fit

# Define a clean result container for curve fitting with full stats
FitResult = namedtuple(
    "FitResult",
    [
        "params",  # Optimal values for the parameters
        "errors",  # Standard deviation of the parameters
        "chisq",  # Raw Chi-squared sum
        "chi_red",  # Reduced Chi-squared (chisq/dof)
        "p_value",  # Scipy-calculated p-value for the fit quality
        "dof",  # Degrees of Freedom
        "model",  # The original model function
    ],
)


def physics_fit(
    model: Callable, x: Iterable, y: Iterable, y_err: Iterable, p0=None
) -> FitResult:
    """
    Advanced wrapper for scipy.optimize.curve_fit.
    Returns a FitResult namedtuple with params, errors, and Scipy Chi-squared statistics.
    """
    x, y, y_err = np.array(x), np.array(y), np.array(y_err)

    # Run the fit using Scipy
    popt, pcov = curve_fit(model, x, y, sigma=y_err, p0=p0, absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))

    # Calculate Chi-Squared Statistics
    residuals = y - model(x, *popt)
    chisq = np.sum((residuals / y_err) ** 2)
    dof = len(x) - len(popt)

    # Use scipy.stats.chi2 for the p-value
    # It represents the probability that a Chi-squared value at least as large as the observed
    # one would occur by chance, assuming the model is correct.
    p_val = stats.chi2.sf(chisq, dof) if dof > 0 else np.nan
    chisq_red = chisq / dof if dof > 0 else np.nan

    return FitResult(
        params=popt,
        errors=perr,
        chisq=chisq,
        chi_red=chisq_red,
        p_value=p_val,
        dof=dof,
        model=model,
    )


# Premium Color Palette
custom_colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B", "#4C9F70"]
mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=custom_colors)

# Global Aesthetics
mpl.rcParams["mathtext.fontset"] = "cm"
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["axes.formatter.use_mathtext"] = True
mpl.rcParams["axes.linewidth"] = 1.5
mpl.rcParams["axes.edgecolor"] = "#333333"
mpl.rcParams["axes.labelcolor"] = "#111111"
mpl.rcParams["axes.labelsize"] = 13
mpl.rcParams["axes.titlesize"] = 16
mpl.rcParams["axes.titleweight"] = "bold"
mpl.rcParams["xtick.color"] = "#333333"
mpl.rcParams["ytick.color"] = "#333333"
mpl.rcParams["xtick.labelsize"] = 12
mpl.rcParams["ytick.labelsize"] = 12
mpl.rcParams["xtick.major.size"] = 6
mpl.rcParams["ytick.major.size"] = 6
mpl.rcParams["xtick.minor.size"] = 3
mpl.rcParams["ytick.minor.size"] = 3
mpl.rcParams["xtick.major.width"] = 1.2
mpl.rcParams["ytick.major.width"] = 1.2

# Shadows and clean backgrounds
mpl.rcParams["figure.facecolor"] = "#ffffff"
mpl.rcParams["axes.facecolor"] = "#ffffff"


def set_style(ax=None, title=None, xlabel=None, ylabel=None, grid=True):
    """Applies a stunning, publication-ready style to plots."""

    target = ax if ax else plt.gca()

    if grid:
        target.grid(
            True,
            which="major",
            color="#a0a0a0",
            alpha=0.8,
            linestyle="-",
            linewidth=1.0,
        )
        target.grid(
            True,
            which="minor",
            color="#cccccc",
            alpha=0.5,
            linestyle="--",
            linewidth=0.7,
        )
        from matplotlib.ticker import AutoMinorLocator

        target.xaxis.set_minor_locator(AutoMinorLocator())
        target.yaxis.set_minor_locator(AutoMinorLocator())

    if title:
        target.set_title(title, pad=15, fontsize=16)
    if xlabel:
        target.set_xlabel(xlabel, labelpad=10, fontsize=14.5)
    if ylabel:
        target.set_ylabel(ylabel, labelpad=10, fontsize=14.5)

    # Apply tick label size explicitly
    target.tick_params(axis="both", which="major", labelsize=12)

    # Clean Spines
    target.spines["top"].set_visible(True)
    target.spines["right"].set_visible(True)
    target.spines["top"].set_linewidth(1.5)
    target.spines["right"].set_linewidth(1.5)
    target.spines["left"].set_linewidth(1.5)
    target.spines["bottom"].set_linewidth(1.5)

    plt.gcf().set_dpi(300)


def propagate_error(func: Callable, values: Iterable, errors: Iterable) -> float:
    """Uses autograd to propagate uncertainties automatically."""
    values = np.array(values, dtype=float)
    errors = np.array(errors, dtype=float)

    gradients = []
    for i in range(len(values)):
        grad_func = grad(lambda *args: func(*args), i)
        gradients.append(grad_func(*values))

    gradients = np.array(gradients)
    return np.sqrt(np.sum((gradients**2) * (errors**2)))


def summary_table(results_dict):
    """
    Creates a pandas DataFrame summarizing multiple FitResults.
    results_dict: {"Source Name": FitResult}
    """
    summary = []
    for name, res in results_dict.items():
        row = {
            "Source": name,
            "Chi2_red": round(res.chi_red, 3),
            "p-value": round(res.p_value, 4),
            "DOF": res.dof,
        }
        # Add parameters and their errors
        for i, (p, e) in enumerate(zip(res.params, res.errors, strict=False)):
            row[f"p{i}"] = round(p, 4)
            row[f"p{i}_err"] = round(e, 4)
        summary.append(row)
    return pd.DataFrame(summary)
