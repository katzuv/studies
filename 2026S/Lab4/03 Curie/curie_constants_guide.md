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

### Inductances ($L_{\text{coil1}}$, $L_{\text{coil2}}$)
The self-inductance of a solenoid is calculated as:
$$L = \mu_0 \frac{N^2 A_{\text{coil}}}{h}$$
where:
* **Coil Area ($A_{\text{coil}}$):** $A_{\text{coil}} = \frac{\pi \cdot d^2}{4}$ (cross-sectional area of the coil cylinder).
* **Coil Length ($h$):** The axial length of the coil.
* **Vacuum Permeability ($\mu_0$):** $4\pi \cdot 10^{-7} \ \text{T}\cdot\text{m/A}$.

### Primary Current ($I_1$)
The current driven through the primary coil by an AC voltage generator:
* Given an applied peak voltage $V_p = 1.0\text{ V}$ and the generator's internal output resistance $R_{\text{in}} = 50.0\ \Omega$.
* Assuming low-frequency / quasi-static limit, the impedance is dominated by resistance:
  $$I_1 = \frac{V_p}{R_{\text{in}} + R_{\text{coil1}}}$$

### Magnetic Field at Center ($B_1$)
Calculated using the Biot-Savart law integrated for a finite-length solenoid:
$$B_1 = \frac{\mu_0 \cdot N \cdot I_1}{\sqrt{h^2 + d^2}}$$

### Transformation Ratio ($V_s / V_p$)
Under ideal transformer conditions, the ratio of voltages is equal to the ratio of total magnetic fluxes linked by the coils:
$$\Phi_1 = B_1 A_1 n_1, \quad \Phi_2 = B_1 A_2 n_2$$
$$\frac{V_s}{V_p} = \frac{\Phi_2}{\Phi_1} = \frac{n_2 A_2}{n_1 A_1} = \frac{n_2 d_2^2}{n_1 d_1^2}$$

---

## 2. Oven Heater Parameters (Question 3)

### Heater Wire Resistance ($R_{\text{oven}}$)
* **Heater Wire Length ($L_{\text{wire\_oven}}$):** $n_{\text{oven}} \cdot \pi \cdot D_{\text{oven}}$.
* **Wire Area ($A_{\text{wire\_oven}}$):** $\frac{\pi \cdot d_{\text{wire\_oven}}^2}{4}$.
* **Kanthal Resistivity ($\rho_{\text{kanthal}}$):** $1.45 \cdot 10^{-6}\ \Omega\cdot\text{m}$.
* **Resistance:** $R_{\text{oven}} = \rho_{\text{kanthal}} \frac{L_{\text{wire\_oven}}}{A_{\text{wire\_oven}}}$.

### Heater Power ($P_{\text{oven}}$)
For a DC supply voltage $V_{\text{oven}} = 40\text{ V}$:
$$P_{\text{oven}} = \frac{V_{\text{oven}}^2}{R_{\text{oven}}}$$

### Ideal Heating Rate ($\frac{dT}{dt}$)
Assuming no thermal losses to the environment, all electrical power $P_{\text{oven}}$ is converted to thermal energy raising the temperature of the Kanthal wire:
$$\Delta Q = P_{\text{oven}} \cdot \Delta t = m_{\text{wire}} \cdot c_p \cdot \Delta T$$
$$\frac{dT}{dt} = \frac{P_{\text{oven}}}{m_{\text{wire}} \cdot c_{p\_kanthal}}$$
where wire mass is $m_{\text{wire}} = L_{\text{wire\_oven}} \cdot A_{\text{wire\_oven}} \cdot \rho_{\text{m\_kanthal}}$.

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

---

## 4. Specific Scenarios (Questions 5 & 6)

### Water Kettle (Question 5)
The time $t$ required to heat water of mass $m_{\text{water}}$ by a temperature difference $\Delta T$ under power $P_{\text{kettle}}$:
$$t = \frac{m_{\text{water}} \cdot c_{p\text{\_water}} \cdot (T_{\text{end}} - T_{\text{start}})}{P_{\text{kettle}}}$$

### Cooling Time (Question 6)
Solving the Newton cooling ODE:
$$T(t) = T_{\text{env}} + (T_0 - T_{\text{env}}) e^{-kt}$$
$$e^{-kt} = \frac{T(t) - T_{\text{env}}}{T_0 - T_{\text{env}}}$$
$$t = -\frac{1}{k} \ln\left(\frac{T(t) - T_{\text{env}}}{T_0 - T_{\text{env}}}\right)$$

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
