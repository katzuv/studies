import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from pathlib import Path
    import json
    from scipy.optimize import curve_fit
    from scipy.integrate import trapezoid

    # Import the custom physics lab helper library
    import sys
    sys.path.append(str(Path(r"c:\Users\danda\PycharmProjects\studies")))
    import physlab.core as phys

    # Ensure output data directory exists
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return Path, data_dir, json, mo, np, phys, plt, trapezoid


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bragg X-ray Spectroscopy Data Analysis
    This interactive notebook assists in analyzing X-ray emission spectra. You can switch between **Simulation Mode** (for testing at home) and **Lab Mode** (for uploading real files recorded in the lab).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # User selects the operating mode
    mode_selector = mo.ui.radio(
        options=["Simulation / Testing", "Lab Data (File Upload)"],
        value="Simulation / Testing",
        label="Select Mode:"
    )
    mode_selector
    return (mode_selector,)


@app.cell(hide_code=True)
def _(mo, mode_selector):
    is_sim = mode_selector.value == "Simulation / Testing"

    # Render file upload components or instructions based on mode
    if is_sim:
        mode_instruction = mo.md(
            r"**Simulation Mode Active**: The notebook will automatically generate and use high-fidelity simulated datasets for LiF (2mm), KBr (2mm), and LiF (1mm) with a Copper (Cu) tube."
        ).callout(kind="info")
    else:
        mode_instruction = mo.md(
            r"**Lab Mode Active**: Please upload your goniometer scan data. The expected format is a text file with two tab/space/comma separated columns: `Angle (deg)` and `Intensity (cps)`."
        ).callout(kind="warn")

    mode_instruction
    return (is_sim,)


@app.cell(hide_code=True)
def _(is_sim, mo):
    # File uploaders for Lab Mode
    lif_2mm_uploader = mo.ui.file(label="Upload LiF (2mm) Scan File", filetypes=[".txt", ".csv"]) if not is_sim else None
    kbr_2mm_uploader = mo.ui.file(label="Upload KBr (2mm) Scan File", filetypes=[".txt", ".csv"]) if not is_sim else None
    lif_1mm_uploader = mo.ui.file(label="Upload LiF (1mm) Scan File", filetypes=[".txt", ".csv"]) if not is_sim else None

    # Show them in a row/column if not in simulation mode
    if not is_sim:
        upload_ui = mo.vstack([
            lif_2mm_uploader,
            kbr_2mm_uploader,
            lif_1mm_uploader
        ])
    else:
        upload_ui = mo.md("Uploaders hidden in Simulation Mode.")

    upload_ui
    return kbr_2mm_uploader, lif_1mm_uploader, lif_2mm_uploader


