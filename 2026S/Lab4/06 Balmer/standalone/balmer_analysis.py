#!/usr/bin/env python3
# /// script
# dependencies = [
#     "matplotlib",
#     "numpy",
#     "pandas",
#     "scipy"
# ]
# ///
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt

# Make SVG generation deterministic
plt.rcParams["svg.hashsalt"] = "fixed-string"

def propagate_error(func, params, errors):
    eps = 1e-6
    grad = []
    for i in range(len(params)):
        p_plus = list(params)
        p_minus = list(params)
        p_plus[i] += eps
        p_minus[i] -= eps
        grad.append((func(*p_plus) - func(*p_minus)) / (2.0 * eps))
    variance = sum((g * err) ** 2 for g, err in zip(grad, errors, strict=True))
    return np.sqrt(variance)

class FitResult:
    def __init__(self, params, errors, chi_red):
        self.params = params
        self.errors = errors
        self.chi_red = chi_red

def physics_fit(model, x, y, dy):
    popt, pcov = opt.curve_fit(model, x, y, sigma=dy, absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))
    residuals = y - model(x, *popt)
    chi_red = np.sum((residuals / dy) ** 2) / (len(x) - len(popt))
    return FitResult(popt, perr, chi_red)

def set_style(ax, xlabel="", ylabel=""):
    ax.spines["top"].set_linewidth(1.5)
    ax.spines["right"].set_linewidth(1.5)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
    ax.tick_params(direction="in", top=True, right=True, width=1.5)
    ax.grid(True, linestyle=":", alpha=0.6)

