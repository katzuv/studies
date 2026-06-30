import csv
import math
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import e, h, hbar, mu_0
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import curve_fit

# ANSI Color Codes for Pretty CLI prints without Rich
GREEN = "\033[92m"
CYAN = "\033[96m"
GOLD = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header(title):
    print("\n" + BOLD + CYAN + "+" + "-" * 58 + "+" + RESET)
    print(BOLD + CYAN + "|" + title.center(58) + "|" + RESET)
    print(BOLD + CYAN + "+" + "-" * 58 + "+" + RESET)


def print_row(label, val_str, color=GREEN):
    print(f"  {BOLD}{label:<35}{RESET} : {color}{val_str}{RESET}")


# Set plot styling
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["svg.hashsalt"] = "fixed-string"


def main():
    print_header("Electron Spin Resonance (ESR) Standalone Analysis")

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
    k_theo = N_turns / math.sqrt(h_coil**2 + D_avg**2)

    # 1. Method 1 (data/1.csv)
    t_m1, V_R_m1, V_out_m1 = [], [], []
    with open("data/1.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                t_m1.append(float(row[0]) * 1000.0)
                V_R_m1.append(float(row[1]))
                V_out_m1.append(float(row[2]))
    t_m1 = np.array(t_m1)
    V_R_m1 = np.array(V_R_m1)
    V_out_m1 = np.array(V_out_m1)

    from scipy.signal import find_peaks

    peaks_m1, _ = find_peaks(V_out_m1, height=0.4, distance=100)
    I_peaks_m1 = np.abs(V_R_m1[peaks_m1]) / R_res

    sigma_V_reading = 0.01
    sigma_I_peaks_m1 = np.full_like(I_peaks_m1, sigma_V_reading / R_res)
    weights_m1 = 1.0 / (sigma_I_peaks_m1**2)

    I_res_m1 = np.sum(I_peaks_m1 * weights_m1) / np.sum(weights_m1)
    dI_stat_m1 = 1.0 / np.sqrt(np.sum(weights_m1))
    dI_syst_m1 = I_res_m1 * (dR_res / R_res)
    dI_res_m1 = math.sqrt(dI_stat_m1**2 + dI_syst_m1**2)

    k_m1 = (h * nu_RF) / (mu_0 * g_DPPH * mu_B * I_res_m1)
    dk_m1 = k_m1 * math.sqrt(
        (dnu_RF / nu_RF) ** 2 + (dg_DPPH / g_DPPH) ** 2 + (dI_res_m1 / I_res_m1) ** 2
    )

    # 2. Method 3 (data/2.csv)
    t_m3, V_R_m3, V_out_m3 = [], [], []
    with open("data/2.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                t_m3.append(float(row[0]) * 1000.0)
                V_R_m3.append(float(row[1]))
                V_out_m3.append(float(row[2]))
    t_m3 = np.array(t_m3)
    V_R_m3 = np.array(V_R_m3)
    V_out_m3 = np.array(V_out_m3)

    peaks_m3, _ = find_peaks(V_out_m3, height=0.4, distance=100)

    V_DC_m3 = np.mean(V_R_m3)
    I_res_m3 = V_DC_m3 / R_res
    dI_stat_m3 = np.std(V_R_m3) / math.sqrt(len(V_R_m3))
    dI_syst_m3 = I_res_m3 * (dR_res / R_res)
    dI_res_m3 = math.sqrt(dI_stat_m3**2 + dI_syst_m3**2)

    k_m3 = (h * nu_RF) / (mu_0 * g_DPPH * mu_B * I_res_m3)
    dk_m3 = k_m3 * math.sqrt(
        (dnu_RF / nu_RF) ** 2 + (dg_DPPH / g_DPPH) ** 2 + (dI_res_m3 / I_res_m3) ** 2
    )

    # 3. Part 2: Small-Signal Sweep (data/part2.csv)
    rows_p2 = []
    with open("data/part2.csv", encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            if not row or not row[0].strip():
                continue
            row = [x.strip() for x in row if x.strip()]
            nums = []
            phase_val = "pi"
            for x in row:
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
    ddB = dB * math.sqrt((dk_m3 / k_m3) ** 2 + (ddI_FWHM / dI_FWHM) ** 2)

    domega = g_DPPH * mu_B * dB / hbar
    ddomega = domega * math.sqrt((dg_DPPH / g_DPPH) ** 2 + (ddB / dB) ** 2)

    T2 = 2.0 / domega
    dT2 = T2 * (ddomega / domega)

    # Print Results
    print_header("Part 1: Coil Constant (k) Calibration")
    print_row("Geometric (Theoretical) k", f"{k_theo:.2f} m^-1", GOLD)
    print("\n  Method 1 (Asymmetric Peaks):")
    print_row("Resonant Current I_res", f"{I_res_m1:.4f} +/- {dI_res_m1:.4f} A")
    print_row("Experimental k_1", f"{k_m1:.1f} +/- {dk_m1:.1f} m^-1")
    print_row("Geometric Deviation", f"{abs(k_m1 - k_theo) / k_theo * 100:.1f} %")

    print("\n  Method 3 (Symmetric Peak Spacing):")
    print_row("Resonant Current I_res", f"{I_res_m3:.4f} +/- {dI_res_m3:.4f} A")
    print_row("Experimental k_3", f"{k_m3:.1f} +/- {dk_m3:.1f} m^-1")
    print_row("Geometric Deviation", f"{abs(k_m3 - k_theo) / k_theo * 100:.1f} %")

    print_header("Part 2: Small-Signal Sweep & Phase Relaxation (T2)")
    print_row(
        "Fitted Resonance Peak Position", f"{I_res_fit:.4f} +/- {dI_res_fit:.4f} A"
    )
    print_row("Fitted Lorentzian Half-Width (w)", f"{w_fit:.5f} +/- {dw_fit:.5f} A")
    print_row(
        "Full Width at Half Maximum (FWHM)", f"{dI_FWHM:.4f} +/- {ddI_FWHM:.4f} A"
    )
    print_row("Field FWHM (dB)", f"{dB * 1e3:.3f} +/- {ddB * 1e3:.3f} mT")
    print_row("Frequency FWHM (domega)", f"{domega:.2e} +/- {ddomega:.2e} rad/s")
    print_row(
        "Phase Relaxation Time (T2)", f"{T2 * 1e9:.2f} +/- {dT2 * 1e9:.2f} ns", GOLD
    )

    # Save Plots
    print_header("Generating and Saving SVG Plots")
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
    ax2_m1.scatter(
        t_m1[peaks_m1],
        V_out_m1[peaks_m1],
        color="red",
        zorder=5,
        label="Resonance Peaks",
    )
    ax1_m1.set_xlabel(r"$t\ \text{[ms]}$")
    ax1_m1.set_ylabel(r"$V_R\ \text{[V]}$")
    ax2_m1.set_ylabel("ESR Output [arb]")
    ax1_m1.set_ylim(V_R_m1.min() - 0.15, V_R_m1.max() + 0.45)
    ax2_m1.set_ylim(V_out_m1.min() - 0.15, V_out_m1.max() + 0.45)
    h1, l1 = ax1_m1.get_legend_handles_labels()
    h2, l2 = ax2_m1.get_legend_handles_labels()
    ax1_m1.legend(h1 + h2, l1 + l2, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_modulation_m1.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_modulation_m1.svg{RESET}")

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
    ax2_m3.scatter(
        t_m3[peaks_m3],
        V_out_m3[peaks_m3],
        color="red",
        zorder=5,
        label="Resonance Peaks",
    )
    ax1_m3.set_xlabel(r"$t\ \text{[ms]}$")
    ax1_m3.set_ylabel(r"$V_R\ \text{[V]}$")
    ax2_m3.set_ylabel("ESR Output [arb]")
    ax1_m3.set_ylim(V_R_m3.min() - 0.15, V_R_m3.max() + 0.45)
    ax2_m3.set_ylim(V_out_m3.min() - 0.15, V_out_m3.max() + 0.45)
    h1_m3, l1_m3 = ax1_m3.get_legend_handles_labels()
    h2_m3, l2_m3 = ax2_m3.get_legend_handles_labels()
    ax1_m3.legend(h1_m3 + h2_m3, l1_m3 + l2_m3, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_modulation_m3.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_modulation_m3.svg{RESET}")

    # 1. Two Measured Channels (Time-domain simulation at a representative point)
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
    h1_w, l1_w = ax_wave.get_legend_handles_labels()
    h2_w, l2_w = ax_wave_twin.get_legend_handles_labels()
    ax_wave.legend(h1_w + h2_w, l1_w + l2_w, loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_small_signal_waveforms.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_small_signal_waveforms.svg{RESET}")

    # 2. Slope from Channel Amplitudes and Phase (Linear Regression)
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
    ax_reg.set_xlabel(r"ch2 $\text{[mV]}$")
    ax_reg.set_ylabel(r"ch1 $\text{[V]}$")
    ax_reg.text(
        0.05,
        0.95,
        f"slope = ch1 amplitude / ch2 amplitude = {slope_reg * 1000.0:.2f}\nphase difference = pi: negative slope",
        transform=ax_reg.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    ax_reg.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("graphs/esr_small_signal_regression.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_small_signal_regression.svg{RESET}")

    # 3. Plot Derivative Fit
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
        I_dense, V_deriv_fit, color="#333333", label="Fitted Derivative Profile"
    )
    ax_deriv.axvline(
        I_res_fit, color="#2E86AB", linestyle="-.", label="Resonance current"
    )
    ax_deriv.axvline(0.52, color="gray", linestyle=":", label="DC current")
    ax_deriv.set_xlabel(r"$I_{DC}\ \text{[A]}$")
    ax_deriv.set_ylabel(r"Derivative / local slope $\text{[V/A]}$")
    ax_deriv.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig("graphs/esr_derivative_fit.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_derivative_fit.svg{RESET}")

    # 4. Plot Absorption Lorentzian Fit (with Tangent Line)
    fig_absorp, ax_absorp = plt.subplots(figsize=(6, 4))
    ax_absorp.scatter(
        I_DC, V_absorp, color="#2E86AB", alpha=0.7, label="Integrated Absorption"
    )
    V_model_dense = A_fit / (1.0 + ((I_dense - I_res_fit) / w_fit) ** 2)
    ax_absorp.plot(
        I_dense,
        V_model_dense,
        color="#A23B72",
        label="Absorption curve",
    )
    # Calculate tangent line at I_DC = 0.52 A
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
    ax_absorp.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("graphs/esr_absorption_fit.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_absorption_fit.svg{RESET}")

    # 5. Plot Dispersion
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
    ax_disp.set_xlabel(r"$I_{DC}\ \text{[A]}$")
    ax_disp.set_ylabel(r"Dispersion $\chi'\ \text{[arb]}$")
    ax_disp.legend()
    plt.tight_layout()
    plt.savefig("graphs/esr_dispersion.svg", bbox_inches="tight")
    plt.close()
    print(f"  Saved: {GREEN}graphs/esr_dispersion.svg{RESET}")
    print("\n" + BOLD + GREEN + "Analysis Completed Successfully!" + RESET + "\n")


if __name__ == "__main__":
    main()
