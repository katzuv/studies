#!/usr/bin/env python3
"""
Curie Point Experiment – Measurements and Calculations
Standalone Data Analysis Script.
"""
from collections import namedtuple
from collections.abc import Callable, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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


def format_value(
    val: float,
    err: float | None = None,
    fmt_spec: str = ".2f",
    scale: float = 1.0,
    suffix: str = "",
    style: str = "typst",
) -> str:
    """
    Format a value and optional uncertainty (error) with scaling, suffix, and formatting specs.
    Supports 'typst' and 'latex' styles.
    """
    v = val * scale
    if err is None:
        v_str = f"{v:{fmt_spec}}"
        if suffix:
            if style == "latex" and "10^(" in suffix:
                s = suffix.replace("dot 10^(", r"\times 10^{").replace(")", "}")
                v_str = f"{v_str} {s}"
            else:
                v_str = f"{v_str} {suffix}"
        return v_str

    e = err * scale
    v_str = f"{v:{fmt_spec}}"
    e_str = f"{e:{fmt_spec}}"

    if style == "typst":
        sep = " +- "
        if suffix:
            return f"({v_str}{sep}{e_str}) {suffix}"
        return f"{v_str}{sep}{e_str}"

    # style == "latex"
    sep = r" \pm "
    s = suffix
    if suffix and "10^(" in suffix:
        s = suffix.replace("dot 10^(", r"\times 10^{").replace(")", "}")
        return f"({v_str}{sep}{e_str}) {s}"
    elif suffix:
        return f"({v_str}{sep}{e_str}) {s}"
    return f"{v_str}{sep}{e_str}"