def cauchy_model(lam, A, B):
    return A + B / (lam**2)

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    os.makedirs("graphs", exist_ok=True)
    
    # 1. Load Data
    he_df = pd.read_csv("data/helium_prism.txt", sep=r"\s+", comment="#", names=["lambda", "beta", "dbeta"])
    hg_df = pd.read_csv("data/mercury_prism.txt", sep=r"\s+", comment="#", names=["lambda", "beta", "dbeta"])
    hp_df = pd.read_csv("data/hydrogen_prism.txt", sep=r"\s+", comment="#", names=["line_id", "color", "literature_wavelength", "beta", "dbeta"])
    hg_grating_df = pd.read_csv("data/hydrogen_grating.txt", sep=r"\s+", comment="#", names=["line_id", "color", "literature_wavelength", "order", "beta_plus", "beta_minus", "dbeta"])

    alpha = 60.0
    alpha_rad = np.radians(alpha)

    # 2. Helium Calibration Calculation
    he_ns = np.sin((alpha_rad + np.radians(he_df["beta"])) / 2.0) / np.sin(alpha_rad / 2.0)
    he_dns = (
        np.cos((alpha_rad + np.radians(he_df["beta"])) / 2.0)
        / (2.0 * np.sin(alpha_rad / 2.0))
    ) * np.radians(he_df["dbeta"])

    # Fit Cauchy formula
    fit_res = physics_fit(cauchy_model, he_df["lambda"].to_numpy(), he_ns.to_numpy(), he_dns.to_numpy())
    A_fit, B_fit = fit_res.params
    dA_fit, dB_fit = fit_res.errors
    chi_red = fit_res.chi_red

    # R^2 calculation
    fit_y = cauchy_model(he_df["lambda"].to_numpy(), A_fit, B_fit)
    ss_res = np.sum((he_ns - fit_y)**2)
    ss_tot = np.sum((he_ns - np.mean(he_ns))**2)
    r_sq = 1.0 - (ss_res / ss_tot)
    
    stats_text = (
        f"$R^2 = {r_sq:.3f}$\n"
        f"$\\chi^2_\\mathrm{{red}} = {chi_red:.3f}$"
    )

    # Mapping to display colors
    he_colors = {
        707: "Red", 706: "Red", 668: "Red", 667: "Red",
        588: "Yellow", 587: "Yellow", 501: "Green",
        492: "Blue-Green", 472: "Blue", 471: "Blue",
        448: "Blue", 447: "Blue"
    }
    display_colors = {
        "Red": "#D32F2F",
        "Yellow": "#C48400",
        "Green": "#388E3C",
        "Blue-Green": "#0097A7",
        "Blue": "#1976D2"
    }

    # 2.1 Plot n vs lambda
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.errorbar(he_df["lambda"], he_ns, yerr=he_dns, fmt="none", ecolor="gray", capsize=3, zorder=1)
    for lam, n_val in zip(he_df["lambda"], he_ns, strict=True):
        name = he_colors.get(int(round(lam)), "gray")
        dot_color = display_colors.get(name, "gray")
        ax1.scatter(lam, n_val, color=dot_color, edgecolors="black", s=60, zorder=2)
        
        if name == "Green":
            x_pos = lam + 7
            ha_align = "left"
        elif name in ("Blue-Green", "Blue"):
            x_pos = lam - 7
            ha_align = "right"
        else:
            x_pos = lam
            ha_align = "center"

        y_pos = n_val
        if ha_align == "center":
            y_pos += 0.0008
            va_align = "bottom"
        else:
            va_align = "center"

        ax1.text(x_pos, y_pos, name, fontsize=8, color=dot_color, fontweight="bold", ha=ha_align, va=va_align)

    l_grid = np.linspace(400, 750, 200)
    ax1.plot(l_grid, cauchy_model(l_grid, A_fit, B_fit), color="#C73E1D", label="Cauchy Fit", zorder=1)
    set_style(ax1, xlabel=r"$\lambda \ \text{[nm]}$", ylabel=r"Refractive Index $n$")
    ax1.set_ylim(min(he_ns) - 0.005, max(he_ns) + 0.005)
    ax1.legend()
    ax1.text(0.95, 0.85, stats_text, transform=ax1.transAxes, va="top", ha="right",
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    plt.tight_layout()
    fig1.savefig("graphs/helium_dispersion.svg", format="svg")
    plt.close(fig1)

    # 2.2 Linearized Plot (n vs 1/lambda^2)
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    inv_lam_sq = 1.0 / (he_df["lambda"]**2)
    inv_lam_sq_grid = 1.0 / (l_grid**2)

    ax2.errorbar(inv_lam_sq * 1e6, he_ns, yerr=he_dns, fmt="none", ecolor="gray", capsize=3, zorder=1)
    for lam, inv_lam_val, _n_val in zip(he_df["lambda"], inv_lam_sq, he_ns, strict=True):
        name = he_colors.get(int(round(lam)), "gray")
        dot_color = display_colors.get(name, "gray")
        ax2.scatter(inv_lam_val * 1e6, _n_val, color=dot_color, edgecolors="black", s=60, zorder=2)
        
        if name == "Green":
            x_pos = inv_lam_val * 1e6 - 0.06
            ha_align = "right"
        elif name in ("Blue-Green", "Blue"):
            x_pos = inv_lam_val * 1e6 + 0.06
            ha_align = "left"
        else:
            x_pos = inv_lam_val * 1e6
            ha_align = "center"

        y_pos = _n_val
        if ha_align == "center":
            y_pos += 0.0008
            va_align = "bottom"
        else:
            va_align = "center"

        ax2.text(x_pos, y_pos, name, fontsize=8, color=dot_color, fontweight="bold", ha=ha_align, va=va_align)

    ax2.plot(inv_lam_sq_grid * 1e6, A_fit + B_fit * inv_lam_sq_grid, color="#C73E1D", label="Linear Cauchy Fit", zorder=1)
    set_style(ax2, xlabel=r"$1/\lambda^2 \ [10^{-6} \ \text{nm}^{-2}]$", ylabel=r"Refractive Index $n$")
    ax2.set_ylim(min(he_ns) - 0.005, max(he_ns) + 0.005)
    ax2.set_xlim(left=(1.0 / (750.0**2)) * 1e6)
    ax2.legend()
    ax2.text(0.05, 0.95, stats_text, transform=ax2.transAxes, va="top", ha="left",
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    plt.tight_layout()
    fig2.savefig("graphs/helium_linearized.svg", format="svg")
    plt.close(fig2)

    # 2.3 Residuals Plot
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    residuals = he_ns - cauchy_model(he_df["lambda"].to_numpy(), A_fit, B_fit)
    ax3.errorbar(he_df["lambda"], residuals, yerr=he_dns, fmt="o", color="#A23B72", capsize=3)
    ax3.axhline(0, color="gray", linestyle="--")
    set_style(ax3, xlabel=r"$\lambda \ \text{[nm]}$", ylabel=r"Residuals $n - n_{\text{fit}}$")
    plt.tight_layout()
    fig3.savefig("graphs/helium_residuals.svg", format="svg")
    plt.close(fig3)

    # 3. Mercury Green Line Verification
    hg_row = hg_df.iloc[0]
    beta_hg = hg_row["beta"]
    dbeta_hg = hg_row["dbeta"]
    n_hg = np.sin((alpha_rad + np.radians(beta_hg)) / 2.0) / np.sin(alpha_rad / 2.0)
    dn_hg = (
        np.cos((alpha_rad + np.radians(beta_hg)) / 2.0)
        / (2.0 * np.sin(alpha_rad / 2.0))
    ) * np.radians(dbeta_hg)

    def get_lam(A_p, B_p, n_v):
        return np.sqrt(B_p / (n_v - A_p))

    lam_pred = get_lam(A_fit, B_fit, n_hg)
    dlam_pred = propagate_error(get_lam, [A_fit, B_fit, n_hg], [dA_fit, dB_fit, dn_hg])
    lam_ref = 546.00
    sigma_dist = abs(lam_pred - lam_ref) / dlam_pred

    # 4. Hydrogen Prism Analysis
    quantum_n = {"Red": 3, "Blue-Green": 4, "Blue": 5}
    R_inf_theo = 10973731.568
    prism_R_vals = []
    
    for _, row in hp_df.iterrows():
        color = row["color"]
        beta = row["beta"]
        dbeta = row["dbeta"]
        
        n_p = np.sin((alpha_rad + np.radians(beta)) / 2.0) / np.sin(alpha_rad / 2.0)
        dn_p = (
            np.cos((alpha_rad + np.radians(beta)) / 2.0)
            / (2.0 * np.sin(alpha_rad / 2.0))
        ) * np.radians(dbeta)
        
        lam = get_lam(A_fit, B_fit, n_p)
        dlam = propagate_error(get_lam, [A_fit, B_fit, n_p], [dA_fit, dB_fit, dn_p])
        
        n_q = quantum_n.get(color, 3)
        factor = 0.25 - 1.0 / (n_q**2)
        R = 1.0 / ((lam * 1e-9) * factor)
        dR = R * (dlam / lam)
        
        prism_R_vals.append((R, dR))

    # 5. Hydrogen Grating Analysis
    lines_density = 500.0  # lines/mm
    d_grating = (1.0e6) / lines_density
    grating_R_vals = {}
    
    for _, row in hg_grating_df.iterrows():
        color = row["color"]
        m = row["order"]
        bp = row["beta_plus"]
        bm = row["beta_minus"]
        db = row["dbeta"]
        
        bp_rad = np.radians(bp)
        bm_rad = np.radians(bm)
        db_rad = np.radians(db)
        
        sin_term = (np.sin(bp_rad) + np.sin(bm_rad)) / 2.0
        lam = (d_grating / m) * sin_term
        
        dsin_term = 0.5 * (np.cos(bp_rad) + np.cos(bm_rad)) * db_rad
        dlam = (d_grating / m) * dsin_term
        
        n_q = quantum_n.get(color, 3)
        factor = 0.25 - 1.0 / (n_q**2)
        R = 1.0 / ((lam * 1e-9) * factor)
        dR = R * (dlam / lam)
        
        if color not in grating_R_vals:
            grating_R_vals[color] = []
        grating_R_vals[color].append((R, dR))

    # Average Rydberg Prism
    R_prism_list = [r[0] for r in prism_R_vals]
    dR_prism_list = [r[1] for r in prism_R_vals]
    w_prism = 1.0 / (np.array(dR_prism_list) ** 2)
    R_avg_prism = np.sum(np.array(R_prism_list) * w_prism) / np.sum(w_prism)
    dR_avg_prism = 1.0 / np.sqrt(np.sum(w_prism))
    prism_sig = abs(R_avg_prism - R_inf_theo) / dR_avg_prism
    prism_disc = abs(R_avg_prism - R_inf_theo) / R_inf_theo * 100.0

    # Average Rydberg Grating
    R_grating_all = []
    dR_grating_all = []
    for color, vals in grating_R_vals.items():
        for r, dr in vals:
            R_grating_all.append(r)
            dR_grating_all.append(dr)
    
    w_grating = 1.0 / (np.array(dR_grating_all) ** 2)
    R_avg_grating = np.sum(np.array(R_grating_all) * w_grating) / np.sum(w_grating)
    dR_avg_grating = 1.0 / np.sqrt(np.sum(w_grating))
    grating_sig = abs(R_avg_grating - R_inf_theo) / dR_avg_grating
    grating_disc = abs(R_avg_grating - R_inf_theo) / R_inf_theo * 100.0

    # 6. Pretty Prints using clean ASCII
    print("=" * 80)
    print("               BALMER SERIES EXPERIMENT ANALYSES RESULTS")
    print("=" * 80)
    print(f" {'Parameter':<45} | {'Value':<30}")
    print("-" * 80)
    print(f" {'Cauchy Parameter A':<45} | {A_fit:.6f} +/- {dA_fit:.6f}")
    print(f" {'Cauchy Parameter B':<45} | {B_fit:.1f} +/- {dB_fit:.1f} nm^2")
    print("-" * 80)
    print(f" {'Mercury Green predicted wavelength':<45} | {lam_pred:.2f} +/- {dlam_pred:.2f} nm")
    print(f" {'Mercury Green reference wavelength':<45} | {lam_ref:.2f} nm")
    print(f" {'Mercury Green statistical distance':<45} | {sigma_dist:.2f} sigma")
    print("-" * 80)
    print(f" {'Rydberg Constant (Prism Method)':<45} | {R_avg_prism:.4e} +/- {dR_avg_prism:.4e} m^-1")
    print(f" {'Prism Rydberg Discrepancy from Bohr':<45} | {prism_disc:.3f}% ({prism_sig:.2f} sigma)")
    print(f" {'Rydberg Constant (Grating Method)':<45} | {R_avg_grating:.4e} +/- {dR_avg_grating:.4e} m^-1")
    print(f" {'Grating Rydberg Discrepancy from Bohr':<45} | {grating_disc:.3f}% ({grating_sig:.2f} sigma)")
    print(f" {'Theoretical Bohr Rydberg Prediction (R_inf)':<45} | {R_inf_theo:.4e} m^-1")
    print("=" * 80)

if __name__ == "__main__":
    main()