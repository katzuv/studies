import marimo

__generated_with = "0.23.13"
app = marimo.App(width="full", app_title="Balmer series experiment analysis")


@app.cell(hide_code=True)
def imports_and_setup():
    import sys
    from pathlib import Path

    # Find the repository root containing 'physlab'
    try:
        _curr = Path(__file__).resolve()
    except NameError:
        _curr = Path(".").resolve()

    _root = None
    for _p in [_curr] + list(_curr.parents):
        if (_p / "physlab").exists():
            _root = _p
            break
    if _root is None:
        _root = Path(".")

    sys.path.append(str(_root))

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.constants import c, e, epsilon_0, h, m_e

    from physlab.core import (
        export_constants,
        physics_fit,
        propagate_error,
        set_style,
    )

    # Make SVG generation deterministic
    plt.rcParams["svg.hashsalt"] = "fixed-string"
    return (
        Path,
        c,
        e,
        epsilon_0,
        export_constants,
        h,
        m_e,
        mo,
        np,
        pd,
        physics_fit,
        plt,
        propagate_error,
        set_style,
    )


@app.cell(hide_code=True)
def helper_functions(np):
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

    return (
        get_graph_reference_lambda,
        get_line_color,
        get_quantum_n,
        get_theory_lambda,
    )


@app.cell(hide_code=True)
def render_title():
    return


@app.cell(hide_code=True)
def interactive_controls(mo):
    # Grating lines density input
    lines_density = mo.ui.number(
        start=100.0,
        stop=2000.0,
        value=500.0,
        step=1.0,
        label="Diffraction Grating Density (lines/mm):",
    )

    # Prism apex angle input for Helium calibration
    prism_alpha = mo.ui.number(
        start=30.0,
        stop=90.0,
        value=60.0,
        step=0.01,
        label="Prism Apex Angle α for He & H (deg):",
    )

    # Prism apex angle input for Mercury verification
    prism_alpha_hg = mo.ui.number(
        start=30.0,
        stop=90.0,
        value=60.0,
        step=0.01,
        label="Prism Apex Angle α for Hg (deg):",
    )

    # Angle measurement uncertainty input
    dbeta_default = mo.ui.number(
        start=0.001,
        stop=0.5,
        value=0.073,
        step=0.001,
        label="Angle Measurement Uncertainty δβ (deg):",
    )

    # Output the controls layout as the last expression so Marimo renders it
    _controls_md = mo.md(
        f"""
    ## Experimental Setup & Calibration Controls
    Adjust the nominal parameters below according to your laboratory equipment:

    * {lines_density}
    * {prism_alpha}
    * {prism_alpha_hg} *(Use this if the measured prism apex angle was different during the Mercury verification)*
    * {dbeta_default}
    """
    )
    _controls_md  # noqa: B018
    return lines_density, prism_alpha, prism_alpha_hg


