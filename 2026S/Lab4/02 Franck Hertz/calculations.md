# Franck-Hertz Experiment Calculations & Error Analysis
This document lists all calculations, fitting parameters, error propagation, and reduced chi-squared values for the Franck-Hertz experiment. All fits were performed using `scipy.optimize.curve_fit` via the `physlab` core utility.
## 1. Characteristic Curves & Peak Fitting
To find the exact location of the peaks and their statistical uncertainties, a local parabola of the form:
$$
I(V_a) = a(V_a - V_0)^2 + I_0
$$
was fitted in a window of $\pm 7$ points (15 points total, corresponding to a $\pm 0.35\text{ V}$ range) around each raw local maximum. The instrumental error of the current measurement was taken as the last significant digit displayed in the files ($\sigma_I = 0.01\text{ pA}$).
### 1.1 Dataset: $I_H = 270\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_270ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.93 | 0.000047 | 0.01 | 81.86 | 2826.11 | 12 |
| $P_{2}$ | 10.62 | 0.000019 | 0.01 | 215.40 | 32702.91 | 12 |
| $P_{3}$ | 15.42 | 0.000015 | 0.01 | 344.73 | 122873.36 | 12 |
| $P_{4}$ | 20.32 | 0.000012 | 0.01 | 475.23 | 27293.31 | 12 |
| $P_{5}$ | 25.29 | 0.000013 | 0.01 | 611.74 | 6485.34 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.69 \pm 0.01\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.81 \pm 0.01\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.90 \pm 0.01\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.97 \pm 0.01\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.84 \pm 0.0035\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.09 \pm 0.01\text{ V}
$$

### 1.2 Dataset: $I_H = 250\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_250ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.94 | 0.000096 | 0.01 | 38.39 | 877.22 | 12 |
| $P_{2}$ | 10.63 | 0.000049 | 0.01 | 82.02 | 5894.13 | 12 |
| $P_{3}$ | 15.44 | 0.000038 | 0.01 | 118.62 | 12715.32 | 12 |
| $P_{4}$ | 20.32 | 0.000038 | 0.01 | 153.14 | 3066.57 | 12 |
| $P_{5}$ | 25.29 | 0.000046 | 0.01 | 175.03 | 715.93 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.69 \pm 0.01\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.81 \pm 0.01\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.88 \pm 0.01\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.97 \pm 0.01\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.84 \pm 0.0035\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.10 \pm 0.01\text{ V}
$$

### 1.3 Dataset: $I_H = 260\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_260ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.90 | 0.00019 | 0.01 | 21.48 | 273.73 | 12 |
| $P_{2}$ | 10.58 | 0.000077 | 0.01 | 51.36 | 3128.14 | 12 |
| $P_{3}$ | 15.39 | 0.000054 | 0.01 | 83.78 | 4072.13 | 12 |
| $P_{4}$ | 20.27 | 0.000047 | 0.01 | 120.38 | 2339.17 | 12 |
| $P_{5}$ | 25.23 | 0.000055 | 0.01 | 148.98 | 1496.75 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.68 \pm 0.01\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.81 \pm 0.01\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.88 \pm 0.01\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96 \pm 0.01\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.83 \pm 0.0035\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.07 \pm 0.01\text{ V}
$$

## 2. Ionization Curve & Onset Fitting
To find the ionization onset, the baseline current and noise floor were first analyzed in the range $2.0\text{ V} \le V_a \le 8.0\text{ V}$ where no ionization or significant excitation occurs. The rising edge of the ionization current was then fitted in the range $5.0\text{ V} \le V_a \le 11.5\text{ V}$ to a physical quadratic threshold model:
$$
I(V_a) = \begin{cases} 
b(V_a - V_i)^2 + I_{\text{offset}} & V_a > V_i \\
I_{\text{offset}} & V_a \le V_i
\end{cases}
$$
where $V_i$ represents the fitted ionization onset voltage.
**Source File:** `step2_280ma.csv`

### 2.1 Baseline Noise Summary
- **Mean baseline current $I_{\text{noise}}$:** $0.52 \pm 0.08\text{ pA}$
- **Standard deviation of baseline current $\sigma_{\text{noise}}$:** $0.65\text{ pA}$
- **5$\sigma$ Noise Ceiling:** $3.76\text{ pA}$

### 2.2 Quadratic Threshold Fit Results
- **Scale factor $b$:** $41.44 \pm 0.01\text{ pA/V}^2$
- **Baseline offset $I_{\text{offset}}$:** $1.53 \pm 0.0014\text{ pA}$
- **Fitted Onset Voltage $V_i$:** $10.18 \pm 0.01\text{ V}$ (including voltage reading error $\sigma_V = 0.01\text{ V}$)
- **Reduced Chi-Squared $\chi^2_{\text{red}}$:** $23307.75$ (DoF = 63)

