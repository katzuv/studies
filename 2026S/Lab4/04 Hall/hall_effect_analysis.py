# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.10.0",
#     "pandas",
#     "numpy",
#     "matplotlib",
#     "scipy",
# ]
# ///

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats
    from scipy.constants import e, k
    import os

    # Modern styling
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#2c3e50'
    plt.rcParams['axes.labelcolor'] = '#2c3e50'
    plt.rcParams['xtick.color'] = '#7f8c8d'
    plt.rcParams['ytick.color'] = '#7f8c8d'
    plt.rcParams['grid.color'] = '#ecf0f1'
    plt.rcParams['grid.linestyle'] = '-'
    plt.rcParams['axes.edgecolor'] = '#bdc3c7'
    plt.rcParams['axes.linewidth'] = 0.8

    # Constants
    d = 1.0e-3  # m
    W = 10.0e-3  # m
    L = 16.0e-3  # m
    q_e = -e  # C (electron charge)

    # Generic Helper Functions
    def load_data(filename, cols, header_exists=False):
        path = f"data/{filename}"
        if header_exists:
            df = pd.read_csv(path, sep=r'\s+', comment='#')
            df.columns = cols
        else:
            df = pd.read_csv(path, sep=r'\s+', comment='#', names=cols)
        return df

    def fit_linear(x, y):
        slope, intercept, r_val, _, _ = stats.linregress(x, y)
        return slope, intercept, r_val**2

    def format_sci_latex(val, precision=4):
        if val == 0:
            return "0"
        exponent = int(np.floor(np.log10(abs(val))))
        mantissa = val / (10**exponent)
        if exponent == 0:
            return f"{mantissa:.{precision}f}"
        return f"{mantissa:.{precision}f} \\times 10^{{{exponent}}}"

    def plot_scatter_with_fit(x, y, xlabel, ylabel, title, fit_x=None, fit_y=None, fit_lbl="", filename=None, color='#3498db', fit_color='#e74c3c', highlight_x=None, highlight_y=None, highlight_lbl=""):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(x, y, color=color, s=45, alpha=0.8, label='Data points', zorder=3)
        if highlight_x is not None and highlight_y is not None:
            ax.scatter(highlight_x, highlight_y, color='#e74c3c', s=45, label=highlight_lbl, zorder=4)
        if fit_x is not None and fit_y is not None:
            ax.plot(fit_x, fit_y, color=fit_color, linewidth=1.8, linestyle='--', label=fit_lbl, zorder=5)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(title, fontsize=11, fontweight='bold', pad=12)
        ax.grid(True, zorder=1)
        ax.legend(frameon=True, facecolor='white', edgecolor='none')
        fig.tight_layout()
        if filename:
            os.makedirs('graphs', exist_ok=True)
            fig.savefig(f"graphs/{filename}", format='svg')
        plt.show()

    return (
        L,
        W,
        d,
        e,
        fit_linear,
        format_sci_latex,
        k,
        load_data,
        mo,
        np,
        plot_scatter_with_fit,
        q_e,
    )


@app.cell(hide_code=True)
def _(mo):
    material_selector = mo.ui.radio(options=['P-Type', 'N-Type'], value='P-Type', label='Select Semiconductor Material:')
    material_selector
    return (material_selector,)


@app.cell(hide_code=True)
def _(material_selector):
    data_suffix = "_n_type" if material_selector.value == 'N-Type' else ""
    return (data_suffix,)


@app.cell(hide_code=True)
def _(data_suffix, mo):
    material = "N-Type" if "n_type" in data_suffix else "P-Type"
    mo.md(fr"""
    # Hall Effect Experiment Analysis ({material} Semiconductor)

    This notebook analyzes experimental data from a semiconductor sample (Germanium) to determine:
    1. The **sample resistance** $R$ and **misalignment parameter** $\beta$ from the Zero Field Experiment.
    2. The **Hall coefficient** $R_H$, **carrier concentration** $n$, and **mobility** $\mu$ from Room Temperature Experiments (varying current and varying magnetic field).
    3. The **bandgap energy** $E_g$ of Germanium from the Heating/Cooling Experiment.

    ## Active Configuration
    * **Analyzing Material:** **{material}** (data_suffix = `"{data_suffix}"`)
    """)
    return (material,)


