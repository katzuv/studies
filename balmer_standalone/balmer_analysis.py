import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
from scipy.constants import c, e, epsilon_0, h, m_e

# Make SVG generation deterministic
plt.rcParams["svg.hashsalt"] = "fixed-string"


# ==========================================
# 1. UTILITY FUNCTIONS
# ==========================================


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
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.tick_params(axis="both", which="major", labelsize=9)


# Wavelength mapping helpers
def get_theory_lambda(line_id):
    theory_map = {
        "red": 656.27,
        "blue-green": 486.13,
        "green": 486.13,
        "blue": 434.05,
        "violet": 410.17,
    }
    line_str = str(line_id).strip().lower()
    if line_str in theory_map:
        return theory_map[line_str]

    try:
        val = float(line_str)
        balmer_wavs = [656.27, 486.13, 434.05, 410.17]
        closest_wav = min(balmer_wavs, key=lambda w: abs(w - val))
        if abs(closest_wav - val) < 30.0:
            return closest_wav
    except ValueError:
        pass
    return np.nan


def get_graph_reference_lambda(line_id):
    theory_map = {
        "red": 657.0,
        "blue-green": 486.0,
        "green": 486.0,
        "blue": 434.0,
        "violet": 410.0,
    }
    line_str = str(line_id).strip().lower()
    if line_str in theory_map:
        return theory_map[line_str]

    try:
        val = float(line_str)
        graph_wavs = [657.0, 486.0, 434.0, 410.0]
        closest_wav = min(graph_wavs, key=lambda w: abs(w - val))
        if abs(closest_wav - val) < 30.0:
            return closest_wav
    except ValueError:
        pass
    return np.nan


def get_quantum_n(line_id):
    quantum_ns = {
        "red": 3,
        "blue-green": 4,
        "green": 4,
        "blue": 5,
        "violet": 6,
    }
    line_str = str(line_id).strip().lower()
    if line_str in quantum_ns:
        return quantum_ns[line_str]

    try:
        ref_wav = get_graph_reference_lambda(line_id)
        if not np.isnan(ref_wav):
            balmer_wavs = [656.27, 486.13, 434.05, 410.17]
            closest_wav = min(balmer_wavs, key=lambda w: abs(w - ref_wav))
            balmer_n = {656.27: 3, 486.13: 4, 434.05: 5, 410.17: 6}
            return balmer_n[closest_wav]
    except ValueError:
        pass
    return np.nan


def get_line_color(line_id):
    color_map = {
        "red": "Red",
        "blue-green": "Blue-Green",
        "green": "Blue-Green",
        "blue": "Blue",
        "violet": "Violet",
    }
    line_str = str(line_id).strip().lower()
    if line_str in color_map:
        return color_map[line_str]

    try:
        val = float(line_str)
        balmer_wavs = [656.27, 486.13, 434.05, 410.17]
        closest_wav = min(balmer_wavs, key=lambda w: abs(w - val))
        wav_colors = {
            656.27: "Red",
            486.13: "Blue-Green",
            434.05: "Blue",
            410.17: "Violet",
        }
        if abs(closest_wav - val) < 30.0:
            return wav_colors[closest_wav]
    except ValueError:
        pass
    return "Unknown"


# ==========================================
# 2. MAIN EXECUTION
# ==========================================