@app.cell(hide_code=True)
def _(data_dir, np):
    def generate_synthetic_data(crystal_name, diaphragm_mm, noise_scale=15.0):
        """Generates realistic Bragg diffraction intensities for Copper (Cu) anode tube (35kV, 1mA)."""
        angles = np.arange(3.0, 75.1, 0.1) # Bragg angles in degrees

        # Crystal parameters
        # LiF(200) d=201.4pm, KBr(200) d=329.9pm
        d = 201.4 if crystal_name == "LiF" else 329.9
        hc = 1239.84193 # eV*nm = 1239841.93 eV*pm

        # Calculate matching energies (n=1) for Bragg angles to construct background
        energies_n1 = (hc * 1e3) / (2 * d * np.sin(np.radians(angles))) # in eV
        energies_n1_kev = energies_n1 / 1000.0

        # Bremsstrahlung background: Kramers' Law approximation + Duane-Hunt limit at 35keV
        E_max = 35.0 # keV
        I_brem = np.zeros_like(angles)

        # Only energy values below E_max are produced
        valid_mask = energies_n1_kev < E_max
        # Kramers law / smooth background curve
        I_brem[valid_mask] = 1200.0 * (E_max - energies_n1_kev[valid_mask]) * (1.0 - np.exp(-energies_n1_kev[valid_mask] / 5.0)) / (energies_n1_kev[valid_mask] ** 0.5)

        # Absorption edge step for Bromine K-edge in KBr (13.47 keV)
        if crystal_name == "KBr":
            # Above 13.47 keV, crystal absorption increases dramatically, so reflectivity drops
            step_mask = energies_n1_kev > 13.47
            I_brem[step_mask] *= 0.35

        # Add characteristic lines (Cu Ka = 8.04 keV, Cu Kb = 8.91 keV)
        # We model diffraction orders n = 1, 2, 3
        I_peaks = np.zeros_like(angles)

        # Resolution of peaks depends on diaphragm size
        sigma_theta = 0.15 if diaphragm_mm == 2.0 else 0.08

        peaks_def = [
            {"name": "Ka", "E": 8.04, "rel_int": 10000.0},
            {"name": "Kb", "E": 8.91, "rel_int": 2500.0}
        ]

        for n in [1, 2, 3]:
            for p in peaks_def:
                # Find Bragg angle for this order n and energy E
                val_to_arcsin = (hc * n) / (2 * d * p["E"])
                if val_to_arcsin <= 1.0:
                    theta_peak_deg = np.degrees(np.arcsin(val_to_arcsin))
                    # Scale intensity by 1/n^1.5 for higher order efficiency loss
                    peak_amp = p["rel_int"] * (1.0 / (n ** 1.5)) * (1.0 if diaphragm_mm == 2.0 else 0.55)
                    # Gaussian peak shape
                    I_peaks += peak_amp * np.exp(-0.5 * ((angles - theta_peak_deg) / sigma_theta) ** 2)

        # Total intensity with noise
        total_intensity = I_brem + I_peaks
        noise = np.random.normal(0, noise_scale, size=len(angles))
        # Ensure intensity is non-negative and counts are integers
        total_intensity = np.clip(total_intensity + noise, 0, None)

        # Save to file
        file_path = data_dir / f"simulated_{crystal_name.lower()}_{int(diaphragm_mm)}mm.txt"
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
    lif_1mm_uploader,
    lif_2mm_uploader,
    np,
):
    # Parse files based on current mode
    def load_data(uploader, crystal_name, diaphragm_mm):
        if is_sim:
            # Generate and load simulation file
            angles, intensity, filepath = generate_synthetic_data(crystal_name, diaphragm_mm)
            return angles, intensity, filepath
        else:
            # Load uploaded file
            if uploader is None or not uploader.value:
                return None, None, None

            # Get filename and extension
            orig_name = uploader.value[0]["name"]
            ext = Path(orig_name).suffix
            if not ext:
                ext = ".txt"

            # Destination name based on parameters (e.g. lif2mm.csv)
            dest_filename = f"{crystal_name.lower()}{int(diaphragm_mm)}mm{ext}"
            dest_path = data_dir / dest_filename

            # Save the file to data/ directory
            dest_path.write_bytes(uploader.value[0]["contents"])

            # Read bytes and convert to text
            content = uploader.value[0]["contents"].decode("utf-8")
            angles = []
            intensity = []

            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        angles.append(float(parts[0]))
                        intensity.append(float(parts[1]))
                    except ValueError:
                        continue

            return np.array(angles), np.array(intensity), dest_path

    # Load all three datasets
    lif_2mm_ang, lif_2mm_int, lif_2mm_file = load_data(lif_2mm_uploader, "LiF", 2.0)
    kbr_2mm_ang, kbr_2mm_int, kbr_2mm_file = load_data(kbr_2mm_uploader, "KBr", 2.0)
    lif_1mm_ang, lif_1mm_int, lif_1mm_file = load_data(lif_1mm_uploader, "LiF", 1.0)
    return (
        kbr_2mm_ang,
        kbr_2mm_file,
        kbr_2mm_int,
        lif_1mm_ang,
        lif_1mm_file,
        lif_1mm_int,
        lif_2mm_ang,
        lif_2mm_file,
        lif_2mm_int,
    )