@app.cell(hide_code=True)
def _(
    data_suffix,
    fit_linear,
    format_sci_latex,
    load_data,
    np,
    plot_scatter_with_fit,
):
    # Load and fit Zero Field Data
    df_zf = load_data(f"zero_field{data_suffix}.txt", ['Ip_mA', 'T_C', 'Uh_mV', 'Up_mV'])

    # 1. Conductance fit
    slope_cond, intercept_cond, _ = fit_linear(df_zf['Up_mV'], df_zf['Ip_mA'])
    R_zf = 1.0 / slope_cond

    # 2. Misalignment fit
    slope_beta, intercept_beta, _ = fit_linear(df_zf['Up_mV'], df_zf['Uh_mV'])

    # Plots
    _x = np.linspace(df_zf['Up_mV'].min(), df_zf['Up_mV'].max(), 100)

    # Graph 1
    plot_scatter_with_fit(
        df_zf['Up_mV'], df_zf['Uh_mV'], 'Probe Voltage $U_p$ (mV)', 'Measured Hall Voltage $U\'_H$ (mV)',
        'Measured Hall Voltage $U\'_H$ vs Probe Voltage $U_p$',
        _x, slope_beta * _x + intercept_beta, fr'Fit: $U_H = {format_sci_latex(slope_beta, precision=2)} U_p + {intercept_beta:.2f}$',
        f"uh_vs_up{data_suffix}.svg", color='#2ecc71', fit_color='#f39c12'
    )

    # Graph 2
    plot_scatter_with_fit(
        df_zf['Up_mV'], df_zf['Ip_mA'], 'Probe Voltage $U_p$ (mV)', 'Sample Current $I_p$ (mA)',
        'Sample Current $I_p$ vs Probe Voltage $U_p$',
        _x, slope_cond * _x + intercept_cond, f'Fit: $I_p = {slope_cond:.5f} U_p + {intercept_cond:.2f}$',
        f"ip_vs_up{data_suffix}.svg", color='#3498db', fit_color='#e74c3c'
    )
    return R_zf, intercept_beta, slope_beta, slope_cond


@app.cell(hide_code=True)
def _(
    L,
    R_zf,
    W,
    d,
    format_sci_latex,
    intercept_beta,
    mo,
    slope_beta,
    slope_cond,
):
    rho_zf = R_zf * W * d / L
    mo.md(fr"""
    ### Zero Field Results
    * **Sample Resistance $R$:** $1/G = {R_zf:.4f}\ \Omega$ (Conductance $G = {slope_cond:.6f}\ \text{{S}}$)
    * **Resistivity $\rho_{{xx}}$ (at $B = 0$):** ${format_sci_latex(rho_zf)}\ \Omega\cdot\text{{m}}$
    * **Misalignment Parameter $\beta$:** ${format_sci_latex(slope_beta)}$ (Offset: ${intercept_beta:.2f}\ \text{{mV}}$)
    """)
    return


