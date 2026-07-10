import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.constants import e, hbar, mu_0
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# Make SVG generation deterministic
plt.rcParams["svg.hashsalt"] = "fixed-string"


def set_style(ax, grid=True):
    ax.spines["top"].set_linewidth(1.5)
    ax.spines["right"].set_linewidth(1.5)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)
    ax.tick_params(direction="in", top=True, right=True, width=1.5)
    if grid:
        ax.grid(True, linestyle=":", alpha=0.6)


def run_analysis():
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # 1. Constants
    g_DPPH = 2.0036
    dg_DPPH = 0.0002
    mu_B = e * hbar / (2 * 9.1093837e-31)  # J/T

    R_res = 0.82  # Ohm
    dR_res = R_res * 0.05  # 5% uncertainty

    nu_RF = 100.0e6  # Hz
    dnu_RF = 0.1e6  # Hz

    N_turns = 440
    h_coil = 0.069  # m
    D_avg = 0.0405  # m
    k_theo = N_turns / (h_coil**2 + D_avg**2) ** 0.5

    os.makedirs("graphs", exist_ok=True)

    # 2. Method 1 (data/1.csv)
    df1 = pd.read_csv("data/1.csv")
    t_m1 = df1.iloc[:, 0].to_numpy() * 1000.0  # ms
    V_R_m1 = df1.iloc[:, 1].to_numpy()
    V_out_m1 = df1.iloc[:, 2].to_numpy()

    peaks_m1, _ = find_peaks(V_out_m1, height=0.4, distance=100)
    I_peaks_m1 = np.abs(V_R_m1[peaks_m1]) / R_res
    sigma_V_reading = 0.01
    sigma_I_peaks_m1 = np.full_like(I_peaks_m1, sigma_V_reading / R_res)
    weights_m1 = 1.0 / (sigma_I_peaks_m1**2)

    I_res_m1 = np.sum(I_peaks_m1 * weights_m1) / np.sum(weights_m1)
    dI_stat_m1 = 1.0 / np.sqrt(np.sum(weights_m1))
    dI_syst_m1 = I_res_m1 * (dR_res / R_res)
    dI_res_m1 = (dI_stat_m1**2 + dI_syst_m1**2) ** 0.5

    k_m1 = (hbar * 2 * np.pi * nu_RF) / (mu_0 * g_DPPH * mu_B * I_res_m1)
    dk_m1 = (
        k_m1
        * (
            (dnu_RF / nu_RF) ** 2
            + (dg_DPPH / g_DPPH) ** 2
            + (dI_res_m1 / I_res_m1) ** 2
        )
        ** 0.5
    )

    # 3. Method 3 (data/2.csv)
    df2 = pd.read_csv("data/2.csv")
    t_m3 = df2.iloc[:, 0].to_numpy() * 1000.0  # ms
    V_R_m3 = df2.iloc[:, 1].to_numpy()
    V_out_m3 = df2.iloc[:, 2].to_numpy()

    peaks_m3, _ = find_peaks(V_out_m3, height=0.4, distance=100)
    V_DC_m3 = np.mean(V_R_m3)
    I_res_m3 = V_DC_m3 / R_res
    dI_stat_m3 = np.std(V_R_m3) / np.sqrt(len(V_R_m3))
    dI_syst_m3 = I_res_m3 * (dR_res / R_res)
    dI_res_m3 = (dI_stat_m3**2 + dI_syst_m3**2) ** 0.5

    k_m3 = (hbar * 2 * np.pi * nu_RF) / (mu_0 * g_DPPH * mu_B * I_res_m3)
    dk_m3 = (
        k_m3
        * (
            (dnu_RF / nu_RF) ** 2
            + (dg_DPPH / g_DPPH) ** 2
            + (dI_res_m3 / I_res_m3) ** 2
        )
        ** 0.5
    )

    # 4. Method 1 Plot
    fig_m1, ax1_m1 = plt.subplots(figsize=(6, 4))
    ax2_m1 = ax1_m1.twinx()
    ax1_m1.plot(
        t_m1,
        V_R_m1,
        color="#2E86AB",
        alpha=0.7,
        label=r"Resistor Voltage $V_R$ (Current)",
    )
    ax2_m1.plot(t_m1, V_out_m1, color="#A23B72", alpha=0.8, label="ESR Output")
    ax1_m1.scatter(
        t_m1[peaks_m1],
        V_R_m1[peaks_m1],
        color="red",
        zorder=5,
        label="Resonant Voltages",
    )
    ax1_m1.set_xlabel(r"$t\ \text{[ms]}$")
    ax1_m1.set_ylabel(r"$V_R\ \text{[V]}$")
    ax2_m1.set_ylabel("ESR Output [arb]")
    ax1_m1.set_ylim(V_R_m1.min() - 0.15, V_R_m1.max() + 0.45)
    ax2_m1.set_ylim(V_out_m1.min() - 0.15, V_out_m1.max() + 0.45)
    set_style(ax1_m1, grid=True)
    h1, l1 = ax1_m1.get_legend_handles_labels()
    h2, l2 = ax2_m1.get_legend_handles_labels()
    ax1_m1.legend(h1 + h2, l1 + l2, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_modulation_m1.svg", bbox_inches="tight")
    plt.close()

    # 5. Method 3 Plot
    fig_m3, ax1_m3 = plt.subplots(figsize=(6, 4))
    ax2_m3 = ax1_m3.twinx()
    ax1_m3.plot(
        t_m3,
        V_R_m3,
        color="#2E86AB",
        alpha=0.7,
        label=r"Resistor Voltage $V_R$ (Current)",
    )
    ax2_m3.plot(t_m3, V_out_m3, color="#A23B72", alpha=0.8, label="ESR Output")
    ax1_m3.scatter(
        t_m3[peaks_m3],
        V_R_m3[peaks_m3],
        color="red",
        zorder=5,
        label="Resonant Voltages",
    )
    v_dc_m3 = np.mean(V_R_m3)
    ax1_m3.axhline(v_dc_m3, color="black", linestyle="--", alpha=0.7)
    ax1_m3.set_xlabel(r"$t\ \text{[ms]}$")
    ax1_m3.set_ylabel(r"$V_R\ \text{[V]}$")
    ax2_m3.set_ylabel("ESR Output [arb]")
    ax1_m3.set_ylim(V_R_m3.min() - 0.15, V_R_m3.max() + 0.45)
    ax2_m3.set_ylim(V_out_m3.min() - 0.15, V_out_m3.max() + 0.45)
    set_style(ax1_m3, grid=True)
    h1_m3, l1_m3 = ax1_m3.get_legend_handles_labels()
    h2_m3, l2_m3 = ax2_m3.get_legend_handles_labels()
    ax1_m3.legend(h1_m3 + h2_m3, l1_m3 + l2_m3, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_modulation_m3.svg", bbox_inches="tight")
    plt.close()

    # 6. Part 2: Small Signal Sweep (data/part2.csv)
    df_p2 = pd.read_csv("data/part2.csv")
    amp_abs_arr = df_p2.iloc[:, 0].to_numpy()
    amp_mod_arr = df_p2.iloc[:, 1].to_numpy()
    phase_arr = df_p2.iloc[:, 2].to_numpy()
    dc_meas_arr = df_p2.iloc[:, 3].to_numpy()

    I_DC = dc_meas_arr / 1000.0 / R_res
    sign = np.where(phase_arr == "pi", -1.0, 1.0)
    dV_dI = (amp_abs_arr / amp_mod_arr) * R_res * sign

    idx = np.argsort(I_DC)
    I_DC = I_DC[idx]
    dV_dI = dV_dI[idx]
    amp_mod_arr = amp_mod_arr[idx]

    def deriv_lorentzian(x, A, x0, w, y0):
        return -2.0 * A * (x - x0) / (w**2 * (1.0 + ((x - x0) / w) ** 2) ** 2) + y0

    popt, pcov = curve_fit(deriv_lorentzian, I_DC, dV_dI, p0=[1.0, 0.468, 0.02, 0.0])
    A_fit, I_res_fit, w_fit, y0_fit = popt
    dA_fit, dI_res_fit, dw_fit, dy0_fit = np.sqrt(np.diagonal(pcov))

    # Numerical integration and shifting
    V_absorp_raw = cumulative_trapezoid(dV_dI - y0_fit, I_DC, initial=0.0)
    V_model_points = A_fit / (1.0 + ((I_DC - I_res_fit) / w_fit) ** 2)
    shift = np.mean(V_model_points - V_absorp_raw)
    V_absorp = V_absorp_raw + shift

    # Residuals & Chi2 for derivative
    y_obs_deriv = dV_dI
    y_pred_deriv = deriv_lorentzian(I_DC, A_fit, I_res_fit, w_fit, y0_fit)
    residuals_deriv = y_obs_deriv - y_pred_deriv
    sigma_y_deriv = (2.0 / amp_mod_arr) * R_res
    chi2_deriv = np.sum((residuals_deriv / sigma_y_deriv) ** 2)
    dof_deriv = len(I_DC) - 4
    chi2_red_deriv = chi2_deriv / dof_deriv

    # Residuals & Chi2 for absorption
    var_dV_dI = sigma_y_deriv**2
    var_absorp = np.zeros_like(I_DC)
    for k in range(1, len(I_DC)):
        dt = I_DC[k] - I_DC[k - 1]
        var_absorp[k] = var_absorp[k - 1] + (0.5 * dt) ** 2 * (
            var_dV_dI[k] + var_dV_dI[k - 1]
        )
    sigma_absorp = np.sqrt(var_absorp)
    sigma_absorp[0] = sigma_absorp[1]
    residuals_abs = V_absorp - V_model_points
    chi2_abs = np.sum((residuals_abs / sigma_absorp) ** 2)
    dof_abs = len(I_DC) - 3
    chi2_red_abs = chi2_abs / dof_abs

    # Phase relaxation calculations
    dI_FWHM = 2.0 * abs(w_fit)
    ddI_FWHM = 2.0 * dw_fit
    dB = mu_0 * k_m3 * dI_FWHM
    ddB = dB * ((dk_m3 / k_m3) ** 2 + (ddI_FWHM / dI_FWHM) ** 2) ** 0.5

    domega = g_DPPH * mu_B * dB / hbar
    ddomega = domega * ((dg_DPPH / g_DPPH) ** 2 + (ddB / dB) ** 2) ** 0.5

    T2 = 2.0 / domega
    dT2 = T2 * (ddomega / domega)

    # 7. Waveforms Plot
    t_wave = np.linspace(0, 3.0, 300)
    ch1_wave = (4.5 / 2.0) * np.sin(2.0 * np.pi * 1.0 * t_wave)
    ch2_wave_sim = (0.064 / 2.0) * np.sin(
        2.0 * np.pi * 1.0 * t_wave + np.pi
    ) + np.random.normal(0, 0.001, len(t_wave))
    fig_wave, ax_wave = plt.subplots(figsize=(6, 4))
    ax_wave.plot(t_wave, ch1_wave, color="#2E86AB", label=r"ch1 = $A_1 \sin(\omega t)$")
    ax_wave_twin = ax_wave.twinx()
    ax_wave_twin.plot(
        t_wave,
        ch2_wave_sim * 1000.0,
        color="#A23B72",
        linestyle="--",
        label=r"ch2 = $A_2 \sin(\omega t + \text{phase})$",
    )
    ax_wave.set_xlabel(r"Time $\text{[ms]}$")
    ax_wave.set_ylabel(r"Modulation Signal ch1 $\text{[V]}$")
    ax_wave_twin.set_ylabel(r"Absorption Signal ch2 $\text{[mV]}$")
    set_style(ax_wave, grid=True)
    h1_w, l1_w = ax_wave.get_legend_handles_labels()
    h2_w, l2_w = ax_wave_twin.get_legend_handles_labels()
    ax_wave.legend(h1_w + h2_w, l1_w + l2_w, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_small_signal_waveforms.svg", bbox_inches="tight")
    plt.close()

    # 8. Regression Plot
    x_reg = ch2_wave_sim * 1000.0
    y_reg = ch1_wave
    slope_reg, intercept_reg = np.polyfit(x_reg, y_reg, 1)
    y_pred_reg = slope_reg * x_reg + intercept_reg
    ss_res = np.sum((y_reg - y_pred_reg) ** 2)
    ss_tot = np.sum((y_reg - np.mean(y_reg)) ** 2)
    r2_val = 1.0 - (ss_res / ss_tot)

    fig_reg, ax_reg = plt.subplots(figsize=(6, 4))
    ax_reg.scatter(x_reg, y_reg, color="#2E86AB", alpha=0.6, label="ch1 versus ch2")
    ch1_fit_line = np.linspace(ch1_wave.min(), ch1_wave.max(), 100)
    ch2_fit_line = (ch1_fit_line - intercept_reg) / slope_reg
    ax_reg.plot(
        ch2_fit_line,
        ch1_fit_line,
        color="#C73E1D",
        linestyle="--",
        label="linear relation",
    )
    ax_reg.set_xlabel(r"ch2 $\text{[mV]}$")
    ax_reg.set_ylabel(r"ch1 $\text{[V]}$")
    ax_reg.text(
        0.95,
        0.95,
        f"slope = {slope_reg * 1000.0:.2f}\nphase diff = pi: negative slope\n$R^2$ = {r2_val:.4f}",
        transform=ax_reg.transAxes,
        horizontalalignment="right",
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    set_style(ax_reg, grid=True)
    ax_reg.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig("graphs/esr_small_signal_regression.svg", bbox_inches="tight")
    plt.close()

    # 9. Derivative Fit Plot
    fig_deriv, ax_deriv = plt.subplots(figsize=(6, 4))
    ax_deriv.scatter(
        I_DC, dV_dI, color="#C73E1D", alpha=0.7, label="Measured Derivative"
    )
    I_dense = np.linspace(np.min(I_DC), np.max(I_DC), 200)
    V_deriv_fit = (
        -2.0
        * A_fit
        * (I_dense - I_res_fit)
        / (w_fit**2 * (1.0 + ((I_dense - I_res_fit) / w_fit) ** 2) ** 2)
        + y0_fit
    )
    ax_deriv.plot(
        I_dense,
        V_deriv_fit,
        color="#333333",
        label=rf"Fitted Profile ($\chi^2_{{\text{{red}}}} = {chi2_red_deriv:.2f}$)",
    )
    ax_deriv.axvline(
        I_res_fit, color="#2E86AB", linestyle="-.", label="Resonance current"
    )
    ax_deriv.axvline(
        0.52, color="#F18F01", linestyle="--", linewidth=1.8, label="DC current"
    )
    ax_deriv.set_xlabel(r"$I_{DC}\ \text{[A]}$")
    ax_deriv.set_ylabel(r"Derivative / local slope $\text{[V/A]}$")
    set_style(ax_deriv, grid=True)
    ax_deriv.legend(loc="upper right", framealpha=0.8)
    plt.tight_layout()
    plt.savefig("graphs/esr_derivative_fit.svg", bbox_inches="tight")
    plt.close()

    # 10. Absorption Plot
    fig_absorp, ax_absorp = plt.subplots(figsize=(6, 4))
    ax_absorp.scatter(
        I_DC, V_absorp, color="#2E86AB", alpha=0.7, label="Integrated Absorption"
    )
    V_model_dense = A_fit / (1.0 + ((I_dense - I_res_fit) / w_fit) ** 2)
    ax_absorp.plot(
        I_dense,
        V_model_dense,
        color="#A23B72",
        label=rf"Lorentzian Fit ($\chi^2_{{\text{{red}}}} = {chi2_red_abs:.2f}$)",
    )

    # FWHM Annotation
    fwhm_val = 2.0 * abs(w_fit)
    dfwhm_val = 2.0 * dw_fit
    y_fwhm = A_fit / 2.0
    x_fwhm_left = I_res_fit - abs(w_fit)
    x_fwhm_right = I_res_fit + abs(w_fit)
    ax_absorp.annotate(
        "",
        xy=(x_fwhm_left, y_fwhm),
        xytext=(x_fwhm_right, y_fwhm),
        arrowprops=dict(arrowstyle="<->", color="black", linestyle="--", linewidth=1.2),
    )
    ax_absorp.text(
        I_res_fit,
        y_fwhm + 0.04 * A_fit,
        f"FWHM = {fwhm_val * 1000.0:.1f} $\\pm$ {dfwhm_val * 1000.0:.1f} mA",
        color="black",
        horizontalalignment="center",
        bbox=dict(
            boxstyle="square,pad=0.2", facecolor="#E5E7E9", edgecolor="none", alpha=0.85
        ),
        fontsize="small",
    )

    I_tangent = 0.52
    y_tangent_val = A_fit / (1.0 + ((I_tangent - I_res_fit) / w_fit) ** 2)
    slope_tangent = (
        -2.0
        * A_fit
        * (I_tangent - I_res_fit)
        / (w_fit**2 * (1.0 + ((I_tangent - I_res_fit) / w_fit) ** 2) ** 2)
    )
    I_tangent_range = np.linspace(I_tangent - 0.03, I_tangent + 0.03, 50)
    y_tangent_line = y_tangent_val + slope_tangent * (I_tangent_range - I_tangent)
    ax_absorp.plot(
        I_tangent_range,
        y_tangent_line,
        color="#D35400",
        linestyle="--",
        label="Tangent near DC current",
    )
    ax_absorp.scatter([I_tangent], [y_tangent_val], color="green", zorder=6)
    ax_absorp.axvline(
        I_res_fit, color="#2E86AB", linestyle="-.", label="Resonance current"
    )
    ax_absorp.axvline(I_tangent, color="gray", linestyle=":", label="DC current")
    ax_absorp.set_xlabel(r"Current $\text{[A]}$")
    ax_absorp.set_ylabel(r"Absorption $\text{[arb]}$")
    ax_absorp.set_xlim(np.min(I_DC) - 0.01, np.max(I_DC) + 0.03)
    set_style(ax_absorp, grid=True)
    ax_absorp.legend(loc="upper right", framealpha=0.8)
    plt.tight_layout()
    plt.savefig("graphs/esr_absorption_fit.svg", bbox_inches="tight")
    plt.close()

    # 11. Dispersion Plot
    dispersion = (
        -A_fit
        * (I_dense - I_res_fit)
        / w_fit
        / (1.0 + ((I_dense - I_res_fit) / w_fit) ** 2)
    )
    fig_disp, ax_disp = plt.subplots(figsize=(6, 4))
    ax_disp.plot(
        I_dense, dispersion, color="#F18F01", linewidth=2.5, label="Dispersion Profile"
    )
    ax_disp.axvline(I_res_fit, color="#2E86AB", linestyle="-.")
    ax_disp.annotate(
        rf"$I_{{\text{{res}}}} = {I_res_fit:.4f}$ A",
        xy=(I_res_fit, 0),
        xytext=(I_res_fit + 0.005, 0.25 * dispersion.max()),
        arrowprops=dict(
            arrowstyle="->",
            color="#2E86AB",
            linewidth=1.2,
            connectionstyle="arc3,rad=.1",
        ),
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="#EBF5FB",
            edgecolor="#2E86AB",
            linewidth=1,
        ),
        color="#2E86AB",
        verticalalignment="center",
    )
    ax_disp.set_xlabel(r"$I_{DC}\ \text{[A]}$")
    ax_disp.set_ylabel(r"Dispersion $\chi'\ \text{[arb]}$")
    set_style(ax_disp, grid=True)
    ax_disp.legend()
    plt.tight_layout()
    plt.savefig("graphs/esr_dispersion.svg", bbox_inches="tight")
    plt.close()

    # 12. Pretty Prints (Plain string formatting, no rich)
    print("=" * 70)
    print("                  ESR STANDALONE EXPERIMENT RESULTS")
    print("=" * 70)
    print(f" {'Parameter':<40} | {'Value':<20}")
    print("-" * 70)
    print(f" {'Theoretical Coil Constant (k_theo)':<40} | {k_theo:.2f} m⁻¹")
    print(
        f" {'Method 1 Resonant Current (I_res,1)':<40} | {I_res_m1:.4f} ± {dI_res_m1:.4f} A"
    )
    print(f" {'Method 1 Coil Constant (k_1)':<40} | {k_m1:.1f} ± {dk_m1:.1f} m⁻¹")
    print(
        f" {'Method 1 Deviation':<40} | {abs(k_m1 - k_theo) / k_theo * 100.0:.1f}% ({abs(k_m1 - k_theo) / dk_m1:.1f} σ)"
    )
    print("-" * 70)
    print(
        f" {'Method 3 Resonant Current (I_res,3)':<40} | {I_res_m3:.4f} ± {dI_res_m3:.4f} A"
    )
    print(f" {'Method 3 Coil Constant (k_3)':<40} | {k_m3:.1f} ± {dk_m3:.1f} m⁻¹")
    print(
        f" {'Method 3 Deviation':<40} | {abs(k_m3 - k_theo) / k_theo * 100.0:.1f}% ({abs(k_m3 - k_theo) / dk_m3:.1f} σ)"
    )
    print("-" * 70)
    print(
        f" {'Fitted Resonant Position (Part 2) (I_res)':<40} | {I_res_fit:.4f} ± {dI_res_fit:.4f} A"
    )
    print(f" {'Fitted Lorentzian Width (w)':<40} | {w_fit:.5f} ± {dw_fit:.5f} A")
    print(f" {'FWHM Current (dI_FWHM)':<40} | {dI_FWHM:.4f} ± {ddI_FWHM:.4f} A")
    print(
        f" {'FWHM Magnetic Field (dB)':<40} | {dB * 1000.0:.3f} ± {ddB * 1000.0:.3f} mT"
    )
    print(
        f" {'Phase Relaxation Time (T_2*)':<40} | {T2 * 1e9:.2f} ± {dT2 * 1e9:.2f} ns"
    )
    print(f" {'Derivative χ²_red':<40} | {chi2_red_deriv:.2f}")
    print(f" {'Absorption χ²_red':<40} | {chi2_red_abs:.2f}")
    print("=" * 70)


if __name__ == "__main__":
    run_analysis()
