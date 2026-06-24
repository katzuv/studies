# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib>=3.11.0",
#     "numpy>=2.5.0",
#     "pandas>=3.0.3",
#     "scipy>=1.18.0",
# ]
# ///
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Force UTF-8 on Windows command lines if possible
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        fallback_chars = {
            "╔": "+", "═": "-", "╗": "+", "╠": "+", "╦": "-", "╬": "+", "╣": "+",
            "║": "|", "╫": "+", "╩": "-", "╝": "+", "─": "-", "╟": "+", "╢": "+",
            "Ω": "Ohm", "ρ": "rho", "β": "beta", "μ": "mu", "·": "*", "³": "^3",
            "⁻": "-", "²": "^2", "±": "+/-", "×": "x", "°": "deg", "π": "pi",
            "⁻³": "^-3"
        }
        fallback_text = "".join(fallback_chars.get(c, c) for c in text)
        print(fallback_text)

# Constants
d = 1.0e-3     # Sample thickness (m)
W = 10.0e-3    # Sample width (m)
L = 16.0e-3    # Sample length (m)
e_charge = 1.602176634e-19  # Elementary charge (C)
kB_eV = 8.617333262e-5      # Boltzmann constant (eV/K)

def linear_model(x, a, b):
    return a * x + b

def run_fit(x, y, y_err):
    popt, pcov = curve_fit(linear_model, x, y, sigma=y_err, absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

def calc_r2(x, y, popt):
    residuals = y - linear_model(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1.0 - ss_res / ss_tot if ss_tot != 0 else 1.0

# Graph Styling helper (Clean publication style, pure white background)
def apply_plot_style(ax, xlabel, ylabel, grid=True):
    ax.set_facecolor("#ffffff")
    if grid:
        ax.grid(True, which="both", color="#cccccc", linestyle="--", linewidth=0.7)
    ax.set_xlabel(xlabel, fontsize=12, labelpad=8)
    ax.set_ylabel(ylabel, fontsize=12, labelpad=8)
    ax.tick_params(axis="both", which="major", labelsize=10)
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_linewidth(1.2)
        ax.spines[spine].set_color("#333333")

def run_analysis(data_suffix, material_name):
    # Load zero field data
    df_zf = pd.read_csv(f"data/zero_field{data_suffix}.txt", sep=r"\s+", comment="#", names=["Ip_mA", "T_C", "Uh_mV", "Up_mV"])
    
    # 1. Conductance fit: Ip (mA) = G * Up (mV) + intercept
    # Step 1: Initial fit to estimate scale of errors
    popt_cond_init, _ = run_fit(df_zf["Up_mV"], df_zf["Ip_mA"], np.ones_like(df_zf["Ip_mA"]))
    y_err_cond = np.sqrt(1.0**2 + (popt_cond_init[0] * 1.0)**2)
    popt_cond, perr_cond = run_fit(df_zf["Up_mV"], df_zf["Ip_mA"], np.full_like(df_zf["Ip_mA"], y_err_cond))
    
    G = popt_cond[0]
    dG = perr_cond[0]
    R_zf = 1.0 / G
    dR_zf = dG / (G**2)
    rho_zf = R_zf * W * d / L
    drho_zf = dR_zf * W * d / L
    
    # 2. Misalignment fit: Uh_mV = beta * Up_mV + intercept
    popt_beta_init, _ = run_fit(df_zf["Up_mV"], df_zf["Uh_mV"], np.ones_like(df_zf["Uh_mV"]))
    y_err_beta = np.sqrt(1.0**2 + popt_beta_init[0]**2)
    popt_beta, perr_beta = run_fit(df_zf["Up_mV"], df_zf["Uh_mV"], np.full_like(df_zf["Uh_mV"], y_err_beta))
    beta = popt_beta[0]
    dbeta = perr_beta[0]
    
    # Plots for zero field
    fig, ax = plt.subplots(figsize=(6, 4))
    x_line = np.linspace(df_zf["Up_mV"].min(), df_zf["Up_mV"].max(), 100)
    ax.errorbar(df_zf["Up_mV"], df_zf["Uh_mV"], xerr=1.0, yerr=1.0, fmt="o", color="#2ecc71", label="Data")
    ax.plot(x_line, linear_model(x_line, *popt_beta), color="#f39c12", linestyle="--", label="Fit")
    apply_plot_style(ax, "Probe Voltage $U_p$ (mV)", "Hall Voltage $U'_H$ (mV)")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(f"graphs/uh_vs_up{data_suffix}.svg")
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(df_zf["Up_mV"], df_zf["Ip_mA"], xerr=1.0, yerr=1.0, fmt="o", color="#3498db", label="Data")
    ax.plot(x_line, linear_model(x_line, *popt_cond), color="#e74c3c", linestyle="--", label="Fit")
    apply_plot_style(ax, "Probe Voltage $U_p$ (mV)", "Sample Current $I_p$ (mA)")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(f"graphs/ip_vs_up{data_suffix}.svg")
    plt.close(fig)
    
    # 3. Room Temperature - Varying Current (constant B = 301 mT)
    df_curr = pd.read_csv(f"data/varying_current{data_suffix}.txt", sep=r"\s+", comment="#", names=["Ip_mA", "T_C", "Uh_mV", "Up_mV"])
    dUh_curr = np.sqrt(1.0**2 + (df_curr["Up_mV"] * dbeta)**2 + (beta * 1.0)**2)
    df_curr["Uh_corr_mV"] = df_curr["Uh_mV"] - beta * df_curr["Up_mV"]
    
    popt_curr_init, _ = run_fit(df_curr["Ip_mA"], df_curr["Uh_corr_mV"], dUh_curr)
    y_err_s_curr = np.sqrt(dUh_curr**2 + (popt_curr_init[0] * 1.0)**2)
    popt_curr, perr_curr = run_fit(df_curr["Ip_mA"], df_curr["Uh_corr_mV"], y_err_s_curr)
    
    s_curr = popt_curr[0]
    ds_curr = perr_curr[0]
    B_curr = 301.0e-3
    dB_curr = 1.0e-3
    RH_curr = s_curr * d / B_curr
    dRH_curr = abs(RH_curr) * np.sqrt((ds_curr / s_curr)**2 + (dB_curr / B_curr)**2)
    n_curr = 1.0 / (abs(RH_curr) * e_charge)
    dn_curr = n_curr * (dRH_curr / abs(RH_curr))
    
    popt_r0_init, _ = run_fit(df_curr["Ip_mA"], df_curr["Up_mV"], np.ones_like(df_curr["Ip_mA"]))
    y_err_r0_curr = np.sqrt(1.0**2 + (popt_r0_init[0] * 1.0)**2)
    popt_r0, perr_r0 = run_fit(df_curr["Ip_mA"], df_curr["Up_mV"], np.full_like(df_curr["Ip_mA"], y_err_r0_curr))
    r0_curr = popt_r0[0]
    dr0_curr = perr_r0[0]
    rho_curr = r0_curr * W * d / L
    drho_curr = dr0_curr * W * d / L
    mu_curr = abs(RH_curr) / rho_curr
    dmu_curr = mu_curr * np.sqrt((dRH_curr / RH_curr)**2 + (drho_curr / rho_curr)**2)
    
    # 4. Room Temperature - Varying Field (constant Ip = 30 mA)
    df_field = pd.read_csv(f"data/varying_field{data_suffix}.txt", sep=r"\s+", comment="#", names=["B_mT", "T_C", "Uh_mV", "Up_mV"])
    dUh_field = np.sqrt(1.0**2 + (df_field["Up_mV"] * dbeta)**2 + (beta * 1.0)**2) / 1000.0
    B_T = df_field["B_mT"] / 1000.0
    dB_T = 1.0e-3
    Uh_corr_V = (df_field["Uh_mV"] - beta * df_field["Up_mV"]) / 1000.0
    
    popt_field_init, _ = run_fit(B_T, Uh_corr_V, dUh_field)
    y_err_s_field = np.sqrt(dUh_field**2 + (popt_field_init[0] * 1.0e-3)**2)
    popt_field, perr_field = run_fit(B_T, Uh_corr_V, y_err_s_field)
    s_field = popt_field[0]
    ds_field = perr_field[0]
    I_field = 30.0e-3
    dI_field = 1.0e-3
    RH_field = s_field * d / I_field
    dRH_field = abs(RH_field) * np.sqrt((ds_field / s_field)**2 + (dI_field / I_field)**2)
    n_field = 1.0 / (abs(RH_field) * e_charge)
    dn_field = n_field * (dRH_field / abs(RH_field))
    
    mean_Up_V = df_field["Up_mV"].mean() / 1000.0
    dmean_Up_V = 0.001
    r0_field = mean_Up_V / I_field
    dr0_field = r0_field * np.sqrt((dmean_Up_V / mean_Up_V)**2 + (dI_field / I_field)**2)
    rho_field = r0_field * W * d / L
    drho_field = dr0_field * W * d / L
    mu_field = abs(RH_field) / rho_field
    dmu_field = mu_field * np.sqrt((dRH_field / RH_field)**2 + (drho_field / rho_field)**2)
    
    # Save room temp plots
    fig, ax = plt.subplots(figsize=(6, 4))
    x_line_curr = np.linspace(df_curr["Ip_mA"].min(), df_curr["Ip_mA"].max(), 100)
    ax.errorbar(df_curr["Ip_mA"], df_curr["Uh_corr_mV"], xerr=1.0, yerr=dUh_curr, fmt="o", color="#9b59b6", label="Data")
    ax.plot(x_line_curr, linear_model(x_line_curr, *popt_curr), color="#2ecc71", linestyle="--", label="Fit")
    apply_plot_style(ax, "Sample Current $I_p$ (mA)", "Corrected Hall Voltage $U_H$ (mV)")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(f"graphs/uh_vs_ip_varying_current{data_suffix}.svg")
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    x_line_field = np.linspace(B_T.min(), B_T.max(), 100)
    ax.errorbar(B_T, Uh_corr_V, xerr=dB_T, yerr=dUh_field, fmt="o", color="#e67e22", label="Data")
    ax.plot(x_line_field, linear_model(x_line_field, *popt_field), color="#34495e", linestyle="--", label="Fit")
    apply_plot_style(ax, "Magnetic Field $B$ (T)", "Corrected Hall Voltage $U_H$ (V)")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(f"graphs/uh_vs_b_varying_field{data_suffix}.svg")
    plt.close(fig)
    
    # 5. Heating/Cooling Experiment for Energy Gap Eg
    df_heat = pd.read_csv(f"data/varying_temp{data_suffix}.txt", sep=r"\s+", comment="#")
    df_heat.columns = ["T_C", "Uh_mV", "Up_mV"]
    df_heat["T_K"] = df_heat["T_C"] + 273.15
    df_heat["inv_T"] = 1.0 / df_heat["T_K"]
    df_heat["Uh_corr_mV"] = df_heat["Uh_mV"] - beta * df_heat["Up_mV"]
    
    Up_0 = df_heat["Up_mV"].iloc[0]
    df_heat["ln_sigma_sigma0"] = np.log(Up_0 / df_heat["Up_mV"])
    df_heat["dln_sigma"] = 1.0 * np.sqrt(1.0 / (Up_0**2) + 1.0 / (df_heat["Up_mV"]**2))
    
    df_high_T = df_heat[df_heat["T_C"] >= 100.0]
    popt_Eg, perr_Eg = run_fit(df_high_T["inv_T"], df_high_T["ln_sigma_sigma0"], df_high_T["dln_sigma"])
    slope_Eg = popt_Eg[0]
    dslope_Eg = perr_Eg[0]
    
    Eg = -2.0 * kB_eV * slope_Eg
    dEg = 2.0 * kB_eV * dslope_Eg
    
    # Plot heating curve
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(df_heat["inv_T"], df_heat["ln_sigma_sigma0"], yerr=df_heat["dln_sigma"], fmt="o", color="#bdc3c7", label="Full data")
    ax.errorbar(df_high_T["inv_T"], df_high_T["ln_sigma_sigma0"], yerr=df_high_T["dln_sigma"], fmt="o", color="#c0392b", label="Intrinsic regime ($T \\geq 100^\\circ$C)")
    x_line_heat = np.linspace(df_high_T["inv_T"].min(), df_high_T["inv_T"].max(), 100)
    ax.plot(x_line_heat, linear_model(x_line_heat, *popt_Eg), color="#c0392b", linestyle="--", label="Fit")
    apply_plot_style(ax, "$1/T$ (K$^{-1}$)", "$\\ln(\\sigma/\\sigma_0)$")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(f"graphs/ln_sigma_vs_inv_t{data_suffix}.svg")
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df_heat["T_C"], df_heat["Uh_corr_mV"], color="#c0392b" if data_suffix == "" else "#2980b9", linewidth=2, label="Corrected $U_H$")
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
    apply_plot_style(ax, "Temperature $T$ ($^\\circ$C)", "Corrected Hall Voltage $U_H$ (mV)")
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(f"graphs/uh_vs_temp{data_suffix}.svg")
    plt.close(fig)
    
    return {
        "R_zf": R_zf, "dR_zf": dR_zf,
        "rho_zf": rho_zf, "drho_zf": drho_zf,
        "beta": beta, "dbeta": dbeta,
        "RH_curr": RH_curr, "dRH_curr": dRH_curr,
        "n_curr": n_curr, "dn_curr": dn_curr,
        "rho_curr": rho_curr, "drho_curr": drho_curr,
        "mu_curr": mu_curr, "dmu_curr": dmu_curr,
        "RH_field": RH_field, "dRH_field": dRH_field,
        "n_field": n_field, "dn_field": dn_field,
        "rho_field": rho_field, "drho_field": drho_field,
        "mu_field": mu_field, "dmu_field": dmu_field,
        "Eg": Eg, "dEg": dEg
    }

def main():
    os.makedirs("graphs", exist_ok=True)
    
    safe_print("\033[1;36mRunning data analysis for Germanium samples...\033[0m")
    res_p = run_analysis("", "P-Type")
    res_n = run_analysis("_n_type", "N-Type")
    
    fmt_sci = lambda val, err: f"({val/10**int(np.floor(np.log10(abs(val)))):.4f} \u00b1 {err/10**int(np.floor(np.log10(abs(val)))):.4f})\u00d710^{int(np.floor(np.log10(abs(val))))}"
    fmt_std = lambda val, err, p=4: f"{val:.{p}f} \u00b1 {err:.{p}f}"
    
    # Beautiful table with unicode box-drawing characters and ANSI colors
    title = "PHYSICAL CONSTANTS AND PARAMETERS SUMMARY"
    safe_print("\n\033[90m╔" + "═"*94 + "╗\033[0m")
    safe_print(f"\033[90m║\033[0m{title:^94}\033[90m║\033[0m")
    safe_print("\033[90m╠" + "═"*38 + "╦" + "═"*27 + "╦" + "═"*27 + "╣\033[0m")
    
    hdr_param = f"{'Parameter':<36}"
    hdr_p = f"{'P-Type (Error)':<25}"
    hdr_n = f"{'N-Type (Error)':<25}"
    safe_print(f"\033[90m║\033[0m \033[1;33m{hdr_param}\033[0m \033[90m║\033[0m \033[1;33m{hdr_p}\033[0m \033[90m║\033[0m \033[1;33m{hdr_n}\033[0m \033[90m║\033[0m")
    safe_print("\033[90m╠" + "═"*38 + "╬" + "═"*27 + "╬" + "═"*27 + "╣\033[0m")
    
    def print_row(param, val_p, val_n):
        safe_print(f"\033[90m║\033[0m {param:<36} \033[90m║\033[0m {val_p:<25} \033[90m║\033[0m {val_n:<25} \033[90m║\033[0m")
        
    print_row("Zero-Field Resistance R [\u03a9]", fmt_std(res_p['R_zf'], res_p['dR_zf'], 3), fmt_std(res_n['R_zf'], res_n['dR_zf'], 3))
    print_row("Zero-Field Resistivity \u03c1 [\u03a9\u00b7m]", fmt_sci(res_p['rho_zf'], res_p['drho_zf']), fmt_sci(res_n['rho_zf'], res_n['drho_zf']))
    print_row("Misalignment Parameter \u03b2", fmt_std(res_p['beta'], res_p['dbeta'], 5), fmt_std(res_n['beta'], res_n['dbeta'], 5))
    
    safe_print("\033[90m╠" + "─"*38 + "╫" + "─"*27 + "╫" + "─"*27 + "╣\033[0m")
    
    print_row("RH (Varying Current) [m\u00b3/C]", fmt_sci(res_p['RH_curr'], res_p['dRH_curr']), fmt_sci(res_n['RH_curr'], res_n['dRH_curr']))
    print_row("RH (Varying Field) [m\u00b3/C]", fmt_sci(res_p['RH_field'], res_p['dRH_field']), fmt_sci(res_n['RH_field'], res_n['dRH_field']))
    print_row("Carrier Conc. n (Current) [m\u207b\u00b3]", fmt_sci(res_p['n_curr'], res_p['dn_curr']), fmt_sci(res_n['n_curr'], res_n['dn_curr']))
    print_row("Carrier Conc. n (Field) [m\u207b\u00b3]", fmt_sci(res_p['n_field'], res_p['dn_field']), fmt_sci(res_n['n_field'], res_n['dn_field']))
    print_row("Resistivity \u03c1 (Current) [\u03a9\u00b7m]", fmt_sci(res_p['rho_curr'], res_p['drho_curr']), fmt_sci(res_n['rho_curr'], res_n['drho_curr']))
    print_row("Resistivity \u03c1 (Field) [\u03a9\u00b7m]", fmt_sci(res_p['rho_field'], res_p['drho_field']), fmt_sci(res_n['rho_field'], res_n['drho_field']))
    print_row("Mobility \u03bc (Current) [m\u00b2/(V\u00b7sec)]", fmt_std(res_p['mu_curr'], res_p['dmu_curr'], 4), fmt_std(res_n['mu_curr'], res_n['dmu_curr'], 4))
    print_row("Mobility \u03bc (Field) [m\u00b2/(V\u00b7sec)]", fmt_std(res_p['mu_field'], res_p['dmu_field'], 4), fmt_std(res_n['mu_field'], res_n['dmu_field'], 4))
    
    safe_print("\033[90m╠" + "─"*38 + "╫" + "─"*27 + "╫" + "─"*27 + "╣\033[0m")
    
    print_row("Energy Gap Eg [eV]", fmt_std(res_p['Eg'], res_p['dEg'], 4), fmt_std(res_n['Eg'], res_n['dEg'], 4))
    safe_print("\033[90m╚" + "═"*38 + "╩" + "═"*27 + "╩" + "═"*27 + "╝\033[0m")
    
    safe_print("\n\033[1;32mAll SVG graphs have been saved to the 'graphs/' directory.\033[0m")

if __name__ == "__main__":
    main()