@app.cell(hide_code=True)
def _(
    L,
    W,
    d,
    data_suffix,
    fit_linear,
    load_data,
    np,
    plot_scatter_with_fit,
    q_e,
    slope_beta,
):
    # Load RT datasets
    df_curr = load_data(f"varying_current{data_suffix}.txt", ['Ip_mA', 'T_C', 'Uh_mV', 'Up_mV'])
    df_curr['Uh_corr_mV'] = df_curr['Uh_mV'] - slope_beta * df_curr['Up_mV']

    df_field = load_data(f"varying_field{data_suffix}.txt", ['B_mT', 'T_C', 'Uh_mV', 'Up_mV'])
    df_field['Uh_corr_mV'] = df_field['Uh_mV'] - slope_beta * df_field['Up_mV']

    # 1. Varying Current Analysis (constant B = 301 mT)
    s_curr, int_curr, _ = fit_linear(df_curr['Ip_mA'], df_curr['Uh_corr_mV'])
    B_curr = 301.0e-3
    RH_curr = s_curr * d / B_curr
    carrier_type_curr = "p-type" if RH_curr > 0 else "n-type"
    q_carrier_curr = -q_e if RH_curr > 0 else q_e
    n_curr = 1.0 / (abs(RH_curr) * q_carrier_curr)

    r_0_curr, _, _ = fit_linear(df_curr['Ip_mA'], df_curr['Up_mV'])
    rho_curr = r_0_curr * W * d / L
    mu_curr = abs(RH_curr) / rho_curr

    # 2. Varying Field Analysis (constant Ip = 30 mA)
    B_T = df_field['B_mT'] / 1000.0
    Uh_V = df_field['Uh_corr_mV'] / 1000.0
    s_field, int_field, _ = fit_linear(B_T, Uh_V)
    I_field = 30.0e-3
    RH_field = s_field * d / I_field
    carrier_type_field = "p-type" if RH_field > 0 else "n-type"
    q_carrier_field = -q_e if RH_field > 0 else q_e
    n_field = 1.0 / (abs(RH_field) * q_carrier_field)

    r_0_field = (df_field['Up_mV'].mean() / 1000.0) / I_field
    rho_field = r_0_field * W * d / L
    mu_field = abs(RH_field) / rho_field

    # Plots
    # Graph 3
    _x3 = np.linspace(df_curr['Ip_mA'].min(), df_curr['Ip_mA'].max(), 100)
    plot_scatter_with_fit(
        df_curr['Ip_mA'], df_curr['Uh_corr_mV'], 'Sample Current $I_p$ (mA)', 'Corrected Hall Voltage $U_H$ (mV)',
        'Corrected Hall Voltage $U_H$ vs Sample Current $I_p$',
        _x3, s_curr * _x3 + int_curr, f'Fit: $U_H = {s_curr:.3f} I_p + {int_curr:.2f}$',
        f"uh_vs_ip_varying_current{data_suffix}.svg", color='#9b59b6', fit_color='#2ecc71'
    )

    # Graph 4
    _x4 = np.linspace(B_T.min(), B_T.max(), 100)
    plot_scatter_with_fit(
        B_T, Uh_V, 'Magnetic Field $B$ (T)', 'Corrected Hall Voltage $U_H$ (V)',
        'Corrected Hall Voltage $U_H$ vs Magnetic Field $B$',
        _x4, s_field * _x4 + int_field, f'Fit: $U_H = {s_field:.4f} B + {int_field:.4f}$',
        f"uh_vs_b_varying_field{data_suffix}.svg", color='#e67e22', fit_color='#34495e'
    )
    return (
        B_curr,
        I_field,
        RH_curr,
        RH_field,
        carrier_type_curr,
        carrier_type_field,
        mu_curr,
        mu_field,
        n_curr,
        n_field,
        rho_curr,
        rho_field,
        s_curr,
        s_field,
    )


