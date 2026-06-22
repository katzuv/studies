import marimo

__generated_with = "0.23.9"
app = marimo.App(auto_download=["html"])

with app.setup:
    import json
    import sys
    from pathlib import Path

    # Add studies root path to sys.path to allow importing physlab
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.special import erf

    from physlab import format_value, physics_fit, set_style


@app.cell(hide_code=True)
def title_section():
    mo.md(r"""
    # Curie Point Experiment – Measurements and Calculations
    This notebook is used for preliminary calculations of the system constants and as a scratchpad for data analysis during the experiment.

    ## Part 1: System and Coil Constants
    """)
    return


@app.cell(hide_code=True)
def coil_geometry_explanation():
    mo.md(r"""
    ### 2. Geometric Parameters of the Coils
    We define the physical dimensions of the primary (outer - 1) and secondary (inner - 2) coils:
    * Turn diameter ($d_1, d_2$)
    * Coil length ($h_1, h_2$)
    * Number of turns ($n_1, n_2$)
    * Copper wire diameter ($d_{\text{wire1}}, d_{\text{wire2}}$)
    """)
    return


@app.cell
def load_constants_from_json():
    _parent_dir = Path(__file__).parent
    _json_path = _parent_dir / "constants" / "constants.json"
    constants_data = json.loads(_json_path.read_text(encoding="utf-8"))
    return (constants_data,)


@app.cell(hide_code=True)
def render_summary_table(constants_data):
    symbol_latex = {
        'R_"coil1"': r"R_{\text{coil1}}",
        'L_"coil1"': r"L_{\text{coil1}}",
        'R_"coil2"': r"R_{\text{coil2}}",
        'L_"coil2"': r"L_{\text{coil2}}",
        "I_1": r"I_1",
        "B_1": r"B_1",
        "V_s / V_p": r"V_s / V_p",
        'R_"oven"': r"R_{\text{oven}}",
        'P_"oven"': r"P_{\text{oven}}",
        "dd(T)/dd(t)": r"\frac{dT}{dt}",
        'R_"th"': r"R_{\text{th}}",
        't_"cool"': r"t_{\text{cool}}",
    }

    unit_latex = {
        "Omega": r"\Omega",
        '"H"': r"\text{H}",
        '"A"': r"\text{A}",
        '"T"': r"\text{T}",
        "": "",
        '"W"': r"\text{W}",
        '"K" / "sec"': r"\text{K}/\text{s}",
        '"K" / "W"': r"\text{K}/\text{W}",
        '"sec"': r"\text{s}",
    }

    df_data = []
    for _const in constants_data:
        sym = _const["symbol"]
        english_name = _const["english_name"]
        latex_sym = symbol_latex.get(sym, sym)
        latex_unit = unit_latex.get(_const["units"], _const["units"])

        # Combine symbol and units in LaTeX, e.g., Symbol [Units]
        if latex_unit:
            combined_sym = f"${latex_sym} \\ [{latex_unit}]$"
        else:
            combined_sym = f"${latex_sym}$"

        # Format values to LaTeX scientific notation and uncertainty using physlab.format_value
        latex_val = format_value(
            _const["value"],
            _const["error"],
            fmt_spec=_const.get("fmt_spec", ".2f"),
            scale=_const.get("scale", 1.0),
            suffix=_const.get("suffix", ""),
            style="latex",
        )
        latex_val = f"${latex_val}$"

        df_data.append(
            {
                "Constant": english_name,
                "Symbol [Units]": mo.md(combined_sym),
                "Calculated Value": mo.md(latex_val),
            }
        )

    table = mo.ui.table(
        df_data,
        selection=None,
        pagination=False,
        show_download=False,
        text_justify_columns={
            "Constant": "left",
            "Symbol [Units]": "center",
            "Calculated Value": "right",
        },
    )
    table = table.style({"width": "fit-content", "margin": "10px 0"}).center()
    table  # noqa: B018
    return


