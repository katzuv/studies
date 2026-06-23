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
    from scipy.constants import e, k
    import os
    from physlab.core import physics_fit, set_style, export_constants

    # Constants
    d = 1.0e-3  # m
    W = 10.0e-3  # m
    L = 16.0e-3  # m
    q_e = -e  # C
    kB_eV = k / e

    # Generic Helper Functions
    def load_data(filename, cols, header_exists=False):
        path = f"data/{filename}"
        if header_exists:
            df = pd.read_csv(path, sep=r'\s+', comment='#')
            df.columns = cols
        else:
            df = pd.read_csv(path, sep=r'\s+', comment='#', names=cols)
        return df

    def linear_model(x, a, b):
        return a * x + b

    return (
        L,
        W,
        d,
        e,
        physics_fit,
        set_style,
        export_constants,
        k,
        load_data,
        mo,
        np,
        pd,
        plt,
        q_e,
        kB_eV,
        linear_model,
        os,
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
    linear_model,
    load_data,
    np,
    physics_fit,
    plt,
    set_style,
    W,
    d,
    L,
):
    # Load and fit Zero Field Data
    df_zf = load_data(f"zero_field{data_suffix}.txt", ['Ip_mA', 'T_C', 'Uh_mV', 'Up_mV'])

    # 1. Conductance fit: Ip = G * Up + intercept
    res_cond_init = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Ip_mA'], np.ones_like(df_zf['Ip_mA']))
    G_init = res_cond_init.params[0]
    y_err_cond = np.sqrt(1.0**2 + (G_init * 1.0)**2)
    fit_cond = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Ip_mA'], np.full_like(df_zf['Ip_mA'], y_err_cond))
    G = fit_cond.params[0]
    dG = fit_cond.errors[0]
    R_zf = 1.0 / G
    dR_zf = dG / (G**2)

    # 2. Misalignment fit: Uh' = beta * Up + intercept
    res_beta_init = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Uh_mV'], np.ones_like(df_zf['Uh_mV']))
    beta_init = res_beta_init.params[0]
    y_err_beta = 1.0 * np.sqrt(1.0 + beta_init**2)
    fit_beta = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Uh_mV'], np.full_like(df_zf['Uh_mV'], y_err_beta))
    beta = fit_beta.params[0]
    dbeta = fit_beta.errors[0]

    # Plots (using private variables to avoid multiple-definition issues in Marimo)
    _fig, _ax = plt.subplots(figsize=(6, 4))
    x_line = np.linspace(df_zf['Up_mV'].min(), df_zf['Up_mV'].max(), 100)
    _ax.errorbar(df_zf['Up_mV'], df_zf['Uh_mV'], xerr=1.0, yerr=1.0, fmt='o', color='#2ecc71', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
    _ax.plot(x_line, linear_model(x_line, *fit_beta.params), color='#f39c12', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
    set_style(ax=_ax, xlabel='Probe Voltage $U_p$ (mV)', ylabel='Hall Voltage $U\'_H$ (mV)', grid=True)
    _ax.legend(frameon=True, facecolor='white', edgecolor='none')
    _fig.tight_layout()
    _fig.savefig(f"graphs/uh_vs_up{data_suffix}.svg", format='svg', metadata={'Date': None})
    plt.close(_fig)

    _fig2, _ax2 = plt.subplots(figsize=(6, 4))
    _ax2.errorbar(df_zf['Up_mV'], df_zf['Ip_mA'], xerr=1.0, yerr=1.0, fmt='o', color='#3498db', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
    _ax2.plot(x_line, linear_model(x_line, *fit_cond.params), color='#e74c3c', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
    set_style(ax=_ax2, xlabel='Probe Voltage $U_p$ (mV)', ylabel='Sample Current $I_p$ (mA)', grid=True)
    _ax2.legend(frameon=True, facecolor='white', edgecolor='none')
    _fig2.tight_layout()
    _fig2.savefig(f"graphs/ip_vs_up{data_suffix}.svg", format='svg', metadata={'Date': None})
    plt.close(_fig2)

    return R_zf, dR_zf, beta, dbeta, G, dG


@app.cell(hide_code=True)
def _(
    L,
    R_zf,
    dR_zf,
    W,
    d,
    beta,
    dbeta,
    mo,
    G,
):
    rho_zf = R_zf * W * d / L
    drho_zf = dR_zf * W * d / L
    mo.md(fr"""
    ### Zero Field Results
    * **Sample Resistance $R$:** $1/G = {R_zf:.4f} \pm {dR_zf:.4f}\ \Omega$
    * **Resistivity $\rho_{{xx}}$ (at $B = 0$):** ${rho_zf:.5e} \pm {drho_zf:.5e}\ \Omega\cdot\text{{m}}$
    * **Misalignment Parameter $\beta$:** ${beta:.5f} \pm {dbeta:.5f}$
    """)
    return drho_zf, rho_zf


@app.cell(hide_code=True)
def _(
    L,
    W,
    d,
    data_suffix,
    linear_model,
    load_data,
    np,
    physics_fit,
    plt,
    set_style,
    beta,
    dbeta,
    e,
):
    # Load RT datasets
    df_curr = load_data(f"varying_current{data_suffix}.txt", ['Ip_mA', 'T_C', 'Uh_mV', 'Up_mV'])
    dUh_curr = np.sqrt(1.0**2 + (df_curr['Up_mV'] * dbeta)**2 + (beta * 1.0)**2)
    df_curr['Uh_corr_mV'] = df_curr['Uh_mV'] - beta * df_curr['Up_mV']

    df_field = load_data(f"varying_field{data_suffix}.txt", ['B_mT', 'T_C', 'Uh_mV', 'Up_mV'])
    dUh_field = np.sqrt(1.0**2 + (df_field['Up_mV'] * dbeta)**2 + (beta * 1.0)**2) / 1000.0

    # 1. Varying Current Analysis (constant B = 301 mT)
    res_s_curr_init = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Uh_corr_mV'], dUh_curr)
    s_curr_init = res_s_curr_init.params[0]
    y_err_s_curr = np.sqrt(dUh_curr**2 + (s_curr_init * 1.0)**2)
    fit_s_curr = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Uh_corr_mV'], y_err_s_curr)
    s_curr = fit_s_curr.params[0]
    ds_curr = fit_s_curr.errors[0]

    B_curr = 301.0e-3
    dB_curr = 1.0e-3
    RH_curr = s_curr * d / B_curr
    dRH_curr = abs(RH_curr) * np.sqrt((ds_curr / s_curr)**2 + (dB_curr / B_curr)**2)

    carrier_type_curr = "p-type" if RH_curr > 0 else "n-type"
    n_curr = 1.0 / (abs(RH_curr) * e)
    dn_curr = n_curr * (dRH_curr / abs(RH_curr))

    res_r0_curr_init = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Up_mV'], np.ones_like(df_curr['Ip_mA']))
    r0_curr_init = res_r0_curr_init.params[0]
    y_err_r0_curr = np.sqrt(1.0**2 + (r0_curr_init * 1.0)**2)
    fit_r0_curr = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Up_mV'], np.full_like(df_curr['Ip_mA'], y_err_r0_curr))
    r0_curr = fit_r0_curr.params[0]
    dr0_curr = fit_r0_curr.errors[0]

    rho_curr = r0_curr * W * d / L
    drho_curr = dr0_curr * W * d / L
    mu_curr = abs(RH_curr) / rho_curr
    dmu_curr = mu_curr * np.sqrt((dRH_curr / RH_curr)**2 + (drho_curr / rho_curr)**2)

    # 2. Varying Field Analysis (constant Ip = 30 mA)
    B_T = df_field['B_mT'] / 1000.0
    dB_T = 1.0e-3
    Uh_corr_V = (df_field['Uh_mV'] - beta * df_field['Up_mV']) / 1000.0

    res_s_field_init = physics_fit(linear_model, B_T, Uh_corr_V, dUh_field)
    s_field_init = res_s_field_init.params[0]
    y_err_s_field = np.sqrt(dUh_field**2 + (s_field_init * 1.0e-3)**2)
    fit_s_field = physics_fit(linear_model, B_T, Uh_corr_V, y_err_s_field)
    s_field = fit_s_field.params[0]
    ds_field = fit_s_field.errors[0]

    I_field = 30.0e-3
    dI_field = 1.0e-3
    RH_field = s_field * d / I_field
    dRH_field = abs(RH_field) * np.sqrt((ds_field / s_field)**2 + (dI_field / I_field)**2)

    carrier_type_field = "p-type" if RH_field > 0 else "n-type"
    n_field = 1.0 / (abs(RH_field) * e)
    dn_field = n_field * (dRH_field / abs(RH_field))

    mean_Up_V = df_field['Up_mV'].mean() / 1000.0
    dmean_Up_V = 0.001
    r0_field = mean_Up_V / I_field
    dr0_field = r0_field * np.sqrt((dmean_Up_V / mean_Up_V)**2 + (dI_field / I_field)**2)

    rho_field = r0_field * W * d / L
    drho_field = dr0_field * W * d / L
    mu_field = abs(RH_field) / rho_field
    dmu_field = mu_field * np.sqrt((dRH_field / RH_field)**2 + (drho_field / rho_field)**2)

    # Plots using private variables to avoid multiple definition issues
    _fig3, _ax3 = plt.subplots(figsize=(6, 4))
    x_line_curr = np.linspace(df_curr['Ip_mA'].min(), df_curr['Ip_mA'].max(), 100)
    _ax3.errorbar(df_curr['Ip_mA'], df_curr['Uh_corr_mV'], xerr=1.0, yerr=dUh_curr, fmt='o', color='#9b59b6', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
    _ax3.plot(x_line_curr, linear_model(x_line_curr, *fit_s_curr.params), color='#2ecc71', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
    set_style(ax=_ax3, xlabel='Sample Current $I_p$ (mA)', ylabel='Corrected Hall Voltage $U_H$ (mV)', grid=True)
    _ax3.legend(frameon=True, facecolor='white', edgecolor='none')
    _fig3.tight_layout()
    _fig3.savefig(f"graphs/uh_vs_ip_varying_current{data_suffix}.svg", format='svg', metadata={'Date': None})
    plt.close(_fig3)

    _fig4, _ax4 = plt.subplots(figsize=(6, 4))
    x_line_field = np.linspace(B_T.min(), B_T.max(), 100)
    _ax4.errorbar(B_T, Uh_corr_V, xerr=dB_T, yerr=dUh_field, fmt='o', color='#e67e22', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
    _ax4.plot(x_line_field, linear_model(x_line_field, *fit_s_field.params), color='#34495e', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
    set_style(ax=_ax4, xlabel='Magnetic Field $B$ (T)', ylabel='Corrected Hall Voltage $U_H$ (V)', grid=True)
    _ax4.legend(frameon=True, facecolor='white', edgecolor='none')
    _fig4.tight_layout()
    _fig4.savefig(f"graphs/uh_vs_b_varying_field{data_suffix}.svg", format='svg', metadata={'Date': None})
    plt.close(_fig4)

    return (
        B_curr,
        dB_curr,
        I_field,
        dI_field,
        RH_curr,
        dRH_curr,
        RH_field,
        dRH_field,
        carrier_type_curr,
        carrier_type_field,
        mu_curr,
        dmu_curr,
        mu_field,
        dmu_field,
        n_curr,
        dn_curr,
        n_field,
        dn_field,
        rho_curr,
        drho_curr,
        rho_field,
        drho_field,
        s_curr,
        ds_curr,
        s_field,
        ds_field,
    )


@app.cell(hide_code=True)
def _(
    B_curr,
    dB_curr,
    I_field,
    dI_field,
    RH_curr,
    dRH_curr,
    RH_field,
    dRH_field,
    carrier_type_curr,
    carrier_type_field,
    material,
    mo,
    mu_curr,
    dmu_curr,
    mu_field,
    dmu_field,
    n_curr,
    dn_curr,
    n_field,
    dn_field,
    rho_curr,
    drho_curr,
    rho_field,
    drho_field,
    s_curr,
    ds_curr,
    s_field,
    ds_field,
):
    mo.md(fr"""
    ### Room Temperature Results ({material})

    | Parameter | Varying Current ($B = {B_curr*1000.0:.1f} \pm {dB_curr*1000.0:.1f}\ \text{{mT}}$) | Varying Field ($I_p = {I_field*1000.0:.1f} \pm {dI_field*1000.0:.1f}\ \text{{mA}}$) |
    |---|---|---|
    | **Fit Slope** | $S_{{H, I}} = {s_curr:.4f} \pm {ds_curr:.4f}\ \Omega$ | $S_{{H, B}} = {s_field:.4f} \pm {ds_field:.4f}\ \text{{V/T}}$ |
    | **Hall Coefficient ($R_H$)** | ${RH_curr:.2e} \pm {dRH_curr:.2e}\ \text{{m}}^3/\text{{C}}$ | ${RH_field:.2e} \pm {dRH_field:.2e}\ \text{{m}}^3/\text{{C}}$ |
    | **Carrier Type** | **{carrier_type_curr.upper()}** | **{carrier_type_field.upper()}** |
    | **Carrier Concentration ($n$)** | ${n_curr:.2e} \pm {dn_curr:.2e}\ \text{{m}}^{{-3}}$ | ${n_field:.2e} \pm {dn_field:.2e}\ \text{{m}}^{{-3}}$ |
    | **Resistivity ($\rho_{{xx}}$)** | ${rho_curr:.2e} \pm {drho_curr:.2e}\ \Omega\cdot\text{{m}}$ | ${rho_field:.2e} \pm {drho_field:.2e}\ \Omega\cdot\text{{m}}$ |
    | **Hall Mobility ($\mu$)** | ${mu_curr:.4f} \pm {dmu_curr:.4f}\ \text{{m}}^2/(\text{{V}}\cdot\text{{s}})$ | ${mu_field:.4f} \pm {dmu_field:.4f}\ \text{{m}}^2/(\text{{V}}\cdot\text{{s}})$ |
    """)
    return


@app.cell(hide_code=True)
def _(
    data_suffix,
    linear_model,
    load_data,
    np,
    physics_fit,
    plt,
    set_style,
    kB_eV,
):
    df_heat = load_data(f"varying_temp{data_suffix}.txt", ['T_C', 'Uh_mV', 'Up_mV'], header_exists=True)
    df_heat['T_K'] = df_heat['T_C'] + 273.15
    df_heat['inv_T'] = 1.0 / df_heat['T_K']

    Up_0 = df_heat['Up_mV'].iloc[0]
    df_heat['ln_sigma_sigma0'] = np.log(Up_0 / df_heat['Up_mV'])
    dln_sig = 1.0 * np.sqrt(1.0 / (Up_0**2) + 1.0 / (df_heat['Up_mV']**2))
    df_heat['dln_sigma'] = dln_sig

    df_high_T = df_heat[df_heat['T_C'] >= 100.0]
    fit_Eg = physics_fit(linear_model, df_high_T['inv_T'], df_high_T['ln_sigma_sigma0'], df_high_T['dln_sigma'])
    slope_Eg = fit_Eg.params[0]
    dslope_Eg = fit_Eg.errors[0]

    Eg_val = -2.0 * kB_eV * slope_Eg
    dEg_val = 2.0 * kB_eV * dslope_Eg

    # Plot using private variables
    _fig5, _ax5 = plt.subplots(figsize=(6, 4))
    x_line_heat = np.linspace(df_high_T['inv_T'].min(), df_high_T['inv_T'].max(), 100)
    _ax5.errorbar(df_heat['inv_T'], df_heat['ln_sigma_sigma0'], yerr=df_heat['dln_sigma'], fmt='o', color='#bdc3c7', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
    _ax5.errorbar(df_high_T['inv_T'], df_high_T['ln_sigma_sigma0'], yerr=df_high_T['dln_sigma'], fmt='o', color='#c0392b', markersize=4, elinewidth=1, capsize=1.5, label='Intrinsic regime ($T \geq 100^\circ$C)', zorder=4)
    _ax5.plot(x_line_heat, linear_model(x_line_heat, *fit_Eg.params), color='#c0392b', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
    set_style(ax=_ax5, xlabel='$1/T$ ($\text{K}^{-1}$)', ylabel='$\ln(\sigma/\sigma_0)$', grid=True)
    _ax5.legend(frameon=True, facecolor='white', edgecolor='none')
    _fig5.tight_layout()
    _fig5.savefig(f"graphs/ln_sigma_vs_inv_t{data_suffix}.svg", format='svg', metadata={'Date': None})
    plt.close(_fig5)

    return Eg_val, dEg_val, slope_Eg, dslope_Eg


@app.cell(hide_code=True)
def _(Eg_val, dEg_val, mo):
    mo.md(fr"""
    ### Bandgap Results
    * **Calculated Energy Gap ($E_g = -2 \cdot k_B \cdot \text{{Slope}}$):** **{Eg_val:.4f} $\pm$ {dEg_val:.4f} eV**
    """)
    return


@app.cell(hide_code=True)
def _(
    L,
    W,
    d,
    e,
    physics_fit,
    kB_eV,
    linear_model,
    load_data,
    export_constants,
    os,
    plt,
    set_style,
    np,
):
    # Batch run cell that exports all constants and graphs for BOTH P-Type and N-Type
    # This runs automatically in the background to ensure consistency with main.typ
    def run_batch_analysis_for(data_suffix):
        material_lbl = "P-Type" if data_suffix == "" else "N-Type"
        mat_lower = "p" if data_suffix == "" else "n"
        
        # 1. Zero Field Experiment
        df_zf = load_data(f"zero_field{data_suffix}.txt", ['Ip_mA', 'T_C', 'Uh_mV', 'Up_mV'])
        res_cond_init = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Ip_mA'], np.ones_like(df_zf['Ip_mA']))
        G_init = res_cond_init.params[0]
        y_err_cond = np.sqrt(1.0**2 + (G_init * 1.0)**2)
        fit_cond = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Ip_mA'], np.full_like(df_zf['Ip_mA'], y_err_cond))
        G = fit_cond.params[0]
        dG = fit_cond.errors[0]
        R_zf = 1.0 / G
        dR_zf = dG / (G**2)
        rho_zf = R_zf * W * d / L
        drho_zf = dR_zf * W * d / L
        
        res_beta_init = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Uh_mV'], np.ones_like(df_zf['Uh_mV']))
        beta_init = res_beta_init.params[0]
        y_err_beta = 1.0 * np.sqrt(1.0 + beta_init**2)
        fit_beta = physics_fit(linear_model, df_zf['Up_mV'], df_zf['Uh_mV'], np.full_like(df_zf['Uh_mV'], y_err_beta))
        beta = fit_beta.params[0]
        dbeta = fit_beta.errors[0]
        
        # Plot Zero Field
        _fig_zf, _ax_zf = plt.subplots(figsize=(6, 4))
        x_line = np.linspace(df_zf['Up_mV'].min(), df_zf['Up_mV'].max(), 100)
        _ax_zf.errorbar(df_zf['Up_mV'], df_zf['Uh_mV'], xerr=1.0, yerr=1.0, fmt='o', color='#2ecc71', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
        _ax_zf.plot(x_line, linear_model(x_line, *fit_beta.params), color='#f39c12', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
        set_style(ax=_ax_zf, xlabel='Probe Voltage $U_p$ (mV)', ylabel='Hall Voltage $U\'_H$ (mV)', grid=True)
        _ax_zf.legend(frameon=True, facecolor='white', edgecolor='none')
        _fig_zf.tight_layout()
        _fig_zf.savefig(f"graphs/uh_vs_up{data_suffix}.svg", format='svg', metadata={'Date': None})
        plt.close(_fig_zf)
        
        _fig_cond, _ax_cond = plt.subplots(figsize=(6, 4))
        _ax_cond.errorbar(df_zf['Up_mV'], df_zf['Ip_mA'], xerr=1.0, yerr=1.0, fmt='o', color='#3498db', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
        _ax_cond.plot(x_line, linear_model(x_line, *fit_cond.params), color='#e74c3c', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
        set_style(ax=_ax_cond, xlabel='Probe Voltage $U_p$ (mV)', ylabel='Sample Current $I_p$ (mA)', grid=True)
        _ax_cond.legend(frameon=True, facecolor='white', edgecolor='none')
        _fig_cond.tight_layout()
        _fig_cond.savefig(f"graphs/ip_vs_up{data_suffix}.svg", format='svg', metadata={'Date': None})
        plt.close(_fig_cond)
        
        # 2. Room Temperature - Varying Current (constant B = 301 mT)
        df_curr = load_data(f"varying_current{data_suffix}.txt", ['Ip_mA', 'T_C', 'Uh_mV', 'Up_mV'])
        dUh_curr = np.sqrt(1.0**2 + (df_curr['Up_mV'] * dbeta)**2 + (beta * 1.0)**2)
        df_curr['Uh_corr_mV'] = df_curr['Uh_mV'] - beta * df_curr['Up_mV']
        
        res_s_curr_init = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Uh_corr_mV'], dUh_curr)
        s_curr_init = res_s_curr_init.params[0]
        y_err_s_curr = np.sqrt(dUh_curr**2 + (s_curr_init * 1.0)**2)
        fit_s_curr = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Uh_corr_mV'], y_err_s_curr)
        s_curr = fit_s_curr.params[0]
        ds_curr = fit_s_curr.errors[0]
        
        B_curr = 301.0e-3  # T
        dB_curr = 1.0e-3   # T
        RH_curr = s_curr * d / B_curr
        dRH_curr = abs(RH_curr) * np.sqrt((ds_curr / s_curr)**2 + (dB_curr / B_curr)**2)
        carrier_type_curr = "p-type" if RH_curr > 0 else "n-type"
        n_curr = 1.0 / (abs(RH_curr) * e)
        dn_curr = n_curr * (dRH_curr / abs(RH_curr))
        
        res_r0_curr_init = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Up_mV'], np.ones_like(df_curr['Ip_mA']))
        r0_curr_init = res_r0_curr_init.params[0]
        y_err_r0_curr = np.sqrt(1.0**2 + (r0_curr_init * 1.0)**2)
        fit_r0_curr = physics_fit(linear_model, df_curr['Ip_mA'], df_curr['Up_mV'], np.full_like(df_curr['Ip_mA'], y_err_r0_curr))
        r0_curr = fit_r0_curr.params[0]
        dr0_curr = fit_r0_curr.errors[0]
        rho_curr = r0_curr * W * d / L
        drho_curr = dr0_curr * W * d / L
        mu_curr = abs(RH_curr) / rho_curr
        dmu_curr = mu_curr * np.sqrt((dRH_curr / RH_curr)**2 + (drho_curr / rho_curr)**2)
        
        # Plot Varying Current
        _fig_curr, _ax_curr = plt.subplots(figsize=(6, 4))
        x_line_curr = np.linspace(df_curr['Ip_mA'].min(), df_curr['Ip_mA'].max(), 100)
        _ax_curr.errorbar(df_curr['Ip_mA'], df_curr['Uh_corr_mV'], xerr=1.0, yerr=dUh_curr, fmt='o', color='#9b59b6', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
        _ax_curr.plot(x_line_curr, linear_model(x_line_curr, *fit_s_curr.params), color='#2ecc71', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
        set_style(ax=_ax_curr, xlabel='Sample Current $I_p$ (mA)', ylabel='Corrected Hall Voltage $U_H$ (mV)', grid=True)
        _ax_curr.legend(frameon=True, facecolor='white', edgecolor='none')
        _fig_curr.tight_layout()
        _fig_curr.savefig(f"graphs/uh_vs_ip_varying_current{data_suffix}.svg", format='svg', metadata={'Date': None})
        plt.close(_fig_curr)
        
        # 3. Room Temperature - Varying Field (constant Ip = 30 mA)
        df_field = load_data(f"varying_field{data_suffix}.txt", ['B_mT', 'T_C', 'Uh_mV', 'Up_mV'])
        B_T = df_field['B_mT'] / 1000.0
        dB_T = 1.0e-3 # T
        Uh_corr_V = (df_field['Uh_mV'] - beta * df_field['Up_mV']) / 1000.0
        dUh_field = np.sqrt(1.0**2 + (df_field['Up_mV'] * dbeta)**2 + (beta * 1.0)**2) / 1000.0
        
        res_s_field_init = physics_fit(linear_model, B_T, Uh_corr_V, dUh_field)
        s_field_init = res_s_field_init.params[0]
        y_err_s_field = np.sqrt(dUh_field**2 + (s_field_init * 1.0e-3)**2)
        fit_s_field = physics_fit(linear_model, B_T, Uh_corr_V, y_err_s_field)
        s_field = fit_s_field.params[0]
        ds_field = fit_s_field.errors[0]
        
        I_field = 30.0e-3  # A
        dI_field = 1.0e-3  # A
        RH_field = s_field * d / I_field
        dRH_field = abs(RH_field) * np.sqrt((ds_field / s_field)**2 + (dI_field / I_field)**2)
        carrier_type_field = "p-type" if RH_field > 0 else "n-type"
        n_field = 1.0 / (abs(RH_field) * e)
        dn_field = n_field * (dRH_field / abs(RH_field))
        
        mean_Up_V = df_field['Up_mV'].mean() / 1000.0
        dmean_Up_V = 0.001
        r0_field = mean_Up_V / I_field
        dr0_field = r0_field * np.sqrt((dmean_Up_V / mean_Up_V)**2 + (dI_field / I_field)**2)
        rho_field = r0_field * W * d / L
        drho_field = dr0_field * W * d / L
        mu_field = abs(RH_field) / rho_field
        dmu_field = mu_field * np.sqrt((dRH_field / RH_field)**2 + (drho_field / rho_field)**2)
        
        # Plot Varying Field
        _fig_field, _ax_field = plt.subplots(figsize=(6, 4))
        x_line_field = np.linspace(B_T.min(), B_T.max(), 100)
        _ax_field.errorbar(B_T, Uh_corr_V, xerr=dB_T, yerr=dUh_field, fmt='o', color='#e67e22', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
        _ax_field.plot(x_line_field, linear_model(x_line_field, *fit_s_field.params), color='#34495e', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
        set_style(ax=_ax_field, xlabel='Magnetic Field $B$ (T)', ylabel='Corrected Hall Voltage $U_H$ (V)', grid=True)
        _ax_field.legend(frameon=True, facecolor='white', edgecolor='none')
        _fig_field.tight_layout()
        _fig_field.savefig(f"graphs/uh_vs_b_varying_field{data_suffix}.svg", format='svg', metadata={'Date': None})
        plt.close(_fig_field)
        
        # 4. Bandgap energy
        df_heat = load_data(f"varying_temp{data_suffix}.txt", ['T_C', 'Uh_mV', 'Up_mV'], header_exists=True)
        df_heat['T_K'] = df_heat['T_C'] + 273.15
        df_heat['inv_T'] = 1.0 / df_heat['T_K']
        Up_0 = df_heat['Up_mV'].iloc[0]
        df_heat['ln_sigma_sigma0'] = np.log(Up_0 / df_heat['Up_mV'])
        dln_sig = 1.0 * np.sqrt(1.0 / (Up_0**2) + 1.0 / (df_heat['Up_mV']**2))
        df_heat['dln_sigma'] = dln_sig
        
        df_high_T = df_heat[df_heat['T_C'] >= 100.0]
        fit_Eg = physics_fit(linear_model, df_high_T['inv_T'], df_high_T['ln_sigma_sigma0'], df_high_T['dln_sigma'])
        slope_Eg = fit_Eg.params[0]
        dslope_Eg = fit_Eg.errors[0]
        Eg_val = -2.0 * kB_eV * slope_Eg
        dEg_val = 2.0 * kB_eV * dslope_Eg
        
        # Plot Bandgap
        _fig_heat, _ax_heat = plt.subplots(figsize=(6, 4))
        x_line_heat = np.linspace(df_high_T['inv_T'].min(), df_high_T['inv_T'].max(), 100)
        _ax_heat.errorbar(df_heat['inv_T'], df_heat['ln_sigma_sigma0'], yerr=df_heat['dln_sigma'], fmt='o', color='#bdc3c7', markersize=4, elinewidth=1, capsize=1.5, label='Data points', zorder=3)
        _ax_heat.errorbar(df_high_T['inv_T'], df_high_T['ln_sigma_sigma0'], yerr=df_high_T['dln_sigma'], fmt='o', color='#c0392b', markersize=4, elinewidth=1, capsize=1.5, label='Intrinsic regime ($T \geq 100^\circ$C)', zorder=4)
        _ax_heat.plot(x_line_heat, linear_model(x_line_heat, *fit_Eg.params), color='#c0392b', linewidth=1.5, linestyle='--', label='Fit', zorder=5)
        set_style(ax=_ax_heat, xlabel='$1/T$ ($\text{K}^{-1}$)', ylabel='$\ln(\sigma/\sigma_0)$', grid=True)
        _ax_heat.legend(frameon=True, facecolor='white', edgecolor='none')
        _fig_heat.tight_layout()
        _fig_heat.savefig(f"graphs/ln_sigma_vs_inv_t{data_suffix}.svg", format='svg', metadata={'Date': None})
        plt.close(_fig_heat)
        
        results = [
            {"hebrew_name": f"התנגדות אפס שדה ({material_lbl})", "english_name": f"Zero Field Resistance ({material_lbl})", "hebrew_var": f"R_zf_{mat_lower}", "english_var": f"R_zf_{mat_lower}", "symbol": f"R_(\"zf\", {mat_lower})", "value": R_zf, "error": dR_zf, "units": "Omega", "fmt_spec": ".3f"},
            {"hebrew_name": f"התנגדות סגולית אפס שדה ({material_lbl})", "english_name": f"Zero Field Resistivity ({material_lbl})", "hebrew_var": f"rho_zf_{mat_lower}", "english_var": f"rho_zf_{mat_lower}", "symbol": f"rho_(\"zf\", {mat_lower})", "value": rho_zf, "error": drho_zf, "units": "Omega * \"m\"", "scale": 1.0, "fmt_spec": ".5e"},
            {"hebrew_name": f"פרמטר אי-תיאום ({material_lbl})", "english_name": f"Misalignment Parameter ({material_lbl})", "hebrew_var": f"beta_{mat_lower}", "english_var": f"beta_{mat_lower}", "symbol": f"beta_{mat_lower}", "value": beta, "error": dbeta, "units": "", "fmt_spec": ".5f"},
            
            {"hebrew_name": f"שיפוע מתח הול זרם ({material_lbl})", "english_name": f"Hall Voltage Current Slope ({material_lbl})", "hebrew_var": f"s_curr_{mat_lower}", "english_var": f"s_curr_{mat_lower}", "symbol": f"S_(\"H,I\", {mat_lower})", "value": s_curr, "error": ds_curr, "units": "Omega", "fmt_spec": ".4f"},
            {"hebrew_name": f"קבוע הול מזרם משתנה ({material_lbl})", "english_name": f"Hall Coefficient from Current ({material_lbl})", "hebrew_var": f"RH_curr_{mat_lower}", "english_var": f"RH_curr_{mat_lower}", "symbol": f"R_(\"H,I\", {mat_lower})", "value": RH_curr, "error": dRH_curr, "units": "\"m\"^3 / \"C\"", "fmt_spec": ".2e"},
            {"hebrew_name": f"ריכוז נושאי מטען מזרם ({material_lbl})", "english_name": f"Carrier Concentration from Current ({material_lbl})", "hebrew_var": f"n_curr_{mat_lower}", "english_var": f"n_curr_{mat_lower}", "symbol": f"n_(\"I\", {mat_lower})", "value": n_curr, "error": dn_curr, "units": "\"m\"^(-3)", "fmt_spec": ".2e"},
            {"hebrew_name": f"התנגדות סגולית מזרם ({material_lbl})", "english_name": f"Resistivity from Current ({material_lbl})", "hebrew_var": f"rho_curr_{mat_lower}", "english_var": f"rho_curr_{mat_lower}", "symbol": f"rho_(\"I\", {mat_lower})", "value": rho_curr, "error": drho_curr, "units": "Omega * \"m\"", "fmt_spec": ".5e"},
            {"hebrew_name": f"מוביליות הול מזרם ({material_lbl})", "english_name": f"Hall Mobility from Current ({material_lbl})", "hebrew_var": f"mu_curr_{mat_lower}", "english_var": f"mu_curr_{mat_lower}", "symbol": f"mu_(\"I\", {mat_lower})", "value": mu_curr, "error": dmu_curr, "units": "\"m\"^2 / (\"V\" * sec)", "fmt_spec": ".4f"},
            
            {"hebrew_name": f"שיפוע מתח הול שדה ({material_lbl})", "english_name": f"Hall Voltage Field Slope ({material_lbl})", "hebrew_var": f"s_field_{mat_lower}", "english_var": f"s_field_{mat_lower}", "symbol": f"S_(\"H,B\", {mat_lower})", "value": s_field, "error": ds_field, "units": "\"V\"/\"T\"", "fmt_spec": ".4f"},
            {"hebrew_name": f"קבוע הול משדה משתנה ({material_lbl})", "english_name": f"Hall Coefficient from Field ({material_lbl})", "hebrew_var": f"RH_field_{mat_lower}", "english_var": f"RH_field_{mat_lower}", "symbol": f"R_(\"H,B\", {mat_lower})", "value": RH_field, "error": dRH_field, "units": "\"m\"^3 / \"C\"", "fmt_spec": ".2e"},
            {"hebrew_name": f"ריכוז נושאי מטען משדה ({material_lbl})", "english_name": f"Carrier Concentration from Field ({material_lbl})", "hebrew_var": f"n_field_{mat_lower}", "english_var": f"n_field_{mat_lower}", "symbol": f"n_(\"B\", {mat_lower})", "value": n_field, "error": dn_field, "units": "\"m\"^(-3)", "fmt_spec": ".2e"},
            {"hebrew_name": f"התנגדות סגולית משדה ({material_lbl})", "english_name": f"Resistivity from Field ({material_lbl})", "hebrew_var": f"rho_field_{mat_lower}", "english_var": f"rho_field_{mat_lower}", "symbol": f"rho_(\"B\", {mat_lower})", "value": rho_field, "error": drho_field, "units": "Omega * \"m\"", "fmt_spec": ".5e"},
            {"hebrew_name": f"מוביליות הול משדה ({material_lbl})", "english_name": f"Hall Mobility from Field ({material_lbl})", "hebrew_var": f"mu_field_{mat_lower}", "english_var": f"mu_field_{mat_lower}", "symbol": f"mu_(\"B\", {mat_lower})", "value": mu_field, "error": dmu_field, "units": "\"m\"^2 / (\"V\" * sec)", "fmt_spec": ".4f"},
            
            {"hebrew_name": f"פער אנרגיה ({material_lbl})", "english_name": f"Bandgap Energy ({material_lbl})", "hebrew_var": f"Eg_{mat_lower}", "english_var": f"Eg_{mat_lower}", "symbol": f"E_(\"g\", {mat_lower})", "value": Eg_val, "error": dEg_val, "units": "\"eV\"", "fmt_spec": ".4f"}
        ]
        return results

    # Run for both and export constants
    os.makedirs("graphs", exist_ok=True)
    os.makedirs("constants", exist_ok=True)
    res_p = run_batch_analysis_for("")
    res_n = run_batch_analysis_for("_n_type")
    export_constants(res_p + res_n, "constants")
    return (run_batch_analysis_for,)


if __name__ == "__main__":
    app.run()