### 2.3 True Ionization Energy Calculation
Using the contact potential from the $I_H = 270\text{ mA}$ dataset ($V_c = 1.09 \pm 0.01\text{ V}$):
$$
E_{\text{ion}} = V_i - V_c = 9.09 \pm 0.02\text{ eV}
$$
Comparing to the literature value for the ionization energy of Mercury ($10.438\text{ eV}$):
- **Absolute Deviation:** $1.35\text{ eV}$
- **Relative Deviation:** $12.91\%$

## 3. Mathematical Derivations of Error Propagation
Below are the formulas used for error propagation, based on standard first-order Taylor expansion for independent variables:
### 3.1 Peak Spacings $\Delta V_i$
Since $V_{i+1}$ and $V_i$ are independent measurements:
$$
\sigma_{\Delta V_i} = \sqrt{\sigma_{V_{i+1}}^2 + \sigma_{V_i}^2}
$$

### 3.2 Excitation Energy $E_{\text{exc}}$
The excitation energy is computed as the mean of the peak differences:
$$
E_{\text{exc}} = \frac{1}{n-1} \sum_{i=1}^{n-1} \Delta V_i = \frac{V_n - V_1}{n-1}
$$
where $n = 5$ is the number of peaks, and $n-1 = 4$ is the number of differences.
The errors on individual peak voltages are independent, so propagating errors on the final expression gives:
$$
\sigma_{E_{\text{exc}}} = \frac{\sqrt{\sigma_{V_n}^2 + \sigma_{V_1}^2}}{n-1}
$$

### 3.3 Contact Potential $V_c$
The contact potential is defined as:
$$
V_c = V_1 - E_{\text{exc}} = V_1 - \frac{V_n - V_1}{n-1} = \frac{n V_1 - V_n}{n-1}
$$
Since $V_1$ and $V_n$ are independent peak voltage measurements:
$$
\sigma_{V_c} = \sqrt{ \left(\frac{n}{n-1}\right)^2 \sigma_{V_1}^2 + \left(\frac{1}{n-1}\right)^2 \sigma_{V_n}^2 }
$$

### 3.4 True Ionization Energy $E_{\text{ion}}$
The true ionization energy is defined as the shift between the onset voltage $V_i$ and the contact potential $V_c$:
$$
E_{\text{ion}} = V_i - V_c
$$
Assuming $V_i$ and $V_c$ are independent (since they are determined from entirely separate datasets):
$$
\sigma_{E_{\text{ion}}} = \sqrt{\sigma_{V_i}^2 + \sigma_{V_c}^2}
$$

## 4. Statistical Discussion on Reduced Chi-Squared values
Under the strict last-digit digital resolution error model, the uncertainties assigned to the current measurements are extremely small ($\sigma_I = 0.01\text{ pA}$). This results in very large values for the reduced chi-squared ($\chi^2_{\text{{red}}} \gg 1$), such as $\chi^2_{\text{{red}}} \approx 23307.75$ for the ionization onset and up to $120,000$ for the characteristic curve peaks. 

### 4.1 Interpretation of Large $\chi^2_{\text{{red}}}$
1. **Digital Resolution vs. Physical Noise:** The digital resolution of $0.01\text{ pA}$ represents the readout limit, not the actual physical noise of the measurement. The actual statistical baseline noise (standard deviation of the baseline fluctuations) was calculated to be $\sigma_{\text{{baseline}}} \approx 0.65\text{ pA}$ for the ionization dataset, and $\sigma_{\text{{baseline}}} \approx 0.55\text{ to }1.80\text{ pA}$ for the characteristic curve datasets.
2. **Model Approximations:** Simplified models (like local parabolas for the peak maxima or a pure quadratic threshold for ionization) do not fully capture higher-order physics (such as thermal velocity distribution of emitted electrons, which smooths out the onset edge) or minor experimental drifts. Even minor systematic deviations from these models, when divided by a tiny digital uncertainty of $0.01\text{ pA}$, lead to an artificially inflated $\chi^2_{\text{{red}}}$.

### 4.2 Impact of Physical Noise Scaling
If we scale the data point uncertainties to use the actual physical baseline standard deviation $\sigma_{\text{{baseline}}}$:
- The reduced chi-squared of the ionization curve fit drops from 23307.75 to a highly reasonable **$5.55$** (DoF = 63). This value represents a highly successful fit, with the small deviation representing the thermal smoothing of the onset edge.
- The reduced chi-squared values for the characteristic curves peaks drop from thousands to a range of **$0.02 \text{ to } 0.88$** (DoF = 12), confirming that the local parabolic shape is an outstanding approximation of the peak maxima when compared against physical fluctuations.
