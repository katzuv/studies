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
| $P_{1}$ | 5.92883 | 0.00005 | 0.01000 | 81.863 | 2826.11 | 12 |
| $P_{2}$ | 10.61591 | 0.00002 | 0.01000 | 215.401 | 32702.91 | 12 |
| $P_{3}$ | 15.42452 | 0.00001 | 0.01000 | 344.732 | 122873.36 | 12 |
| $P_{4}$ | 20.32352 | 0.00001 | 0.01000 | 475.234 | 27293.31 | 12 |
| $P_{5}$ | 25.28876 | 0.00001 | 0.01000 | 611.740 | 6485.34 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.68708 \pm 0.01414\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.80862 \pm 0.01414\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.89900 \pm 0.01414\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96524 \pm 0.01414\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.83998 \pm 0.00354\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.08885 \pm 0.01275\text{ V}
$$

### 1.2 Dataset: $I_H = 250\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_250ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.93500 | 0.00010 | 0.01000 | 38.386 | 877.22 | 12 |
| $P_{2}$ | 10.62585 | 0.00005 | 0.01000 | 82.022 | 5894.13 | 12 |
| $P_{3}$ | 15.43569 | 0.00004 | 0.01000 | 118.621 | 12715.32 | 12 |
| $P_{4}$ | 20.31953 | 0.00004 | 0.01000 | 153.137 | 3066.57 | 12 |
| $P_{5}$ | 25.28819 | 0.00005 | 0.01000 | 175.031 | 715.93 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.69085 \pm 0.01414\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.80984 \pm 0.01414\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.88384 \pm 0.01414\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96866 \pm 0.01414\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.83830 \pm 0.00354\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.09670 \pm 0.01275\text{ V}
$$

### 1.3 Dataset: $I_H = 260\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_260ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.89906 | 0.00019 | 0.01000 | 21.482 | 273.73 | 12 |
| $P_{2}$ | 10.58055 | 0.00008 | 0.01000 | 51.362 | 3128.14 | 12 |
| $P_{3}$ | 15.39044 | 0.00005 | 0.01000 | 83.785 | 4072.13 | 12 |
| $P_{4}$ | 20.27124 | 0.00005 | 0.01000 | 120.380 | 2339.17 | 12 |
| $P_{5}$ | 25.23164 | 0.00005 | 0.01000 | 148.981 | 1496.75 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.68149 \pm 0.01414\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.80989 \pm 0.01414\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.88080 \pm 0.01414\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96041 \pm 0.01414\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.83315 \pm 0.00354\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.06591 \pm 0.01275\text{ V}
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
- **Mean baseline current $I_{\text{noise}}$:** $0.51885 \pm 0.08297\text{ pA}$
- **Standard deviation of baseline current $\sigma_{\text{noise}}$:** $0.64803\text{ pA}$
- **5$\sigma$ Noise Ceiling:** $3.75899\text{ pA}$

### 2.2 Quadratic Threshold Fit Results
- **Scale factor $b$:** $41.4396 \pm 0.0131\text{ pA/V}^2$
- **Baseline offset $I_{\text{offset}}$:** $1.5312 \pm 0.0014\text{ pA}$
- **Fitted Onset Voltage $V_i$:** $10.17891 \pm 0.01000\text{ V}$ (including voltage reading error $\sigma_V = 0.01\text{ V}$)
- **Reduced Chi-Squared $\chi^2_{\text{red}}$:** $23307.75$ (DoF = 63)

### 2.3 True Ionization Energy Calculation
Using the contact potential from the $I_H = 270\text{ mA}$ dataset ($V_c = 1.08885 \pm 0.01275\text{ V}$):
$$
E_{\text{ion}} = V_i - V_c = 9.09006 \pm 0.01620\text{ eV}
$$
Comparing to the literature value for the ionization energy of Mercury ($10.438\text{ eV}$):
- **Absolute Deviation:** $1.348\text{ eV}$
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
