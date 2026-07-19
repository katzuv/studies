# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "autograd>=1.6.2",
#     "marimo>=0.23.14",
#     "matplotlib>=3.11.0",
#     "numpy>=2.5.1",
#     "pandas>=2.2.2",
#     "scipy>=1.18.0",
#     "rich>=13.7.0",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import json

    # Import the custom physics lab helper library
    import sys
    from pathlib import Path

    import marimo as mo
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.constants as sp
    from scipy.integrate import trapezoid

    matplotlib.rcParams["svg.hashsalt"] = "bragg-lab-svg-salt"

    # Monkeypatch savefig to enforce deterministic SVG metadata
    _original_savefig = matplotlib.figure.Figure.savefig

    def _deterministic_savefig(self, *args, **kwargs):
        if (
            len(args) > 0
            and str(args[0]).endswith(".svg")
            or "format" in kwargs
            and kwargs["format"] == "svg"
        ):
            meta = kwargs.get("metadata", {}) or {}
            meta["Date"] = None
            kwargs["metadata"] = meta
        return _original_savefig(self, *args, **kwargs)

    matplotlib.figure.Figure.savefig = _deterministic_savefig

    # Dynamic path resolution to studies directory containing physlab
    studies_path = None
    try:
        for p in Path(__file__).resolve().parents:
            if (p / "physlab").is_dir():
                studies_path = p
                break
    except Exception:
        pass
    if not studies_path:
        for _p in [Path.cwd()] + list(Path.cwd().parents):
            if (p / "physlab").is_dir():
                studies_path = p
                break
    if studies_path and str(studies_path) not in sys.path:
        sys.path.insert(0, str(studies_path))
    import physlab.core as phys

    # Ensure output data directory exists
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return Path, data_dir, json, mo, np, phys, plt, sp, trapezoid


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bragg X-ray Spectroscopy Data Analysis
    This interactive notebook assists in analyzing X-ray emission spectra. Please upload your goniometer scan files below to begin.
    """)
    return


@app.cell(hide_code=True)
def _():
    is_sim = False
    return (is_sim,)


@app.cell(hide_code=True)
def _(is_sim, mo):
    # File uploaders for Lab Mode
    lif_2mm_uploader = (
        mo.ui.file(label="Upload LiF (2mm) Scan File", filetypes=[".txt", ".csv"])
        if not is_sim
        else None
    )
    kbr_2mm_uploader = (
        mo.ui.file(label="Upload KBr (2mm) Scan File", filetypes=[".txt", ".csv"])
        if not is_sim
        else None
    )
    lif_5mm_uploader = (
        mo.ui.file(label="Upload LiF (5mm) Scan File", filetypes=[".txt", ".csv"])
        if not is_sim
        else None
    )

    # Show them in a row/column if not in simulation mode
    if not is_sim:
        upload_ui = mo.vstack([lif_2mm_uploader, kbr_2mm_uploader, lif_5mm_uploader])
    else:
        upload_ui = mo.md("Uploaders hidden in Simulation Mode.")

    upload_ui
    return kbr_2mm_uploader, lif_2mm_uploader, lif_5mm_uploader


@app.cell(hide_code=True)
def _(data_dir, np):
    def generate_synthetic_data(crystal_name, diaphragm_mm, noise_scale=3.0):
        """Generates realistic Bragg diffraction intensities for anode tubes (35kV, 1mA)."""
        angles = np.arange(3.0, 75.1, 0.1)  # Bragg angles in degrees

        # Crystal parameters
        # LiF(200) d=201.4pm, KBr(200) d=329.9pm
        d = 201.4 if crystal_name == "LiF" else 329.9
        hc = 1239.84193  # eV*nm = 1239841.93 eV*pm

        # Calculate matching energies (n=1) for Bragg angles to construct background
        energies_n1 = (hc * 1e3) / (2 * d * np.sin(np.radians(angles)))  # in eV
        energies_n1_kev = energies_n1 / 1000.0

        # Bremsstrahlung background: Kramers' Law approximation + Duane-Hunt limit at 35keV
        E_max = 35.0  # keV
        I_brem = np.zeros_like(angles)

        # Only energy values below E_max are produced
        valid_mask = energies_n1_kev < E_max
        # Kramers law / smooth background curve, scaled to ~100-300 cps background
        I_brem[valid_mask] = (
            100.0
            * (E_max - energies_n1_kev[valid_mask])
            * (1.0 - np.exp(-energies_n1_kev[valid_mask] / 5.0))
            / (energies_n1_kev[valid_mask] ** 0.5)
        )

        # Absorption edge step for Bromine K-edge in KBr (13.47 keV)
        if crystal_name == "KBr":
            # Above 13.47 keV, crystal absorption increases dramatically, so reflectivity drops
            step_mask = energies_n1_kev > 13.47
            I_brem[step_mask] *= 0.35

        # Both use Mo (Ka = 17.48, Kb = 19.61 keV)
        if crystal_name == "LiF":
            peaks_def = [
                {"name": "Ka", "E": 17.48, "rel_int": 2000.0},
                {"name": "Kb", "E": 19.61, "rel_int": 500.0},
            ]
        else:  # KBr
            peaks_def = [
                {"name": "Ka", "E": 17.48, "rel_int": 600.0},
                {"name": "Kb", "E": 19.61, "rel_int": 150.0},
            ]

        I_peaks = np.zeros_like(angles)

        # Resolution of peaks depends on diaphragm size
        sigma_theta = (
            0.15 if diaphragm_mm == 2.0 else (0.35 if diaphragm_mm == 5.0 else 0.08)
        )

        for n in [1, 2, 3, 4, 5, 6]:
            for p in peaks_def:
                # Find Bragg angle for this order n and energy E
                val_to_arcsin = (hc * n) / (2 * d * p["E"])
                if val_to_arcsin <= 1.0:
                    theta_peak_deg = np.degrees(np.arcsin(val_to_arcsin))
                    # Scale intensity by 1/n^1.5 for higher order efficiency loss
                    peak_amp = (
                        p["rel_int"]
                        * (1.0 / (n**1.5))
                        * (
                            1.0
                            if diaphragm_mm == 2.0
                            else (1.8 if diaphragm_mm == 5.0 else 0.55)
                        )
                    )
                    # Gaussian peak shape
                    I_peaks += peak_amp * np.exp(
                        -0.5 * ((angles - theta_peak_deg) / sigma_theta) ** 2
                    )

        # Total intensity with noise
        total_intensity = I_brem + I_peaks
        noise = np.random.normal(0, noise_scale, size=len(angles))
        # Ensure intensity is non-negative and counts are integers
        total_intensity = np.clip(total_intensity + noise, 0, None)

        # Save to file
        file_path = (
            data_dir / f"simulated_{crystal_name.lower()}_{int(diaphragm_mm)}mm.txt"
        )
        with file_path.open("w", encoding="utf-8") as f:
            f.write("# Bragg angle (deg)\tIntensity (cps)\n")
            for a, val in zip(angles, total_intensity, strict=False):
                f.write(f"{a:.2f}\t{val:.1f}\n")

        return angles, total_intensity, file_path

    return (generate_synthetic_data,)


@app.cell(hide_code=True)
def _(
    Path,
    data_dir,
    generate_synthetic_data,
    is_sim,
    kbr_2mm_uploader,
    lif_2mm_uploader,
    lif_5mm_uploader,
    np,
):
    # Parse files based on current mode
    def load_data(uploader, crystal_name, diaphragm_mm):
        if is_sim:
            # Generate and load simulation file
            angles, intensity, filepath = generate_synthetic_data(
                crystal_name, diaphragm_mm
            )
            return angles, intensity, filepath
        else:
            # Check if there is an uploaded file
            has_upload = uploader is not None and uploader.value

            # Destination path default
            dest_filename = f"{crystal_name.lower()}{int(diaphragm_mm)}mm.txt"
            dest_path = data_dir / dest_filename

            if has_upload:
                # Save the uploaded file to data/ directory
                orig_name = uploader.value[0].name
                ext = Path(orig_name).suffix or ".txt"
                dest_filename = f"{crystal_name.lower()}{int(diaphragm_mm)}mm{ext}"
                dest_path = data_dir / dest_filename
                dest_path.write_bytes(uploader.value[0].contents)

            # Look for existing files (.txt or .csv)
            chosen_path = None
            if dest_path.exists():
                chosen_path = dest_path
            elif dest_path.with_suffix(".csv").exists():
                chosen_path = dest_path.with_suffix(".csv")
            elif dest_path.with_suffix(".txt").exists():
                chosen_path = dest_path.with_suffix(".txt")

            if chosen_path is not None:
                # Read bytes and convert to text
                content = chosen_path.read_text(encoding="utf-8")
                angles = []
                intensity = []

                for line in content.splitlines():
                    line = line.strip()
                    if (
                        not line
                        or line.startswith("#")
                        or line.startswith("Time")
                        or "θ" in line
                    ):
                        continue
                    parts = line.split()
                    try:
                        if len(parts) == 6:
                            # 6 columns format: Time, Impulse, U, I, Detector_angle, Crystal_angle
                            angles.append(float(parts[5]))
                            intensity.append(float(parts[1]))
                        elif len(parts) >= 2:
                            # Default 2 columns format: Bragg_angle, Intensity
                            angles.append(float(parts[0]))
                            intensity.append(float(parts[1]))
                    except ValueError:
                        continue

                return np.array(angles), np.array(intensity), chosen_path

            return None, None, None

    # Load all three datasets
    lif_2mm_ang, lif_2mm_int, lif_2mm_file = load_data(lif_2mm_uploader, "LiF", 2.0)
    kbr_2mm_ang, kbr_2mm_int, kbr_2mm_file = load_data(kbr_2mm_uploader, "KBr", 2.0)
    lif_5mm_ang, lif_5mm_int, lif_5mm_file = load_data(lif_5mm_uploader, "LiF", 5.0)
    return (
        kbr_2mm_ang,
        kbr_2mm_file,
        kbr_2mm_int,
        lif_2mm_ang,
        lif_2mm_file,
        lif_2mm_int,
        lif_5mm_ang,
        lif_5mm_file,
        lif_5mm_int,
    )


@app.cell(hide_code=True)
def _(kbr_2mm_file, lif_2mm_file, lif_5mm_file, mo):
    # Status display
    def file_status(filename, label):
        if filename:
            return mo.md(f"🟢 **{label}**: Loaded from `{filename.name}`")
        return mo.md(f"🔴 **{label}**: No file uploaded.")

    status_block = mo.vstack(
        [
            file_status(lif_2mm_file, "LiF (2mm)"),
            file_status(kbr_2mm_file, "KBr (2mm)"),
            file_status(lif_5mm_file, "LiF (5mm)"),
        ]
    )
    status_block
    return


@app.cell(hide_code=True)
def _(np, sp):
    def angle_to_energy(angle_deg, d_pm, n=1):
        """Converts Bragg angle in degrees to energy in keV."""
        hc = 1239.84193  # eV*nm
        d_nm = d_pm / 1000.0
        wavelength = (2 * d_nm * np.sin(np.radians(angle_deg))) / n
        energy_ev = hc / wavelength
        return energy_ev / 1000.0  # Convert to keV

    def findtheta(E_ev, d_meters, n=1):
        """Converts photon energy (eV) to Bragg angle (degrees) for order n."""
        # Convert energy from eV to Joules (multiply by elementary charge)
        E_joules = E_ev * sp.electron_volt
        # Correct wavelength formula: lam = h * c / E
        lam = (sp.Planck * sp.speed_of_light) / E_joules
        # Bragg's Law: sin(theta) = n * lam / (2 * d)
        sinth = (n * lam) / (2.0 * d_meters)
        if sinth > 1.0:
            return None
        return np.degrees(np.arcsin(sinth))

    return angle_to_energy, findtheta


@app.cell(hide_code=True)
def _(
    angle_to_energy,
    findtheta,
    kbr_2mm_ang,
    kbr_2mm_int,
    lif_2mm_ang,
    lif_2mm_int,
    lif_5mm_ang,
    lif_5mm_int,
    np,
    phys,
    plt,
):
    fig_raw_angle = None
    fig_raw_energy = None
    fig_kbr_angle = None
    fig_kbr_energy = None
    fig_lif5mm_angle = None
    fig_lif5mm_energy = None

    _cu_lines = {"K_alpha": 8.04, "K_beta": 8.91}
    _mo_lines = {"K_alpha": 17.48, "K_beta": 19.61}

    # 1. LiF (2mm) Plots
    if lif_2mm_ang is not None and len(lif_2mm_ang) > 0:
        # Define confirmed visible peaks for LiF
        _lif_confirmed_peaks = [
            (9.03, 9.20, r"$K_\beta$", 1),
            (10.14, 10.30, r"$K_\alpha$", 1),
            (18.31, 18.30, r"$K_\beta$", 2),
            (20.64, 20.70, r"$K_\alpha$", 2),
            (31.91, 32.10, r"$K_\alpha$", 3),
        ]

        _peaks_x = []
        _peaks_y = []
        _labels = {}

        for _theo, _exp, _lbl, _n in _lif_confirmed_peaks:
            _idx = np.argmin(np.abs(lif_2mm_ang - _exp))
            _actual_ang = lif_2mm_ang[_idx]
            _actual_int = lif_2mm_int[_idx]
            _peaks_x.append(_actual_ang)
            _peaks_y.append(_actual_int)
            _labels[_actual_ang] = f"{_lbl} (n={_n})\n{_actual_ang:.2f}°"

        # Angle Plot
        _fig_ang, ax_ang = plt.subplots(figsize=(7, 5), layout="constrained")
        ax_ang.plot(
            lif_2mm_ang,
            lif_2mm_int,
            label="LiF (2mm) Data",
            color="#2E86AB",
        )
        if _peaks_x:
            ax_ang.scatter(
                _peaks_x,
                _peaks_y,
                color="#C73E1D",
                marker="o",
                s=45,
                zorder=5,
                label="Confirmed Peaks",
            )
            for _px, _py in zip(_peaks_x, _peaks_y, strict=True):
                ax_ang.text(
                    _px + 0.5,
                    _py * 1.1,
                    _labels[_px],
                    color="#C73E1D",
                    fontsize=8,
                    fontweight="bold",
                )
                ax_ang.axvline(_px, color="#C73E1D", linestyle=":", alpha=0.4)

        ax_ang.set_yscale("log")
        phys.set_style(
            ax_ang,
            xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)",
            ylabel="Intensity (log cps)",
        )
        ax_ang.yaxis.set_minor_locator(plt.NullLocator())
        ax_ang.legend()
        fig_raw_angle = _fig_ang
        _fig_ang.savefig("data/spectrum_vs_angle.svg")

        # Energy Plot
        _fig_eng, ax_eng = plt.subplots(figsize=(7, 5), layout="constrained")
        _energies_kev = angle_to_energy(lif_2mm_ang, 201.4, n=1)
        _valid_idx = lif_2mm_ang > 3.0
        ax_eng.plot(
            _energies_kev[_valid_idx],
            lif_2mm_int[_valid_idx],
            label="LiF (2mm) Data",
            color="#A23B72",
        )
        if _peaks_x:
            _peaks_e = angle_to_energy(np.array(_peaks_x), 201.4, n=1)
            ax_eng.scatter(
                _peaks_e,
                _peaks_y,
                color="#C73E1D",
                marker="x",
                s=60,
                zorder=5,
                label="Detected Peaks",
            )
            for _pe, _py in zip(_peaks_e, _peaks_y, strict=True):
                _best_line = ""
                _best_n = 1
                _min_diff = float("inf")
                for _line, _E_ref in _mo_lines.items():
                    for _n_val in [1, 2, 3, 4, 5, 6]:
                        _apparent_E = _E_ref / _n_val
                        _diff = abs(_pe - _apparent_E)
                        if _diff < _min_diff:
                            _min_diff = _diff
                            _best_line = _line
                            _best_n = _n_val

                _label = r"$K_\alpha$" if _best_line == "K_alpha" else r"$K_\beta$"
                ax_eng.text(
                    _pe + 0.2,
                    _py * 1.05,
                    f"{_label} (n={_best_n})\n{_pe:.2f} keV",
                    color="#C73E1D",
                    fontsize=9,
                    fontweight="bold",
                )
                ax_eng.axvline(_pe, color="#C73E1D", linestyle=":", alpha=0.5)

        phys.set_style(ax_eng, xlabel=r"Energy $E$ (keV)", ylabel="Intensity (cps)")
        ax_eng.set_xlim(3.0, 25.0)
        ax_eng.legend()
        # plt.tight_layout()
        fig_raw_energy = _fig_eng
        _fig_eng.savefig("data/spectrum_vs_energy.svg")

    # 2. KBr (2mm) Plots
    if kbr_2mm_ang is not None and len(kbr_2mm_ang) > 0:
        # Define confirmed visible peaks
        _kbr_confirmed_peaks = [
            (5.50, 5.50, r"$K_\beta$", 1),
            (6.17, 6.20, r"$K_\alpha$", 1),
            (12.42, 12.50, r"$K_\alpha$", 2),
            (16.71, 17.40, r"$K_\beta$", 3),
            (18.82, 18.90, r"$K_\alpha$", 3),
            (25.47, 25.60, r"$K_\alpha$", 4),
            (32.52, 31.30, r"$K_\alpha$", 5),
            (35.10, 36.30, r"$K_\beta$", 6),
        ]

        _peaks_x = []
        _peaks_y = []
        _labels = {}

        for _theo, _exp, _lbl, _n in _kbr_confirmed_peaks:
            _idx = np.argmin(np.abs(kbr_2mm_ang - _exp))
            _actual_ang = kbr_2mm_ang[_idx]
            _actual_int = kbr_2mm_int[_idx]
            _peaks_x.append(_actual_ang)
            _peaks_y.append(_actual_int)
            _labels[_actual_ang] = f"{_lbl} (n={_n})\n{_actual_ang:.2f}°"

        # Angle Plot
        _fig_ang_kbr, ax_ang_kbr = plt.subplots(figsize=(7, 5), layout="constrained")
        ax_ang_kbr.plot(
            kbr_2mm_ang,
            kbr_2mm_int,
            label="KBr (2mm) Data",
            color="#F18F01",
        )
        if _peaks_x:
            ax_ang_kbr.scatter(
                _peaks_x,
                _peaks_y,
                color="#2E86AB",
                marker="o",
                s=45,
                zorder=5,
                label="Confirmed Peaks",
            )

        # Add text labels and vertical lines
        for _px, _py in zip(_peaks_x, _peaks_y, strict=True):
            _lbl = _labels[_px]
            ax_ang_kbr.text(
                _px + 0.3,
                _py * 1.1,
                _lbl,
                color="#2E86AB",
                fontsize=8,
                fontweight="bold",
            )
            ax_ang_kbr.axvline(_px, color="#2E86AB", linestyle=":", alpha=0.4)

        ax_ang_kbr.set_yscale("log")
        phys.set_style(
            ax_ang_kbr,
            xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)",
            ylabel="Intensity (log cps)",
        )
        ax_ang_kbr.yaxis.set_minor_locator(plt.NullLocator())
        ax_ang_kbr.legend()
        fig_kbr_angle = _fig_ang_kbr
        _fig_ang_kbr.savefig("data/kbr_spectrum_vs_angle.svg")

        # Energy Plot
        _fig_eng_kbr, ax_eng_kbr = plt.subplots(figsize=(7, 5), layout="constrained")
        _energies_kev_kbr = angle_to_energy(kbr_2mm_ang, 329.9, n=1)
        _valid_idx_kbr = kbr_2mm_ang > 3.0
        ax_eng_kbr.plot(
            _energies_kev_kbr[_valid_idx_kbr],
            kbr_2mm_int[_valid_idx_kbr],
            label="KBr (2mm) Data",
            color="#C73E1D",
        )
        if _peaks_x:
            _peaks_e_kbr = angle_to_energy(np.array(_peaks_x), 329.9, n=1)
            ax_eng_kbr.scatter(
                _peaks_e_kbr,
                _peaks_y,
                color="#C73E1D",
                marker="x",
                s=60,
                zorder=5,
                label="Detected Peaks",
            )
            for _pe, _py in zip(_peaks_e_kbr, _peaks_y, strict=True):
                _best_line = ""
                _best_n = 1
                _min_diff = float("inf")
                for _line, _E_ref in _mo_lines.items():
                    for _n_val in [1, 2, 3, 4, 5, 6]:
                        _apparent_E = _E_ref / _n_val
                        _diff = abs(_pe - _apparent_E)
                        if _diff < _min_diff:
                            _min_diff = _diff
                            _best_line = _line
                            _best_n = _n_val

                _label = r"$K_\alpha$" if _best_line == "K_alpha" else r"$K_\beta$"
                ax_eng_kbr.text(
                    _pe + 0.2,
                    _py * 1.05,
                    f"{_label} (n={_best_n})\n{_pe:.2f} keV",
                    color="#C73E1D",
                    fontsize=9,
                    fontweight="bold",
                )
                ax_eng_kbr.axvline(_pe, color="#C73E1D", linestyle=":", alpha=0.5)

        phys.set_style(ax_eng_kbr, xlabel=r"Energy $E$ (keV)", ylabel="Intensity (cps)")
        ax_eng_kbr.set_xlim(3.0, 25.0)
        ax_eng_kbr.legend()
        # plt.tight_layout()
        fig_kbr_energy = _fig_eng_kbr
        _fig_eng_kbr.savefig("data/kbr_spectrum_vs_energy.svg")

    # 3. LiF (5mm) Plots
    if lif_5mm_ang is not None and len(lif_5mm_ang) > 0:
        import scipy.signal as _sig

        _peaks, _ = _sig.find_peaks(lif_5mm_int, prominence=30, distance=3)
        _peaks_found_lif5mm = [
            (lif_5mm_ang[_p], lif_5mm_int[_p]) for _p in _peaks if lif_5mm_ang[_p] > 5.0
        ]

        # Use best match per theoretical line
        _peaks_x = []
        _peaks_y = []
        for _line_name, _E in _mo_lines.items():
            _E_ev = 17479.34 if _line_name == "K_alpha" else 19608.3
            for _n in [1, 2, 3, 4, 5, 6]:
                _ta = findtheta(_E_ev, 201.4 * 1e-12, _n)
                if _ta is not None:
                    _best_pe = None
                    _min_diff = float("inf")
                    for _exp_angle, _counts in _peaks_found_lif5mm:
                        _diff = abs(_exp_angle - _ta)
                        if _diff < _min_diff and _diff < 1.0:
                            _min_diff = _diff
                            _best_pe = (_exp_angle, _counts)
                    if _best_pe:
                        _peaks_x.append(_best_pe[0])
                        _peaks_y.append(_best_pe[1])

        # Angle Plot
        _fig_ang, ax_ang = plt.subplots(figsize=(7, 5), layout="constrained")
        ax_ang.plot(
            lif_5mm_ang,
            lif_5mm_int,
            label="LiF (5mm) Data",
            color="#2E86AB",
        )
        if _peaks_x:
            ax_ang.scatter(
                _peaks_x,
                _peaks_y,
                color="#C73E1D",
                marker="x",
                s=60,
                zorder=5,
                label="Detected Peaks",
            )
            for _px, _py in zip(_peaks_x, _peaks_y, strict=True):
                ax_ang.text(
                    _px + 0.5,
                    _py * 1.1,
                    f"{_px:.2f}°",
                    color="#C73E1D",
                    fontsize=9,
                    fontweight="bold",
                )
                ax_ang.axvline(_px, color="#C73E1D", linestyle=":", alpha=0.5)

        ax_ang.set_yscale("log")
        phys.set_style(
            ax_ang,
            xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)",
            ylabel="Intensity (log cps)",
        )
        ax_ang.yaxis.set_minor_locator(plt.NullLocator())
        ax_ang.legend()
        # plt.tight_layout()
        fig_lif5mm_angle = _fig_ang
        _fig_ang.savefig("data/lif5mm_spectrum_vs_angle.svg")

        # Energy Plot
        _fig_eng, ax_eng = plt.subplots(figsize=(7, 5), layout="constrained")
        _energies_kev = angle_to_energy(lif_5mm_ang, 201.4, n=1)
        _valid_idx = lif_5mm_ang > 3.0
        ax_eng.plot(
            _energies_kev[_valid_idx],
            lif_5mm_int[_valid_idx],
            label="LiF (5mm) Data",
            color="#A23B72",
        )
        if _peaks_x:
            _peaks_e = angle_to_energy(np.array(_peaks_x), 201.4, n=1)
            ax_eng.scatter(
                _peaks_e,
                _peaks_y,
                color="#C73E1D",
                marker="x",
                s=60,
                zorder=5,
                label="Detected Peaks",
            )
            for _pe, _py in zip(_peaks_e, _peaks_y, strict=True):
                _best_line = ""
                _best_n = 1
                _min_diff = float("inf")
                for _line, _E_ref in _mo_lines.items():
                    for _n_val in [1, 2, 3, 4, 5, 6]:
                        _apparent_E = _E_ref / _n_val
                        _diff = abs(_pe - _apparent_E)
                        if _diff < _min_diff:
                            _min_diff = _diff
                            _best_line = _line
                            _best_n = _n_val

                _label = r"$K_\alpha$" if _best_line == "K_alpha" else r"$K_\beta$"
                ax_eng.text(
                    _pe + 0.2,
                    _py * 1.05,
                    f"{_label} (n={_best_n})\n{_pe:.2f} keV",
                    color="#C73E1D",
                    fontsize=9,
                    fontweight="bold",
                )
                ax_eng.axvline(_pe, color="#C73E1D", linestyle=":", alpha=0.5)

        phys.set_style(ax_eng, xlabel=r"Energy $E$ (keV)", ylabel="Intensity (cps)")
        ax_eng.set_xlim(3.0, 25.0)
        ax_eng.legend()
        # plt.tight_layout()
        fig_lif5mm_energy = _fig_eng
        _fig_eng.savefig("data/lif5mm_spectrum_vs_energy.svg")
    return (
        fig_kbr_angle,
        fig_kbr_energy,
        fig_lif5mm_angle,
        fig_lif5mm_energy,
        fig_raw_angle,
        fig_raw_energy,
    )


@app.cell(hide_code=True)
def _(
    fig_kbr_angle,
    fig_kbr_energy,
    fig_lif5mm_angle,
    fig_lif5mm_energy,
    fig_raw_angle,
    fig_raw_energy,
    mo,
):
    _plots = []
    if fig_raw_angle is not None:
        _plots.extend(
            [mo.md("### LiF (2mm) Spectra"), mo.hstack([fig_raw_angle, fig_raw_energy])]
        )
    if fig_kbr_angle is not None:
        _plots.extend(
            [mo.md("### KBr (2mm) Spectra"), mo.hstack([fig_kbr_angle, fig_kbr_energy])]
        )
    if fig_lif5mm_angle is not None:
        _plots.extend(
            [
                mo.md("### LiF (5mm) Spectra"),
                mo.hstack([fig_lif5mm_angle, fig_lif5mm_energy]),
            ]
        )
    _layout = mo.vstack(_plots) if _plots else None
    _layout
    return


@app.cell(hide_code=True)
def _(
    angle_to_energy,
    kbr_2mm_ang,
    kbr_2mm_int,
    lif_2mm_ang,
    lif_2mm_int,
    phys,
    plt,
):
    # 2. Compare Crystals (LiF vs KBr)
    fig_crystal = None
    if lif_2mm_ang is not None and kbr_2mm_ang is not None:
        _fig, ax_crys = plt.subplots(figsize=(8, 5), layout="constrained")

        # Convert both to energy (n=1)
        lif_e = angle_to_energy(lif_2mm_ang[lif_2mm_ang > 3.0], 201.4, n=1)
        lif_y = lif_2mm_int[lif_2mm_ang > 3.0]

        kbr_e = angle_to_energy(kbr_2mm_ang[kbr_2mm_ang > 3.0], 329.9, n=1)
        kbr_y = kbr_2mm_int[kbr_2mm_ang > 3.0]

        ax_crys.plot(lif_e, lif_y, label="LiF (200) - $d=201.4$ pm", color="#2E86AB")
        ax_crys.plot(kbr_e, kbr_y, label="KBr (200) - $d=329.9$ pm", color="#F18F01")

        # Mark K-edge of Bromine (13.47 keV)
        ax_crys.axvline(
            13.47,
            color="#C73E1D",
            linestyle="--",
            alpha=0.8,
            label="Br K-edge: 13.47 keV",
        )

        phys.set_style(ax_crys, xlabel="Energy (keV)", ylabel="Intensity (cps)")
        ax_crys.legend()

        # plt.tight_layout()
        fig_crystal = _fig
        _fig.savefig("data/crystal_comparison.svg")

    fig_crystal
    return


@app.cell(hide_code=True)
def _(
    lif_2mm_ang,
    lif_2mm_int,
    lif_5mm_ang,
    lif_5mm_int,
    phys,
    plt,
    trapezoid,
):
    # 3. Compare Diaphragms (2mm vs 5mm)
    fig_diaphragm = None
    if lif_2mm_ang is not None and lif_5mm_ang is not None:
        _max_ang = min(lif_2mm_ang.max(), lif_5mm_ang.max())

        mask_2mm = (lif_2mm_ang >= 5.0) & (lif_2mm_ang <= _max_ang)
        mask_5mm = (lif_5mm_ang >= 5.0) & (lif_5mm_ang <= _max_ang)

        a2_sub, i2_sub = lif_2mm_ang[mask_2mm], lif_2mm_int[mask_2mm]
        a5_sub, i5_sub = lif_5mm_ang[mask_5mm], lif_5mm_int[mask_5mm]

        # Normalize by area to compare line resolution
        y_2mm_norm = i2_sub / trapezoid(i2_sub, a2_sub)
        y_5mm_norm = i5_sub / trapezoid(i5_sub, a5_sub)

        _fig, ax_dia = plt.subplots(figsize=(8.5, 5), layout="constrained")
        ax_dia.plot(
            a2_sub,
            y_2mm_norm,
            label="2mm Diaphragm",
            color="#2E86AB",
            alpha=0.9,
            linewidth=1.5,
        )
        ax_dia.plot(
            a5_sub,
            y_5mm_norm,
            label="5mm Diaphragm",
            color="#A23B72",
            alpha=0.9,
            linewidth=1.5,
        )

        ax_dia.set_yscale("log")
        ax_dia.set_xlim(5.0, _max_ang)
        ax_dia.yaxis.set_minor_locator(plt.NullLocator())

        phys.set_style(
            ax_dia,
            xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)",
            ylabel="Normalized Intensity (log scale)",
            title="Diaphragm Resolution Comparison (LiF 200)",
        )
        ax_dia.legend(loc="upper right")

        fig_diaphragm = _fig
        _fig.savefig("data/collimator_comparison.svg")
        _fig.savefig("data/collimator_comparison.png", dpi=300)

        # Raw Intensity comparison plot cut at end of data
        _fig_raw, ax_raw = plt.subplots(figsize=(8.5, 5), layout="constrained")
        ax_raw.plot(
            a2_sub,
            i2_sub,
            label="2mm Diaphragm",
            color="#2E86AB",
            alpha=0.9,
            linewidth=1.5,
        )
        ax_raw.plot(
            a5_sub,
            i5_sub,
            label="5mm Diaphragm",
            color="#A23B72",
            alpha=0.9,
            linewidth=1.5,
        )
        ax_raw.set_yscale("log")
        ax_raw.set_xlim(5.0, _max_ang)
        ax_raw.yaxis.set_minor_locator(plt.NullLocator())

        phys.set_style(
            ax_raw,
            xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)",
            ylabel="Intensity (cps, log scale)",
            title="Raw Intensity Comparison (2mm vs 5mm Diaphragm)",
        )
        ax_raw.legend(loc="upper right")

        _fig_raw.savefig("data/collimator_comparison_raw.svg")
        _fig_raw.savefig("data/collimator_comparison_raw.png", dpi=300)
        plt.close(_fig_raw)

    fig_diaphragm
    return


@app.cell(hide_code=True)
def _(angle_to_energy, lif_2mm_ang, lif_2mm_int, mo, np, phys, plt):
    # 3b. Compare Diffraction Orders (n=1, 2, 3) vs Actual Energy for LiF (2mm)
    fig_orders = None
    orders_table_ui = None
    if lif_2mm_ang is not None and len(lif_2mm_ang) > 0:
        fig_orders, ax_ord = plt.subplots(figsize=(8, 5.5), layout="constrained")

        # Divide into angles and plot each order n=1, 2, 3
        ranges = {
            1: (5.0, 15.0, "#2E86AB"),
            2: (15.0, 25.0, "#A23B72"),
            3: (25.0, 45.0, "#F18F01"),
        }

        for n, (min_a, max_a, color) in ranges.items():
            mask = (lif_2mm_ang >= min_a) & (lif_2mm_ang <= max_a)
            if np.any(mask):
                ord_ang = lif_2mm_ang[mask]
                ord_int = lif_2mm_int[mask]
                ord_energy = angle_to_energy(ord_ang, 201.4, n=n)

                # Plot in range of characteristic lines
                valid = (ord_energy >= 12.0) & (ord_energy <= 24.0)
                if np.any(valid):
                    sort_idx = np.argsort(ord_energy[valid])
                    ax_ord.plot(
                        ord_energy[valid][sort_idx],
                        ord_int[valid][sort_idx],
                        label=f"Order n={n}",
                        color=color,
                        linewidth=1.5,
                    )

        # Confirmed peak search windows for LiF (2mm)
        peaks_order_info = [
            {"n": 1, "line": "K_beta", "win": (8.8, 9.5), "lbl": r"$K_\beta$"},
            {"n": 1, "line": "K_alpha", "win": (9.8, 10.6), "lbl": r"$K_\alpha$"},
            {"n": 2, "line": "K_beta", "win": (18.0, 18.8), "lbl": r"$K_\beta$"},
            {"n": 2, "line": "K_alpha", "win": (20.3, 21.1), "lbl": r"$K_\alpha$"},
            {"n": 3, "line": "K_alpha", "win": (31.5, 32.5), "lbl": r"$K_\alpha$"},
        ]

        theo_ka, theo_kb = 17.48, 19.61
        d_theta_rad = np.radians(0.05)

        # Mark peaks on the graph and collect table data
        results_by_order = {1: {}, 2: {}, 3: {}}

        for _p in peaks_order_info:
            n = _p["n"]
            mask = (lif_2mm_ang >= _p["win"][0]) & (lif_2mm_ang <= _p["win"][1])
            sub_ang = lif_2mm_ang[mask]
            sub_int = lif_2mm_int[mask]
            max_idx = np.argmax(sub_int)
            ang_max = sub_ang[max_idx]
            counts_max = sub_int[max_idx]
            e_max = angle_to_energy(ang_max, 201.4, n=n)

            # Scatter point ('x') & annotation on figure
            ax_ord.scatter(
                e_max,
                counts_max,
                color="#C73E1D",
                marker="x",
                s=55,
                linewidth=1.8,
                zorder=5,
            )
            ax_ord.annotate(
                f"{_p['lbl']} (n={n})\n{e_max:.2f} keV",
                (e_max, counts_max),
                xytext=(e_max + 0.3, counts_max * 1.15),
                arrowprops=dict(arrowstyle="->", color="#C73E1D", lw=0.8),
                color="#C73E1D",
                fontsize=8,
                fontweight="bold",
            )

            theo_val = theo_ka if _p["line"] == "K_alpha" else theo_kb
            diff_val = abs(e_max - theo_val)
            dE_val = e_max * (1 / np.tan(np.radians(ang_max))) * d_theta_rad
            sig_val = diff_val / dE_val

            results_by_order[n][_p["line"]] = {
                "energy": e_max,
                "diff": diff_val,
                "sigma": sig_val,
            }

        # Mark literature values
        ax_ord.axvline(
            17.48,
            color="#C73E1D",
            linestyle="--",
            alpha=0.6,
            label=r"Mo $K_\alpha$ (17.48 keV)",
        )
        ax_ord.axvline(
            19.61,
            color="#333333",
            linestyle="--",
            alpha=0.6,
            label=r"Mo $K_\beta$ (19.61 keV)",
        )

        phys.set_style(ax_ord, xlabel="Energy (keV)", ylabel="Intensity (cps)")
        ax_ord.grid(True, linestyle=":", alpha=0.6)
        ax_ord.legend(loc="upper right")
        fig_orders.savefig("data/spectrum_orders.svg")

        # Table rows for marimo UI
        table_rows = []
        for n in [1, 2, 3]:
            ka_info = results_by_order[n].get("K_alpha")
            kb_info = results_by_order[n].get("K_beta")

            ka_str = f"{ka_info['energy']:.2f} keV" if ka_info else "—"
            sig_ka_str = (
                f"{ka_info['diff']:.2f} keV ({ka_info['sigma']:.1f}σ)"
                if ka_info
                else "—"
            )

            kb_str = f"{kb_info['energy']:.2f} keV" if kb_info else "—"
            sig_kb_str = (
                f"{kb_info['diff']:.2f} keV ({kb_info['sigma']:.1f}σ)"
                if kb_info
                else "—"
            )

            table_rows.append(
                {
                    "Order (n)": n,
                    "E(K_alpha)": ka_str,
                    "K_alpha Sigma": sig_ka_str,
                    "E(K_beta)": kb_str,
                    "K_beta Sigma": sig_kb_str,
                }
            )

        orders_table_ui = mo.ui.table(
            table_rows, label="Peak Energies per Diffraction Order (LiF 2mm)"
        )

    orders_layout = (
        mo.vstack([fig_orders, orders_table_ui]) if fig_orders is not None else None
    )
    return (orders_layout,)


@app.cell(hide_code=True)
def _(angle_to_energy, kbr_2mm_ang, kbr_2mm_int, mo, np, phys, plt):
    # 3c. Compare Diffraction Orders (n=1, 2, 3) vs Actual Energy for KBr (2mm)
    _fig_kbr_orders = None
    _kbr_orders_table_ui = None
    if kbr_2mm_ang is not None and len(kbr_2mm_ang) > 0:
        _fig_kbr_orders, _ax_ord = plt.subplots(figsize=(8, 5.5), layout="constrained")

        # Angle ranges for KBr orders (n=1..6):
        # n=1: 3.0 - 10.0 deg
        # n=2: 10.0 - 15.0 deg
        # n=3: 15.0 - 22.0 deg
        # n=4: 22.0 - 27.5 deg
        # n=5: 27.5 - 34.0 deg
        # n=6: 34.0 - 39.0 deg
        _ranges = {
            1: (3.0, 10.0, "#2E86AB"),
            2: (10.0, 15.0, "#A23B72"),
            3: (15.0, 22.0, "#F18F01"),
            4: (22.0, 27.5, "#E76F51"),
            5: (27.5, 34.0, "#2A9D8F"),
            6: (34.0, 39.0, "#6A4C93"),
        }

        for _n, (_min_a, _max_a, _color) in _ranges.items():
            _mask = (kbr_2mm_ang >= _min_a) & (kbr_2mm_ang <= _max_a)
            if np.any(_mask):
                _ord_ang = kbr_2mm_ang[_mask]
                _ord_int = kbr_2mm_int[_mask]
                _ord_energy = angle_to_energy(_ord_ang, 329.9, n=_n)

                # Plot in range of characteristic lines
                _valid = (_ord_energy >= 12.0) & (_ord_energy <= 24.0)
                if np.any(_valid):
                    _sort_idx = np.argsort(_ord_energy[_valid])
                    _ax_ord.plot(
                        _ord_energy[_valid][_sort_idx],
                        _ord_int[_valid][_sort_idx],
                        label=f"Order n={_n}",
                        color=_color,
                        linewidth=1.5,
                    )

        # Confirmed peak search windows for KBr (2mm) across n=1..6
        _peaks_order_info = [
            {"n": 1, "line": "K_beta", "win": (5.2, 5.8), "lbl": r"$K_\beta$"},
            {"n": 1, "line": "K_alpha", "win": (5.9, 6.5), "lbl": r"$K_\alpha$"},
            {"n": 2, "line": "K_alpha", "win": (12.1, 12.9), "lbl": r"$K_\alpha$"},
            {"n": 3, "line": "K_beta", "win": (16.8, 17.8), "lbl": r"$K_\beta$"},
            {"n": 3, "line": "K_alpha", "win": (18.4, 19.4), "lbl": r"$K_\alpha$"},
            {"n": 4, "line": "K_beta", "win": (22.0, 23.2), "lbl": r"$K_\beta$"},
            {"n": 4, "line": "K_alpha", "win": (25.0, 26.2), "lbl": r"$K_\alpha$"},
            {"n": 5, "line": "K_beta", "win": (27.8, 29.0), "lbl": r"$K_\beta$"},
            {"n": 5, "line": "K_alpha", "win": (32.0, 33.2), "lbl": r"$K_\alpha$"},
            {"n": 6, "line": "K_beta", "win": (34.4, 35.6), "lbl": r"$K_\beta$"},
        ]

        _theo_ka, _theo_kb = 17.48, 19.61
        _d_theta_rad = np.radians(0.05)

        _results_by_order = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

        for _p in _peaks_order_info:
            _n = _p["n"]
            _mask = (kbr_2mm_ang >= _p["win"][0]) & (kbr_2mm_ang <= _p["win"][1])
            _sub_ang = kbr_2mm_ang[_mask]
            _sub_int = kbr_2mm_int[_mask]
            if len(_sub_int) > 0:
                _max_idx = np.argmax(_sub_int)
                _ang_max = _sub_ang[_max_idx]
                _counts_max = _sub_int[_max_idx]
                _e_max = angle_to_energy(_ang_max, 329.9, n=_n)

                # Scatter point ('x') on figure
                _ax_ord.scatter(
                    _e_max,
                    _counts_max,
                    color="#C73E1D",
                    marker="x",
                    s=55,
                    linewidth=1.8,
                    zorder=5,
                )

                _theo_val = _theo_ka if _p["line"] == "K_alpha" else _theo_kb
                _diff_val = abs(_e_max - _theo_val)
                _dE_val = _e_max * (1 / np.tan(np.radians(_ang_max))) * _d_theta_rad
                _sig_val = _diff_val / _dE_val

                _results_by_order[_n][_p["line"]] = {
                    "energy": _e_max,
                    "diff": _diff_val,
                    "sigma": _sig_val,
                }

        # Mark Br K-edge absorption line (13.47 keV)
        _ax_ord.axvline(
            13.47,
            color="#27AE60",
            linestyle="-.",
            alpha=0.85,
            linewidth=1.5,
            label=r"Br $K$-edge (13.47 keV)",
        )

        # Mark literature values
        _ax_ord.axvline(
            17.48,
            color="#C73E1D",
            linestyle="--",
            alpha=0.6,
            label=r"Mo $K_\alpha$ (17.48 keV)",
        )
        _ax_ord.axvline(
            19.61,
            color="#333333",
            linestyle="--",
            alpha=0.6,
            label=r"Mo $K_\beta$ (19.61 keV)",
        )

        phys.set_style(_ax_ord, xlabel="Energy (keV)", ylabel="Intensity (cps)")
        _ax_ord.grid(True, linestyle=":", alpha=0.6)
        _ax_ord.legend(loc="upper right")
        _fig_kbr_orders.savefig("data/kbr_spectrum_orders.svg")
        _fig_kbr_orders.savefig("data/kbr_spectrum_orders.png", dpi=300)

        # Table rows for marimo UI
        _table_rows = []
        for _n in [1, 2, 3, 4, 5, 6]:
            _ka_info = _results_by_order[_n].get("K_alpha")
            _kb_info = _results_by_order[_n].get("K_beta")

            _ka_str = f"{_ka_info['energy']:.2f} keV" if _ka_info else "—"
            _sig_ka_str = (
                f"{_ka_info['diff']:.2f} keV ({_ka_info['sigma']:.1f}σ)"
                if _ka_info
                else "—"
            )

            _kb_str = f"{_kb_info['energy']:.2f} keV" if _kb_info else "—"
            _sig_kb_str = (
                f"{_kb_info['diff']:.2f} keV ({_kb_info['sigma']:.1f}σ)"
                if _kb_info
                else "—"
            )

            _table_rows.append(
                {
                    "Order (n)": _n,
                    "E(K_alpha)": _ka_str,
                    "K_alpha Sigma": _sig_ka_str,
                    "E(K_beta)": _kb_str,
                    "K_beta Sigma": _sig_kb_str,
                }
            )

        _kbr_orders_table_ui = mo.ui.table(
            _table_rows, label="Peak Energies per Diffraction Order (KBr 2mm)"
        )

    _kbr_orders_layout = (
        mo.vstack([_fig_kbr_orders, _kbr_orders_table_ui])
        if _fig_kbr_orders is not None
        else None
    )
    return (_kbr_orders_layout,)


@app.cell(hide_code=True)
def _(
    findtheta,
    kbr_2mm_ang,
    kbr_2mm_int,
    lif_2mm_ang,
    lif_2mm_int,
    mo,
    np,
    phys,
    plt,
):
    # 1. Construct the Theoretical Angles Reference Table
    _theo_data = []

    # Both crystals use Molybdenum anode tube (Ka = 17.479 keV, Kb = 19.608 keV)
    _mo_lines = {"Mo K_alpha (17.479 keV)": 17479.34, "Mo K_beta (19.608 keV)": 19608.3}

    # LiF
    for _line_name, _E in _mo_lines.items():
        _n = 1
        while True:
            _theta = findtheta(_E, 201.4 * 1e-12, _n)
            if _theta is None:
                break
            _theo_data.append(
                {
                    "Crystal": "LiF (d=201.4 pm)",
                    "Emission Line": _line_name,
                    "Order (n)": _n,
                    "Bragg Angle θ_B (deg)": round(_theta, 2),
                }
            )
            _n += 1

    # KBr
    for _line_name, _E in _mo_lines.items():
        _n = 1
        while True:
            _theta = findtheta(_E, 329.9 * 1e-12, _n)
            if _theta is None:
                break
            _theo_data.append(
                {
                    "Crystal": "KBr (d=329.9 pm)",
                    "Emission Line": _line_name,
                    "Order (n)": _n,
                    "Bragg Angle θ_B (deg)": round(_theta, 2),
                }
            )
            _n += 1

    _theo_table = mo.ui.table(
        _theo_data, label="Theoretical Bragg Angles (Mo on both LiF and KBr)"
    )

    import scipy.signal as _sig

    # 2. Match LiF experimental peaks
    _comp_data_lif = []
    _offsets_lif = []
    if lif_2mm_ang is not None and len(lif_2mm_ang) > 0:
        _box = np.ones(7) / 7.0
        _smoothed = np.convolve(lif_2mm_int, _box, mode="same")
        _peaks, _ = _sig.find_peaks(_smoothed, prominence=20, distance=5)
        _peaks_found_lif = [
            (lif_2mm_ang[_p], lif_2mm_int[_p]) for _p in _peaks if lif_2mm_ang[_p] > 5.0
        ]

        for _row in _theo_data:
            if "LiF" in _row["Crystal"]:
                _best_pe = None
                _min_diff = float("inf")
                for _exp_angle, _counts in _peaks_found_lif:
                    _diff = abs(_exp_angle - _row["Bragg Angle θ_B (deg)"])
                    if _diff < _min_diff and _diff < 0.3:
                        _min_diff = _diff
                        _best_pe = (_exp_angle, _counts)

                if _best_pe:
                    _exp_angle, _counts = _best_pe
                    _theo_angle = _row["Bragg Angle θ_B (deg)"]
                    _offset = _exp_angle - _theo_angle
                    _offsets_lif.append(_offset)

                    # Estimate local background as the minimum in a 3-degree window around the peak
                    _bg_mask = (lif_2mm_ang >= _exp_angle - 1.5) & (
                        lif_2mm_ang <= _exp_angle + 1.5
                    )
                    _bg_val = np.min(lif_2mm_int[_bg_mask]) if np.any(_bg_mask) else 0.0
                    _snr = (_counts - _bg_val) / np.sqrt(max(_counts, 1.0))

                    _comp_data_lif.append(
                        {
                            "Line": _row["Emission Line"].split(" ")[1],
                            "Order (n)": _row["Order (n)"],
                            "Theoretical θ_B (deg)": round(_theo_angle, 2),
                            "Experimental θ_B (deg)": round(_exp_angle, 2),
                            "Offset Δθ_B (deg)": round(_offset, 2),
                            "Intensity (cps)": int(_counts),
                            "SNR": round(max(_snr, 0.0), 1),
                        }
                    )

    _comp_table_lif = mo.ui.table(
        _comp_data_lif, label="Experimental vs. Theoretical Peaks (Mo on LiF)"
    )

    # 3. Match KBr confirmed peaks
    _comp_data_kbr = []
    _offsets_kbr = []
    if kbr_2mm_ang is not None and len(kbr_2mm_ang) > 0:
        _kbr_confirmed_peaks = [
            (5.50, 5.50, "Mo K_beta (19.608 keV)", 1),
            (6.17, 6.20, "Mo K_alpha (17.479 keV)", 1),
            (12.42, 12.50, "Mo K_alpha (17.479 keV)", 2),
            (16.71, 17.40, "Mo K_beta (19.608 keV)", 3),
            (18.82, 18.90, "Mo K_alpha (17.479 keV)", 3),
            (25.47, 25.60, "Mo K_alpha (17.479 keV)", 4),
            (32.52, 31.30, "Mo K_alpha (17.479 keV)", 5),
            (35.10, 36.30, "Mo K_beta (19.608 keV)", 6),
        ]

        for _theo, _exp, _line_name, _n in _kbr_confirmed_peaks:
            _idx = np.argmin(np.abs(kbr_2mm_ang - _exp))
            _actual_ang = kbr_2mm_ang[_idx]
            _actual_int = kbr_2mm_int[_idx]
            _offset = _actual_ang - _theo

            _offsets_kbr.append(_offset)

            # Estimate local background as the minimum in a 3-degree window around the peak
            _bg_mask = (kbr_2mm_ang >= _actual_ang - 1.5) & (
                kbr_2mm_ang <= _actual_ang + 1.5
            )
            _bg_val = np.min(kbr_2mm_int[_bg_mask]) if np.any(_bg_mask) else 0.0
            _snr = (_actual_int - _bg_val) / np.sqrt(max(_actual_int, 1.0))

            _comp_data_kbr.append(
                {
                    "Line": _line_name.split(" ")[1],
                    "Order (n)": _n,
                    "Theoretical θ_B (deg)": round(_theo, 2),
                    "Experimental θ_B (deg)": round(_actual_ang, 2),
                    "Offset Δθ_B (deg)": round(_offset, 2),
                    "Intensity (cps)": int(_actual_int),
                    "SNR": round(max(_snr, 0.0), 1),
                }
            )

    _comp_table_kbr = mo.ui.table(
        _comp_data_kbr, label="Experimental vs. Theoretical Peaks (Mo on KBr)"
    )

    # 4. Construct comparison summary layout and calibration curves
    _avg_offset_text_lif = ""
    if _offsets_lif:
        _avg_offset_lif = np.mean(_offsets_lif)
        _std_lif = np.std(_offsets_lif, ddof=1)
        _sem_lif = _std_lif / np.sqrt(len(_offsets_lif))
        _avg_offset_text_lif = (
            f"💡 **Average LiF Goniometer Zero-Point Shift:** "
            f"$\\Delta\\theta_B = {_avg_offset_lif:.2f}^\\circ \\pm {_sem_lif:.2f}^\\circ$ "
            f"(std dev $\\sigma = {_std_lif:.2f}^\\circ$)."
        )

    _avg_offset_text_kbr = ""
    if _offsets_kbr:
        _avg_offset_kbr = np.mean(_offsets_kbr)
        _std_kbr = np.std(_offsets_kbr, ddof=1)
        _sem_kbr = _std_kbr / np.sqrt(len(_offsets_kbr))
        _avg_offset_text_kbr = (
            f"💡 **Average KBr Goniometer Zero-Point Shift:** "
            f"$\\Delta\\theta_B = {_avg_offset_kbr:.2f}^\\circ \\pm {_sem_kbr:.2f}^\\circ$ "
            f"(std dev $\\sigma = {_std_kbr:.2f}^\\circ$)."
        )

    # Generate the calibration curves plot
    if plt is not None:
        _fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), layout="constrained")

        # LiF Plot
        _lif_theo = np.array([r["Theoretical θ_B (deg)"] for r in _comp_data_lif])
        _lif_exp = np.array([r["Experimental θ_B (deg)"] for r in _comp_data_lif])

        ax1.scatter(
            _lif_theo,
            _lif_exp,
            color="#2E86AB",
            marker="o",
            s=55,
            label="Experimental Peaks",
            zorder=5,
        )
        _x_line_lif = np.linspace(np.min(_lif_theo) - 1.0, np.max(_lif_theo) + 1.0, 100)
        ax1.plot(
            _x_line_lif,
            _x_line_lif + _avg_offset_lif,
            color="#C73E1D",
            linestyle="--",
            label=f"Fit (Offset = {_avg_offset_lif:+.2f}°)",
        )
        phys.set_style(
            ax1,
            xlabel=r"Theoretical Bragg Angle $\theta_{\text{theo}}$ ($^\circ$)",
            ylabel=r"Experimental Bragg Angle $\theta_{\text{exp}}$ ($^\circ$)",
            title="LiF Goniometer Calibration",
        )
        ax1.legend()

        # KBr Plot
        _kbr_theo = np.array([r["Theoretical θ_B (deg)"] for r in _comp_data_kbr])
        _kbr_exp = np.array([r["Experimental θ_B (deg)"] for r in _comp_data_kbr])

        ax2.scatter(
            _kbr_theo,
            _kbr_exp,
            color="#F18F01",
            marker="o",
            s=55,
            label="Experimental Peaks",
            zorder=5,
        )
        _x_line_kbr = np.linspace(np.min(_kbr_theo) - 2.0, np.max(_kbr_theo) + 2.0, 100)
        ax2.plot(
            _x_line_kbr,
            _x_line_kbr + _avg_offset_kbr,
            color="#C73E1D",
            linestyle="--",
            label=f"Fit (Offset = {_avg_offset_kbr:+.2f}°)",
        )
        phys.set_style(
            ax2,
            xlabel=r"Theoretical Bragg Angle $\theta_{\text{theo}}$ ($^\circ$)",
            ylabel=r"Experimental Bragg Angle $\theta_{\text{exp}}$ ($^\circ$)",
            title="KBr Goniometer Calibration",
        )
        ax2.legend()

        _fig.savefig("data/calibration_curves.svg")

    _layout = mo.vstack(
        [
            mo.md("## Theoretical Reference & Experimental Peak Comparison"),
            mo.md(
                "This section compares calculated Bragg angles $\\theta_B$ with experimental peaks."
            ),
            mo.md("### 1. Molybdenum Theoretical Bragg Angles $\\theta_B$"),
            _theo_table,
            mo.md(
                "### 2. Experimental Peak Match & Alignment Deviation $\\Delta\\theta_B$ (LiF)"
            ),
            _comp_table_lif,
            mo.md(_avg_offset_text_lif) if _avg_offset_text_lif else mo.md(""),
            mo.md(
                "### 3. Experimental Peak Match & Alignment Deviation $\\Delta\\theta_B$ (KBr)"
            ),
            _comp_table_kbr,
            mo.md(_avg_offset_text_kbr) if _avg_offset_text_kbr else mo.md(""),
        ]
    )

    import marimo as _marimo

    if not _marimo.running_in_notebook():
        try:
            from rich.console import Console as _Console
            from rich.table import Table as _Table

            _console = _Console()
            if _comp_data_lif:
                _t_lif = _Table(
                    title="LiF (2mm) Peak Alignment",
                    show_header=True,
                    header_style="bold blue",
                )
                for _k in _comp_data_lif[0]:
                    _t_lif.add_column(_k)
                for _row in _comp_data_lif:
                    _t_lif.add_row(*[str(_v) for _v in _row.values()])
                _console.print(_t_lif)
            if _comp_data_kbr:
                _t_kbr = _Table(
                    title="KBr (2mm) Peak Alignment",
                    show_header=True,
                    header_style="bold green",
                )
                for _k in _comp_data_kbr[0]:
                    _t_kbr.add_column(_k)
                for _row in _comp_data_kbr:
                    _t_kbr.add_row(*[str(_v) for _v in _row.values()])
                _console.print(_t_kbr)
        except Exception:
            pass

    _layout
    return


@app.cell(hide_code=True)
def _(
    kbr_2mm_ang,
    kbr_2mm_int,
    lif_2mm_ang,
    lif_2mm_int,
    lif_5mm_ang,
    lif_5mm_int,
    np,
    phys,
    plt,
):
    # 4. Peak Fitting (Gaussian fit of Cu Ka and Kb first-order peaks)
    fit_status_list = []
    results = {}

    def _double_gaussian_with_bg(
        x, amp_a, ctr_a, sig_a, amp_b, ctr_b, sig_b, bg_slope, bg_inter
    ):
        gauss_a = amp_a * np.exp(-0.5 * ((x - ctr_a) / sig_a) ** 2)
        gauss_b = amp_b * np.exp(-0.5 * ((x - ctr_b) / sig_b) ** 2)
        bg = bg_slope * x + bg_inter
        return gauss_a + gauss_b + bg

    hc = 1239.84193  # eV * nm
    d_theta = 0.05  # degrees

    def _get_de(theta, d_theta_val, d_nm):
        theta_rad = np.radians(theta)
        d_theta_rad = np.radians(d_theta_val)
        deriv = -hc * np.cos(theta_rad) / (2 * d_nm * (np.sin(theta_rad) ** 2))
        return abs(deriv) * d_theta_rad

    def _angle_to_energy(angle_deg, d_nm):
        return hc / (2 * d_nm * np.sin(np.radians(angle_deg)))

    def _analyze_dataset(
        ang,
        intensity,
        d_nm,
        min_ang,
        max_ang,
        p0,
        crystal_name,
        diaphragm_mm,
        plot_filename,
    ):
        if ang is None or len(ang) == 0:
            return None

        # Fit double Gaussian
        fit_mask = (ang >= min_ang) & (ang <= max_ang)
        x_fit = ang[fit_mask]
        y_fit = intensity[fit_mask]
        y_err = np.sqrt(np.clip(y_fit, 1.0, None))

        fit_res = phys.physics_fit(_double_gaussian_with_bg, x_fit, y_fit, y_err, p0=p0)

        # Centroids and standard errors from fit
        ctr_ka, ctr_kb = fit_res.params[1], fit_res.params[4]
        err_ka, err_kb = fit_res.errors[1], fit_res.errors[4]

        fit_E_ka = _angle_to_energy(ctr_ka, d_nm)
        fit_E_ka_err = _get_de(ctr_ka, np.sqrt(err_ka**2 + d_theta**2), d_nm)
        fit_E_kb = _angle_to_energy(ctr_kb, d_nm)
        fit_E_kb_err = _get_de(ctr_kb, np.sqrt(err_kb**2 + d_theta**2), d_nm)

        # Plot the fit results
        _fig, ax_fit = plt.subplots(figsize=(8, 5), layout="constrained")
        ax_fit.errorbar(
            x_fit,
            y_fit,
            yerr=y_err,
            fmt="o",
            color="#333333",
            markersize=3,
            label="Data",
            alpha=0.6,
        )

        x_dense = np.linspace(x_fit.min(), x_fit.max(), 300)
        ax_fit.plot(
            x_dense,
            _double_gaussian_with_bg(x_dense, *fit_res.params),
            color="#C73E1D",
            linewidth=2.0,
            label="Fit",
        )

        # Plot baseline background
        ax_fit.plot(
            x_dense,
            fit_res.params[6] * x_dense + fit_res.params[7],
            color="#A23B72",
            linestyle=":",
            label="Background",
        )

        phys.set_style(
            ax_fit,
            xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)",
            ylabel="Intensity (cps)",
        )
        ax_fit.legend()
        _fig.savefig(f"data/{plot_filename}")
        plt.close(_fig)

        # Max Intensity for Ka and Kb in their specific windows
        ka_mask = (x_fit >= (ctr_ka - 0.5)) & (x_fit <= (ctr_ka + 0.5))
        x_ka = x_fit[ka_mask]
        y_ka = y_fit[ka_mask]
        max_ang_ka = x_ka[np.argmax(y_ka)]
        max_E_ka = _angle_to_energy(max_ang_ka, d_nm)
        max_E_ka_err = _get_de(max_ang_ka, d_theta, d_nm)

        kb_mask = (x_fit >= (ctr_kb - 0.5)) & (x_fit <= (ctr_kb + 0.5))
        x_kb = x_fit[kb_mask]
        y_kb = y_fit[kb_mask]
        max_ang_kb = x_kb[np.argmax(y_kb)]
        max_E_kb = _angle_to_energy(max_ang_kb, d_nm)
        max_E_kb_err = _get_de(max_ang_kb, d_theta, d_nm)

        # Centroid (Center of mass) in the same windows
        def _get_centroid(px, py):
            y_bg = np.linspace(py[0], py[-1], len(py))
            y_sub = np.clip(py - y_bg, 0, None)
            if np.sum(y_sub) > 0:
                c = np.sum(px * y_sub) / np.sum(y_sub)
            else:
                c = np.sum(px * py) / np.sum(py)
            return c

        cent_ang_ka = _get_centroid(x_ka, y_ka)
        cent_E_ka = _angle_to_energy(cent_ang_ka, d_nm)
        cent_E_ka_err = _get_de(cent_ang_ka, d_theta, d_nm)

        cent_ang_kb = _get_centroid(x_kb, y_kb)
        cent_E_kb = _angle_to_energy(cent_ang_kb, d_nm)
        cent_E_kb_err = _get_de(cent_ang_kb, d_theta, d_nm)

        return {
            "max_ka": (max_E_ka, max_E_ka_err),
            "max_kb": (max_E_kb, max_E_kb_err),
            "centroid_ka": (cent_E_ka, cent_E_ka_err),
            "centroid_kb": (cent_E_kb, cent_E_kb_err),
            "fit_ka": (fit_E_ka, fit_E_ka_err),
            "fit_kb": (fit_E_kb, fit_E_kb_err),
        }

    # 1. LiF 2mm Fit
    res_lif2 = _analyze_dataset(
        lif_2mm_ang,
        lif_2mm_int,
        0.2014,
        8.0,
        11.5,
        [3700.0, 10.3, 0.15, 1000.0, 9.2, 0.15, 0.0, 50.0],
        "LiF",
        2.0,
        "peak_fit.svg",
    )
    if res_lif2:
        results["Mo_Ka"] = res_lif2["fit_ka"]
        results["Mo_Kb"] = res_lif2["fit_kb"]

        results["Mo_Ka_LiF_2mm_max"] = res_lif2["max_ka"]
        results["Mo_Ka_LiF_2mm_centroid"] = res_lif2["centroid_ka"]
        results["Mo_Ka_LiF_2mm_gaussian"] = res_lif2["fit_ka"]

        results["Mo_Kb_LiF_2mm_max"] = res_lif2["max_kb"]
        results["Mo_Kb_LiF_2mm_centroid"] = res_lif2["centroid_kb"]
        results["Mo_Kb_LiF_2mm_gaussian"] = res_lif2["fit_kb"]

        fit_status_list.append(
            f"**LiF 2mm**: $K_\\alpha = {res_lif2['fit_ka'][0] / 1000.0:.3f} \\pm {res_lif2['fit_ka'][1] / 1000.0:.3f} \\text{{ keV}}$, $K_\\beta = {res_lif2['fit_kb'][0] / 1000.0:.3f} \\pm {res_lif2['fit_kb'][1] / 1000.0:.3f} \\text{{ keV}}$"
        )

    # 2. KBr 2mm Fit
    res_kbr2 = _analyze_dataset(
        kbr_2mm_ang,
        kbr_2mm_int,
        0.3299,
        5.0,
        7.0,
        [770.0, 6.2, 0.15, 270.0, 5.5, 0.15, 0.0, 50.0],
        "KBr",
        2.0,
        "kbr_peak_fit.svg",
    )
    if res_kbr2:
        results["Mo_Ka_KBr_2mm_max"] = res_kbr2["max_ka"]
        results["Mo_Ka_KBr_2mm_centroid"] = res_kbr2["centroid_ka"]
        results["Mo_Ka_KBr_2mm_gaussian"] = res_kbr2["fit_ka"]

        results["Mo_Kb_KBr_2mm_max"] = res_kbr2["max_kb"]
        results["Mo_Kb_KBr_2mm_centroid"] = res_kbr2["centroid_kb"]
        results["Mo_Kb_KBr_2mm_gaussian"] = res_kbr2["fit_kb"]

        fit_status_list.append(
            f"**KBr 2mm**: $K_\\alpha = {res_kbr2['fit_ka'][0] / 1000.0:.3f} \\pm {res_kbr2['fit_ka'][1] / 1000.0:.3f} \\text{{ keV}}$, $K_\\beta = {res_kbr2['fit_kb'][0] / 1000.0:.3f} \\pm {res_kbr2['fit_kb'][1] / 1000.0:.3f} \\text{{ keV}}$"
        )

    # 3. LiF 5mm Fit
    res_lif5 = _analyze_dataset(
        lif_5mm_ang,
        lif_5mm_int,
        0.2014,
        8.0,
        11.5,
        [3700.0, 10.3, 0.3, 1000.0, 9.2, 0.3, 0.0, 50.0],
        "LiF",
        5.0,
        "lif5mm_peak_fit.svg",
    )
    if res_lif5:
        results["Mo_Ka_LiF_5mm_max"] = res_lif5["max_ka"]
        results["Mo_Ka_LiF_5mm_centroid"] = res_lif5["centroid_ka"]
        results["Mo_Ka_LiF_5mm_gaussian"] = res_lif5["fit_ka"]

        results["Mo_Kb_LiF_5mm_max"] = res_lif5["max_kb"]
        results["Mo_Kb_LiF_5mm_centroid"] = res_lif5["centroid_kb"]
        results["Mo_Kb_LiF_5mm_gaussian"] = res_lif5["fit_kb"]

        fit_status_list.append(
            f"**LiF 5mm**: $K_\\alpha = {res_lif5['fit_ka'][0] / 1000.0:.3f} \\pm {res_lif5['fit_ka'][1] / 1000.0:.3f} \\text{{ keV}}$, $K_\\beta = {res_lif5['fit_kb'][0] / 1000.0:.3f} \\pm {res_lif5['fit_kb'][1] / 1000.0:.3f} \\text{{ keV}}$"
        )

    fit_status = "Successfully fitted peaks:\n\n" + "\n\n".join(fit_status_list)

    import marimo as _marimo

    if not _marimo.running_in_notebook():
        try:
            from rich.console import Console as _Console

            _console = _Console()
            _console.print(f"\n[bold green]{fit_status}[/bold green]\n")
        except Exception:
            pass

    return fit_status, results


@app.cell(hide_code=True)
def _(fit_status, mo):
    mo.md(f"""
    ### Peak Fitting Results\n{fit_status}
    """)
    return


@app.cell(hide_code=True)
def _(data_dir, json, mo, phys, results):
    if results:
        # Prepare constant schema list
        # We will save the fitted energies to the constants directory
        # complying with studies project rules.
        constants_list = [
            {
                "hebrew_name": "אנרגיית קו אלפא מוליבדן",
                "english_name": "Molybdenum K-alpha Energy",
                "hebrew_var": "אנרגיית_קא_מוליבדן",
                "english_var": "E_Mo_Ka",
                "symbol": "E_(K_alpha)",
                "value": results["Mo_Ka"][0] / 1000.0,
                "error": results["Mo_Ka"][1] / 1000.0,
                "units": '"keV"',
                "scale": 1.0,
                "fmt_spec": ".3f",
                "suffix": "",
            },
            {
                "hebrew_name": "אנרגיית קו בטא מוליבדן",
                "english_name": "Molybdenum K-beta Energy",
                "hebrew_var": "אנרגיית_קב_מוליבדן",
                "english_var": "E_Mo_Kb",
                "symbol": "E_(K_beta)",
                "value": results["Mo_Kb"][0] / 1000.0,
                "error": results["Mo_Kb"][1] / 1000.0,
                "units": '"keV"',
                "scale": 1.0,
                "fmt_spec": ".3f",
                "suffix": "",
            },
        ]

        # Add all 18 configuration constants dynamically
        crystals = [
            ("LiF_2mm", "ליפ_2ממ", "LiF 2mm"),
            ("KBr_2mm", "קבר_2ממ", "KBr 2mm"),
            ("LiF_5mm", "ליפ_5ממ", "LiF 5mm"),
        ]
        lines = [("Ka", "קא", "K-alpha", "K_alpha"), ("Kb", "קב", "K-beta", "K_beta")]
        criteria = [
            ("max", "עוצמה", "Max", "max"),
            ("centroid", "צנטרואיד", "Centroid", "centroid"),
            ("gaussian", "גאוסיאן", "Gaussian", "gaussian"),
        ]

        for crys_code, crys_heb, crys_eng in crystals:
            for line_code, line_heb, line_eng_name, line_symbol in lines:
                for crit_code, crit_heb, crit_eng_name, crit_symbol in criteria:
                    res_key = f"Mo_{line_code}_{crys_code}_{crit_code}"
                    if res_key in results:
                        # Export English suffix version (e.g. _max)
                        constants_list.append(
                            {
                                "hebrew_name": f"אנרגיית קו {line_heb} מוליבדן {crys_heb.replace('_', ' ')} {crit_heb}",
                                "english_name": f"Molybdenum {line_eng_name} {crys_eng} {crit_eng_name} Energy",
                                "hebrew_var": f"אנרגיית_{line_heb}_מוליבדן_{crys_heb}_{crit_code}",
                                "english_var": f"E_Mo_{line_code}_{crys_code}_{crit_code}",
                                "symbol": f'E_({line_symbol}, "{crys_eng}, {crit_symbol}")',
                                "value": results[res_key][0] / 1000.0,
                                "error": results[res_key][1] / 1000.0,
                                "units": '"keV"',
                                "scale": 1.0,
                                "fmt_spec": ".3f",
                                "suffix": "",
                            }
                        )
                        # Export Hebrew suffix version (e.g. _עוצמה)
                        constants_list.append(
                            {
                                "hebrew_name": f"אנרגיית קו {line_heb} מוליבדן {crys_heb.replace('_', ' ')} {crit_heb} עברית",
                                "english_name": f"Molybdenum {line_eng_name} {crys_eng} {crit_eng_name} Energy Hebrew",
                                "hebrew_var": f"אנרגיית_{line_heb}_מוליבדן_{crys_heb}_{crit_heb}",
                                "english_var": f"E_Mo_{line_code}_{crys_code}_{crit_code}_heb",
                                "symbol": f'E_({line_symbol}, "{crys_eng}, {crit_symbol}")',
                                "value": results[res_key][0] / 1000.0,
                                "error": results[res_key][1] / 1000.0,
                                "units": '"keV"',
                                "scale": 1.0,
                                "fmt_spec": ".3f",
                                "suffix": "",
                            }
                        )

        # Export the constants to data/ directory
        exported = phys.export_constants(constants_list, data_dir)

        # Append statistical distances (z-scores) dynamically to constants.typ
        typ_path = data_dir / "constants.typ"
        if typ_path.exists():
            typ_content = typ_path.read_text(encoding="utf-8")
            z_lines = []
            lit_vals = {"Ka": 17.479, "Kb": 19.608}
            for crys_code, crys_heb, _crys_eng in crystals:
                for line_code, line_heb, _line_eng_name, _line_symbol in lines:
                    for crit_code, crit_heb, _crit_eng_name, _crit_symbol in criteria:
                        res_key = f"Mo_{line_code}_{crys_code}_{crit_code}"
                        if res_key in results:
                            val_kev = results[res_key][0] / 1000.0
                            err_kev = results[res_key][1] / 1000.0
                            lit_kev = lit_vals[line_code]
                            z_score = abs(val_kev - lit_kev) / err_kev
                            rel_err = (abs(val_kev - lit_kev) / lit_kev) * 100.0

                            var_base = (
                                f"אנרגיית_{line_heb}_מוליבדן_{crys_heb}_{crit_code}"
                            )
                            eng_base = f"E_Mo_{line_code}_{crys_code}_{crit_code}"

                            z_lines.append(
                                f"#let {var_base}_מרחק = ${z_score:.1f} sigma$\n"
                            )
                            z_lines.append(f"#let {eng_base}_z = {var_base}_מרחק\n")
                            z_lines.append(
                                f"#let {var_base}_שגיאה_יחסית = ${rel_err:.2f} %$\n"
                            )
                            z_lines.append(
                                f"#let {eng_base}_rel_err = {var_base}_שגיאה_יחסית\n"
                            )

                            var_heb_base = (
                                f"אנרגיית_{line_heb}_מוליבדן_{crys_heb}_{crit_heb}"
                            )
                            eng_heb_base = (
                                f"E_Mo_{line_code}_{crys_code}_{crit_code}_heb"
                            )
                            z_lines.append(
                                f"#let {var_heb_base}_מרחק = ${z_score:.1f} sigma$\n"
                            )
                            z_lines.append(
                                f"#let {eng_heb_base}_z = {var_heb_base}_מרחק\n"
                            )
                            z_lines.append(
                                f"#let {var_heb_base}_שגיאה_יחסית = ${rel_err:.2f} %$\n"
                            )
                            z_lines.append(
                                f"#let {eng_heb_base}_rel_err = {var_heb_base}_שגיאה_יחסית\n"
                            )

            typ_path.write_text(
                typ_content + "\n// Statistical distances\n" + "".join(z_lines),
                encoding="utf-8",
            )

        export_msg = mo.md(
            f"""**Constants Saved**: Successfully saved fitted physical parameters to `data/constants.json` and `data/constants.typ`.

    ```json
    {json.dumps(exported, indent=2, ensure_ascii=False)}
    ```"""
        ).callout(kind="success")
    else:
        export_msg = mo.md("No fit results available to export yet.").callout(
            kind="warn"
        )

    export_msg
    return


if __name__ == "__main__":
    import sys

    if "--script" in sys.argv or "-s" in sys.argv:
        import json
        from pathlib import Path

        from rich.console import Console
        from rich.table import Table

        console = Console()
        console.print(
            "[bold cyan]=======================================================[/]"
        )
        console.print(
            "[bold cyan]       Bragg Spectroscopy Marimo Analysis Results      [/]"
        )
        console.print(
            "[bold cyan]=======================================================[/]"
        )

        # Load constants.json if it exists
        constants_path = Path("data/constants.json")
        if constants_path.exists():
            try:
                data = json.loads(constants_path.read_text(encoding="utf-8"))
                table = Table(
                    title="Fitted X-ray Energies & Error Analysis",
                    show_header=True,
                    header_style="bold magenta",
                )
                table.add_column("Parameter / Line", style="dim")
                table.add_column("Experimental Value (keV)", justify="right")
                table.add_column("Uncertainty (keV)", justify="right")
                table.add_column("Literature (keV)", justify="right")
                table.add_column("Relative Error", justify="right")
                table.add_column("Statistical Distance", justify="right")

                for item in data:
                    table.add_row(
                        item.get("name", ""),
                        f"{item.get('value', 0.0):.3f}",
                        f"{item.get('error', 0.0):.3f}",
                        f"{item.get('lit', 0.0):.3f}",
                        f"{item.get('percentage_error', 0.0):.2f}%",
                        f"{item.get('z_score', 0.0):.1f} sigma",
                    )
                console.print(table)
            except Exception as e:
                console.print(f"[red]Error parsing constants.json: {e}[/]")
        else:
            console.print(
                "[yellow]No data/constants.json found. Run the marimo server or standalone.py first to export it.[/]"
            )
    else:
        app.run()