@app.cell(hide_code=True)
def _(kbr_2mm_file, lif_1mm_file, lif_2mm_file, mo):
    # Status display
    def file_status(filename, label):
        if filename:
            return mo.md(f"🟢 **{label}**: Loaded from `{filename.name}`")
        return mo.md(f"🔴 **{label}**: No file uploaded.")

    status_block = mo.vstack([
        file_status(lif_2mm_file, "LiF (2mm)"),
        file_status(kbr_2mm_file, "KBr (2mm)"),
        file_status(lif_1mm_file, "LiF (1mm)"),
    ])
    status_block
    return


@app.cell(hide_code=True)
def _(np):
    def angle_to_energy(angle_deg, d_pm, n=1):
        """Converts Bragg angle in degrees to energy in keV."""
        hc = 1239.84193 # eV*nm
        d_nm = d_pm / 1000.0
        wavelength = (2 * d_nm * np.sin(np.radians(angle_deg))) / n
        energy_ev = hc / wavelength
        return energy_ev / 1000.0 # Convert to keV


    return (angle_to_energy,)


@app.cell(hide_code=True)
def _(angle_to_energy, lif_2mm_ang, lif_2mm_int, phys, plt):
    # 1. Plot raw spectrum vs angle and energy
    fig_raw = None
    if lif_2mm_ang is not None and len(lif_2mm_ang) > 0:
        # Create double panel plot (Angle vs Energy)
        _fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Plot vs Angle (linear and log scale)
        ax1.plot(lif_2mm_ang, lif_2mm_int, label="LiF (2mm)", color="#2E86AB")
        ax1.set_yscale("log")
        phys.set_style(ax1, xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)", ylabel="Intensity (log cps)")
        ax1.legend()

        # Convert angles to Energy (n=1) for plot
        energies_kev = angle_to_energy(lif_2mm_ang, 201.4, n=1)
        # filter out very small angles that give non-physical large energies
        valid_idx = lif_2mm_ang > 3.0

        ax2.plot(energies_kev[valid_idx], lif_2mm_int[valid_idx], label="LiF (2mm)", color="#A23B72")
        phys.set_style(ax2, xlabel=r"Energy $E$ (keV)", ylabel="Intensity (cps)")
        ax2.legend()

        plt.tight_layout()
        fig_raw = _fig
        _fig.savefig("data/spectrum_orders.svg")

    fig_raw
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
        _fig, ax_crys = plt.subplots(figsize=(8, 5))

        # Convert both to energy (n=1)
        lif_e = angle_to_energy(lif_2mm_ang[lif_2mm_ang > 3.0], 201.4, n=1)
        lif_y = lif_2mm_int[lif_2mm_ang > 3.0]

        kbr_e = angle_to_energy(kbr_2mm_ang[kbr_2mm_ang > 3.0], 329.9, n=1)
        kbr_y = kbr_2mm_int[kbr_2mm_ang > 3.0]

        ax_crys.plot(lif_e, lif_y, label="LiF (200) - $d=201.4$ pm", color="#2E86AB")
        ax_crys.plot(kbr_e, kbr_y, label="KBr (200) - $d=329.9$ pm", color="#F18F01")

        # Mark K-edge of Bromine (13.47 keV)
        ax_crys.axvline(13.47, color="#C73E1D", linestyle="--", alpha=0.8, label="Br K-edge: 13.47 keV")

        phys.set_style(ax_crys, xlabel="Energy (keV)", ylabel="Intensity (cps)")
        ax_crys.legend()

        plt.tight_layout()
        fig_crystal = _fig
        _fig.savefig("data/crystal_comparison.svg")

    fig_crystal
    return