@app.cell(hide_code=True)
def experiment_section_explanation():
    mo.md(r"""
    ---

    ## Part 3: Experimental Measurements and Data Analysis
    In this part, we load the experimental data and perform fits and analysis.
    """)
    return


@app.cell(hide_code=True)
def part_a_explanation():
    mo.md(r"""
    ### Part A: Frequency Response Measurements
    The goal of this part is to measure the induced secondary voltage as a function of frequency for three different cores:
    * Air core ($V_{s0}$)
    * Ferrite core ($V_{s1}$)
    * Invar core ($V_{s2}$)

    This is used to determine the optimal operating frequency.

    The induced EMF according to Faraday's Law:
    $$\epsilon = -N \frac{d\Phi}{dt}$$
    For a sinusoidal current $I_1(t) = I_0 \sin(\omega t)$, the induced secondary voltage is proportional to the angular frequency $\omega = 2\pi f$.

    Load the frequency sweep measurements from the data acquisition software:
    """)
    return


@app.cell
def load_frequency_response_data():
    try:
        _parent_dir = Path(__file__).parent
    except NameError:
        _parent_dir = Path(".")
    _csv_path = _parent_dir / "data" / "freq_sweep.csv"
    _df = pd.read_csv(_csv_path)

    # Filter by core type
    vs0_data = _df[_df["Core Type"] == "VS0 (Air core)"].reset_index(drop=True)
    vs1_data = _df[_df["Core Type"] == "VS1 (N1)"].reset_index(drop=True)
    vs2_data = _df[_df["Core Type"] == "VS2 (N2)"].reset_index(drop=True)
    return vs0_data, vs1_data, vs2_data


@app.cell(hide_code=True)
def part_a_plotting_explanation():
    mo.md(r"""
    Plot the induced voltage $V_s$ vs frequency $f$ (with logarithmic x-axis), and plot the ratio $V_s / V_{s0}$ to select the optimal frequency:
    """)
    return