@app.cell(hide_code=True)
def _(
    B_curr,
    I_field,
    RH_curr,
    RH_field,
    carrier_type_curr,
    carrier_type_field,
    format_sci_latex,
    material,
    mo,
    mu_curr,
    mu_field,
    n_curr,
    n_field,
    q_e,
    rho_curr,
    rho_field,
    s_curr,
    s_field,
):
    mo.md(fr"""
    ### Room Temperature Results & Parameter Comparison ({material})

    We calculate the physical parameters using the electron charge constant $q_e = {format_sci_latex(q_e)}\ \text{{C}}$:

    | Parameter | Varying Current ($B = {B_curr*1000.0:.1f}\ \text{{mT}}$) | Varying Field ($I_p = {I_field*1000.0:.1f}\ \text{{mA}}$) |
    |---|---|---|
    | **Fit Slope** | $S_{{H, I}} = {s_curr:.5f}\ \Omega$ | $S_{{H, B}} = {s_field:.5f}\ \text{{V/T}}$ |
    | **Hall Coefficient ($R_H$)** | ${format_sci_latex(RH_curr)}\ \text{{m}}^3/\text{{C}}$ | ${format_sci_latex(RH_field)}\ \text{{m}}^3/\text{{C}}$ |
    | **Carrier Type** | **{carrier_type_curr.upper()}** | **{carrier_type_field.upper()}** |
    | **Carrier Concentration ($n$)** | ${format_sci_latex(n/1.0e6 if (n:=n_curr) else 0.0)}\ \text{{cm}}^{{-3}}$ | ${format_sci_latex(n/1.0e6 if (n:=n_field) else 0.0)}\ \text{{cm}}^{{-3}}$ |
    | **Resistivity ($\rho_{{xx}}$)** | ${format_sci_latex(rho_curr)}\ \Omega\cdot\text{{m}}$ | ${format_sci_latex(rho_field)}\ \Omega\cdot\text{{m}}$ |
    | **Hall Mobility ($\mu$)** | ${mu_curr:.4f}\ \text{{m}}^2/(\text{{V}}\cdot\text{{s}})$ | ${mu_field:.4f}\ \text{{m}}^2/(\text{{V}}\cdot\text{{s}})$ |
    """)
    return


@app.cell(hide_code=True)
def _(data_suffix, e, fit_linear, k, load_data, np, plot_scatter_with_fit):
    # Load dataset
    df_heat = load_data(f"varying_temp{data_suffix}.txt", ['T_C', 'Uh_mV', 'Up_mV'], header_exists=True)
    df_heat['T_K'] = df_heat['T_C'] + 273.15
    df_heat['inv_T'] = 1.0 / df_heat['T_K']

    # Calculate ln(sigma/sigma_0) where sigma is proportional to 1/Up
    # We use the first point as the reference Up_0 (lowest temperature)
    Up_0 = df_heat['Up_mV'].iloc[0]
    df_heat['ln_sigma_sigma0'] = np.log(Up_0 / df_heat['Up_mV'])

    # Intrinsic fit range (T >= 100°C)
    df_high_T = df_heat[df_heat['T_C'] >= 100.0]
    slope_Eg, intercept_Eg, _ = fit_linear(df_high_T['inv_T'], df_high_T['ln_sigma_sigma0'])

    kB = k / e
    # For ln(sigma/sigma_0) = -Eg / (2 * kB * T) + const, the slope is -Eg / (2 * kB)
    # Therefore, Eg = -2.0 * kB * slope
    Eg_val = -2.0 * kB * slope_Eg

    # Graph 5 Plot
    _x5 = np.linspace(df_high_T['inv_T'].min(), df_high_T['inv_T'].max(), 100)
    plot_scatter_with_fit(
        df_heat['inv_T'], df_heat['ln_sigma_sigma0'], r'$1/T$ ($\text{K}^{-1}$)', r'$\ln(\sigma/\sigma_0)$',
        r'$\ln(\sigma/\sigma_0)$ vs $1/T$ (Bandgap Fitting)',
        _x5, slope_Eg * _x5 + intercept_Eg, fr'Fit: $E_g = {Eg_val:.4f}\ \text{{eV}}$',
        f"ln_sigma_vs_inv_t{data_suffix}.svg", color='#bdc3c7', fit_color='#c0392b',
        highlight_x=df_high_T['inv_T'], highlight_y=df_high_T['ln_sigma_sigma0'], highlight_lbl=r'Intrinsic regime ($T \geq 100^\circ\text{C}$)'
    )
    return Eg_val, intercept_Eg, slope_Eg


@app.cell(hide_code=True)
def _(Eg_val, intercept_Eg, mo, slope_Eg):
    mo.md(fr"""
    ### Bandgap Results
    * **High-Temperature Fit Slope:** ${slope_Eg:.2f}\ \text{{K}}$
    * **Intercept:** ${intercept_Eg:.4f}$
    * **Calculated Energy Gap ($E_g = -2 \cdot k_B \cdot \text{{Slope}}$):** **{Eg_val:.4f} eV**
    """)
    return


if __name__ == "__main__":
    app.run()