@app.cell(hide_code=True)
def _(
    lif_1mm_ang,
    lif_1mm_int,
    lif_2mm_ang,
    lif_2mm_int,
    phys,
    plt,
    trapezoid,
):
    # 3. Compare Diaphragms (2mm vs 1mm)
    fig_diaphragm = None
    if lif_2mm_ang is not None and lif_1mm_ang is not None:
        _fig, ax_dia = plt.subplots(figsize=(8, 5))

        # Crop to the Cu Ka and Kb first-order peak region
        # For LiF, 8.04 keV is around 22.4 degrees, 8.91 keV is around 20.1 degrees
        mask_2mm = (lif_2mm_ang > 18.0) & (lif_2mm_ang < 25.0)
        mask_1mm = (lif_1mm_ang > 18.0) & (lif_1mm_ang < 25.0)

        # Normalize by area to compare line resolution
        y_2mm_norm = lif_2mm_int[mask_2mm] / trapezoid(lif_2mm_int[mask_2mm], lif_2mm_ang[mask_2mm])
        y_1mm_norm = lif_1mm_int[mask_1mm] / trapezoid(lif_1mm_int[mask_1mm], lif_1mm_ang[mask_1mm])

        ax_dia.plot(lif_2mm_ang[mask_2mm], y_2mm_norm, label="2mm Diaphragm", color="#2E86AB")
        ax_dia.plot(lif_1mm_ang[mask_1mm], y_1mm_norm, label="1mm Diaphragm", color="#A23B72")

        phys.set_style(ax_dia, xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)", ylabel="Normalized Intensity")
        ax_dia.legend()

        plt.tight_layout()
        fig_diaphragm = _fig
        _fig.savefig("data/collimator_comparison.svg")

    fig_diaphragm
    return