@app.cell
def plot_frequency_response(vs0_data, vs1_data, vs2_data):
    try:
        _parent_dir = Path(__file__).parent
    except NameError:
        _parent_dir = Path(".")

    # Calculate ratios Vs/Vp
    _freqs = vs0_data["Frequency (Hz)"]
    _vs0_vp = vs0_data["CH2 (V)"] / vs0_data["CH1 (V)"]
    _vs1_vp = vs1_data["CH2 (V)"] / vs1_data["CH1 (V)"]
    _vs2_vp = vs2_data["CH2 (V)"] / vs2_data["CH1 (V)"]

    # Explicit x-ticks for better readability on log scale
    _ticks = [100, 200, 300, 500, 1000, 2000, 3000, 4000]

    # Graph 1: Vs/Vp as a function of frequency
    _fig1, _ax1 = plt.subplots(figsize=(6, 4.5))
    _ax1.semilogx(_freqs, _vs0_vp, label="Air core ($V_{s0}/V_p$)")
    _ax1.semilogx(_freqs, _vs1_vp, label="Ferrite core ($V_{s1}/V_p$)")
    _ax1.semilogx(_freqs, _vs2_vp, label="Invar core ($V_{s2}/V_p$)")
    set_style(_ax1, xlabel="$f \\ [\\mathrm{Hz}]$", ylabel="$V_s / V_p$")
    _ax1.set_xticks(_ticks)
    _ax1.set_xticklabels([str(t) for t in _ticks])
    _ax1.legend(frameon=True)
    plt.tight_layout()
    _fig1.savefig(
        _parent_dir / "graphs" / "frequency_response_vs_vp.svg",
        format="svg",
        bbox_inches="tight",
    )
    plot1 = mo.as_html(_fig1)
    plt.close(_fig1)

    # Graph 2: Vs/Vair as a function of frequency for the magnetic cores
    _vs1_v0 = vs1_data["CH2 (V)"] / vs0_data["CH2 (V)"]
    _vs2_v0 = vs2_data["CH2 (V)"] / vs0_data["CH2 (V)"]

    _fig2, _ax2 = plt.subplots(figsize=(6, 4.5))
    _ax2.semilogx(_freqs, _vs1_v0, label="Ferrite core ($V_{s1}/V_{s0}$)")
    _ax2.semilogx(_freqs, _vs2_v0, label="Invar core ($V_{s2}/V_{s0}$)")
    set_style(_ax2, xlabel="$f \\ [\\mathrm{Hz}]$", ylabel="$V_s / V_{\\mathrm{air}}$")
    _ax2.set_xticks(_ticks)
    _ax2.set_xticklabels([str(t) for t in _ticks])
    _ax2.legend(frameon=True)
    plt.tight_layout()
    fig2_path = _parent_dir / "graphs" / "frequency_response_ratio.svg"
    _fig2.savefig(fig2_path, format="svg", bbox_inches="tight")
    plot2 = mo.as_html(_fig2)
    plt.close(_fig2)

    # Graph 3: Vs directly as a function of frequency
    _vs0 = vs0_data["CH2 (V)"]
    _vs1 = vs1_data["CH2 (V)"]
    _vs2 = vs2_data["CH2 (V)"]

    _fig3, _ax3 = plt.subplots(figsize=(6, 4.5))
    _ax3.semilogx(_freqs, _vs0, label="Air core ($V_{s0}$)")
    _ax3.semilogx(_freqs, _vs1, label="Ferrite core ($V_{s1}$)")
    _ax3.semilogx(_freqs, _vs2, label="Invar core ($V_{s2}$)")
    set_style(_ax3, xlabel="$f \\ [\\mathrm{Hz}]$", ylabel="$V_s \\ [\\mathrm{V}]$")
    _ax3.set_xticks(_ticks)
    _ax3.set_xticklabels([str(t) for t in _ticks])
    _ax3.legend(frameon=True)
    plt.tight_layout()
    fig3_path = _parent_dir / "graphs" / "frequency_response_vs.svg"
    _fig3.savefig(fig3_path, format="svg", bbox_inches="tight")
    plot3 = mo.as_html(_fig3)
    plt.close(_fig3)

    plots = mo.hstack([plot1, plot2, plot3])
    plots  # noqa: B018
    return


@app.cell(hide_code=True)
def part_b_explanation():
    mo.md(r"""
    ### Part B: Heating and Cooling of Ferrite Core
    We measure the induced secondary voltage $V_s$ as a function of temperature $T$ to identify the Curie temperature ($T_c$) where the magnetic phase transition occurs.
    We fit the temperature-time profile $T(t)$ during cooling to Newton's law of cooling:
    $$\frac{dT}{dt} = -k(T - T_{\text{env}})$$
    which has the solution:
    $$T(t) = T_{\text{env}} + (T_0 - T_{\text{env}}) e^{-kt}$$
    """)
    return


