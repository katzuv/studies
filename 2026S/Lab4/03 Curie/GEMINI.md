# Curie Point Experiment Context & Structure

## 1. Directory Structure & File Inventory
* **Manuals:**
  * `Instructions.pdf` / `Lab4 03 Curie.pdf`: Hebrew lab guides detailing theoretical background and experimental procedures.
* **Constants Workflow:**
  * `consts.py`: Python CLI script. Uses measured parameters to compute analytical constants. Generates `constants.json` and `constants.typ` via `physlab.export_constants`.
  * `constants.json` / `constants.schema.json`: Schema-compliant data store loaded by the Marimo notebook and Typst report.
  * `constants.typ`: Automatically generated Typst variable bindings.
  * `constants_output.svg`: Styled console output table saved by `consts.py`.
  * `curie_constants_guide.md`: Markdown guide detailing equations and exact analytical derivations.
* **Data Analysis & Plots:**
  * `curie_notebook.py`: Interactive Marimo notebook for data analysis and plotting.
  * `freq_sweep.csv`: Frequency response measurements (`Core Type`, `Frequency (Hz)`, `CH1 (V)` [primary $V_p$], `CH2 (V)` [secondary $V_s$]) for VS0 (Air), VS1 (Ferrite/N1), VS2 (Invar/N2).
  * `frequency_response_vs_vp.svg` / `frequency_response_ratio.svg`: Generated frequency response plots.
* **Report:**
  * `main.typ` / `main.pdf`: Typst report template and compiled report.

## 2. Measured Coil Parameters (Question 1)
* **Primary Coil (Outer - 1):** $R_{\text{coil1}} = 11.8\ \Omega$, $L_{\text{coil1}} = 5.7\ \text{mH}$
* **Secondary Coil (Inner - 2):** $R_{\text{coil2}} = 123.3\ \Omega$, $L_{\text{coil2}} = 84.1\ \text{mH}$

## 3. Experimental Core Physics & Calculations
* **Part A: Frequency Response (100–4000 Hz):**
  * Measure $V_s(f)$ for Air ($V_{s0}$), Ferrite ($V_{s1}$), and Invar ($V_{s2}$) to find optimal frequency.
  * Plot $V_s/V_p$ and $V_s/V_{\text{air}}$ vs $f$ on log-scale (ticks: 100, 200, 300, 500, 1000, 2000, 3000, 4000 Hz).
  * Ideal transformation ratio: $\frac{V_s}{V_p} \approx \frac{N_2 \cdot d_2^2}{N_1 \cdot d_1^2} \approx 0.653$.
* **Part B & C: Heating/Cooling and Curie Temperature:**
  * Measure secondary voltage $V_s$ (proportional to magnetic permeability $\mu_r$) vs temperature $T$.
  * Curie Temp ($T_c$): Ferrite ($T_c \approx 120^\circ\text{C}-150^\circ\text{C}$), Invar ($T_c \approx 230^\circ\text{C}-280^\circ\text{C}$).
  * Cooling profile fits Newton's Law of Cooling:
    $$\frac{dT}{dt} = -k(T - T_{\text{env}}) \implies T(t) = T_{\text{env}} + (T_0 - T_{\text{env}})e^{-kt}$$
    where $k = \frac{1}{R_{\text{th}} \cdot m \cdot c_p}$ (decay constant).
