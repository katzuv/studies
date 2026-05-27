from collections import namedtuple
from collections.abc import Callable, Iterable

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


def set_style(ax=None, title=None, xlabel=None, ylabel=None, grid=True):
    """Applies a consistent 'Physical Review' style to plots."""
    target = ax if ax else plt.gca()

    if grid:
        target.grid(True, which="major", alpha=0.6, linestyle="-")
        target.grid(True, which="minor", alpha=0.3, linestyle="--")
        # Ensure minor ticks are enabled
        from matplotlib.ticker import AutoMinorLocator
        target.xaxis.set_minor_locator(AutoMinorLocator())
        target.yaxis.set_minor_locator(AutoMinorLocator())

    if title:
        target.set_title(title, weight="bold", pad=15)
    if xlabel:
        target.set_xlabel(xlabel)
    if ylabel:
        target.set_ylabel(ylabel)

    target.spines["top"].set_visible(False)
    target.spines["right"].set_visible(False)

    # Set high DPI for saving
    plt.gcf().set_dpi(150)


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
