# Bragg X-ray Spectroscopy: Data Analysis & Guide

This README outlines the theory, equipment parameters, expected line energies, and specific calculations required for analyzing the data from the Bragg X-ray spectroscopy experiment. It serves as a standalone context manual for data processing.

## 1. Physical Formulas & Bragg's Law

### Bragg Diffraction Condition
When X-ray radiation is reflected off crystal lattice planes, constructive interference occurs at Bragg angles $\theta_B$ satisfying:
$$2 d \sin(\theta_B) = n \lambda$$
- $d$: Interplanar spacing of the analyzer crystal.
- $\theta_B$: Bragg angle (half of the detector angle $2\theta_B$ in the $1:2$ coupling mode).
- $n$: Diffraction order ($n = 1, 2, 3, \dots$).
- $\lambda$: Wavelength of the diffracted X-rays.

### Photon Energy Conversion
Using the relation $E = \frac{h c}{\lambda}$, the Bragg condition yields the photon energy $E$:
$$E(\theta_B) = \frac{h c \cdot n}{2 d \sin(\theta_B)}$$

#### Numerical Constants
- Planck's constant times speed of light: $h c \approx 1239.84193 \text{ eV}\cdot\text{nm} = 1.23984193 \text{ keV}\cdot\text{nm}$
- For $d$ in picometers ($\text{pm}$):
  $$E(\theta_B) = \frac{1239.84193 \cdot 10^3 \text{ eV}\cdot\text{pm}}{2 d \sin(\theta_B)} \cdot n = \frac{619920.965}{d \sin(\theta_B)} \cdot n \quad [\text{eV}]$$

---

## 2. Experimental Constants

### Analyzer Crystals
| Crystal | Reflection Plane | Lattice Parameter $a$ | Interplanar Spacing $d_{200}$ |
| :--- | :--- | :--- | :--- |
| **LiF** | $(200)$ | $402.8 \text{ pm}$ ($4.028 \text{ \AA}$) | **$201.4 \text{ pm}$ ($2.014 \text{ \AA}$)** |
| **KBr** | $(200)$ | $659.8 \text{ pm}$ ($6.598 \text{ \AA}$) | **$329.9 \text{ pm}$ ($3.299 \text{ \AA}$)** |

*Note on calculation:* For cubic structures, $d_{hkl} = \frac{a}{\sqrt{h^2+k^2+l^2}}$. For $(200)$, $d_{200} = \frac{a}{2}$.

### Characteristic X-ray Lines (Expected Energies in $\text{keV}$)
Characteristic lines are produced by transitions filling K or L shell vacancies.

| Metal Anode | $Z$ | $K_{\alpha 1,2}$ (Siegbahn) | $K_{\beta 1}$ (Siegbahn) | $L$ Series (Approx. range) |
| :--- | :--- | :--- | :--- | :--- |
| **Copper (Cu)** | $29$ | $8.04 \text{ keV}$ | $8.91 \text{ keV}$ | $0.93 \text{ keV}$ (usually too low to detect) |
| **Iron (Fe)** | $26$ | $6.40 \text{ keV}$ | $7.06 \text{ keV}$ | $0.71 \text{ keV}$ (usually too low to detect) |
| **Molybdenum (Mo)** | $42$ | $17.44 \text{ keV}$ | $19.61 \text{ keV}$ | $2.29\text{--}2.5 \text{ keV}$ |
| **Tungsten (W)** | $74$ | $59.3 \text{ keV}$ (exceeds $35 \text{ kV}$ anode voltage) | $67.2 \text{ keV}$ | $L_{\alpha 1}$: $8.40 \text{ keV}$, $L_{\beta 1}$: $9.67 \text{ keV}$ |

### Absorption Edges
- **Bromine (Br) K-edge**: **$13.47 \text{ keV}$**.
  - When using the **KBr** analyzer crystal, self-absorption of Bromine atoms inside the crystal increases dramatically above $13.47 \text{ keV}$, which causes a sudden drop in the crystal's reflectivity.
  - This manifests as a sharp downward step in the measured intensity of the bremsstrahlung background at the Bragg angle corresponding to $13.47 \text{ keV}$.

---

## 3. Data Analysis Requirements

### Data Cleaning
1.  **Exclude $n=0$ (Direct Beam)**: The scan around small angles ($\theta_B \lesssim 3^\circ$) contains the intense direct transmission beam. Cut this section out prior to analyzing diffraction spectra.
2.  **Log-Scale Inspection**: Plotting $\log(\text{Intensity})$ vs. Angle helps clearly distinguish weak high-order peaks ($n=2, 3$) and the bremsstrahlung background profile.

### Calculations & Fitting
1.  **Peak Energy Centroid**: Use Gaussian fitting to find the peak positions:
    $$I(E) = I_{bg}(E) + I_0 \exp\left( -\frac{(E - E_c)^2}{2\sigma^2} \right)$$
    The centroid $E_c$ represents the energy of the transition.
2.  **Energy Resolution (FWHM)**:
    $$\Delta E = 2\sqrt{2\ln 2} \cdot \sigma \approx 2.355 \sigma$$
    Compare this actual line width with the detector sampling resolution $\Delta \theta_B \cdot \frac{dE}{d\theta_B}$.
3.  **Signal-to-Noise Ratio (SNR)**:
    $$\text{SNR} = \frac{I_{\text{peak}} - I_{\text{background}}}{\sigma_{\text{noise}}}$$
4.  **Energy Level Diagram Construction**:
    Using the measured characteristic transition energies $E(K_\alpha)$ and $E(K_\beta)$ along with the literature values of the K-edge (binding energy $E_K$), calculate the binding energies of the $L$ and $M$ shells:
    - $E_L \approx E_K - E(K_\alpha)$
    - $E_M \approx E_K - E(K_\beta)$

---

## 4. Lab Git Clone Optimization (Fast Checkout)

To clone only the necessary directories (Bragg experiment, `physlab` core library, and Typst styles) along with Python configuration files (`pyproject.toml` and `uv.lock`) without downloading the entire semester archives:

```powershell
# 1. Clone the repository without checking out files
git clone --depth 1 --no-checkout https://github.com/katzuv/studies.git studies
cd studies

# 2. Enable sparse-checkout in cone mode
git sparse-checkout init --cone

# 3. Choose the specific directories and files to include
git sparse-checkout set "2026S/Lab4/07 Bragg" "physlab" "typst" "pyproject.toml" "uv.lock" ".agents" ".gitignore"

# 4. Checkout the branch
git checkout main
```

### Restoring/Downloading the Rest of the Repository Later
If you want to disable the sparse checkout filters later (for example, once you are back home on a fast connection) and download the entire repository:

```powershell
# Disable sparse checkout filters and populate the full repository tree
git sparse-checkout disable
```
