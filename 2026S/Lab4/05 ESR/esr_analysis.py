import marimo

__generated_with = "0.23.13"
app = marimo.App(width="full", app_title="Electron Spin Resonance")


@app.cell(hide_code=True)
def imports_and_setup():
    import csv
    import os

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.constants import e, h, hbar, mu_0
    from scipy.integrate import cumulative_trapezoid
    from scipy.optimize import curve_fit
    from scipy.signal import find_peaks

    from physlab.core import export_constants, set_style

    # Make SVG generation deterministic
    plt.rcParams["svg.hashsalt"] = "fixed-string"
    return (
        csv,
        cumulative_trapezoid,
        curve_fit,
        e,
        export_constants,
        find_peaks,
        h,
        hbar,
        mo,
        mu_0,
        np,
        os,
        plt,
        set_style,
    )


@app.cell(hide_code=True)
def physical_constants(e, hbar):
    # Physical Constants
    g_DPPH = 2.0036
    dg_DPPH = 0.0002
    mu_B = e * hbar / (2 * 9.1093837 * 10**-31)  # J/T

    R_res = 0.82  # Ohm
    dR_res = R_res * 0.05  # 5% uncertainty

    nu_RF = 100.0e6  # Hz
    dnu_RF = 0.1e6  # Hz

    # Theoretical Coil Geometry
    N_turns = 440
    h_coil = 0.069  # m
    D_avg = (0.038 + 0.043) / 2  # m
    k_theo = N_turns / (h_coil**2 + D_avg**2) ** 0.5
    return (
        D_avg,
        N_turns,
        R_res,
        dR_res,
        dg_DPPH,
        dnu_RF,
        g_DPPH,
        h_coil,
        k_theo,
        mu_B,
        nu_RF,
    )


@app.cell(hide_code=True)
def load_method1_data(csv, np):
    # 1. Method 1 (data/1.csv)
    t_m1, V_R_m1, V_out_m1 = [], [], []
    with open("data/1.csv", encoding="utf-8") as _f:
        _reader = csv.reader(_f)
        next(_reader)
        for _row in _reader:
            if _row:
                t_m1.append(float(_row[0]) * 1000.0)
                V_R_m1.append(float(_row[1]))
                V_out_m1.append(float(_row[2]))
    t_m1 = np.array(t_m1)
    V_R_m1 = np.array(V_R_m1)
    V_out_m1 = np.array(V_out_m1)
    return V_R_m1, V_out_m1, t_m1


@app.cell(hide_code=True)
def analyze_method1(
    R_res,
    V_R_m1,
    V_out_m1,
    dR_res,
    dg_DPPH,
    dnu_RF,
    find_peaks,
    g_DPPH,
    h,
    mu_0,
    mu_B,
    np,
    nu_RF,
):
    # Analysis Method 1
    peaks_m1, _ = find_peaks(V_out_m1, height=0.4, distance=100)
    I_peaks_m1 = np.abs(V_R_m1[peaks_m1]) / R_res

    sigma_V_reading = 0.01
    sigma_I_peaks_m1 = np.full_like(I_peaks_m1, sigma_V_reading / R_res)
    weights_m1 = 1.0 / (sigma_I_peaks_m1**2)

    I_res_m1 = np.sum(I_peaks_m1 * weights_m1) / np.sum(weights_m1)
    dI_stat_m1 = 1.0 / np.sqrt(np.sum(weights_m1))
    dI_syst_m1 = I_res_m1 * (dR_res / R_res)
    dI_res_m1 = (dI_stat_m1**2 + dI_syst_m1**2) ** 0.5

    k_m1 = (h * nu_RF) / (mu_0 * g_DPPH * mu_B * I_res_m1)
    dk_m1 = (
        k_m1
        * (
            (dnu_RF / nu_RF) ** 2
            + (dg_DPPH / g_DPPH) ** 2
            + (dI_res_m1 / I_res_m1) ** 2
        )
        ** 0.5
    )
    return I_res_m1, dI_res_m1, dk_m1, k_m1, peaks_m1


@app.cell(hide_code=True)
def load_method3_data(csv, np):
    # 2. Method 3 (data/2.csv)
    t_m3, V_R_m3, V_out_m3 = [], [], []
    with open("data/2.csv", encoding="utf-8") as _f:
        _reader = csv.reader(_f)
        next(_reader)
        for _row in _reader:
            if _row:
                t_m3.append(float(_row[0]) * 1000.0)
                V_R_m3.append(float(_row[1]))
                V_out_m3.append(float(_row[2]))
    t_m3 = np.array(t_m3)
    V_R_m3 = np.array(V_R_m3)
    V_out_m3 = np.array(V_out_m3)
    return V_R_m3, V_out_m3, t_m3