@app.cell(hide_code=True)
def load_data_files(Path, np):
    # Find the repository root or experiment directory
    try:
        _curr = Path(__file__).resolve()
    except NameError:
        _curr = Path(".").resolve()

    exp_dir = None
    for _p in [_curr] + list(_curr.parents):
        if _p.name == "06 Balmer" or (_p / "2026S/Lab4/06 Balmer").exists():
            exp_dir = _p if _p.name == "06 Balmer" else _p / "2026S/Lab4/06 Balmer"
            break
    if exp_dir is None:
        exp_dir = Path(".")

    data_dir = exp_dir / "data"

    # Fallbacks in case files don't exist
    he_fallback = np.array(
        [
            [706.52, 48.87, 0.02],
            [667.82, 49.08, 0.02],
            [587.56, 49.68, 0.02],
            [501.57, 50.67, 0.02],
            [492.19, 50.82, 0.02],
            [471.31, 51.16, 0.02],
            [447.15, 51.63, 0.02],
        ]
    )

    mercury_fallback = np.array([[546.07, 50.10, 0.02]])

    h_prism_fallback = [
        {"line_id": "Red", "beta": 49.16, "dbeta": 0.02},
        {"line_id": "Blue-Green", "beta": 50.91, "dbeta": 0.02},
        {"line_id": "Blue", "beta": 51.92, "dbeta": 0.02},
        {"line_id": "Violet", "beta": 52.52, "dbeta": 0.02},
    ]

    h_grating_fallback = [
        {
            "line_id": "Red",
            "order": 1,
            "beta_plus": 23.75,
            "beta_minus": 22.86,
            "dbeta": 0.02,
        },
        {
            "line_id": "Blue-Green",
            "order": 1,
            "beta_plus": 17.26,
            "beta_minus": 16.80,
            "dbeta": 0.02,
        },
        {
            "line_id": "Blue",
            "order": 1,
            "beta_plus": 15.34,
            "beta_minus": 14.98,
            "dbeta": 0.02,
        },
        {
            "line_id": "Violet",
            "order": 1,
            "beta_plus": 14.47,
            "beta_minus": 14.14,
            "dbeta": 0.02,
        },
    ]

    # Load Helium Calibration Data
    he_path = data_dir / "helium_prism.txt"
    if he_path.exists():
        try:
            he_data = np.atleast_2d(np.loadtxt(he_path))
        except Exception:
            he_data = np.atleast_2d(he_fallback)
    else:
        he_data = np.atleast_2d(he_fallback)

    # Load Mercury Data
    hg_path = data_dir / "mercury_prism.txt"
    if hg_path.exists():
        try:
            mercury_data = np.atleast_2d(np.loadtxt(hg_path))
        except Exception:
            mercury_data = np.atleast_2d(mercury_fallback)
    else:
        mercury_data = np.atleast_2d(mercury_fallback)

    # Load Hydrogen Prism Data
    hp_path = data_dir / "hydrogen_prism.txt"
    if hp_path.exists():
        try:
            _lines = []
            with open(hp_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        _lines.append(line.split())

            h_prism_data = []
            for tokens in _lines:
                if len(tokens) >= 5:
                    h_prism_data.append(
                        {
                            "line_id": tokens[0],
                            "color": tokens[1],
                            "theory_lambda": float(tokens[2]),
                            "beta": float(tokens[3]),
                            "dbeta": float(tokens[4]),
                        }
                    )
                elif len(tokens) == 3:
                    h_prism_data.append(
                        {
                            "line_id": tokens[0],
                            "beta": float(tokens[1]),
                            "dbeta": float(tokens[2]),
                        }
                    )
                elif len(tokens) == 2:
                    h_prism_data.append(
                        {
                            "line_id": "Unknown",
                            "beta": float(tokens[0]),
                            "dbeta": float(tokens[1]),
                        }
                    )
        except Exception:
            h_prism_data = h_prism_fallback
    else:
        h_prism_data = h_prism_fallback

    # Load Hydrogen Grating Data
    hg_grating_path = data_dir / "hydrogen_grating.txt"
    if hg_grating_path.exists():
        try:
            _lines = []
            with open(hg_grating_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        _lines.append(line.split())

            h_grating_data = []
            for tokens in _lines:
                if len(tokens) >= 7:
                    h_grating_data.append(
                        {
                            "line_id": tokens[0],
                            "color": tokens[1],
                            "theory_lambda": float(tokens[2]),
                            "order": int(tokens[3]),
                            "beta_plus": float(tokens[4]),
                            "beta_minus": float(tokens[5]),
                            "dbeta": float(tokens[6]),
                        }
                    )
                elif len(tokens) == 5:
                    h_grating_data.append(
                        {
                            "line_id": tokens[0],
                            "order": int(tokens[1]),
                            "beta_plus": float(tokens[2]),
                            "beta_minus": float(tokens[3]),
                            "dbeta": float(tokens[4]),
                        }
                    )
        except Exception:
            h_grating_data = h_grating_fallback
    else:
        h_grating_data = h_grating_fallback
    return exp_dir, h_grating_data, h_prism_data, he_data, mercury_data


@app.cell(hide_code=True)
def helium_calibration(he_data, mo, np, physics_fit, prism_alpha):
    # Wavelengths in nm
    he_lambdas = he_data[:, 0]
    he_betas = he_data[:, 1]
    he_dbetas = he_data[:, 2]

    _alpha_rad = np.radians(prism_alpha.value)
    _betas_rad = np.radians(he_betas)
    _dbetas_rad = np.radians(he_dbetas)

    # Refractive index: n = sin((alpha + beta)/2) / sin(alpha/2)
    he_ns = np.sin((_alpha_rad + _betas_rad) / 2.0) / np.sin(_alpha_rad / 2.0)

    # Propagate uncertainty to refractive index n
    he_dns = (
        np.cos((_alpha_rad + _betas_rad) / 2.0)
        * _dbetas_rad
        / (2.0 * np.sin(_alpha_rad / 2.0))
    )

    # Fit Cauchy formula: n(lambda) = A + B / lambda^2
    def cauchy_model(lam, A, B):
        return A + B / (lam**2)

    # We fit lambda in nm, n is dimensionless
    fit_res = physics_fit(cauchy_model, he_lambdas, he_ns, he_dns)
    A_fit, B_fit = fit_res.params
    dA_fit, dB_fit = fit_res.errors

    he_md = mo.md(
        rf"""
    ## Part 1: Prism Calibration (Helium Lines)
    We calculate the refractive index $\\hat{{n}}$ for each Helium line and fit the Cauchy model $\\hat{{n}}(\\lambda) = A + B/\\lambda^2$.

    **Fitted Cauchy Parameters:**
    * **$A$ (dimensionless):** {A_fit:.6f} $\\pm$ {dA_fit:.6f}
    * **$B$ ($\\text{{nm}}^2$):** {B_fit:.1f} $\\pm$ {dB_fit:.1f}
    * **Reduced $\\chi^2$:** {fit_res.chi_red:.3f}
    """
    )
    he_md  # noqa: B018
    return (
        A_fit,
        B_fit,
        cauchy_model,
        dA_fit,
        dB_fit,
        fit_res,
        he_dns,
        he_lambdas,
        he_ns,
    )


@app.cell(hide_code=True)
def plot_calibration(
    A_fit,
    B_fit,
    cauchy_model,
    exp_dir,
    fit_res,
    he_dns,
    he_lambdas,
    he_ns,
    np,
    plt,
    set_style,
):
    # Ensure graphs directory exists inside the experiment directory
    graphs_dir = exp_dir / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)

    # Calculate R^2 and get chi^2_red
    fit_y = cauchy_model(he_lambdas, A_fit, B_fit)
    ss_res = np.sum((he_ns - fit_y)**2)
    ss_tot = np.sum((he_ns - np.mean(he_ns))**2)
    r_sq = 1.0 - (ss_res / ss_tot)
    chi_red = fit_res.chi_red

    stats_text = (
        f"$R^2 = {r_sq:.6f}$\n"
        f"$\\chi^2_\\mathrm{{red}} = {chi_red:.3f}$"
    )

    # Mapping to actual display colors
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

    # 1. Plot n vs lambda (Curved Cauchy Dispersion)
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.errorbar(
        he_lambdas,
        he_ns,
        yerr=he_dns,
        fmt="none",
        ecolor="gray",
        capsize=3,
        zorder=1,
    )

    for lam, n_val in zip(he_lambdas, he_ns, strict=True):
        name = he_colors.get(int(round(lam)), "gray")
        dot_color = display_colors.get(name, "gray")
        # Plot individual colored dot
        ax1.scatter(
            lam,
            n_val,
            color=dot_color,
            edgecolors="black",
            s=60,
            zorder=2,
            label="Helium Data" if lam == he_lambdas[0] else "",
        )
        # Add color text label
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
    set_style(
        ax1, xlabel=r"$\lambda \ \text{[nm]}$", ylabel=r"Refractive Index $n$"
    )
    ax1.set_ylim(min(he_ns) - 0.005, max(he_ns) + 0.005)
    ax1.legend()
    # Add stats box
    ax1.text(
        0.95,
        0.85,
        stats_text,
        transform=ax1.transAxes,
        va="top",
        ha="right",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    plt.tight_layout()
    fig1.savefig(graphs_dir / "helium_dispersion.svg", format="svg")
    plt.close(fig1)

    # 2. Linearized Plot: n vs 1/lambda^2 (Linear Graph)
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    inv_lam_sq = 1.0 / (he_lambdas**2)
    inv_lam_sq_grid = 1.0 / (l_grid**2)

    # Plot error bars only
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
        # Plot individual colored dot
        ax2.scatter(
            inv_lam_val,
            _n_val,
            color=dot_color,
            edgecolors="black",
            s=60,
            zorder=2,
        )
        # Add color text label
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
    # Add stats box
    ax2.text(
        0.05,
        0.95,
        stats_text,
        transform=ax2.transAxes,
        va="top",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    plt.tight_layout()
    fig2.savefig(graphs_dir / "helium_linearized.svg", format="svg")
    plt.close(fig2)

    # 3. Residuals plot
    fig3, ax3 = plt.subplots(figsize=(7, 5))
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
        ylabel=r"Residuals $n - n_{\mathrm{fit}}$",
    )
    # Add stats box
    ax3.text(
        0.95,
        0.95,
        stats_text,
        transform=ax3.transAxes,
        va="top",
        ha="right",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    plt.tight_layout()
    fig3.savefig(graphs_dir / "helium_residuals.svg", format="svg")
    plt.close(fig3)
    return


@app.cell(hide_code=True)
def mercury_verification(
    A_fit,
    B_fit,
    dA_fit,
    dB_fit,
    mercury_data,
    mo,
    np,
    prism_alpha_hg,
    propagate_error,
):
    try:
        lam_ref = mercury_data[0, 0]
        beta_val = mercury_data[0, 1]
        dbeta_val = mercury_data[0, 2]
    except Exception:
        lam_ref = 546.07
        beta_val = 50.10
        dbeta_val = 0.02

    # Convert angle to n using the Hg specific prism apex angle
    _alpha_rad = np.radians(prism_alpha_hg.value)
    _beta_rad = np.radians(beta_val)
    _dbeta_rad = np.radians(dbeta_val)

    _n_val = np.sin((_alpha_rad + _beta_rad) / 2.0) / np.sin(_alpha_rad / 2.0)
    _dn_dbeta = np.cos((_alpha_rad + _beta_rad) / 2.0) / (
        2.0 * np.sin(_alpha_rad / 2.0)
    )
    _dn_val = _dn_dbeta * _dbeta_rad

    # Wavelength lambda = sqrt(B / (n - A))
    def calculate_lambda(A_param, B_param, n_param):
        return np.sqrt(B_param / (n_param - A_param))

    lam_pred = calculate_lambda(A_fit, B_fit, _n_val)

    # Propagate errors of A, B, and n
    dlam_pred = propagate_error(
        calculate_lambda, [A_fit, B_fit, _n_val], [dA_fit, dB_fit, _dn_val]
    )

    sigma_dist = abs(lam_pred - lam_ref) / dlam_pred

    is_success = (
        "SUCCESS" if sigma_dist < 2.0 else "WARNING"
    )

    hg_md = mo.md(
        rf"""
    ## Part 2: Calibration Verification (Mercury Green Line)
    We verify the Cauchy calibration using the Mercury green line (Reference: $546.07\\text{{ nm}}$).

    * Measured Deviation Angle $\\beta$: {beta_val:.2f}$^\\circ$ $\\pm$ {dbeta_val:.2f}$^\\circ$
    * Derived Refractive Index $n$: {_n_val:.5f} $\\pm$ {_dn_val:.5f}
    * **Predicted Wavelength $\\lambda$:** {lam_pred:.2f} $\\pm$ {dlam_pred:.2f} nm
    * **Difference from Reference:** {abs(lam_pred - lam_ref):.3f} nm (Verification: {is_success})
    * **Statistical Distance:** {sigma_dist:.2f}$\\sigma$
    """
    )
    hg_md  # noqa: B018
    return (sigma_dist,)


@app.cell(hide_code=True)
def hydrogen_prism_analysis(
    A_fit,
    B_fit,
    dA_fit,
    dB_fit,
    get_graph_reference_lambda,
    get_line_color,
    get_theory_lambda,
    h_prism_data,
    mo,
    np,
    pd,
    prism_alpha,
    propagate_error,
):
    _alpha_rad = np.radians(prism_alpha.value)

    prism_results = []
    _R_inf_theo = 10973731.568

    _quantum_n = {
        "Red": 3,
        "Blue-Green": 4,
        "Blue": 5,
        "Violet": 6
    }

    for _row in h_prism_data:
        _line = _row["line_id"]
        _beta = _row["beta"]
        _dbeta = _row["dbeta"]

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
        _dlam = propagate_error(
            get_lam, [A_fit, B_fit, _n], [dA_fit, dB_fit, _dn]
        )

        # Rydberg calculation
        _n_q = _quantum_n.get(_line, 3)
        _factor = 0.25 - 1.0 / (_n_q**2)
        _R = 1.0 / ((_lam * 1e-9) * _factor)
        _dR = _R * (_dlam / _lam)
        _R_sigma = abs(_R - _R_inf_theo) / _dR

        _theory = _row.get("theory_lambda", get_theory_lambda(_line))
        _ref = get_graph_reference_lambda(_line)
        _color = _row.get("color", get_line_color(_line))
        _diff = _lam - _ref if not np.isnan(_ref) else np.nan
        _pct_diff = (
            (_diff / _ref) * 100.0 if not np.isnan(_ref) else np.nan
        )
        _sigma_dist = (
            abs(_lam - _ref) / _dlam
            if not np.isnan(_ref) and _dlam > 0
            else np.nan
        )

        prism_results.append(
            {
                "Line": _line,
                "Color": _color,
                "Beta (deg)": _beta,
                "Refractive Index n": _n,
                "Calculated Wavelength (nm)": _lam,
                "Uncertainty (nm)": _dlam,
                "Reference (nm)": _ref,
                "Theory (nm)": _theory,
                "Difference (nm)": _diff,
                "Percent Difference (%)": _pct_diff,
                "Sigma Distance": _sigma_dist,
                "R [m^-1]": _R,
                "dR [m^-1]": _dR,
                "R Sigma Distance": _R_sigma,
            }
        )

    df_prism = pd.DataFrame(prism_results)
    df_prism_render = df_prism.copy()
    _num_cols = df_prism_render.select_dtypes(include=[np.number]).columns
    df_prism_render[_num_cols] = df_prism_render[_num_cols].round(4)

    h_prism_md = mo.md(
        rf"""
    ## Part 3: Hydrogen Lines - Prism Method
    The wavelengths of the Hydrogen Balmer lines computed from their minimum deviation angles, with individual Rydberg constant calculations:

    {mo.as_html(df_prism_render)}
    """
    )
    h_prism_md  # noqa: B018
    return df_prism, prism_results


@app.cell(hide_code=True)
def hydrogen_grating_analysis(
    get_graph_reference_lambda,
    get_line_color,
    get_theory_lambda,
    h_grating_data,
    lines_density,
    mo,
    np,
    pd,
):
    # Grating period d in nm
    d_grating = (1.0e6) / lines_density.value  # nm
    dd_grating = 0.0  # assume nominal d has negligible error
    _R_inf_theo = 10973731.568

    _quantum_n = {
        "Red": 3,
        "Blue-Green": 4,
        "Blue": 5,
        "Violet": 6
    }

    grating_results = []

    for _row in h_grating_data:
        _line = _row["line_id"]
        _m = _row["order"]
        _bp = _row["beta_plus"]
        _bm = _row["beta_minus"]
        _db = _row["dbeta"]

        _bp_rad = np.radians(_bp)
        _bm_rad = np.radians(_bm)
        _db_rad = np.radians(_db)

        # Incidence angle calculation:
        # sin(i0) = (sin(beta+) - sin(beta-)) / 2
        # Let's use get_i0 function behavior or calculate directly
        _sin_i0 = (np.sin(_bp_rad) - np.sin(_bm_rad)) / 2.0
        _i0_rad = np.arcsin(_sin_i0)

        # d(sin(i0)) = 0.5 * (cos(beta+)dbeta + cos(beta-)dbeta)
        _dsin_i0 = 0.5 * (np.cos(_bp_rad) + np.cos(_bm_rad)) * _db_rad
        _di0_rad = _dsin_i0 / np.cos(_i0_rad)

        # Wavelength lambda = d/m * (sin(beta+) + sin(beta-)) / 2
        # which is lambda = d/m * sin((beta+ + beta-)/2) * cos((beta+ - beta-)/2)
        _sin_term = (np.sin(_bp_rad) + np.sin(_bm_rad)) / 2.0
        _lam = (d_grating / _m) * _sin_term

        # Error propagation for wavelength
        _dsin_term = 0.5 * (np.cos(_bp_rad) + np.cos(_bm_rad)) * _db_rad
        _dlam = (d_grating / _m) * _dsin_term

        # Rydberg calculation
        _n_q = _quantum_n.get(_line, 3)
        _factor = 0.25 - 1.0 / (_n_q**2)
        _R = 1.0 / ((_lam * 1e-9) * _factor)
        _dR = _R * (_dlam / _lam)
        _R_sigma = abs(_R - _R_inf_theo) / _dR

        _theory = _row.get("theory_lambda", get_theory_lambda(_line))
        _ref = get_graph_reference_lambda(_line)
        _color = _row.get("color", get_line_color(_line))
        _diff = _lam - _ref if not np.isnan(_ref) else np.nan
        _pct_diff = (
            (_diff / _ref) * 100.0 if not np.isnan(_ref) else np.nan
        )
        _sigma_dist = (
            abs(_lam - _ref) / _dlam
            if not np.isnan(_ref) and _dlam > 0
            else np.nan
        )

        grating_results.append(
            {
                "Line": _line,
                "Color": _color,
                "Order": _m,
                "Beta+ (deg)": _bp,
                "Beta- (deg)": _bm,
                "Incidence i0 (deg)": np.degrees(_i0_rad),
                "di0 (deg)": np.degrees(_di0_rad),
                "Calculated Wavelength (nm)": _lam,
                "Uncertainty (nm)": _dlam,
                "Reference (nm)": _ref,
                "Theory (nm)": _theory,
                "Difference (nm)": _diff,
                "Percent Difference (%)": _pct_diff,
                "Sigma Distance": _sigma_dist,
                "R [m^-1]": _R,
                "dR [m^-1]": _dR,
                "R Sigma Distance": _R_sigma,
            }
        )

    df_grating = pd.DataFrame(grating_results)
    df_grating_render = df_grating.copy()
    _num_cols = df_grating_render.select_dtypes(include=[np.number]).columns
    df_grating_render[_num_cols] = df_grating_render[_num_cols].round(4)

    h_grating_md = mo.md(
        rf"""
    ## Part 4: Hydrogen Lines - Diffraction Grating Method
    Calculating the wavelengths of the Hydrogen Balmer lines using the diffraction grating, with individual Rydberg constant calculations:
    * Grating spacing $d$: {d_grating:.3f} nm ({lines_density.value:.1f} lines/mm)

    {mo.as_html(df_grating_render)}
    """
    )
    h_grating_md  # noqa: B018
    return df_grating, grating_results


@app.cell(hide_code=True)
def rydberg_calculation(
    c,
    e,
    epsilon_0,
    get_quantum_n,
    grating_results,
    h,
    m_e,
    mo,
    np,
    pd,
    prism_results,
):
    # Rydberg constant R calculation:
    def calc_R(lam_nm, n):
        lam_m = lam_nm * 1e-9
        factor = 0.25 - 1.0 / (n**2)
        return 1.0 / (lam_m * factor)

    # Error propagation for R
    def calc_R_err(lam_nm, dlam_nm, n):
        R_val = calc_R(lam_nm, n)
        return R_val * (dlam_nm / lam_nm)

    # Align prism and grating datasets by line key instead of simple strict zip
    prism_lookup = {str(r["Line"]): r for r in prism_results}
    grating_lookup = {str(r["Line"]): r for r in grating_results}
    all_lines = sorted(
        list(set(prism_lookup.keys()) | set(grating_lookup.keys())), key=str
    )

    # Theoretical Rydberg Constant R_infinity
    R_inf_theo = (m_e * (e**4)) / (8.0 * (epsilon_0**2) * (h**3) * c)

    results_R = []

    for _line in all_lines:
        _n_q = get_quantum_n(_line)

        # Prism R
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

        # Grating R
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
    df_R_render = df_R.copy()
    _num_cols = df_R_render.select_dtypes(include=[np.number]).columns
    df_R_render[_num_cols] = df_R_render[_num_cols].round(4)

    # Weighted Average R with NaN safety
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

    _valid_grating = df_R.dropna(
        subset=["R (Grating) [m^-1]", "dR (Grating) [m^-1]"]
    )
    if not _valid_grating.empty:
        _w_grating = 1.0 / (_valid_grating["dR (Grating) [m^-1]"] ** 2)
        R_avg_grating = np.sum(
        _valid_grating["R (Grating) [m^-1]"] * _w_grating
        ) / np.sum(_w_grating)
        dR_avg_grating = 1.0 / np.sqrt(np.sum(_w_grating))
    else:
        R_avg_grating = np.nan
        dR_avg_grating = np.nan

    prism_sig = (
        abs(R_avg_prism - R_inf_theo) / dR_avg_prism
        if not np.isnan(R_avg_prism) and dR_avg_prism > 0
        else np.nan
    )
    grating_sig = (
        abs(R_avg_grating - R_inf_theo) / dR_avg_grating
        if not np.isnan(R_avg_grating) and dR_avg_grating > 0
        else np.nan
    )

    prism_res_str = (
        f"({R_avg_prism:.4e} $\\pm$ {dR_avg_prism:.4e})"
        if not np.isnan(R_avg_prism)
        else "N/A"
    )
    grating_res_str = (
        f"({R_avg_grating:.4e} $\\pm$ {dR_avg_grating:.4e})"
        if not np.isnan(R_avg_grating)
        else "N/A"
    )
    prism_disc_str = (
        f"{abs(R_avg_prism - R_inf_theo) / R_inf_theo * 100:.3f}%"
        if not np.isnan(R_avg_prism)
        else "N/A"
    )
    grating_disc_str = (
        f"{abs(R_avg_grating - R_inf_theo) / R_inf_theo * 100:.3f}%"
        if not np.isnan(R_avg_grating)
        else "N/A"
    )
    prism_sig_str = (
        f"{prism_sig:.2f}$\\sigma$"
        if not np.isnan(prism_sig)
        else "N/A"
    )
    grating_sig_str = (
        f"{grating_sig:.2f}$\\sigma$"
        if not np.isnan(grating_sig)
        else "N/A"
    )

    rydberg_md = mo.md(
        rf"""
    ## Part 5: Rydberg Constant Calculation & Comparison
    Comparing experimental Rydberg constants to Bohr's theoretical prediction:

    {mo.as_html(df_R_render)}

    ### Summary of Results:
    * **Rydberg Constant (Prism Method):** {prism_res_str} $\text{{m}}^{{-1}}$
    * **Rydberg Constant (Grating Method):** {grating_res_str} $\text{{m}}^{{-1}}$
    * **Theoretical Rydberg Constant $R_\infty$:** {R_inf_theo:.4e} $\text{{m}}^{{-1}}$
    * **Prism discrepancy:** {prism_disc_str} (Distance: {prism_sig_str})
    * **Grating discrepancy:** {grating_disc_str} (Distance: {grating_sig_str})
    """
    )
    rydberg_md  # noqa: B018
    return (
        R_avg_grating,
        R_avg_prism,
        R_inf_theo,
        dR_avg_grating,
        dR_avg_prism,
        grating_sig,
        prism_sig,
    )


@app.cell(hide_code=True)
def summary_section(
    R_avg_grating,
    R_avg_prism,
    R_inf_theo,
    dR_avg_grating,
    dR_avg_prism,
    df_grating,
    df_prism,
    grating_sig,
    mo,
    np,
    pd,
    prism_sig,
):
    # 1. Wavelength Comparison Table
    # Merge prism and grating wavelengths
    p_sub = df_prism[
        [
            "Line",
            "Color",
            "Calculated Wavelength (nm)",
            "Uncertainty (nm)",
            "Reference (nm)",
            "Theory (nm)",
        ]
    ].rename(
        columns={
            "Calculated Wavelength (nm)": "Calculated Prism Wavelength (nm)",
            "Uncertainty (nm)": "Prism Uncertainty (nm)",
        }
    )
    g_sub = df_grating[
        ["Line", "Calculated Wavelength (nm)", "Uncertainty (nm)"]
    ].rename(
        columns={
            "Calculated Wavelength (nm)": "Calculated Grating Wavelength (nm)",
            "Uncertainty (nm)": "Grating Uncertainty (nm)",
        }
    )

    # Merge on Line (converted to str for safety)
    p_sub["Line"] = p_sub["Line"].astype(str)
    g_sub["Line"] = g_sub["Line"].astype(str)
    comparison_df = pd.merge(p_sub, g_sub, on="Line", how="outer")

    # Reorder columns
    comparison_df = comparison_df[
        [
            "Line",
            "Color",
            "Calculated Prism Wavelength (nm)",
            "Prism Uncertainty (nm)",
            "Calculated Grating Wavelength (nm)",
            "Grating Uncertainty (nm)",
            "Reference (nm)",
            "Theory (nm)",
        ]
    ]

    # 2. Rydberg Constants Summary Table
    prism_disc = (
        abs(R_avg_prism - R_inf_theo) / R_inf_theo * 100.0
        if not np.isnan(R_avg_prism)
        else np.nan
    )
    grating_disc = (
        abs(R_avg_grating - R_inf_theo) / R_inf_theo * 100.0
        if not np.isnan(R_avg_grating)
        else np.nan
    )

    rydberg_summary_data = [
        {
            "Method": "Prism Method",
            "Rydberg Constant R (m^-1)": R_avg_prism,
            "Uncertainty dR (m^-1)": dR_avg_prism,
            "Discrepancy from Bohr (%)": prism_disc,
            "Sigma Distance": prism_sig,
        },
        {
            "Method": "Grating Method",
            "Rydberg Constant R (m^-1)": R_avg_grating,
            "Uncertainty dR (m^-1)": dR_avg_grating,
            "Discrepancy from Bohr (%)": grating_disc,
            "Sigma Distance": grating_sig,
        },
        {
            "Method": "Theoretical Bohr Prediction (R_inf)",
            "Rydberg Constant R (m^-1)": R_inf_theo,
            "Uncertainty dR (m^-1)": 0.0,
            "Discrepancy from Bohr (%)": 0.0,
            "Sigma Distance": 0.0,
        },
    ]
    rydberg_summary_df = pd.DataFrame(rydberg_summary_data)

    # Round numerical columns to 4 decimal places for rendering
    comp_render = comparison_df.copy()
    _num_cols_comp = comp_render.select_dtypes(include=[np.number]).columns
    comp_render[_num_cols_comp] = comp_render[_num_cols_comp].round(4)

    ryd_render = rydberg_summary_df.copy()
    _num_cols_ryd = ryd_render.select_dtypes(include=[np.number]).columns
    ryd_render[_num_cols_ryd] = ryd_render[_num_cols_ryd].round(4)

    summary_md = mo.md(
        rf"""
    ## Part 6: Experiment Summary Comparison

    ### 1. Wavelength Comparison Table (nm)
    Comparison of measured Hydrogen Balmer wavelengths from both methods against theoretical values:

    {mo.as_html(comp_render)}

    ### 2. Rydberg Constant Summary Table (m^-1)
    Summary of the final weighted average Rydberg constants computed from each experimental method:

    {mo.as_html(ryd_render)}
    """
    )
    summary_md  # noqa: B018
    return


@app.cell(hide_code=True)
def export_results(
    A_fit,
    B_fit,
    R_avg_grating,
    R_avg_prism,
    dA_fit,
    dB_fit,
    dR_avg_grating,
    dR_avg_prism,
    exp_dir,
    export_constants,
    grating_sig,
    mo,
    np,
    prism_sig,
    sigma_dist,
):
    def clean_float(val):
        return float(val) if not np.isnan(val) else None

    constants_data = [
        {
            "hebrew_name": "פרמטר קושי A",
            "english_name": "Cauchy Parameter A",
            "hebrew_var": "פרמטר_קושי_A",
            "english_var": "cauchy_a",
            "symbol": "A",
            "value": float(A_fit),
            "error": float(dA_fit),
            "units": "",
            "fmt_spec": ".5f",
        },
        {
            "hebrew_name": "פרמטר קושי B",
            "english_name": "Cauchy Parameter B",
            "hebrew_var": "פרמטר_קושי_B",
            "english_var": "cauchy_b",
            "symbol": "B",
            "value": float(B_fit),
            "error": float(dB_fit),
            "units": "\"nm\"^2",
            "fmt_spec": ".1f",
        },
        {
            "hebrew_name": "קבוע רידברג (מנסרה)",
            "english_name": "Rydberg Constant (Prism)",
            "hebrew_var": "קבוע_רידברג_מנסרה",
            "english_var": "rydberg_prism",
            "symbol": "R_p",
            "value": clean_float(R_avg_prism),
            "error": clean_float(dR_avg_prism),
            "units": "\"m\"^(-1)",
            "fmt_spec": ".4e",
        },
        {
            "hebrew_name": "קבוע רידברג (סריג)",
            "english_name": "Rydberg Constant (Grating)",
            "hebrew_var": "קבוע_רידברג_סריג",
            "english_var": "rydberg_grating",
            "symbol": "R_g",
            "value": clean_float(R_avg_grating),
            "error": clean_float(dR_avg_grating),
            "units": "\"m\"^(-1)",
            "fmt_spec": ".4e",
        },
        {
            "hebrew_name": "מרחק סטטיסטי קבוע רידברג (מנסרה)",
            "english_name": "Rydberg Constant Sigma Distance (Prism)",
            "hebrew_var": "מרחק_רידברג_מנסרה",
            "english_var": "rydberg_prism_sigma",
            "symbol": "sigma_(R_p)",
            "value": clean_float(prism_sig),
            "error": None,
            "units": "",
            "fmt_spec": ".2f",
        },
        {
            "hebrew_name": "מרחק סטטיסטי קבוע רידברג (סריג)",
            "english_name": "Rydberg Constant Sigma Distance (Grating)",
            "hebrew_var": "מרחק_רידברג_סריג",
            "english_var": "rydberg_grating_sigma",
            "symbol": "sigma_(R_g)",
            "value": clean_float(grating_sig),
            "error": None,
            "units": "",
            "fmt_spec": ".2f",
        },
        {
            "hebrew_name": "מרחק סטטיסטי כספית",
            "english_name": "Mercury Green Line Sigma Distance",
            "hebrew_var": "מרחק_כספית",
            "english_var": "mercury_green_sigma",
            "symbol": "sigma_(H g)",
            "value": clean_float(sigma_dist),
            "error": None,
            "units": "",
            "fmt_spec": ".2f",
        },
    ]

    # Save to constants folder inside the experiment directory
    constants_dir = exp_dir / "constants"
    constants_dir.mkdir(parents=True, exist_ok=True)
    export_constants(constants_data, constants_dir)

    export_md = mo.md(
        """
    ### Export Status:
    Data has been successfully exported to `constants/constants.json` and `constants/constants.typ`!
    """
    )
    export_md  # noqa: B018
    return


if __name__ == "__main__":
    app.run()