def export_constants(constants_data: list[dict], directory) -> list[dict]:
    """
    Export constants to constants.json (schema compliant) and constants.typ declarations.
    Automatically generates formatted values and error variables.
    """
    import json
    from pathlib import Path

    output_dir = Path(directory)

    # 1. Generate formatted_value for each constant
    for item in constants_data:
        fmt_spec = item.get("fmt_spec", ".2f")
        scale = item.get("scale", 1.0)
        suffix = item.get("suffix", "")
        item["formatted_value"] = format_value(
            item["value"], item["error"], fmt_spec, scale, suffix, style="typst"
        )

    # 2. Save JSON file (schema compliant)
    json_constants = []
    for item in constants_data:
        clean_item = {
            "hebrew_name": item["hebrew_name"],
            "english_name": item["english_name"],
            "hebrew_var": item["hebrew_var"],
            "english_var": item["english_var"],
            "symbol": item["symbol"],
            "value": item["value"],
            "error": item["error"],
            "units": item["units"],
            "formatted_value": item["formatted_value"],
            "scale": item.get("scale", 1.0),
            "fmt_spec": item.get("fmt_spec", ".2f"),
            "suffix": item.get("suffix", ""),
        }
        json_constants.append(clean_item)

    json_path = output_dir / "constants.json"
    json_path.write_text(
        json.dumps(json_constants, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3. Generate Typst declarations file
    typst_lines = [
        "// Automatically generated constants for Typst\n",
        "#let pm = $plus.minus$\n",
        "#let פמ = $plus.minus$\n\n",
    ]
    for item in constants_data:
        val_expr = item["formatted_value"]
        if item["units"]:
            val_expr = rf"{val_expr} \ {item['units']}"
        typst_lines.append(f"#let {item['hebrew_var']} = ${val_expr}$\n")
        typst_lines.append(f"#let {item['english_var']} = ${val_expr}$\n")

        # Format and append error variables
        err_val = item["error"]
        if err_val is None:
            err_expr = "none"
        else:
            scale = item.get("scale", 1.0)
            fmt_spec = item.get("fmt_spec", ".2f")
            suffix = item.get("suffix", "")
            e = err_val * scale
            e_str = f"{e:{fmt_spec}}"
            err_expr = rf"{e_str} {suffix}" if suffix else e_str
            if item["units"]:
                err_expr = rf"{err_expr} \ {item['units']}"
            err_expr = f"${err_expr}$"

        typst_lines.append(f"#let שגיאת_{item['hebrew_var']} = {err_expr}\n")
        typst_lines.append(f"#let {item['english_var']}_err = {err_expr}\n")

    typst_path = output_dir / "constants.typ"
    typst_path.write_text("".join(typst_lines), encoding="utf-8")

    return json_constants


import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import erf

# Assuming physlab is an available local or custom package in your lab environment


# =====================================================================
# 1. Helper Functions & Physics Models
# =====================================================================

def cooling_model(t, T_env, T0, k):
    """Newton's Law of Cooling model."""
    return T_env + (T0 - T_env) * np.exp(-k * t)


def erf_model(T, Tc, dT):
    """Error function model for modeling the ferromagnetic transition."""
    return 0.5 * (1.0 - erf((T - Tc) / (dT * np.sqrt(2.0))))


def split_data(df):
    """Splits dataframe into heating and cooling segments based on max temperature."""
    max_idx = df["Temp (C)"].idxmax()
    heating_df = df.iloc[:max_idx].copy()
    cooling_df = df.iloc[max_idx:].copy()
    return heating_df, cooling_df


def fit_cooling(cooling_df, p0):
    """Fits the cooling temperature profile to Newton's law of cooling."""
    times = pd.to_datetime(cooling_df["DateTime"], format="%d/%m/%Y %H:%M:%S")
    t_s = (times - times.min()).dt.total_seconds().values
    T_s = cooling_df["Temp (C)"].values
    T_err = np.ones_like(T_s) * 0.1
    fit_temp = physics_fit(cooling_model, t_s, T_s, T_err, p0=p0)
    return t_s, T_s, fit_temp


def fit_curie(heating_df, cooling_df, h_range, c_range, p0_h, p0_c):
    """Fits the Curie transition temperature for both heating and cooling legs."""
    h_transition = heating_df[
        (heating_df["Temp (C)"] >= h_range[0]) & (heating_df["Temp (C)"] <= h_range[1])
    ]
    c_transition = cooling_df[
        (cooling_df["Temp (C)"] >= c_range[0]) & (cooling_df["Temp (C)"] <= c_range[1])
    ]

    V_raw_h = h_transition["RMS CH2 (V)"].values
    V_min_h, V_max_h = V_raw_h.min(), V_raw_h.max()
    V_norm_h = (V_raw_h - V_min_h) / (V_max_h - V_min_h)
    V_err_h = np.ones_like(V_raw_h) * (0.01 / (V_max_h - V_min_h))

    V_raw_c = c_transition["RMS CH2 (V)"].values
    V_min_c, V_max_c = V_raw_c.min(), V_raw_c.max()
    V_norm_c = (V_raw_c - V_min_c) / (V_max_c - V_min_c)
    V_err_c = np.ones_like(V_raw_c) * (0.01 / (V_max_c - V_min_c))

    fit_h = physics_fit(
        erf_model,
        h_transition["Temp (C)"].values,
        V_norm_h,
        V_err_h,
        p0=p0_h,
    )
    fit_c = physics_fit(
        erf_model,
        c_transition["Temp (C)"].values,
        V_norm_c,
        V_err_c,
        p0=p0_c,
    )
    return fit_h, fit_c


def generate_and_save_plots(
    material_name,
    heating_df,
    cooling_df,
    fit_h,
    fit_c,
    fit_temp,
    t_s,
    T_s,
    h_range,
    c_range,
    xmin,
    ymin,
    parent_dir,
):
    """Generates and saves diagnostic analysis plots for the magnetic cores."""
    # Plot 1: Hysteresis Loop and erf Transition fits
    fig1 = plt.figure(figsize=(6, 4.5))
    plt.scatter(heating_df["Temp (C)"], heating_df["RMS CH2 (V)"], s=1.5, alpha=0.4, label="Heating data", color="#2E86AB")
    plt.scatter(cooling_df["Temp (C)"], cooling_df["RMS CH2 (V)"], s=1.5, alpha=0.4, label="Cooling data", color="#A23B72")

    h_trans = heating_df[(heating_df["Temp (C)"] >= h_range[0]) & (heating_df["Temp (C)"] <= h_range[1])]
    c_trans = cooling_df[(cooling_df["Temp (C)"] >= c_range[0]) & (cooling_df["Temp (C)"] <= c_range[1])]
    V_min_h, V_max_h = h_trans["RMS CH2 (V)"].min(), h_trans["RMS CH2 (V)"].max()
    V_min_c, V_max_c = c_trans["RMS CH2 (V)"].min(), c_trans["RMS CH2 (V)"].max()

    T_fit_h = np.linspace(h_range[0], h_range[1], 300)
    plt.plot(T_fit_h, V_min_h + (V_max_h - V_min_h) * erf_model(T_fit_h, *fit_h.params), color="#0D47A1", linewidth=2.0, label="Heating Fit")
    
    T_fit_c = np.linspace(c_range[0], c_range[1], 300)
    plt.plot(T_fit_c, V_min_c + (V_max_c - V_min_c) * erf_model(T_fit_c, *fit_c.params), color="#4A148C", linewidth=2.0, label="Cooling Fit")

    plt.axvline(fit_h.params[0], color="#0D47A1", linestyle="--", alpha=0.8)
    plt.axvline(fit_c.params[0], color="#4A148C", linestyle="--", alpha=0.8)

    set_style(xlabel="Temperature ($^\\circ\\mathrm{C}$)", ylabel="Voltage ($V_s$ [V])")
    plt.xlim(left=xmin)
    plt.ylim(bottom=ymin)
    plt.legend(frameon=True)
    plt.tight_layout()
    fig1.savefig(parent_dir / f"{material_name}_curie_fit.svg", format="svg", bbox_inches="tight")
    plt.close(fig1)

    # Plot 2: Newton Cooling Curve Fit
    fig2 = plt.figure(figsize=(6, 4.5))
    plt.scatter(t_s, T_s, s=1.5, alpha=0.5, label="Cooling data", color="#2E86AB")
    t_fit = np.linspace(0, t_s.max(), 300)
    plt.plot(t_fit, cooling_model(t_fit, *fit_temp.params), color="#C73E1D", linewidth=2.0, label="Newton Fit")
    
    set_style(xlabel="Time $t \\ [\\mathrm{sec}]$", ylabel="Temperature ($^\\circ\\mathrm{C}$)")
    plt.yscale("log")
    plt.legend(frameon=True)
    plt.tight_layout()
    fig2.savefig(parent_dir / f"{material_name}_cooling_fit.svg", format="svg", bbox_inches="tight")
    plt.close(fig2)


def export_material_results(material_name, hebrew_material, fit_h, fit_c, fit_temp, k_theory, parent_dir):
    """Saves analytical fitting output params to structured JSON and Typst markup."""
    results = [
        {
            "hebrew_name": f"טמפרטורת קירי בחימום ({hebrew_material})",
            "english_name": f"Curie Temperature (Heating) - {material_name.capitalize()}",
            "hebrew_var": f"טמפרטורת_קירי_חימום_{material_name}",
            "english_var": f"curie_temp_heating_{material_name}",
            "symbol": 'T_(c, "heat")',
            "value": fit_h.params[0],
            "error": fit_h.params[1],
            "units": '"°C"',
            "scale": 1.0,
            "fmt_spec": ".2f",
            "suffix": "",
        },
        {
            "hebrew_name": f"טמפרטורת קירי בקירור ({hebrew_material})",
            "english_name": f"Curie Temperature (Cooling) - {material_name.capitalize()}",
            "hebrew_var": f"טמפרטורת_קירי_קירור_{material_name}",
            "english_var": f"curie_temp_cooling_{material_name}",
            "symbol": 'T_(c, "cool")',
            "value": fit_c.params[0],
            "error": fit_c.params[1],
            "units": '"°C"',
            "scale": 1.0,
            "fmt_spec": ".2f",
            "suffix": "",
        },
        {
            "hebrew_name": f"קבוע קירור ניסיוני ({hebrew_material})",
            "english_name": f"Experimental Cooling Constant - {material_name.capitalize()}",
            "hebrew_var": f"קבוע_קירור_ניסיוני_{material_name}",
            "english_var": f"cooling_constant_exp_{material_name}",
            "symbol": 'k_"exp"',
            "value": fit_temp.params[2],
            "error": fit_temp.errors[2],
            "units": '"sec"^(-1)',
            "scale": 1.0,
            "fmt_spec": ".6f",
            "suffix": "",
        },
        {
            "hebrew_name": f"קבוע קירור תיאורטי ({hebrew_material})",
            "english_name": f"Theoretical Cooling Constant - {material_name.capitalize()}",
            "hebrew_var": f"קבוע_קירור_תיאורטי_{material_name}",
            "english_var": f"cooling_constant_theory_{material_name}",
            "symbol": 'k_"theory"',
            "value": k_theory,
            "error": None,
            "units": '"sec"^(-1)',
            "scale": 1.0,
            "fmt_spec": ".4f",
            "suffix": "",
        },
    ]

    for item in results:
        fmt_spec = item.get("fmt_spec", ".2f")
        scale = item.get("scale", 1.0)
        suffix = item.get("suffix", "")
        item["formatted_value"] = format_value(
            item["value"], item["error"], fmt_spec, scale, suffix, style="typst"
        )

    # Save summary JSON
    json_path = parent_dir / f"{material_name}_results.json"
    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate Typst report file
    typst_lines = [f"// Automatically generated {material_name} fit results for Typst\n\n"]
    for item in results:
        val_expr = item["formatted_value"]
        if item["units"]:
            val_expr = rf"{val_expr} \ {item['units']}"
        typst_lines.append(f"#let {item['hebrew_var']} = ${val_expr}$\n")
        typst_lines.append(f"#let {item['english_var']} = ${val_expr}$\n")

        err_val = item["error"]
        if err_val is None:
            err_expr = "none"
        else:
            scale = item.get("scale", 1.0)
            fmt_spec = item.get("fmt_spec", ".2f")
            suffix = item.get("suffix", "")
            e = err_val * scale
            e_str = f"{e:{fmt_spec}}"
            err_expr = rf"{e_str} {suffix}" if suffix else e_str
            if item["units"]:
                err_expr = rf"{err_expr} \ {item['units']}"
            err_expr = f"${err_expr}$"

        typst_lines.append(f"#let שגיאת_{item['hebrew_var']} = {err_expr}\n")
        typst_lines.append(f"#let {item['english_var']}_err = {err_expr}\n")

    typst_path = parent_dir / f"{material_name}_results.typ"
    typst_path.write_text("".join(typst_lines), encoding="utf-8")


# =====================================================================
# 2. Main Execution Pipeline
# =====================================================================

def main():
    parent_dir = Path(__file__).parent if "__file__" in locals() else Path(".")
    
    print("=" * 60)
    print("  Curie Point Experiment - Analytical Data Framework  ")
    print("=" * 60)

    # -----------------------------------------------------------------
    # Part 1 & 2: System Constants Initialization
    # -----------------------------------------------------------------
    constants_path = parent_dir / "constants.json"
    if constants_path.exists():
        print(f"\n[+] Loading system parameters from: {constants_path.name}")
        constants_data = json.loads(constants_path.read_text(encoding="utf-8"))
        
        # Displaying a clean table representation in standard output
        records = []
        for c in constants_data:
            records.append({
                "Constant Parameter": c["english_name"],
                "Symbol": c["symbol"],
                "Value": c["value"],
                "Uncertainty": c["error"],
                "Units": c["units"]
            })
        print(pd.DataFrame(records).to_string(index=False))
    else:
        print(f"\n[-] warning: {constants_path.name} not found. Skipping parameter summary table.")

    # -----------------------------------------------------------------
    # Part A: Frequency Response Data Evaluation
    # -----------------------------------------------------------------
    freq_path = parent_dir / "freq_sweep.csv"
    if freq_path.exists():
        print(f"\n[+] Parsing frequency sweep dataset: {freq_path.name}")
        df_freq = pd.read_csv(freq_path)
        
        vs0_data = df_freq[df_freq["Core Type"] == "VS0 (Air core)"].reset_index(drop=True)
        vs1_data = df_freq[df_freq["Core Type"] == "VS1 (N1)"].reset_index(drop=True)
        vs2_data = df_freq[df_freq["Core Type"] == "VS2 (N2)"].reset_index(drop=True)

        freqs = vs0_data["Frequency (Hz)"]
        vs0_vp = vs0_data["CH2 (V)"] / vs0_data["CH1 (V)"]
        vs1_vp = vs1_data["CH2 (V)"] / vs1_data["CH1 (V)"]
        vs2_vp = vs2_data["CH2 (V)"] / vs2_data["CH1 (V)"]

        ticks = [100, 200, 300, 500, 1000, 2000, 3000, 4000]

        # Figure 1: Vs/Vp Ratio
        fig1, ax1 = plt.subplots(figsize=(6, 4.5))
        ax1.semilogx(freqs, vs0_vp, label="Air core ($V_{s0}/V_p$)")
        ax1.semilogx(freqs, vs1_vp, label="Ferrite core ($V_{s1}/V_p$)")
        ax1.semilogx(freqs, vs2_vp, label="Invar core ($V_{s2}/V_p$)")
        set_style(ax1, xlabel="$f \\ [\\mathrm{Hz}]$", ylabel="$V_s / V_p$")
        ax1.set_xticks(ticks)
        ax1.set_xticklabels([str(t) for t in ticks])
        ax1.legend(frameon=True)
        plt.tight_layout()
        fig1.savefig(parent_dir / "frequency_response_vs_vp.svg", format="svg", bbox_inches="tight")
        
        # Figure 2: Relative Permeability Ratio (Vs / V_air)
        vs1_v0 = vs1_data["CH2 (V)"] / vs0_data["CH2 (V)"]
        vs2_v0 = vs2_data["CH2 (V)"] / vs0_data["CH2 (V)"]

        fig2, ax2 = plt.subplots(figsize=(6, 4.5))
        ax2.semilogx(freqs, vs1_v0, label="Ferrite core ($V_{s1}/V_{s0}$)")
        ax2.semilogx(freqs, vs2_v0, label="Invar core ($V_{s2}/V_{s0}$)")
        set_style(ax2, xlabel="$f \\ [\\mathrm{Hz}]$", ylabel="$V_s / V_{\\mathrm{air}}$")
        ax2.set_xticks(ticks)
        ax2.set_xticklabels([str(t) for t in ticks])
        ax2.legend(frameon=True)
        plt.tight_layout()
        fig2.savefig(parent_dir / "frequency_response_ratio.svg", format="svg", bbox_inches="tight")
        print("[+] Frequency response vector plots saved successfully (.svg format).")
    else:
        print(f"\n[-] warning: {freq_path.name} data file omitted. Skipping Part A calculations.")

    # -----------------------------------------------------------------
    # Part B: Ferrite Phase Transition Pipeline
    # -----------------------------------------------------------------
    ferrite_path = parent_dir / "curie_data_ferrit.csv"
    if ferrite_path.exists():
        print("\n[+] Executing non-linear fitting pipeline for: Ferrite Core")
        df_ferrite = pd.read_csv(ferrite_path, comment="#")
        
        h_df, c_df = split_data(df_ferrite)
        t_s, T_s, fit_ferrite_temp = fit_cooling(c_df, p0=[24.0, 174.0, 0.001])
        fit_ferrite_h, fit_ferrite_c = fit_curie(h_df, c_df, (120, 150), (125, 165), [133.0, 0.5], [138.0, 0.5])

        generate_and_save_plots("ferrite", h_df, c_df, fit_ferrite_h, fit_ferrite_c, fit_ferrite_temp, t_s, T_s, (120, 150), (125, 165), 100, 1.9, parent_dir)
        export_material_results("ferrite", "פריט", fit_ferrite_h, fit_ferrite_c, fit_ferrite_temp, k_theory=0.0829, parent_dir=parent_dir)

        print("\n>>> Ferrite Fit Outputs Summary:")
        print(f"  - Curie Temp (Heating) : {fit_ferrite_h.params[0]:.2f} +/- {fit_ferrite_h.params[1]:.2f} °C")
        print(f"  - Curie Temp (Cooling) : {fit_ferrite_c.params[0]:.2f} +/- {fit_ferrite_c.params[1]:.2f} °C")
        print(f"  - Cooling Constant k   : {fit_ferrite_temp.params[2]:.6f} s^-1 (Theoretical: 0.082900 s^-1)")
    else:
        print(f"\n[-] warning: {ferrite_path.name} not found.")

    # -----------------------------------------------------------------
    # Part C: Invar Phase Transition Pipeline
    # -----------------------------------------------------------------
    invar_path = parent_dir / "curie_data_invar.csv"
    if invar_path.exists():
        print("\n[+] Executing non-linear fitting pipeline for: Invar Core")
        df_invar = pd.read_csv(invar_path, comment="#")
        
        h_df, c_df = split_data(df_invar)
        t_s, T_s, fit_invar_temp = fit_cooling(c_df, p0=[74.0, 293.0, 0.001])
        fit_invar_h, fit_invar_c = fit_curie(h_df, c_df, (220, 275), (220, 275), [246.0, 5.0], [250.0, 5.0])

        generate_and_save_plots("invar", h_df, c_df, fit_invar_h, fit_invar_c, fit_invar_temp, t_s, T_s, (220, 275), (220, 275), 100, 1.9, parent_dir)
        export_material_results("invar", "אינבר", fit_invar_h, fit_invar_c, fit_invar_temp, k_theory=0.0483, parent_dir=parent_dir)

        print("\n>>> Invar Fit Outputs Summary:")
        print(f"  - Curie Temp (Heating) : {fit_invar_h.params[0]:.2f} +/- {fit_invar_h.params[1]:.2f} °C")
        print(f"  - Curie Temp (Cooling) : {fit_invar_c.params[0]:.2f} +/- {fit_invar_c.params[1]:.2f} °C")
        print(f"  - Cooling Constant k   : {fit_invar_temp.params[2]:.6f} s^-1 (Theoretical: 0.048300 s^-1)")
    else:
        print(f"\n[-] warning: {invar_path.name} not found.")

    print("\n[+] Pipeline execution completed successfully. Structural plots and analytics data dumped to working directory.\n")


if __name__ == "__main__":
    main()