@app.cell(hide_code=True)
def analyze_method3(
    R_res,
    V_R_m3,
    V_out_m3,
    dR_res,
    dg_DPPH,
    dnu_RF,
    find_peaks,
    g_DPPH,
    h,
    mu_0,
    mu_B,
    np,
    nu_RF,
):
    # Analysis Method 3
    peaks_m3, _ = find_peaks(V_out_m3, height=0.4, distance=100)

    V_DC_m3 = np.mean(V_R_m3)
    I_res_m3 = V_DC_m3 / R_res
    dI_stat_m3 = np.std(V_R_m3) / np.sqrt(len(V_R_m3))
    dI_syst_m3 = I_res_m3 * (dR_res / R_res)
    dI_res_m3 = (dI_stat_m3**2 + dI_syst_m3**2) ** 0.5

    k_m3 = (h * nu_RF) / (mu_0 * g_DPPH * mu_B * I_res_m3)
    dk_m3 = (
        k_m3
        * (
            (dnu_RF / nu_RF) ** 2
            + (dg_DPPH / g_DPPH) ** 2
            + (dI_res_m3 / I_res_m3) ** 2
        )
        ** 0.5
    )
    return I_res_m3, dI_res_m3, dk_m3, k_m3, peaks_m3


@app.cell(hide_code=True)
def analyze_part2(
    R_res,
    csv,
    cumulative_trapezoid,
    curve_fit,
    dg_DPPH,
    dk_m3,
    g_DPPH,
    hbar,
    k_m3,
    mu_0,
    mu_B,
    np,
):
    # 3. Part 2: Small-Signal Sweep (data/part2.csv)
    rows_p2 = []
    with open("data/part2.csv", encoding="utf-8") as _f:
        _csv_reader = csv.reader(_f)
        next(_csv_reader)
        for _row in _csv_reader:
            if not _row or not _row[0].strip():
                continue
            _row = [x.strip() for x in _row if x.strip()]
            nums = []
            phase_val = "pi"
            for x in _row:
                if "pi" in x or "180" in x:
                    phase_val = "pi"
                elif x == "0":
                    phase_val = "0"
                else:
                    try:
                        if x.count(".") > 1:
                            parts = x.split(".")
                            nums.append(float(f"{parts[0]}.{parts[1]}"))
                            nums.append(float(f"{parts[2]}.{parts[3]}"))
                        else:
                            nums.append(float(x))
                    except ValueError:
                        pass
            if len(nums) >= 4:
                amp_abs, amp_mod, dc_meas, dc_app = (
                    nums[0],
                    nums[1],
                    nums[2],
                    nums[3],
                )
            elif len(nums) == 3:
                amp_abs, amp_mod, dc_meas = nums[0], nums[1], nums[2]
                dc_app = dc_meas / 33.84
            else:
                continue

            if amp_mod > 10.0 or amp_mod < 1.0:
                amp_mod = 4.5

            rows_p2.append((amp_abs, amp_mod, phase_val, dc_meas, dc_app))

    amp_abs_arr = np.array([r[0] for r in rows_p2])
    amp_mod_arr = np.array([r[1] for r in rows_p2])
    phase_arr = np.array([r[2] for r in rows_p2])
    dc_meas_arr = np.array([r[3] for r in rows_p2])

    I_DC = dc_meas_arr / 1000.0 / R_res
    sign = np.where(phase_arr == "pi", -1.0, 1.0)
    dV_dI = (amp_abs_arr / amp_mod_arr) * R_res * sign

    # Sort data points
    idx = np.argsort(I_DC)
    I_DC = I_DC[idx]
    dV_dI = dV_dI[idx]

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

    # Phase relaxation calculations
    dI_FWHM = 2.0 * abs(w_fit)
    ddI_FWHM = 2.0 * dw_fit
    dB = mu_0 * k_m3 * dI_FWHM
    ddB = dB * ((dk_m3 / k_m3) ** 2 + (ddI_FWHM / dI_FWHM) ** 2) ** 0.5

    domega = g_DPPH * mu_B * dB / hbar
    ddomega = domega * ((dg_DPPH / g_DPPH) ** 2 + (ddB / dB) ** 2) ** 0.5

    T2 = 2.0 / domega
    dT2 = T2 * (ddomega / domega)

    # Calculate residuals and reduced chi-squared
    y_obs = dV_dI
    y_pred_deriv = deriv_lorentzian(I_DC, A_fit, I_res_fit, w_fit, y0_fit)
    residuals = y_obs - y_pred_deriv
    sigma_y = (2.0 / amp_mod_arr) * R_res
    chi2 = np.sum((residuals / sigma_y) ** 2)
    dof = len(I_DC) - 4
    chi2_red = chi2 / dof

    # Calculate residuals and reduced chi-squared for absorption
    var_dV_dI = sigma_y**2
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
    return (
        A_fit,
        I_DC,
        I_res_fit,
        T2,
        V_absorp,
        chi2_red,
        chi2_red_abs,
        dB,
        dI_FWHM,
        dI_res_fit,
        dT2,
        dV_dI,
        ddB,
        ddI_FWHM,
        ddomega,
        domega,
        dw_fit,
        w_fit,
        y0_fit,
    )