def main():
    print("==================================================")
    print("     Balmer Series Experiment Data Analysis       ")
    print("==================================================")

    # 2.1 Setup Paths
    try:
        _curr = Path(__file__).resolve()
        exp_dir = _curr.parent
    except NameError:
        exp_dir = Path(".")
    data_dir = exp_dir / "data"

    # Default parameters
    prism_alpha = 60.0  # deg
    prism_alpha_hg = 60.0  # deg
    lines_density = 500.0  # lines/mm

    # 2.2 Load Helium Calibration Data
    he_path = data_dir / "helium_prism.txt"
    if he_path.exists():
        he_data = np.atleast_2d(np.loadtxt(he_path))
    else:
        raise FileNotFoundError(f"Helium calibration data not found at {he_path}")

    he_lambdas = he_data[:, 0]
    he_betas = he_data[:, 1]
    he_dbetas = he_data[:, 2]

    _alpha_rad = np.radians(prism_alpha)
    _betas_rad = np.radians(he_betas)
    _dbetas_rad = np.radians(he_dbetas)

    he_ns = np.sin((_alpha_rad + _betas_rad) / 2.0) / np.sin(_alpha_rad / 2.0)
    he_dns = (
        np.cos((_alpha_rad + _betas_rad) / 2.0)
        * _dbetas_rad
        / (2.0 * np.sin(_alpha_rad / 2.0))
    )

    # 2.3 Fit Cauchy Formula
    def cauchy_model(lam, A, B):
        return A + B / (lam**2)

    fit_res = physics_fit(cauchy_model, he_lambdas, he_ns, he_dns)
    A_fit, B_fit = fit_res.params
    dA_fit, dB_fit = fit_res.errors

    print("\n--- Part 1: Cauchy Calibration (Helium Lines) ---")
    print(f"Cauchy Parameter A: {A_fit:.6f} +/- {dA_fit:.6f}")
    print(f"Cauchy Parameter B: {B_fit:.2f} +/- {dB_fit:.2f} nm^2")
    print(f"Reduced Chi^2:      {fit_res.chi_red:.3f}")

    # 2.4 Plot Calibration Curve
    graphs_dir = exp_dir / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    # Curved Cauchy Dispersion plot
    ax1.errorbar(
        he_lambdas,
        he_ns,
        yerr=he_dns,
        fmt="none",
        ecolor="gray",
        capsize=3,
        zorder=1,
    )
    he_colors = {
        707: "Red",
        706: "Red",
        668: "Red",
        667: "Red",
        588: "Yellow",
        587: "Yellow",
        501: "Green",
        492: "Blue-Green",
        472: "Blue",
        471: "Blue",
        448: "Blue",
        447: "Blue",
        389: "Violet",
        388: "Violet",
    }
    display_colors = {
        "Red": "#D32F2F",
        "Yellow": "#FBC02D",
        "Green": "#388E3C",
        "Blue-Green": "#0097A7",
        "Blue": "#1976D2",
        "Violet": "#7B1FA2",
    }
    for lam, n_val in zip(he_lambdas, he_ns, strict=True):
        name = he_colors.get(int(round(lam)), "gray")
        dot_color = display_colors.get(name, "gray")
        ax1.scatter(lam, n_val, color=dot_color, edgecolors="black", s=60, zorder=2)
        ax1.text(
            lam,
            n_val + 0.0008,
            name,
            fontsize=8,
            color=dot_color,
            fontweight="bold",
            ha="center",
            va="bottom",
        )

    l_grid = np.linspace(400, 750, 200)
    ax1.plot(
        l_grid,
        cauchy_model(l_grid, A_fit, B_fit),
        color="#C73E1D",
        label="Cauchy Fit",
        zorder=1,
    )
    set_style(ax1, xlabel=r"$\lambda \ \text{[nm]}$", ylabel=r"Refractive Index $n$")
    ax1.set_ylim(min(he_ns) - 0.005, max(he_ns) + 0.005)
    ax1.legend()

    # Linearized Plot: n vs 1/lambda^2
    inv_lam_sq = 1.0 / (he_lambdas**2)
    inv_lam_sq_grid = 1.0 / (l_grid**2)
    ax2.errorbar(
        inv_lam_sq,
        he_ns,
        yerr=he_dns,
        fmt="none",
        ecolor="gray",
        capsize=3,
        zorder=1,
    )
    for lam, inv_lam_val, _n_val in zip(he_lambdas, inv_lam_sq, he_ns, strict=True):
        name = he_colors.get(int(round(lam)), "gray")
        dot_color = display_colors.get(name, "gray")
        ax2.scatter(
            inv_lam_val, _n_val, color=dot_color, edgecolors="black", s=60, zorder=2
        )
        ax2.text(
            inv_lam_val,
            _n_val + 0.0008,
            name,
            fontsize=8,
            color=dot_color,
            fontweight="bold",
            ha="center",
            va="bottom",
        )

    ax2.plot(
        inv_lam_sq_grid,
        A_fit + B_fit * inv_lam_sq_grid,
        color="#C73E1D",
        label="Linear Cauchy Fit",
        zorder=1,
    )
    set_style(
        ax2,
        xlabel=r"$1/\lambda^2 \ \text{[nm}^{-2}\text{]}$",
        ylabel=r"Refractive Index $n$",
    )
    ax2.set_ylim(min(he_ns) - 0.005, max(he_ns) + 0.005)
    ax2.legend()

    # Residuals plot
    _residuals = he_ns - cauchy_model(he_lambdas, A_fit, B_fit)
    ax3.errorbar(
        he_lambdas,
        _residuals,
        yerr=he_dns,
        fmt="o",
        color="#A23B72",
        capsize=3,
    )
    ax3.axhline(0, color="gray", linestyle="--")
    set_style(
        ax3,
        xlabel=r"$\lambda \ \text{[nm]}$",
        ylabel=r"Residuals $n - n_{\text{fit}}$",
    )

    plt.tight_layout()
    plt.savefig(graphs_dir / "helium_calibration.svg", format="svg")
    plt.close()
    print("Calibration graph saved to graphs/helium_calibration.svg")

    # 2.5 Verify with Mercury Green Line
    hg_path = data_dir / "mercury_prism.txt"
    if hg_path.exists():
        mercury_data = np.atleast_2d(np.loadtxt(hg_path))
        lam_ref_hg = mercury_data[0, 0]
        beta_hg = mercury_data[0, 1]
        dbeta_hg = mercury_data[0, 2]

        _alpha_hg_rad = np.radians(prism_alpha_hg)
        _beta_hg_rad = np.radians(beta_hg)
        _dbeta_hg_rad = np.radians(dbeta_hg)

        _n_hg = np.sin((_alpha_hg_rad + _beta_hg_rad) / 2.0) / np.sin(
            _alpha_hg_rad / 2.0
        )
        _dn_hg = (
            np.cos((_alpha_hg_rad + _beta_hg_rad) / 2.0)
            * _dbeta_hg_rad
            / (2.0 * np.sin(_alpha_hg_rad / 2.0))
        )

        def calculate_lambda(A_param, B_param, n_param):
            return np.sqrt(B_param / (n_param - A_param))

        lam_pred_hg = calculate_lambda(A_fit, B_fit, _n_hg)
        dlam_pred_hg = propagate_error(
            calculate_lambda, [A_fit, B_fit, _n_hg], [dA_fit, dB_fit, _dn_hg]
        )

        print("\n--- Part 2: Calibration Verification (Mercury Green Line) ---")
        print(f"Reference Wavelength:  {lam_ref_hg:.2f} nm")
        print(f"Measured Angle beta:   {beta_hg:.3f} +/- {dbeta_hg:.3f} deg")
        print(f"Calculated Ref. Index: {_n_hg:.5f} +/- {_dn_hg:.5f}")
        print(f"Calculated Wavelength: {lam_pred_hg:.2f} +/- {dlam_pred_hg:.2f} nm")
        print(f"Absolute Difference:   {abs(lam_pred_hg - lam_ref_hg):.3f} nm")
    else:
        print("\nMercury data file not found, skipping Part 2.")

    # 2.6 Analyze Hydrogen Lines - Prism Method
    hp_path = data_dir / "hydrogen_prism.txt"
    prism_results = []
    if hp_path.exists():
        _lines = []
        with open(hp_path, encoding="utf-8") as _f:
            for line in _f:
                line = line.strip()
                if line and not line.startswith("#"):
                    _lines.append(line.split())

        for tokens in _lines:
            if len(tokens) >= 5:
                _line = tokens[0]
                _color_name = tokens[1]
                _theory_val = float(tokens[2])
                _beta = float(tokens[3])
                _dbeta = float(tokens[4])
            else:
                _line = tokens[0]
                _color_name = get_line_color(_line)
                _theory_val = get_theory_lambda(_line)
                _beta = float(tokens[1])
                _dbeta = float(tokens[2])

            _beta_rad = np.radians(_beta)
            _dbeta_rad = np.radians(_dbeta)

            _n = np.sin((_alpha_rad + _beta_rad) / 2.0) / np.sin(_alpha_rad / 2.0)
            _dn = (
                np.cos((_alpha_rad + _beta_rad) / 2.0)
                / (2.0 * np.sin(_alpha_rad / 2.0))
            ) * _dbeta_rad

            def get_lam(A_param, B_param, n_val):
                return np.sqrt(B_param / (n_val - A_param))

            _lam = get_lam(A_fit, B_fit, _n)
            _dlam = propagate_error(get_lam, [A_fit, B_fit, _n], [dA_fit, dB_fit, _dn])

            _ref = get_graph_reference_lambda(_line)
            _diff = _lam - _ref if not np.isnan(_ref) else np.nan
            _pct_diff = (_diff / _ref) * 100.0 if not np.isnan(_ref) else np.nan
            _sigma_dist = (
                abs(_lam - _ref) / _dlam if not np.isnan(_ref) and _dlam > 0 else np.nan
            )

            prism_results.append(
                {
                    "Line": _line,
                    "Color": _color_name,
                    "Beta (deg)": _beta,
                    "Refractive Index n": _n,
                    "Calculated Wavelength (nm)": _lam,
                    "Uncertainty (nm)": _dlam,
                    "Reference (nm)": _ref,
                    "Theory (nm)": _theory_val,
                    "Difference (nm)": _diff,
                    "Percent Difference (%)": _pct_diff,
                    "Sigma Distance": _sigma_dist,
                }
            )
        df_prism = pd.DataFrame(prism_results)
        print("\n--- Part 3: Hydrogen Lines - Prism Method ---")
        print(df_prism.round(4).to_string(index=False))
    else:
        df_prism = pd.DataFrame()
        print("\nHydrogen prism data file not found, skipping Part 3.")

    # 2.7 Analyze Hydrogen Lines - Grating Method
    hg_grating_path = data_dir / "hydrogen_grating.txt"
    grating_results = []
    d_grating = 1e6 / lines_density
    if hg_grating_path.exists():
        _lines = []
        with open(hg_grating_path, encoding="utf-8") as _f:
            for line in _f:
                line = line.strip()
                if line and not line.startswith("#"):
                    _lines.append(line.split())

        for tokens in _lines:
            if len(tokens) >= 7:
                _line = tokens[0]
                _color_name = tokens[1]
                _theory_val = float(tokens[2])
                _m = int(tokens[3])
                _bp = float(tokens[4])
                _bm = float(tokens[5])
                _db = float(tokens[6])
            else:
                _line = tokens[0]
                _color_name = get_line_color(_line)
                _theory_val = get_theory_lambda(_line)
                _m = int(tokens[1])
                _bp = float(tokens[2])
                _bm = float(tokens[3])
                _db = float(tokens[4])

            _bp_rad = np.radians(_bp)
            _bm_rad = np.radians(_bm)
            _db_rad = np.radians(_db)

            def get_i0(bp_val, bm_val):
                num = np.sin(bp_val) - np.sin(bm_val)
                den = 2.0 - np.cos(bp_val) - np.cos(bm_val)
                return np.arctan2(num, den)

            _i0_rad = get_i0(_bp_rad, _bm_rad)
            _di0_rad = propagate_error(get_i0, [_bp_rad, _bm_rad], [_db_rad, _db_rad])

            def get_lambda_grating(bp_val, bm_val, d_val, m_val=_m):
                i0_val = get_i0(bp_val, bm_val)
                return (
                    2.0 * d_val * np.sin(bp_val / 2.0) * np.cos(i0_val + bp_val / 2.0)
                ) / m_val

            _lam = get_lambda_grating(_bp_rad, _bm_rad, d_grating)
            _dlam = propagate_error(
                get_lambda_grating,
                [_bp_rad, _bm_rad, d_grating],
                [_db_rad, _db_rad, 0.0],
            )

            _ref = get_graph_reference_lambda(_line)
            _diff = _lam - _ref if not np.isnan(_ref) else np.nan
            _pct_diff = (_diff / _ref) * 100.0 if not np.isnan(_ref) else np.nan
            _sigma_dist = (
                abs(_lam - _ref) / _dlam if not np.isnan(_ref) and _dlam > 0 else np.nan
            )

            grating_results.append(
                {
                    "Line": _line,
                    "Color": _color_name,
                    "Beta+ (deg)": _bp,
                    "Beta- (deg)": _bm,
                    "Incidence i0 (deg)": np.degrees(_i0_rad),
                    "di0 (deg)": np.degrees(_di0_rad),
                    "Calculated Wavelength (nm)": _lam,
                    "Uncertainty (nm)": _dlam,
                    "Reference (nm)": _ref,
                    "Theory (nm)": _theory_val,
                    "Difference (nm)": _diff,
                    "Percent Difference (%)": _pct_diff,
                    "Sigma Distance": _sigma_dist,
                }
            )
        df_grating = pd.DataFrame(grating_results)
        print("\n--- Part 4: Hydrogen Lines - Grating Method ---")
        print(df_grating.round(4).to_string(index=False))
    else:
        df_grating = pd.DataFrame()
        print("\nHydrogen grating data file not found, skipping Part 4.")

    # 2.8 Rydberg Constant Calculation
    R_inf_theo = (m_e * (e**4)) / (8.0 * (epsilon_0**2) * (h**3) * c)

    def calc_R(lam_nm, n):
        factor = 0.25 - 1.0 / (n**2)
        return 1.0 / (lam_nm * 1e-9 * factor)

    def calc_R_err(lam_nm, dlam_nm, n):
        R_val = calc_R(lam_nm, n)
        return R_val * (dlam_nm / lam_nm)

    prism_lookup = {str(r["Line"]): r for r in prism_results}
    grating_lookup = {str(r["Line"]): r for r in grating_results}
    all_lines = sorted(
        list(set(prism_lookup.keys()) | set(grating_lookup.keys())), key=str
    )

    results_R = []
    for _line in all_lines:
        _n_q = get_quantum_n(_line)

        _R_prism = np.nan
        _dR_prism = np.nan
        _disc_prism = np.nan
        _sigma_prism = np.nan
        if _line in prism_lookup:
            _p = prism_lookup[_line]
            _R_prism = calc_R(_p["Calculated Wavelength (nm)"], _n_q)
            _dR_prism = calc_R_err(
                _p["Calculated Wavelength (nm)"], _p["Uncertainty (nm)"], _n_q
            )
            _disc_prism = ((_R_prism - R_inf_theo) / R_inf_theo) * 100.0
            if _dR_prism > 0:
                _sigma_prism = abs(_R_prism - R_inf_theo) / _dR_prism

        _R_grating = np.nan
        _dR_grating = np.nan
        _disc_grating = np.nan
        _sigma_grating = np.nan
        if _line in grating_lookup:
            _g = grating_lookup[_line]
            _R_grating = calc_R(_g["Calculated Wavelength (nm)"], _n_q)
            _dR_grating = calc_R_err(
                _g["Calculated Wavelength (nm)"], _g["Uncertainty (nm)"], _n_q
            )
            _disc_grating = ((_R_grating - R_inf_theo) / R_inf_theo) * 100.0
            if _dR_grating > 0:
                _sigma_grating = abs(_R_grating - R_inf_theo) / _dR_grating

        results_R.append(
            {
                "Line": _line,
                "n": _n_q,
                "R (Prism) [m^-1]": _R_prism,
                "dR (Prism) [m^-1]": _dR_prism,
                "Discrepancy (Prism) (%)": _disc_prism,
                "Sigma Distance (Prism)": _sigma_prism,
                "R (Grating) [m^-1]": _R_grating,
                "dR (Grating) [m^-1]": _dR_grating,
                "Discrepancy (Grating) (%)": _disc_grating,
                "Sigma Distance (Grating)": _sigma_grating,
            }
        )

    df_R = pd.DataFrame(results_R)
    print("\n--- Part 5: Rydberg Constant Constants per Line ---")
    print(df_R.round(4).to_string(index=False))

    # Calculate averages
    _valid_prism = df_R.dropna(subset=["R (Prism) [m^-1]", "dR (Prism) [m^-1]"])
    if not _valid_prism.empty:
        _w_prism = 1.0 / (_valid_prism["dR (Prism) [m^-1]"] ** 2)
        R_avg_prism = np.sum(_valid_prism["R (Prism) [m^-1]"] * _w_prism) / np.sum(
            _w_prism
        )
        dR_avg_prism = 1.0 / np.sqrt(np.sum(_w_prism))
    else:
        R_avg_prism = np.nan
        dR_avg_prism = np.nan

    _valid_grating = df_R.dropna(subset=["R (Grating) [m^-1]", "dR (Grating) [m^-1]"])
    if not _valid_grating.empty:
        _w_grating = 1.0 / (_valid_grating["dR (Grating) [m^-1]"] ** 2)
        R_avg_grating = np.sum(
            _valid_grating["R (Grating) [m^-1]"] * _w_grating
        ) / np.sum(_w_grating)
        dR_avg_grating = 1.0 / np.sqrt(np.sum(_w_grating))
    else:
        R_avg_grating = np.nan
        dR_avg_grating = np.nan

    print("\n--- Weighted Average Rydberg Constants ---")
    print(f"Theoretical Bohr Prediction: {R_inf_theo:.4e} m^-1")
    if not np.isnan(R_avg_prism):
        prism_disc = abs(R_avg_prism - R_inf_theo) / R_inf_theo * 100.0
        print(
            f"Prism Method average R:      {R_avg_prism:.4e} +/- {dR_avg_prism:.4e} m^-1 (Discrepancy: {prism_disc:.3f}%)"
        )
    if not np.isnan(R_avg_grating):
        grating_disc = abs(R_avg_grating - R_inf_theo) / R_inf_theo * 100.0
        print(
            f"Grating Method average R:    {R_avg_grating:.4e} +/- {dR_avg_grating:.4e} m^-1 (Discrepancy: {grating_disc:.3f}%)"
        )

    # 2.9 Export constants to JSON
    constants_data = {
        "cauchy_a": {
            "value": float(A_fit),
            "error": float(dA_fit),
            "units": "",
        },
        "cauchy_b": {
            "value": float(B_fit),
            "error": float(dB_fit),
            "units": "nm^2",
        },
        "rydberg_prism": {
            "value": float(R_avg_prism) if not np.isnan(R_avg_prism) else None,
            "error": float(dR_avg_prism) if not np.isnan(dR_avg_prism) else None,
            "units": "m^(-1)",
        },
        "rydberg_grating": {
            "value": float(R_avg_grating) if not np.isnan(R_avg_grating) else None,
            "error": float(dR_avg_grating) if not np.isnan(dR_avg_grating) else None,
            "units": "m^(-1)",
        },
    }
    constants_dir = exp_dir / "constants"
    constants_dir.mkdir(parents=True, exist_ok=True)
    with open(constants_dir / "constants.json", "w", encoding="utf-8") as _f:
        json.dump(constants_data, _f, indent=4)
    print(f"\nConstants successfully saved to {constants_dir / 'constants.json'}")
    print("==================================================")


if __name__ == "__main__":
    main()
