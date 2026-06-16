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

    from physlab import format_value


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
    parent_dir = Path(__file__).parent
    json_path = parent_dir / "constants.json"
    constants_data = json.loads(json_path.read_text(encoding="utf-8"))
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
    # TODO: Load data for the 3 cores
    # vs0_data = ... (air)
    # vs1_data = ... (ferrite)
    # vs2_data = ... (invar)
    return


@app.cell(hide_code=True)
def part_a_plotting_explanation():
    mo.md(r"""
    Plot the induced voltage $V_s$ vs frequency $f$ (with logarithmic x-axis), and plot the ratio $V_s / V_{s0}$ to select the optimal frequency:
    """)
    return


@app.cell
def plot_frequency_response():
    # TODO: Plot the frequency response curves and select the optimal frequency
    # Note: Save the plots as SVG and do not include titles inside the graphs.
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
def load_ferrite_data():
    # TODO: Load heating/cooling data for the ferrite sample
    # ferrite_data = ...
    return


@app.cell
def fit_ferrite_cooling():
    # TODO: Fit to Newton's cooling law and extract the experimental k value
    # Compare with the theoretical k_ferrite.
    return


@app.cell
def find_ferrite_curie_temp():
    # TODO: Plot Vs vs T and find the Curie temperature for Ferrite
    return


@app.cell(hide_code=True)
def part_c_explanation():
    mo.md(r"""
    ### Part C: Heating and Cooling of Invar Core
    Repeat the same analysis steps for the Invar (ferromagnet) sample:
    """)
    return


@app.cell
def load_invar_data():
    # TODO: Load heating/cooling data for the invar sample
    # invar_data = ...
    return


@app.cell
def fit_invar_cooling():
    # TODO: Fit to Newton's cooling law and extract k for invar.
    return


@app.cell
def find_invar_curie_temp():
    # TODO: Plot Vs vs T and find the Curie temperature for Invar.
    return


@app.cell(hide_code=True)
def part_d_explanation():
    mo.md(r"""
    ### Part D: Summary of Results and Literature Comparison
    Summarize the measured Curie temperatures for both cores and compare them with the literature values.
    """)
    return


@app.cell
def summarize_results():
    # TODO: Final summary of results
    return


if __name__ == "__main__":
    app.run()