@app.cell(hide_code=True)
def _(lif_2mm_ang, lif_2mm_int, np, phys, plt):
    # 4. Peak Fitting (Gaussian fit of Cu Ka and Kb first-order peaks)
    fit_status = ""
    fig_fit = None
    results = {}

    if lif_2mm_ang is not None and len(lif_2mm_ang) > 0:
        # Define multi-peak model function (Gaussian Ka + Kb + linear background)
        def double_gaussian_with_bg(x, amp_a, ctr_a, sig_a, amp_b, ctr_b, sig_b, bg_slope, bg_inter):
            gauss_a = amp_a * np.exp(-0.5 * ((x - ctr_a) / sig_a) ** 2)
            gauss_b = amp_b * np.exp(-0.5 * ((x - ctr_b) / sig_b) ** 2)
            bg = bg_slope * x + bg_inter
            return gauss_a + gauss_b + bg

        # Fit in angle domain first around n=1 peaks (18.5 - 24.5 degrees)
        fit_mask = (lif_2mm_ang >= 18.5) & (lif_2mm_ang <= 24.5)
        x_fit = lif_2mm_ang[fit_mask]
        y_fit = lif_2mm_int[fit_mask]
        y_err = np.sqrt(np.clip(y_fit, 1.0, None)) # Poisson error approximation

        # Initial guesses: [amp_a, ctr_a, sig_a, amp_b, ctr_b, sig_b, bg_slope, bg_inter]
        p0 = [
            max(y_fit), 22.4, 0.15,
            max(y_fit)/4.0, 20.1, 0.15,
            0.0, min(y_fit)
        ]

        try:
            fit_res = phys.physics_fit(double_gaussian_with_bg, x_fit, y_fit, y_err, p0=p0)

            # Extract fitted centroids
            ctr_ka, ctr_kb = fit_res.params[1], fit_res.params[4]
            err_ka, err_kb = fit_res.errors[1], fit_res.errors[4]

            # Plot the fit results
            _fig, ax_fit = plt.subplots(figsize=(8, 5))
            ax_fit.errorbar(x_fit, y_fit, yerr=y_err, fmt="o", color="#333333", markersize=3, label="Data", alpha=0.6)

            x_dense = np.linspace(18.5, 24.5, 300)
            ax_fit.plot(x_dense, double_gaussian_with_bg(x_dense, *fit_res.params), color="#C73E1D", linewidth=2.0, label="Fit")

            # Plot baseline background
            ax_fit.plot(x_dense, fit_res.params[6] * x_dense + fit_res.params[7], color="#A23B72", linestyle=":", label="Background")

            phys.set_style(ax_fit, xlabel=r"Bragg Angle $\theta_B$ ($^\circ$)", ylabel="Intensity (cps)")
            ax_fit.legend()

            plt.tight_layout()
            fig_fit = _fig
            _fig.savefig("data/peak_fit.svg")

            # Convert angle centroids to energy (keV) using d = 201.4 pm
            E_ka = 1239.84193 / (2 * 0.2014 * np.sin(np.radians(ctr_ka)))
            E_kb = 1239.84193 / (2 * 0.2014 * np.sin(np.radians(ctr_kb)))

            # Propagating errors: dE/d\theta = -hc*cos(\theta) / (2*d*sin^2(\theta))
            # dE = |dE/d\theta| * d\theta
            d_nm = 0.2014
            hc = 1239.84193
            def get_de(theta, d_theta):
                theta_rad = np.radians(theta)
                d_theta_rad = np.radians(d_theta)
                deriv = -hc * np.cos(theta_rad) / (2 * d_nm * (np.sin(theta_rad)**2))
                return abs(deriv) * d_theta_rad

            E_ka_err = get_de(ctr_ka, err_ka)
            E_kb_err = get_de(ctr_kb, err_kb)

            results = {
                "Cu_Ka": (E_ka, E_ka_err),
                "Cu_Kb": (E_kb, E_kb_err)
            }

            fit_status = f"Successfully fitted peaks: $\\text{{Cu }} K_\\alpha = {E_ka/1000.0:.3f} \\pm {E_ka_err/1000.0:.3f} \\text{{ keV}}$ and $\\text{{Cu }} K_\\beta = {E_kb/1000.0:.3f} \\pm {E_kb_err/1000.0:.3f} \\text{{ keV}}$."

        except Exception as e:
            fit_status = f"Fit failed: {str(e)}"
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
                "hebrew_name": "אנרגיית קו אלפא נחושת",
                "english_name": "Copper K-alpha Energy",
                "hebrew_var": "אנרגיית_קא_נחושת",
                "english_var": "E_Cu_Ka",
                "symbol": "E_(K_alpha)",
                "value": results["Cu_Ka"][0] / 1000.0,
                "error": results["Cu_Ka"][1] / 1000.0,
                "units": r"$" + '"keV"' + r"$",
                "scale": 1.0,
                "fmt_spec": ".3f",
                "suffix": ""
            },
            {
                "hebrew_name": "אנרגיית קו בטא נחושת",
                "english_name": "Copper K-beta Energy",
                "hebrew_var": "אנרגיית_קב_נחושת",
                "english_var": "E_Cu_Kb",
                "symbol": "E_(K_beta)",
                "value": results["Cu_Kb"][0] / 1000.0,
                "error": results["Cu_Kb"][1] / 1000.0,
                "units": r"$" + '"keV"' + r"$",
                "scale": 1.0,
                "fmt_spec": ".3f",
                "suffix": ""
            }
        ]

        # Export the constants to data/ directory
        exported = phys.export_constants(constants_list, data_dir)
        export_msg = mo.md(
            f"""**Constants Saved**: Successfully saved fitted physical parameters to `data/constants.json` and `data/constants.typ`.

    ```json
    {json.dumps(exported, indent=2, ensure_ascii=False)}
    ```"""
        ).callout(kind="success")
    else:
        export_msg = mo.md("No fit results available to export yet.").callout(kind="warn")

    export_msg
    return


if __name__ == "__main__":
    app.run()
