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
| $P_{1}$ | 5.92875 | 0.00903 | 0.01347 | 81.856 | 0.07 | 12 |
| $P_{2}$ | 10.61533 | 0.00501 | 0.01118 | 215.386 | 0.45 | 12 |
| $P_{3}$ | 15.42381 | 0.00526 | 0.01130 | 344.532 | 0.88 | 12 |
| $P_{4}$ | 20.32320 | 0.00569 | 0.01151 | 475.205 | 0.11 | 12 |
| $P_{5}$ | 25.28880 | 0.00783 | 0.01270 | 611.729 | 0.02 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.68658 \pm 0.01751\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.80848 \pm 0.01590\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.89939 \pm 0.01613\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96560 \pm 0.01714\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.84001 \pm 0.00463\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.08874 \pm 0.01714\text{ V}
$$

### 1.2 Dataset: $I_H = 250\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_250ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.93488 | 0.00888 | 0.01338 | 38.384 | 0.10 | 12 |
| $P_{2}$ | 10.62531 | 0.00555 | 0.01143 | 82.018 | 0.44 | 12 |
| $P_{3}$ | 15.43486 | 0.00525 | 0.01130 | 118.620 | 0.67 | 12 |
| $P_{4}$ | 20.31924 | 0.00628 | 0.01181 | 153.131 | 0.11 | 12 |
| $P_{5}$ | 25.28827 | 0.00853 | 0.01314 | 175.028 | 0.02 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.69043 \pm 0.01760\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.80955 \pm 0.01607\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.88438 \pm 0.01634\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96903 \pm 0.01767\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.83835 \pm 0.00469\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.09653 \pm 0.01704\text{ V}
$$

### 1.3 Dataset: $I_H = 260\text{ mA}$, $V_R = 1.5\text{ V}$
**Source File:** `step10_260ma.csv`

| Peak | Fitted Position $V_i$ [V] | Fit Error $\sigma_{V_i,\text{fit}}$ [V] | Total Error $\sigma_{V_i}$ [V] | Peak Current $I_i$ [pA] | $\chi^2_{\text{red}}$ | DoF |
| :--- | :----------------------- | :------------------------------------- | :----------------------------- | :--------------------- | :--------------------- | :-- |
| $P_{1}$ | 5.89899 | 0.01108 | 0.01492 | 21.480 | 0.08 | 12 |
| $P_{2}$ | 10.57997 | 0.00559 | 0.01145 | 51.358 | 0.59 | 12 |
| $P_{3}$ | 15.38979 | 0.00501 | 0.01118 | 83.771 | 0.45 | 12 |
| $P_{4}$ | 20.27092 | 0.00576 | 0.01154 | 120.367 | 0.14 | 12 |
| $P_{5}$ | 25.23165 | 0.00827 | 0.01298 | 148.964 | 0.07 | 12 |

**Peak Spacings $\Delta V_i = V_{i+1} - V_i$:**
- $\Delta V_{1} = V_{2} - V_{1} = 4.68098 \pm 0.01881\text{ V}$
- $\Delta V_{2} = V_{3} - V_{2} = 4.80983 \pm 0.01601\text{ V}$
- $\Delta V_{3} = V_{4} - V_{3} = 4.88112 \pm 0.01607\text{ V}$
- $\Delta V_{4} = V_{5} - V_{4} = 4.96074 \pm 0.01737\text{ V}$

**Excitation Energy (Mean Spacing):**
$$
E_{\text{exc}} = \frac{V_5 - V_1}{4} = 4.83317 \pm 0.00494\text{ eV}
$$
**Contact Potential:**
$$
V_c = V_1 - E_{\text{exc}} = 1.06582 \pm 0.01893\text{ V}
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
- **Scale factor $b$:** $41.4396 \pm 0.8521\text{ pA/V}^2$
- **Baseline offset $I_{\text{offset}}$:** $1.5312 \pm 0.0883\text{ pA}$
- **Fitted Onset Voltage $V_i$:** $10.17891 \pm 0.01498\text{ V}$ (including voltage reading error $\sigma_V = 0.01\text{ V}$)
- **Reduced Chi-Squared $\chi^2_{\text{red}}$:** $5.55$ (DoF = 63)

### 2.3 True Ionization Energy Calculation
Using the contact potential from the $I_H = 270\text{ mA}$ dataset ($V_c = 1.08874 \pm 0.01714\text{ V}$):
$$
E_{\text{ion}} = V_i - V_c = 9.09017 \pm 0.02277\text{ eV}
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