@app.cell
def analysis_helpers():
    def split_data(df):
        max_idx = df["Temp (C)"].idxmax()
        heating_df = df.iloc[:max_idx].copy()
        cooling_df = df.iloc[max_idx:].copy()
        return heating_df, cooling_df

    def cooling_model(t, T_env, T0, k):
        return T_env + (T0 - T_env) * np.exp(-k * t)

    def heating_model(t, T_max, T0, k):
        return T_max - (T_max - T0) * np.exp(-k * t)

    def erf_model(T, Tc, dT):
        return 0.5 * (1.0 - erf((T - Tc) / (dT * np.sqrt(2.0))))

    def fit_cooling(cooling_df, p0):
        times = pd.to_datetime(cooling_df["DateTime"], format="%d/%m/%Y %H:%M:%S")
        t_s = (times - times.min()).dt.total_seconds().values
        T_s = cooling_df["Temp (C)"].values
        T_err = np.ones_like(T_s) * 0.1
        fit_temp = physics_fit(cooling_model, t_s, T_s, T_err, p0=p0)
        return t_s, T_s, fit_temp

    def fit_heating(heating_df, p0):
        times = pd.to_datetime(heating_df["DateTime"], format="%d/%m/%Y %H:%M:%S")
        t_s = (times - times.min()).dt.total_seconds().values
        T_s = heating_df["Temp (C)"].values
        T_err = np.ones_like(T_s) * 0.1
        fit_temp = physics_fit(heating_model, t_s, T_s, T_err, p0=p0)
        return t_s, T_s, fit_temp

    def fit_curie(heating_df, cooling_df, h_range, c_range, p0_h, p0_c):
        h_transition = heating_df[
            (heating_df["Temp (C)"] >= h_range[0])
            & (heating_df["Temp (C)"] <= h_range[1])
        ]
        c_transition = cooling_df[
            (cooling_df["Temp (C)"] >= c_range[0])
            & (cooling_df["Temp (C)"] <= c_range[1])
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

    def generate_material_plots(
        material_name,
        heating_df,
        cooling_df,
        fit_h,
        fit_c,
        fit_temp_cool,
        fit_temp_heat,
        t_cool,
        T_cool,
        t_heat,
        T_heat,
        h_range,
        c_range,
        xmin,
        ymin,
        parent_dir,
    ):
        # Graph 1: Hysteresis loop and erf fits
        fig1 = plt.figure(figsize=(6, 4.5))
        plt.scatter(
            heating_df["Temp (C)"],
            heating_df["RMS CH2 (V)"],
            s=1.5,
            alpha=0.4,
            label="Heating data",
            color="#2E86AB",
        )
        plt.scatter(
            cooling_df["Temp (C)"],
            cooling_df["RMS CH2 (V)"],
            s=1.5,
            alpha=0.4,
            label="Cooling data",
            color="#A23B72",
        )

        h_trans = heating_df[
            (heating_df["Temp (C)"] >= h_range[0])
            & (heating_df["Temp (C)"] <= h_range[1])
        ]
        c_trans = cooling_df[
            (cooling_df["Temp (C)"] >= c_range[0])
            & (cooling_df["Temp (C)"] <= c_range[1])
        ]
        V_min_h, V_max_h = h_trans["RMS CH2 (V)"].min(), h_trans["RMS CH2 (V)"].max()
        V_min_c, V_max_c = c_trans["RMS CH2 (V)"].min(), c_trans["RMS CH2 (V)"].max()

        T_fit_h = np.linspace(h_range[0], h_range[1], 300)
        plt.plot(
            T_fit_h,
            V_min_h + (V_max_h - V_min_h) * erf_model(T_fit_h, *fit_h.params),
            color="#0D47A1",
            linewidth=2.0,
            label="Heating Fit",
        )
        T_fit_c = np.linspace(c_range[0], c_range[1], 300)
        plt.plot(
            T_fit_c,
            V_min_c + (V_max_c - V_min_c) * erf_model(T_fit_c, *fit_c.params),
            color="#4A148C",
            linewidth=2.0,
            label="Cooling Fit",
        )

        Tc_h, Tc_c = fit_h.params[0], fit_c.params[0]
        plt.axvline(Tc_h, color="#0D47A1", linestyle="--", alpha=0.8)
        plt.axvline(Tc_c, color="#4A148C", linestyle="--", alpha=0.8)

        set_style(
            xlabel="Temperature ($^\\circ$C)",
            ylabel="RMS Voltage CH2 ($V_s$ [V])",
        )

        plt.xlim(left=xmin)
        plt.ylim(bottom=ymin)
        plt.legend(frameon=True)
        plt.tight_layout()
        fig1.savefig(
            parent_dir / "graphs" / f"{material_name}_curie_fit.svg",
            format="svg",
            bbox_inches="tight",
        )
        plot1 = mo.as_html(fig1)
        plt.close(fig1)

        # Graph 2: Heating & Cooling Curve Fits (Newton's Law)
        fig2 = plt.figure(figsize=(6, 4.5))
        t_peak = t_heat.max()
        plt.scatter(t_heat, T_heat, s=1.5, alpha=0.4, label="Heating data", color="#2E86AB")
        plt.scatter(t_peak + t_cool, T_cool, s=1.5, alpha=0.4, label="Cooling data", color="#A23B72")
        
        t_fit_h = np.linspace(0, t_peak, 300)
        plt.plot(
            t_fit_h,
            heating_model(t_fit_h, *fit_temp_heat.params),
            color="#0D47A1",
            linewidth=2.0,
            label="Heating Fit",
        )
        t_fit_c = np.linspace(t_peak, t_peak + t_cool.max(), 300)
        plt.plot(
            t_fit_c,
            cooling_model(t_fit_c - t_peak, *fit_temp_cool.params),
            color="#C73E1D",
            linewidth=2.0,
            label="Cooling Fit",
        )
        set_style(
            xlabel="Time $[\\mathrm{sec}]$",
            ylabel="Temperature ($^\\circ$C)",
        )
        plt.legend(frameon=True)
        plt.tight_layout()
        fig2.savefig(
            parent_dir / "graphs" / f"{material_name}_cooling_fit.svg",
            format="svg",
            bbox_inches="tight",
        )
        plot2 = mo.as_html(fig2)
        plt.close(fig2)

        # Graph 3: Temperature derivative dT/dt vs Temperature T
        fig3 = plt.figure(figsize=(6, 4.5))
        # Compute smoothed derivatives using central diff with 30s window (15s on each side)
        h_temp = heating_df["Temp (C)"].values
        h_dT_dt = np.full_like(h_temp, np.nan)
        for i in range(15, len(h_temp) - 15):
            h_dT_dt[i] = (h_temp[i + 15] - h_temp[i - 15]) / 30.0

        c_temp = cooling_df["Temp (C)"].values
        c_dT_dt = np.full_like(c_temp, np.nan)
        for i in range(15, len(c_temp) - 15):
            c_dT_dt[i] = (c_temp[i + 15] - c_temp[i - 15]) / 30.0

        plt.plot(h_temp, h_dT_dt, label="Heating phase", color="#2E86AB", alpha=0.8, linewidth=1.5)
        plt.plot(c_temp, c_dT_dt, label="Cooling phase", color="#A23B72", alpha=0.8, linewidth=1.5)
        set_style(
            xlabel="Temperature ($^\\circ$C)",
            ylabel="$dT/dt \\ [^\\circ\\mathrm{C}/\\mathrm{s}]$",
        )
        plt.legend(frameon=True)
        plt.tight_layout()
        fig3.savefig(
            parent_dir / "graphs" / f"{material_name}_dT_dt.svg",
            format="svg",
            bbox_inches="tight",
        )
        plot3 = mo.as_html(fig3)
        plt.close(fig3)

        return plot1, plot2, plot3

    def export_material_results(
        material_name,
        hebrew_material,
        fit_h,
        fit_c,
        fit_temp_cool,
        fit_temp_heat,
        parent_dir,
    ):
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
                "symbol": 'k_"exp,cool"',
                "value": fit_temp_cool.params[2],
                "error": fit_temp_cool.errors[2],
                "units": '"sec"^(-1)',
                "scale": 1.0,
                "fmt_spec": ".6f",
                "suffix": "",
            },
            {
                "hebrew_name": f"קבוע חימום ניסיוני ({hebrew_material})",
                "english_name": f"Experimental Heating Constant - {material_name.capitalize()}",
                "hebrew_var": f"קבוע_חימום_ניסיוני_{material_name}",
                "english_var": f"heating_constant_exp_{material_name}",
                "symbol": 'k_"exp,heat"',
                "value": fit_temp_heat.params[2],
                "error": fit_temp_heat.errors[2],
                "units": '"sec"^(-1)',
                "scale": 1.0,
                "fmt_spec": ".6f",
                "suffix": "",
            },
            {
                "hebrew_name": f"טמפרטורת אסימפטוטת חימום ({hebrew_material})",
                "english_name": f"Heating Asymptotic Temperature - {material_name.capitalize()}",
                "hebrew_var": f"טמפרטורת_אסימפטוטת_חימום_{material_name}",
                "english_var": f"heating_asymptote_{material_name}",
                "symbol": 'T_"max,heat"',
                "value": fit_temp_heat.params[0],
                "error": fit_temp_heat.errors[0],
                "units": '"°C"',
                "scale": 1.0,
                "fmt_spec": ".2f",
                "suffix": "",
            },
        ]

        # Generate formatted values
        for item in results:
            fmt_spec = item.get("fmt_spec", ".2f")
            scale = item.get("scale", 1.0)
            suffix = item.get("suffix", "")
            item["formatted_value"] = format_value(
                item["value"], item["error"], fmt_spec, scale, suffix, style="typst"
            )

        # Save JSON
        json_path = parent_dir / "constants" / f"{material_name}_results.json"
        json_path.write_text(
            json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Generate Typst declarations file
        typst_lines = [
            f"// Automatically generated {material_name} fit results for Typst\n\n"
        ]
        for item in results:
            val_expr = item["formatted_value"]
            if item["units"]:
                val_expr = rf"{val_expr} {item['units']}"
            typst_lines.append(f"#let {item['hebrew_var']} = ${val_expr}$\n")
            typst_lines.append(f"#let {item['english_var']} = {item['hebrew_var']}\n")

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
                    err_expr = rf"{err_expr} {item['units']}"
                err_expr = f"${err_expr}$"

            typst_lines.append(f"#let שגיאת_{item['hebrew_var']} = {err_expr}\n")
            typst_lines.append(
                f"#let {item['english_var']}_err = שגיאת_{item['hebrew_var']}\n"
            )

        typst_path = parent_dir / "constants" / f"{material_name}_results.typ"
        typst_path.write_text("".join(typst_lines), encoding="utf-8")

    return (
        export_material_results,
        fit_cooling,
        fit_curie,
        generate_material_plots,
        split_data,
        fit_heating,
    )


@app.cell
def run_ferrite_pipeline(
    export_material_results,
    fit_cooling,
    fit_curie,
    generate_material_plots,
    split_data,
    fit_heating,
):
    try:
        _parent_dir = Path(__file__).parent
    except NameError:
        _parent_dir = Path(".")

    # 1. Load data
    _csv_path = _parent_dir / "data" / "curie_data_ferrit.csv"
    _df = pd.read_csv(_csv_path, comment="#")

    # 2. Split data
    _ferrite_heating_df, _ferrite_cooling_df = split_data(_df)

    # 3. Fit cooling curve
    # Initial guesses: T_env ~ 24°C, T0 ~ 174°C, k ~ 0.001 s^-1
    _p0_cool = [24.0, 174.0, 0.001]
    _ferrite_t_c, _ferrite_T_c, fit_ferrite_temp_cool = fit_cooling(
        _ferrite_cooling_df, _p0_cool
    )

    # Fit heating curve
    # Initial guesses: T_max ~ 170°C, T0 ~ 25.6°C, k ~ 0.001 s^-1
    _p0_heat = [170.0, 25.6, 0.001]
    _ferrite_t_h, _ferrite_T_h, fit_ferrite_temp_heat = fit_heating(
        _ferrite_heating_df, _p0_heat
    )

    # 4. Fit Curie transition
    _p0_h = [133.0, 0.5]
    _p0_c = [138.0, 0.5]
    fit_ferrite_h, fit_ferrite_c = fit_curie(
        _ferrite_heating_df,
        _ferrite_cooling_df,
        (120, 150),
        (125, 165),
        _p0_h,
        _p0_c,
    )

    # 5. Generate plots
    ferrite_plot1, ferrite_plot2, ferrite_plot3 = generate_material_plots(
        "ferrite",
        _ferrite_heating_df,
        _ferrite_cooling_df,
        fit_ferrite_h,
        fit_ferrite_c,
        fit_ferrite_temp_cool,
        fit_ferrite_temp_heat,
        _ferrite_t_c,
        _ferrite_T_c,
        _ferrite_t_h,
        _ferrite_T_h,
        (120, 150),
        (125, 165),
        100,
        1.9,
        _parent_dir,
    )

    # 6. Export results
    export_material_results(
        "ferrite",
        "פריט",
        fit_ferrite_h,
        fit_ferrite_c,
        fit_ferrite_temp_cool,
        fit_ferrite_temp_heat,
        _parent_dir,
    )
    return (
        ferrite_plot1,
        ferrite_plot2,
        ferrite_plot3,
        fit_ferrite_c,
        fit_ferrite_h,
        fit_ferrite_temp_cool,
        fit_ferrite_temp_heat,
    )


@app.cell(hide_code=True)
def display_ferrite_results(
    ferrite_plot1,
    ferrite_plot2,
    ferrite_plot3,
    fit_ferrite_c,
    fit_ferrite_h,
    fit_ferrite_temp_cool,
):
    _tc_h_str = format_value(
        fit_ferrite_h.params[0], fit_ferrite_h.params[1], ".2f", style="latex"
    )
    _tc_c_str = format_value(
        fit_ferrite_c.params[0], fit_ferrite_c.params[1], ".2f", style="latex"
    )
    _k_exp_str = format_value(
        fit_ferrite_temp_cool.params[2],
        fit_ferrite_temp_cool.errors[2],
        ".6f",
        style="latex",
    )

    _markdown_summary = mo.md(f"""
    ### Analysis Results for Ferrite Core

    1. **Curie Temperature Fit (erf model)**:
       * **Heating phase**: $T_{{c, \\text{{heat}}}} = {_tc_h_str}\\ ^\\circ\\text{{C}}$
       * **Cooling phase**: $T_{{c, \\text{{cool}}}} = {_tc_c_str}\\ ^\\circ\\text{{C}}$
       * *Note*: The difference between heating and cooling Curie points is due to thermal lag between the external heater/thermocouple and the bulk core.

    2. **Newton's Cooling Law Fit**:
       * **Experimental cooling constant**: $k_{{\\text{{exp}}}} = {_k_exp_str}\\ \\text{{s}}^{{-1}}$
       * *Explanation*: The experimental cooling constant is relatively small ($k_{{\\text{{exp}}}} \\approx {_k_exp_str}\\ \\text{{s}}^{{-1}}$) because the core is housed inside the oven assembly. The heat capacity of the entire oven structure (ceramic lining, heating coil, metal shields, etc.) is large, slowing down the cooling rate.
    """)

    _plots = mo.vstack(
        [
            _markdown_summary,
            mo.hstack([ferrite_plot1, ferrite_plot2, ferrite_plot3]),
        ]
    )
    _plots  # noqa: B018
    return


@app.cell(hide_code=True)
def part_c_explanation():
    mo.md(r"""
    ### Part C: Heating and Cooling of Invar Core
    We repeat the exact same analysis steps for the Invar (ferromagnet) sample.
    """)
    return


@app.cell
def run_invar_pipeline(
    export_material_results,
    fit_cooling,
    fit_curie,
    generate_material_plots,
    split_data,
    fit_heating,
):
    try:
        _parent_dir = Path(__file__).parent
    except NameError:
        _parent_dir = Path(".")

    # 1. Load data
    _csv_path = _parent_dir / "data" / "curie_data_invar.csv"
    _df = pd.read_csv(_csv_path, comment="#")

    # 2. Split data
    _invar_heating_df, _invar_cooling_df = split_data(_df)

    # 3. Fit cooling curve
    # Initial guesses: T_env ~ 74°C, T0 ~ 293°C, k ~ 0.001 s^-1
    _p0_cool = [74.0, 293.0, 0.001]
    _invar_t_c, _invar_T_c, fit_invar_temp_cool = fit_cooling(
        _invar_cooling_df, _p0_cool
    )

    # Fit heating curve
    # Initial guesses: T_max ~ 310°C, T0 ~ 30.0°C, k ~ 0.001 s^-1
    _p0_heat = [310.0, 30.0, 0.001]
    _invar_t_h, _invar_T_h, fit_invar_temp_heat = fit_heating(
        _invar_heating_df, _p0_heat
    )

    # 4. Fit Curie transition
    _p0_h = [246.0, 5.0]
    _p0_c = [250.0, 5.0]
    fit_invar_h, fit_invar_c = fit_curie(
        _invar_heating_df,
        _invar_cooling_df,
        (220, 275),
        (220, 275),
        _p0_h,
        _p0_c,
    )

    # 5. Generate plots
    invar_plot1, invar_plot2, invar_plot3 = generate_material_plots(
        "invar",
        _invar_heating_df,
        _invar_cooling_df,
        fit_invar_h,
        fit_invar_c,
        fit_invar_temp_cool,
        fit_invar_temp_heat,
        _invar_t_c,
        _invar_T_c,
        _invar_t_h,
        _invar_T_h,
        (220, 275),
        (220, 275),
        100,
        1.9,
        _parent_dir,
    )

    # 6. Export results
    export_material_results(
        "invar",
        "אינבר",
        fit_invar_h,
        fit_invar_c,
        fit_invar_temp_cool,
        fit_invar_temp_heat,
        _parent_dir,
    )
    return fit_invar_c, fit_invar_h, fit_invar_temp_cool, fit_invar_temp_heat, invar_plot1, invar_plot2, invar_plot3


@app.cell(hide_code=True)
def display_invar_results(
    fit_invar_c,
    fit_invar_h,
    fit_invar_temp_cool,
    invar_plot1,
    invar_plot2,
    invar_plot3,
):
    _tc_h_str = format_value(
        fit_invar_h.params[0], fit_invar_h.params[1], ".2f", style="latex"
    )
    _tc_c_str = format_value(
        fit_invar_c.params[0], fit_invar_c.params[1], ".2f", style="latex"
    )
    _k_exp_str = format_value(
        fit_invar_temp_cool.params[2],
        fit_invar_temp_cool.errors[2],
        ".6f",
        style="latex",
    )

    _markdown_summary = mo.md(f"""
    ### Analysis Results for Invar Core

    1. **Curie Temperature Fit (erf model)**:
       * **Heating phase**: $T_{{c, \\text{{heat}}}} = {_tc_h_str}\\ ^\\circ\\text{{C}}$
       * **Cooling phase**: $T_{{c, \\text{{cool}}}} = {_tc_c_str}\\ ^\\circ\\text{{C}}$
       * *Note*: As with the ferrite core, the difference between heating and cooling Curie points is due to thermal lag.

    2. **Newton's Cooling Law Fit**:
       * **Experimental cooling constant**: $k_{{\\text{{exp}}}} = {_k_exp_str}\\ \\text{{s}}^{{-1}}$
       * *Explanation*: The experimental cooling constant is relatively small ($k_{{\\text{{exp}}}} \\approx {_k_exp_str}\\ \\text{{s}}^{{-1}}$) for the same physical reasons (thermal mass of the oven assembly slowing down heat dissipation).
    """)

    _plots = mo.vstack(
        [
            _markdown_summary,
            mo.hstack([invar_plot1, invar_plot2, invar_plot3]),
        ]
    )
    _plots  # noqa: B018
    return


@app.cell(hide_code=True)
def part_d_explanation():
    mo.md(r"""
    ### Part D: Summary of Results and Literature Comparison
    We summarize the Curie temperatures for both materials and compare them to theoretical/literature values.
    """)
    return


@app.cell
def summarize_results(fit_ferrite_c, fit_ferrite_h, fit_invar_c, fit_invar_h):
    # Summary of Curie temperatures
    _ferrite_tc = (fit_ferrite_h.params[0] + fit_ferrite_c.params[0]) / 2
    _invar_tc = (fit_invar_h.params[0] + fit_invar_c.params[0]) / 2
    return


if __name__ == "__main__":
    app.run()
