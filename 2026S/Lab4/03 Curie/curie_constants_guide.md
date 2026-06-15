# Curie Experiment: Constants and Calculation Guide

This document provides a detailed breakdown of each constant, variable, and formula used in [consts.py](consts.py).

---

## 1. Coil Parameters (Question 1)

### Resistances ($R_{\text{coil1}}$, $R_{\text{coil2}}$)
The resistance of a long wire is given by:
$$R = \rho_{\text{copper}} \frac{L_{\text{wire}}}{A_{\text{wire}}}$$
where:
* **Wire Length ($L_{\text{wire}}$):** $L_{\text{wire}} = N \cdot \pi \cdot d$ (number of turns times the circumference of a single turn).
* **Wire Cross-Sectional Area ($A_{\text{wire}}$):** $A_{\text{wire}} = \frac{\pi \cdot d_{\text{wire}}^2}{4}$ (using the wire's diameter).
* **Copper Resistivity ($\rho_{\text{copper}}$):** $1.72 \cdot 10^{-8} \ \Omega\cdot\text{m}$.

<details>
<summary><b>Click to view exact Question 1 Resistance calculations</b></summary>

* **Primary Coil Resistance ($R_1$):**
  $$L_{\text{wire1}} = n_1 \cdot \pi \cdot d_1 = 518 \cdot \pi \cdot 0.080\text{ m} \approx 130.19\text{ m}$$
  $$A_{\text{wire1}} = \frac{\pi \cdot d_{\text{wire1}}^2}{4} = \frac{\pi \cdot (5 \cdot 10^{-4}\text{ m})^2}{4} \approx 1.9635 \cdot 10^{-7}\text{ m}^2$$
  $$R_1 = \rho_{\text{copper}} \cdot \frac{L_{\text{wire1}}}{A_{\text{wire1}}} = (1.72 \cdot 10^{-8}\ \Omega\cdot\text{m}) \cdot \frac{130.19\text{ m}}{1.9635 \cdot 10^{-7}\text{ m}^2} \approx \mathbf{11.40\ \Omega}$$

* **Secondary Coil Resistance ($R_2$):**
  $$L_{\text{wire2}} = n_2 \cdot \pi \cdot d_2 = 1500 \cdot \pi \cdot 0.038\text{ m} \approx 179.07\text{ m}$$
  $$A_{\text{wire2}} = \frac{\pi \cdot d_{\text{wire2}}^2}{4} = \frac{\pi \cdot (2 \cdot 10^{-4}\text{ m})^2}{4} \approx 3.1416 \cdot 10^{-8}\text{ m}^2$$
  $$R_2 = \rho_{\text{copper}} \cdot \frac{L_{\text{wire2}}}{A_{\text{wire2}}} = (1.72 \cdot 10^{-8}\ \Omega\cdot\text{m}) \cdot \frac{179.07\text{ m}}{3.1416 \cdot 10^{-8}\text{ m}^2} \approx \mathbf{98.04\ \Omega}$$
</details>

### Inductances ($L_{\text{coil1}}$, $L_{\text{coil2}}$)
The self-inductance of a solenoid is calculated as:
$$L = \mu_0 \frac{N^2 A_{\text{coil}}}{h}$$
where:
* **Coil Area ($A_{\text{coil}}$):** $A_{\text{coil}} = \frac{\pi \cdot d^2}{4}$ (cross-sectional area of the coil cylinder).
* **Coil Length ($h$):** The axial length of the coil.
* **Vacuum Permeability ($\mu_0$):** $4\pi \cdot 10^{-7} \ \text{T}\cdot\text{m/A}$.

<details>
<summary><b>Click to view exact Question 1 Inductance calculations</b></summary>

* **Primary Coil Inductance ($L_1$):**
  $$A_{\text{coil1}} = \frac{\pi \cdot d_1^2}{4} = \frac{\pi \cdot 0.080^2}{4} \approx 5.0265 \cdot 10^{-3}\text{ m}^2$$
  $$L_1 = \mu_0 \cdot \frac{n_1^2 \cdot A_{\text{coil1}}}{h_1} = (4\pi \cdot 10^{-7}\ \text{T}\cdot\text{m/A}) \cdot \frac{518^2 \cdot (5.0265 \cdot 10^{-3}\text{ m}^2)}{0.300\text{ m}} \approx 5.65 \cdot 10^{-3}\text{ H} = \mathbf{5.65\text{ mH}}$$

* **Secondary Coil Inductance ($L_2$):**
  $$A_{\text{coil2}} = \frac{\pi \cdot d_2^2}{4} = \frac{\pi \cdot 0.038^2}{4} \approx 1.1341 \cdot 10^{-3}\text{ m}^2$$
  $$L_2 = \mu_0 \cdot \frac{n_2^2 \cdot A_{\text{coil2}}}{h_2} = (4\pi \cdot 10^{-7}\ \text{T}\cdot\text{m/A}) \cdot \frac{1500^2 \cdot (1.1341 \cdot 10^{-3}\text{ m}^2)}{0.048\text{ m}} \approx 6.680 \cdot 10^{-2}\text{ H} = \mathbf{66.80\text{ mH}}$$
</details>

### Primary Current ($I_1$)
The current driven through the primary coil by an AC voltage generator:
* Given an applied peak voltage $V_p = 1.0\text{ V}$ and the generator's internal output resistance $R_{\text{in}} = 50.0\ \Omega$.
* Assuming low-frequency / quasi-static limit, the impedance is dominated by resistance:
  $$I_1 = \frac{V_p}{R_{\text{in}} + R_{\text{coil1}}}$$

<details>
<summary><b>Click to view exact Question 1 Primary Current calculation</b></summary>

$$I_1 = \frac{V_p}{R_{\text{in}} + R_1} = \frac{1.0\text{ V}}{50.0\ \Omega + 11.40\ \Omega} \approx \mathbf{0.0163\text{ A}}$$
</details>

### Magnetic Field at Center ($B_1$)
Calculated using the Biot-Savart law integrated for a finite-length solenoid:
$$B_1 = \frac{\mu_0 \cdot N \cdot I_1}{\sqrt{h^2 + d^2}}$$

<details>
<summary><b>Click to view exact Question 1 Center Magnetic Field calculation</b></summary>

$$B_1 = \frac{\mu_0 \cdot n_1 \cdot I_1}{\sqrt{h_1^2 + d_1^2}} = \frac{(4\pi \cdot 10^{-7}\ \text{T}\cdot\text{m/A}) \cdot 518 \cdot 0.0163\text{ A}}{\sqrt{0.300^2\text{ m}^2 + 0.080^2\text{ m}^2}} = \frac{1.061 \cdot 10^{-5}}{0.3105\text{ m}} \approx 3.41 \cdot 10^{-5}\text{ T} = \mathbf{0.341\text{ Gauss}}$$
</details>

### Transformation Ratio ($V_s / V_p$)
Under ideal transformer conditions, the ratio of voltages is equal to the ratio of total magnetic fluxes linked by the coils:
$$\Phi_1 = B_1 A_1 n_1, \quad \Phi_2 = B_1 A_2 n_2$$
$$\frac{V_s}{V_p} = \frac{\Phi_2}{\Phi_1} = \frac{n_2 A_2}{n_1 A_1} = \frac{n_2 d_2^2}{n_1 d_1^2}$$

<details>
<summary><b>Click to view exact Question 1 Transformation Ratio calculation</b></summary>

$$\frac{V_s}{V_p} = \frac{n_2 \cdot d_2^2}{n_1 \cdot d_1^2} = \frac{1500 \cdot (0.038\text{ m})^2}{518 \cdot (0.080\text{ m})^2} = \frac{2.166}{3.3152} \approx \mathbf{0.653}$$
</details>

---

## 2. Oven Heater Parameters (Question 3)

### Heater Wire Resistance ($R_{\text{oven}}$)
* **Heater Wire Length ($L_{\text{wire, oven}}$):** $n_{\text{oven}} \cdot \pi \cdot D_{\text{oven}}$.
* **Wire Area ($A_{\text{wire, oven}}$):** $\frac{\pi \cdot d_{\text{wire, oven}}^2}{4}$.
* **Kanthal Resistivity ($\rho_{\text{kanthal}}$):** $1.45 \cdot 10^{-6}\ \Omega\cdot\text{m}$.
* **Resistance:** $R_{\text{oven}} = \rho_{\text{kanthal}} \frac{L_{\text{wire, oven}}}{A_{\text{wire, oven}}}$.

### Heater Power ($P_{\text{oven}}$)
For a DC supply voltage $V_{\text{oven}} = 40\text{ V}$:
$$P_{\text{oven}} = \frac{V_{\text{oven}}^2}{R_{\text{oven}}}$$

### Ideal Heating Rate ($\frac{dT}{dt}$)
Assuming no thermal losses to the environment, all electrical power $P_{\text{oven}}$ is converted to thermal energy raising the temperature of the Kanthal wire:
$$\Delta Q = P_{\text{oven}} \cdot \Delta t = m_{\text{wire}} \cdot c_p \cdot \Delta T$$
$$\frac{dT}{dt} = \frac{P_{\text{oven}}}{m_{\text{wire}} \cdot c_{p,\text{ Kanthal}}}$$
where wire mass is $m_{\text{wire}} = L_{\text{wire, oven}} \cdot A_{\text{wire, oven}} \cdot \rho_{\text{m, Kanthal}}$.

<details>
<summary><b>Click to view exact Question 3 calculated values</b></summary>

* **Heater Wire Resistance ($R_{\text{oven}}$):**
  $$L_{\text{wire, oven}} = n_{\text{oven}} \cdot \pi \cdot D_{\text{oven}} = 76 \cdot \pi \cdot 0.0167\text{ m} \approx 3.9875\text{ m}$$
  $$A_{\text{wire, oven}} = \frac{\pi \cdot d_{\text{wire, oven}}^2}{4} = \frac{\pi \cdot (3 \cdot 10^{-4}\text{ m})^2}{4} \approx 7.0686 \cdot 10^{-8}\text{ m}^2$$
  $$R_{\text{oven}} = \rho_{\text{kanthal}} \cdot \frac{L_{\text{wire, oven}}}{A_{\text{wire, oven}}} = (1.45 \cdot 10^{-6}\ \Omega\cdot\text{m}) \cdot \frac{3.9875\text{ m}}{7.0686 \cdot 10^{-8}\text{ m}^2} \approx \mathbf{81.80\ \Omega}$$

* **Heater Power ($P_{\text{oven}}$):**
  $$P_{\text{oven}} = \frac{V_{\text{oven}}^2}{R_{\text{oven}}} = \frac{40.0^2\text{ V}^2}{81.80\ \Omega} \approx \mathbf{19.56\text{ W}}$$

* **Ideal Heating Rate ($dT/dt$):**
  $$m_{\text{wire}} = L_{\text{wire, oven}} \cdot A_{\text{wire, oven}} \cdot \rho_{\text{m, Kanthal}} = 3.9875\text{ m} \cdot (7.0686 \cdot 10^{-8}\text{ m}^2) \cdot (7.1 \cdot 10^3\text{ kg/m}^3) \approx 2.001 \cdot 10^{-3}\text{ kg}$$
  $$\frac{dT}{dt} = \frac{P_{\text{oven}}}{m_{\text{wire}} \cdot c_{p,\text{ Kanthal}}} = \frac{19.56\text{ W}}{(2.001 \cdot 10^{-3}\text{ kg}) \cdot 510\text{ J/(kg·K)}} \approx \mathbf{19.17\text{ K/sec}}$$
</details>

---

## 3. Newton's Cooling Law (Question 4)

### Thermal Resistance of Ceramic Cylinder ($R_{th}$)
For a cylindrical hollow shell of thermal conductivity $\kappa$ and height $h$:
$$R_{th} = \frac{\ln(r_{\text{ext}} / r_{\text{int}})}{2 \pi \kappa h}$$

### Cooling Constant ($k$)
When cooling a sample of mass $m$ and specific heat $c_p$ inside the oven:
$$\frac{dT}{dt} = -k(T - T_{\text{env}})$$
$$k = \frac{1}{R_{th} \cdot m \cdot c_p}$$
where sample mass $m = \text{volume} \cdot \rho_m = \left(L \cdot \frac{\pi d^2}{4}\right) \cdot \rho_m$.

<details>
<summary><b>Click to view exact Question 4 calculated values</b></summary>

* **Ceramic Cylinder Thermal Resistance ($R_{th}$):**
  $$r_{\text{int}} = \frac{0.0127\text{ m}}{2} = 0.00635\text{ m}, \quad r_{\text{ext}} = \frac{0.0315\text{ m}}{2} = 0.01575\text{ m}$$
  $$R_{th} = \frac{\ln(r_{\text{ext}} / r_{\text{int}})}{2\pi \cdot \kappa \cdot h_{\text{ceramic}}} = \frac{\ln(0.01575 / 0.00635)}{2\pi \cdot 1.298\text{ W/(m·K)} \cdot 0.0995\text{ m}} = \frac{0.9083}{0.8115} \approx \mathbf{1.119\text{ K/W}}$$

* **Invar Cooling Constant ($k_{\text{invar}}$):**
  $$V_{\text{invar}} = L \cdot \pi \cdot \left(\frac{d}{2}\right)^2 = 0.040\text{ m} \cdot \pi \cdot 0.006^2\text{ m}^2 \approx 4.5239 \cdot 10^{-6}\text{ m}^3$$
  $$m_{\text{invar}} = V_{\text{invar}} \cdot \rho_{\text{m, Invar}} = (4.5239 \cdot 10^{-6}\text{ m}^3) \cdot 8100\text{ kg/m}^3 \approx 0.03664\text{ kg}$$
  $$k_{\text{invar}} = \frac{1}{R_{th} \cdot m_{\text{invar}} \cdot c_{p,\text{ Invar}}} = \frac{1}{1.119\text{ K/W} \cdot 0.03664\text{ kg} \cdot 505\text{ J/(kg·K)}} \approx \mathbf{0.0483\text{ sec}^{-1}}$$

* **Ferrite Cooling Constant ($k_{\text{ferrite}}$):**
  $$V_{\text{ferrite}} = L \cdot \pi \cdot \left(\frac{d}{2}\right)^2 = 0.0254\text{ m} \cdot \pi \cdot 0.006^2\text{ m}^2 \approx 2.8727 \cdot 10^{-6}\text{ m}^3$$
  $$m_{\text{ferrite}} = V_{\text{ferrite}} \cdot \rho_{\text{m, Ferrite}} = (2.8727 \cdot 10^{-6}\text{ m}^3) \cdot 5000\text{ kg/m}^3 \approx 0.01436\text{ kg}$$
  $$k_{\text{ferrite}} = \frac{1}{R_{th} \cdot m_{\text{ferrite}} \cdot c_{p,\text{ Ferrite}}} = \frac{1}{1.119\text{ K/W} \cdot 0.01436\text{ kg} \cdot 750\text{ J/(kg·K)}} \approx \mathbf{0.0829\text{ sec}^{-1}}$$
</details>

---

## 4. Specific Scenarios (Questions 5 & 6)

### Water Kettle (Question 5)
The time $t$ required to heat water of mass $m_{\text{water}}$ by a temperature difference $\Delta T$ under power $P_{\text{kettle}}$:
$$t = \frac{m_{\text{water}} \cdot c_{p,\text{ water}} \cdot (T_{\text{end}} - T_{\text{start}})}{P_{\text{kettle}}}$$

### Cooling Time (Question 6)
Solving the Newton cooling ODE:
$$T(t) = T_{\text{env}} + (T_0 - T_{\text{env}}) e^{-kt}$$
$$e^{-kt} = \frac{T(t) - T_{\text{env}}}{T_0 - T_{\text{env}}}$$
$$t = -\frac{1}{k} \ln\left(\frac{T(t) - T_{\text{env}}}{T_0 - T_{\text{env}}}\right)$$

<details>
<summary><b>Click to view exact Questions 5 & 6 calculated values</b></summary>

* **Question 5 (Water Kettle Heating Time $t$):**
  $$t = \frac{m_{\text{water}} \cdot c_{p,\text{ water}} \cdot (T_{\text{end}} - T_{\text{start}})}{P_{\text{kettle}}} = \frac{0.2\text{ kg} \cdot 4184\text{ J/(kg·K)} \cdot (100.0^\circ\text{C} - 20.0^\circ\text{C})}{2000.0\text{ W}} = \frac{66944}{2000} \approx \mathbf{33.47\text{ seconds}}$$

* **Question 6 (Cooling Time to 350K $t$):**
  $$t = -\frac{1}{k} \ln\left(\frac{T(t) - T_{\text{env}}}{T_0 - T_{\text{env}}}\right) = -\frac{1}{0.5\text{ sec}^{-1}} \ln\left(\frac{350\text{ K} - 300\text{ K}}{550\text{ K} - 300\text{ K}}\right) = -2 \ln\left(\frac{50}{250}\right) = -2 \ln(0.2) \approx \mathbf{3.22\text{ seconds}}$$
</details>

---

## 5. Physical Q&A

### 1. Is the primary current just the current in the outer coil because we have a voltage over it?
**Yes.** The primary current ($I_1$) is the physical current flowing through the primary (outer) coil because a function generator applies an alternating voltage ($V_p$) across its terminals. Because the primary coil is a closed circuit connected to the generator, current flows through it, generating the alternating magnetic field ($B_1$) on the central axis.

### 2. Can we have zero current while having a voltage?
**Yes, absolutely.** This happens in two major contexts:

1. **Open Circuits (Infinite Resistance):** 
   According to Ohm's Law ($I = V/R$), if a circuit is open, the electrical resistance is infinitely high ($R \to \infty$). A voltage source can establish a potential difference across the open terminals, but the current is exactly zero ($I = 0$).
   * *In this experiment:* This is exactly what happens with the secondary (inner) coil. Due to Faraday's law, a voltage (EMF) is induced across its terminals by the changing magnetic flux. However, because we connect the secondary coil only to a high-impedance voltmeter or oscilloscope channel, the secondary loop is effectively an open circuit. Therefore, **voltage is induced across the secondary coil, but no current flows through it.**
2. **AC Reactive Elements (Phase Shifts):**
   In alternating current (AC) circuits containing inductors or capacitors, voltage and current are out of phase. For a pure inductor, current lags voltage by $90^\circ$ ($\pi/2$ radians). At the exact instant when the sinusoidal AC current passes through zero, the AC voltage is at its maximum peak value. Thus, you can have a non-zero voltage across the element at a moment when the current is zero.

---

## 6. Calculated Constants CLI Output

The image below is the direct SVG output generated from running the `consts.py` script:

![CLI Output Table](constants_output.svg)