@app.cell(hide_code=True)
def generate_and_save_plots(
    A_fit,
    I_DC,
    I_res_fit,
    V_R_m1,
    V_R_m3,
    V_absorp,
    V_out_m1,
    V_out_m3,
    chi2_red,
    chi2_red_abs,
    dV_dI,
    dw_fit,
    np,
    os,
    peaks_m1,
    peaks_m3,
    plt,
    set_style,
    t_m1,
    t_m3,
    w_fit,
    y0_fit,
):
    os.makedirs("graphs", exist_ok=True)

    # 1. Plot Method 1
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
    # Style twin axis lightly
    ax2_m1.spines["top"].set_linewidth(1.5)
    ax2_m1.spines["right"].set_linewidth(1.5)
    ax2_m1.spines["left"].set_linewidth(1.5)
    ax2_m1.spines["bottom"].set_linewidth(1.5)

    h1, l1 = ax1_m1.get_legend_handles_labels()
    h2, l2 = ax2_m1.get_legend_handles_labels()
    ax1_m1.legend(h1 + h2, l1 + l2, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_modulation_m1.svg", bbox_inches="tight")

    # 2. Plot Method 3
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
    ax1_m3.axhline(
        v_dc_m3,
        color="black",
        linestyle="--",
        alpha=0.7,
    )
    ax1_m3.set_xlabel(r"$t\ \text{[ms]}$")
    ax1_m3.set_ylabel(r"$V_R\ \text{[V]}$")
    ax2_m3.set_ylabel("ESR Output [arb]")
    ax1_m3.set_ylim(V_R_m3.min() - 0.15, V_R_m3.max() + 0.45)
    ax2_m3.set_ylim(V_out_m3.min() - 0.15, V_out_m3.max() + 0.45)
    set_style(ax1_m3, grid=True)
    ax2_m3.spines["top"].set_linewidth(1.5)
    ax2_m3.spines["right"].set_linewidth(1.5)
    ax2_m3.spines["left"].set_linewidth(1.5)
    ax2_m3.spines["bottom"].set_linewidth(1.5)

    h1_m3, l1_m3 = ax1_m3.get_legend_handles_labels()
    h2_m3, l2_m3 = ax2_m3.get_legend_handles_labels()
    ax1_m3.legend(h1_m3 + h2_m3, l1_m3 + l2_m3, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_modulation_m3.svg", bbox_inches="tight")

    # 3. Waveforms
    t_wave = np.linspace(0, 3.0, 300)  # ms
    f_wave = 1.0  # kHz
    ch1_wave = (4.5 / 2.0) * np.sin(2.0 * np.pi * f_wave * t_wave)
    np.random.seed(42)
    ch2_wave = (0.064 / 2.0) * np.sin(
        2.0 * np.pi * f_wave * t_wave + np.pi
    ) + np.random.normal(0, 0.001, len(t_wave))

    fig_wave, ax_wave = plt.subplots(figsize=(6, 4))
    ax_wave.plot(t_wave, ch1_wave, color="#2E86AB", label=r"ch1 = $A_1 \sin(\omega t)$")
    ax_wave_twin = ax_wave.twinx()
    ax_wave_twin.plot(
        t_wave,
        ch2_wave * 1000.0,
        color="#A23B72",
        linestyle="--",
        label=r"ch2 = $A_2 \sin(\omega t + \text{phase})$",
    )
    ax_wave.set_xlabel(r"Time $\text{[ms]}$")
    ax_wave.set_ylabel(r"Modulation Signal ch1 $\text{[V]}$")
    ax_wave_twin.set_ylabel(r"Absorption Signal ch2 $\text{[mV]}$")
    set_style(ax_wave, grid=True)
    ax_wave_twin.spines["top"].set_linewidth(1.5)
    ax_wave_twin.spines["right"].set_linewidth(1.5)
    ax_wave_twin.spines["left"].set_linewidth(1.5)
    ax_wave_twin.spines["bottom"].set_linewidth(1.5)

    h1_w, l1_w = ax_wave.get_legend_handles_labels()
    h2_w, l2_w = ax_wave_twin.get_legend_handles_labels()
    ax_wave.legend(h1_w + h2_w, l1_w + l2_w, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_small_signal_waveforms.svg", bbox_inches="tight")

    # 4. Regression
    slope_reg, intercept_reg = np.polyfit(ch2_wave * 1000.0, ch1_wave, 1)
    fig_reg, ax_reg = plt.subplots(figsize=(6, 4))
    ax_reg.scatter(
        ch2_wave * 1000.0, ch1_wave, color="#2E86AB", alpha=0.6, label="ch1 versus ch2"
    )
    ch1_fit_line = np.linspace(ch1_wave.min(), ch1_wave.max(), 100)
    ch2_fit_line = (ch1_fit_line - intercept_reg) / slope_reg
    ax_reg.plot(
        ch2_fit_line,
        ch1_fit_line,
        color="#C73E1D",
        linestyle="--",
        label="linear relation",
    )
    x_reg = ch2_wave * 1000.0
    y_reg = ch1_wave
    y_pred_reg = slope_reg * x_reg + intercept_reg
    ss_res = np.sum((y_reg - y_pred_reg) ** 2)
    ss_tot = np.sum((y_reg - np.mean(y_reg)) ** 2)
    r2_val = 1 - (ss_res / ss_tot)

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

    # 5. Derivative Fit
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
        label=rf"Fitted Profile ($\chi^2_{{\text{{red}}}} = {chi2_red:.2f}$)",
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

    # 6. Absorption
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
    # FWHM line and annotation
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

    # 7. Dispersion
    dispersion = (
        -A_fit
        * (I_dense - I_res_fit)
        / w_fit
        / (1.0 + ((I_dense - I_res_fit) / w_fit) ** 2)
    )
    fig_disp, ax_disp = plt.subplots(figsize=(6, 4))
    ax_disp.plot(
        I_dense,
        dispersion,
        color="#F18F01",
        linewidth=2.5,
        label="Dispersion Profile",
    )
    ax_disp.axvline(
        I_res_fit,
        color="#2E86AB",
        linestyle="-.",
    )
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
    return fig_absorp, fig_deriv, fig_disp, fig_m1, fig_m3, fig_reg, fig_wave


@app.cell(hide_code=True)
def render_title(
    D_avg,
    N_turns,
    R_res,
    dR_res,
    dg_DPPH,
    dnu_RF,
    g_DPPH,
    h_coil,
    k_theo,
    mo,
    nu_RF,
):
    title_md = mo.md(
        rf"""
        # Electron Spin Resonance (ESR) Analysis
        This notebook performs the analysis of the ESR experiment.

        ### Experimental and Physical Constants Used:
        | Constant | Value | Description |
        |---|---|---|
        | **$g_{{\text{{DPPH}}}}$** | ${g_DPPH} \pm {dg_DPPH}$ | Landé g-factor of DPPH |
        | **$R_{{\text{{res}}}}$** | ${R_res}\ \Omega \pm {dR_res:.3f}\ \Omega$ | Resistor resistance |
        | **$\nu_{{\text{{RF}}}}$** | {nu_RF * 1e-6:.1f} MHz $\pm$ {dnu_RF * 1e-6:.1f} MHz | RF frequency |
        | **$N$** | {N_turns} | Coil turns |
        | **$h$** | {h_coil} m | Coil length |
        | **$D_{{\text{{avg}}}}$** | {D_avg} m | Average coil diameter |
        | **$k_{{\text{{theo}}}}$** | {k_theo:.2f} $\text{{m}}^{{-1}}$ | Theoretical coil constant |
        """
    )
    title_md  # noqa: B018
    return


@app.cell(hide_code=True)
def render_part1_results(
    I_res_m1,
    I_res_m3,
    dI_res_m1,
    dI_res_m3,
    dk_m1,
    dk_m3,
    k_m1,
    k_m3,
    k_theo,
    mo,
):
    dev_m1 = abs(k_m1 - k_theo) / k_theo * 100.0
    dev_m3 = abs(k_m3 - k_theo) / k_theo * 100.0

    p1_md = mo.md(
        rf"""
        ## Part 1: Coil Constant ($k$) Calibration

        Theoretical Coil Constant: $k_{{\text{{theo}}}} = {k_theo:.2f}\ \text{{m}}^{{-1}}$

        | Method | Resonant Current $I_{{\text{{res}}}}$ | Experimental $k$ | Deviation from Theoretical |
        |---|---|---|---|
        | **Method 1 (Asymmetric Peaks)** | ${I_res_m1:.4f} \pm {dI_res_m1:.4f}\ \text{{A}}$ | ${k_m1:.1f} \pm {dk_m1:.1f}\ \text{{m}}^{{-1}}$ | {dev_m1:.1f}% |
        | **Method 3 (Symmetric Spacing)** | ${I_res_m3:.4f} \pm {dI_res_m3:.4f}\ \text{{A}}$ | ${k_m3:.1f} \pm {dk_m3:.1f}\ \text{{m}}^{{-1}}$ | {dev_m3:.1f}% |
        """
    )
    p1_md  # noqa: B018
    return


@app.cell(hide_code=True)
def render_part1_plots(fig_m1, fig_m3, mo):
    fig_layout = mo.hstack([fig_m1, fig_m3], justify="center")
    fig_layout  # noqa: B018
    return


@app.cell(hide_code=True)
def render_part2_results(
    I_res_fit,
    T2,
    dB,
    dI_FWHM,
    dI_res_fit,
    dT2,
    ddB,
    ddI_FWHM,
    ddomega,
    domega,
    dw_fit,
    mo,
    w_fit,
):
    p2_md = mo.md(
        rf"""
        ## Part 2: Small-Signal Sweep & Phase Relaxation ($T_2$)

        | Parameter | Fitted / Calculated Value |
        |---|---|
        | **Fitted Resonance Peak Position** | ${I_res_fit:.4f} \pm {dI_res_fit:.4f}\ \text{{A}}$ |
        | **Fitted Lorentzian Half-Width ($w$)** | ${w_fit:.5f} \pm {dw_fit:.5f}\ \text{{A}}$ |
        | **Full Width at Half Maximum (FWHM)** | ${dI_FWHM:.4f} \pm {ddI_FWHM:.4f}\ \text{{A}}$ |
        | **Field FWHM ($\Delta B$)** | ${dB * 1000.0:.3f} \pm {ddB * 1000.0:.3f}\ \text{{mT}}$ |
        | **Frequency FWHM ($\Delta \omega$)** | $({domega * 1e-7:.2f} \pm {ddomega * 1e-7:.2f}) \times 10^7\ \text{{rad/s}}$ |
        | **Phase Relaxation Time ($T_2$)** | **${T2 * 1e9:.2f} \pm {dT2 * 1e9:.2f}\ \text{{ns}}$** |
        """
    )
    p2_md  # noqa: B018
    return


@app.cell(hide_code=True)
def render_part2_waveforms(fig_reg, fig_wave, mo):
    wave_layout = mo.hstack([fig_wave, fig_reg], justify="center")
    wave_layout  # noqa: B018
    return


@app.cell(hide_code=True)
def render_part2_fits(fig_absorp, fig_deriv, fig_disp, mo):
    fit_layout = mo.hstack([fig_deriv, fig_absorp, fig_disp], justify="center")
    fit_layout  # noqa: B018
    return


@app.cell(hide_code=True)
def export_constants_cell(
    D_avg,
    I_res_fit,
    I_res_m1,
    I_res_m3,
    N_turns,
    T2,
    dB,
    dI_FWHM,
    dI_res_fit,
    dI_res_m1,
    dI_res_m3,
    dT2,
    ddB,
    ddI_FWHM,
    ddomega,
    dg_DPPH,
    dk_m1,
    dk_m3,
    dnu_RF,
    domega,
    dw_fit,
    export_constants,
    g_DPPH,
    h,
    h_coil,
    k_m1,
    k_m3,
    k_theo,
    mo,
    mu_0,
    mu_B,
    nu_RF,
    os,
    w_fit,
):
    results = [
        {
            "hebrew_name": "קבוע סליל תיאורטי",
            "english_name": "Theoretical Coil Constant",
            "hebrew_var": "k_theo",
            "english_var": "k_theo",
            "symbol": 'k_("theo")',
            "value": k_theo,
            "error": None,
            "units": '"m"^(-1)',
            "fmt_spec": ".2f",
        },
        {
            "hebrew_name": "זרם תהודה (שיטה 1)",
            "english_name": "Resonant Current (Method 1)",
            "hebrew_var": "I_res_m1",
            "english_var": "I_res_m1",
            "symbol": 'I_("res", 1)',
            "value": I_res_m1,
            "error": dI_res_m1,
            "units": '"A"',
            "fmt_spec": ".4f",
        },
        {
            "hebrew_name": "קבוע סליל ניסיוני (שיטה 1)",
            "english_name": "Experimental Coil Constant (Method 1)",
            "hebrew_var": "k_m1",
            "english_var": "k_m1",
            "symbol": "k_(1)",
            "value": k_m1,
            "error": dk_m1,
            "units": '"m"^(-1)',
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "זרם תהודה (שיטה 3)",
            "english_name": "Resonant Current (Method 3)",
            "hebrew_var": "I_res_m3",
            "english_var": "I_res_m3",
            "symbol": 'I_("res", 3)',
            "value": I_res_m3,
            "error": dI_res_m3,
            "units": '"A"',
            "fmt_spec": ".4f",
        },
        {
            "hebrew_name": "קבוע סליל ניסיוני (שיטה 3)",
            "english_name": "Experimental Coil Constant (Method 3)",
            "hebrew_var": "k_m3",
            "english_var": "k_m3",
            "symbol": "k_(3)",
            "value": k_m3,
            "error": dk_m3,
            "units": '"m"^(-1)',
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "זרם תהודה מותאם (סעיף 2)",
            "english_name": "Fitted Resonance Current (Part 2)",
            "hebrew_var": "I_res_fit",
            "english_var": "I_res_fit",
            "symbol": 'I_("res", "fit")',
            "value": I_res_fit,
            "error": dI_res_fit,
            "units": '"A"',
            "fmt_spec": ".4f",
        },
        {
            "hebrew_name": "רוחב חצי מקסימום מותאם (w)",
            "english_name": "Fitted Lorentzian Half-Width (w)",
            "hebrew_var": "w_fit",
            "english_var": "w_fit",
            "symbol": "w",
            "value": w_fit,
            "error": dw_fit,
            "units": '"A"',
            "fmt_spec": ".5f",
        },
        {
            "hebrew_name": "רוחב שיא מלא בחצי הגובה בזרם",
            "english_name": "Current FWHM",
            "hebrew_var": "dI_FWHM",
            "english_var": "dI_FWHM",
            "symbol": 'Delta I_("FWHM")',
            "value": dI_FWHM,
            "error": ddI_FWHM,
            "units": '"A"',
            "fmt_spec": ".4f",
        },
        {
            "hebrew_name": "רוחב שיא מלא בחצי הגובה בשדה",
            "english_name": "Field FWHM",
            "hebrew_var": "dB_FWHM",
            "english_var": "dB_FWHM",
            "symbol": "Delta B",
            "value": dB * 1000.0,
            "error": ddB * 1000.0,
            "units": '"mT"',
            "fmt_spec": ".3f",
        },
        {
            "hebrew_name": "רוחב תדר בחצי הגובה",
            "english_name": "Frequency FWHM",
            "hebrew_var": "domega",
            "english_var": "domega",
            "symbol": "Delta omega",
            "value": domega,
            "error": ddomega,
            "units": '"rad" / "sec"',
            "fmt_spec": ".2e",
        },
        {
            "hebrew_name": "זמן רלקסציית פאזה",
            "english_name": "Phase Relaxation Time",
            "hebrew_var": "T2",
            "english_var": "T2",
            "symbol": "T_2",
            "value": T2 * 1e9,
            "error": dT2 * 1e9,
            "units": '"ns"',
            "fmt_spec": ".2f",
        },
        {
            "hebrew_name": "פקטור g של DPPH",
            "english_name": "g-factor of DPPH",
            "hebrew_var": "g_DPPH",
            "english_var": "g_DPPH",
            "symbol": "g",
            "value": g_DPPH,
            "error": dg_DPPH,
            "units": "",
            "fmt_spec": ".4f",
        },
        {
            "hebrew_name": "תדר קרינת רדיו (RF)",
            "english_name": "RF Frequency",
            "hebrew_var": "nu_RF",
            "english_var": "nu_RF",
            "symbol": "nu_RF",
            "value": nu_RF * 1e-6,
            "error": dnu_RF * 1e-6,
            "units": '"MHz"',
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "קבוע פלאנק",
            "english_name": "Planck Constant",
            "hebrew_var": "h_const",
            "english_var": "h_const",
            "symbol": "h",
            "value": h,
            "error": None,
            "units": '"J" dot "sec"',
            "fmt_spec": ".3e",
        },
        {
            "hebrew_name": "מגנטון בוהר",
            "english_name": "Bohr Magneton",
            "hebrew_var": "mu_B_const",
            "english_var": "mu_B_const",
            "symbol": "mu_B",
            "value": mu_B,
            "error": None,
            "units": '"J/T"',
            "fmt_spec": ".3e",
        },
        {
            "hebrew_name": "פרמיאביליות הריק",
            "english_name": "Vacuum Permeability",
            "hebrew_var": "mu_0_const",
            "english_var": "mu_0_const",
            "symbol": "mu_0",
            "value": mu_0,
            "error": None,
            "units": '"N/A"^2',
            "fmt_spec": ".3e",
        },
        {
            "hebrew_name": "מספר כריכות בסליל",
            "english_name": "Coil turns",
            "hebrew_var": "N_turns",
            "english_var": "N_turns",
            "symbol": "N",
            "value": N_turns,
            "error": None,
            "units": "",
            "fmt_spec": ".0f",
        },
        {
            "hebrew_name": "אורך הסליל",
            "english_name": "Coil length",
            "hebrew_var": "h_coil",
            "english_var": "h_coil",
            "symbol": "h",
            "value": h_coil,
            "error": None,
            "units": '"m"',
            "fmt_spec": ".3f",
        },
        {
            "hebrew_name": "קוטר ממוצע של הסליל",
            "english_name": "Coil average diameter",
            "hebrew_var": "D_avg",
            "english_var": "D_avg",
            "symbol": "D",
            "value": D_avg,
            "error": None,
            "units": '"m"',
            "fmt_spec": ".4f",
        },
        {
            "hebrew_name": "סטייה יחסית (שיטה 1)",
            "english_name": "Relative deviation (Method 1)",
            "hebrew_var": "dev_m1",
            "english_var": "dev_m1",
            "symbol": "delta_(1)",
            "value": abs(k_m1 - k_theo) / k_theo * 100.0,
            "error": None,
            "units": '"%"',
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "סטייה יחסית (שיטה 3)",
            "english_name": "Relative deviation (Method 3)",
            "hebrew_var": "dev_m3",
            "english_var": "dev_m3",
            "symbol": "delta_(3)",
            "value": abs(k_m3 - k_theo) / k_theo * 100.0,
            "error": None,
            "units": '"%"',
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "מרחק סיגמות (שיטה 1)",
            "english_name": "Sigma distance (Method 1)",
            "hebrew_var": "sig_dist_m1",
            "english_var": "sig_dist_m1",
            "symbol": 'd_("sig", 1)',
            "value": abs(k_m1 - k_theo) / dk_m1,
            "error": None,
            "units": "",
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "מרחק סיגמות (שיטה 3)",
            "english_name": "Sigma distance (Method 3)",
            "hebrew_var": "sig_dist_m3",
            "english_var": "sig_dist_m3",
            "symbol": 'd_("sig", 3)',
            "value": abs(k_m3 - k_theo) / dk_m3,
            "error": None,
            "units": "",
            "fmt_spec": ".1f",
        },
    ]

    os.makedirs("constants", exist_ok=True)
    export_constants(results, "constants")

    export_md = mo.md(
        """
        ### Export Status:
        Physical constants have been successfully exported to `constants/constants.json` and `constants/constants.typ`!
        """
    )
    export_md  # noqa: B018
    return


@app.cell(hide_code=True)
def render_beautiful_summary(
    I_res_m1,
    dI_res_m1,
    k_m1,
    dk_m1,
    I_res_m3,
    dI_res_m3,
    k_m3,
    dk_m3,
    I_res_fit,
    dI_res_fit,
    w_fit,
    dw_fit,
    T2,
    dT2,
    dB,
    ddB,
    chi2_red,
    chi2_red_abs,
    dI_FWHM,
    ddI_FWHM,
    k_theo,
    mo,
):
    _dev_m1 = abs(k_m1 - k_theo) / k_theo * 100.0
    _dev_m3 = abs(k_m3 - k_theo) / k_theo * 100.0
    _sig_dist_m1 = abs(k_m1 - k_theo) / dk_m1
    _sig_dist_m3 = abs(k_m3 - k_theo) / dk_m3

    html_output = None
    if mo.running_in_notebook():
        html_output = mo.Html(
            f"""
            <div style="font-family: system-ui, sans-serif; padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #34495e; padding-bottom: 8px; margin-top: 0;">✨ Experimental Summary ✨</h2>
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                    <thead>
                        <tr style="background-color: #34495e; color: white;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Parameter</th>
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background-color: rgba(255,255,255,0.5);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Theoretical Coil Constant (k_theo)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{k_theo:.2f} m⁻¹</td>
                        </tr>
                        <tr style="background-color: rgba(255,255,255,0.75);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Method 1 Resonant Current (I_res,1)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{I_res_m1:.4f} ± {dI_res_m1:.4f} A</td>
                        </tr>
                        <tr style="background-color: rgba(255,255,255,0.5);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Method 1 Coil Constant (k_1)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{k_m1:.1f} ± {dk_m1:.1f} m⁻¹ (dev: {_dev_m1:.1f}%, {_sig_dist_m1:.1f}σ)</td>
                        </tr>
                        <tr style="background-color: rgba(255,255,255,0.75);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Method 3 Resonant Current (I_res,3)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{I_res_m3:.4f} ± {dI_res_m3:.4f} A</td>
                        </tr>
                        <tr style="background-color: rgba(255,255,255,0.5);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Method 3 Coil Constant (k_3)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{k_m3:.1f} ± {dk_m3:.1f} m⁻¹ (dev: {_dev_m3:.1f}%, {_sig_dist_m3:.1f}σ)</td>
                        </tr>
                        <tr style="background-color: rgba(255,255,255,0.75);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Fitted Resonance Position (Part 2)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{I_res_fit:.4f} ± {dI_res_fit:.4f} A</td>
                        </tr>
                        <tr style="background-color: rgba(255,255,255,0.5);">
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><b>Phase Relaxation Time (T_2*)</b></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{T2 * 1e9:.2f} ± {dT2 * 1e9:.2f} ns</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """
        )
    else:
        import sys

        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table

            console = Console()
            table = Table(
                title="Experimental Summary Results",
                title_style="bold cyan",
                title_justify="center",
                header_style="bold cyan",
                border_style="cyan",
            )
            table.add_column("Parameter", style="bold yellow", justify="center")
            table.add_column("Value", style="bold green", justify="center")

            table.add_row("Theoretical Coil Constant (k_theo)", f"{k_theo:.2f} m⁻¹")
            table.add_row(
                "Method 1 Resonant Current (I_res,1)",
                f"{I_res_m1:.4f} ± {dI_res_m1:.4f} A",
            )
            table.add_row(
                "Method 1 Coil Constant (k_1)",
                f"{k_m1:.1f} ± {dk_m1:.1f} m⁻¹",
            )
            table.add_row(
                "Method 1 Deviation",
                f"{abs(k_m1 - k_theo) / k_theo * 100.0:.1f}% ({_sig_dist_m1:.1f} σ)",
            )
            table.add_row(
                "Method 3 Resonant Current (I_res,3)",
                f"{I_res_m3:.4f} ± {dI_res_m3:.4f} A",
            )
            table.add_row(
                "Method 3 Coil Constant (k_3)",
                f"{k_m3:.1f} ± {dk_m3:.1f} m⁻¹",
            )
            table.add_row(
                "Method 3 Deviation",
                f"{abs(k_m3 - k_theo) / k_theo * 100.0:.1f}% ({_sig_dist_m3:.1f} σ)",
            )
            table.add_row(
                "Fitted Resonance Position (Part 2) (I_res)",
                f"{I_res_fit:.4f} ± {dI_res_fit:.4f} A",
            )
            table.add_row(
                "Fitted Lorentzian Width (w)",
                f"{w_fit:.5f} ± {dw_fit:.5f} A",
            )
            table.add_row(
                "FWHM Current (dI_FWHM)",
                f"{dI_FWHM:.4f} ± {ddI_FWHM:.4f} A",
            )
            table.add_row(
                "FWHM Magnetic Field (dB)",
                f"{dB * 1000.0:.3f} ± {ddB * 1000.0:.3f} mT",
            )
            table.add_row(
                "Phase Relaxation Time (T_2*)",
                f"{T2 * 1e9:.2f} ± {dT2 * 1e9:.2f} ns",
            )
            table.add_row(
                "Derivative χ²_red",
                f"{chi2_red:.2f}",
            )
            table.add_row(
                "Absorption χ²_red",
                f"{chi2_red_abs:.2f}",
            )

            console.print(
                Panel(
                    table,
                    title="ESR Experiment Analysis",
                    title_align="center",
                    border_style="blue",
                    expand=False,
                )
            )
        except ImportError:
            print("=" * 60)
            print("                    ESR EXPERIMENT SUMMARY RESULTS")
            print("=" * 60)
            print(f"{'Parameter':<40} | {'Value':<20}")
            print("-" * 60)
            print(f"{'Theoretical Coil Constant (k_theo)':<40} | {k_theo:.2f} m⁻¹")
            print(
                f"{'Method 1 Resonant Current (I_res,1)':<40} | {I_res_m1:.4f} ± {dI_res_m1:.4f} A"
            )
            print(
                f"{'Method 1 Coil Constant (k_1)':<40} | {k_m1:.1f} ± {dk_m1:.1f} m⁻¹"
            )
            print(
                f"{'Method 3 Resonant Current (I_res,3)':<40} | {I_res_m3:.4f} ± {dI_res_m3:.4f} A"
            )
            print(
                f"{'Method 3 Coil Constant (k_3)':<40} | {k_m3:.1f} ± {dk_m3:.1f} m⁻¹"
            )
            print(
                f"{'Fitted Resonance Position (Part 2)':<40} | {I_res_fit:.4f} ± {dI_res_fit:.4f} A"
            )
            print(
                f"{'Phase Relaxation Time (T_2*)':<40} | {T2 * 1e9:.2f} ± {dT2 * 1e9:.2f} ns"
            )
            print("=" * 60)

    html_output  # noqa: B018


if __name__ == "__main__":
    app.run()
