import math
import sys
from pathlib import Path

# Add studies root path to sys.path to allow importing physlab
sys.path.append(str(Path(__file__).resolve().parents[3]))
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from physlab import export_constants

# Force stdout to use UTF-8 to support Unicode subscripts and superscripts natively on Windows
sys.stdout.reconfigure(encoding="utf-8")

# Initialize rich console with recording enabled to save as SVG
console = Console(record=True)

# ==========================================
# General Physical Constants
# ==========================================
MU_0 = 4 * math.pi * 1e-7  # Vacuum permeability μ₀ [T·m/A]

# ==========================================
# Question 1: Coils and Transformation Ratio
# ==========================================

# Primary coil parameters
d1 = 80e-3  # Turn diameter d₁ [m]
h1 = 0.300  # Coil length h₁ [m]
n1 = 518  # Number of turns n₁
d_wire1 = 5e-4  # Copper wire diameter [m]

# Secondary coil parameters
d2 = 38e-3  # Turn diameter d₂ [m]
h2 = 0.048  # Average coil length h₂ [m] (between 0.046 and 0.050)
n2 = 1500  # Number of turns n₂
d_wire2 = 2e-4  # Copper wire diameter [m]

rho_copper = 1.72e-8  # Specific resistivity of copper ρ_copper [Ω·m]

# a. Calculate coil resistance: R = ρ_copper · L_wire / A_wire
L_wire1 = n1 * math.pi * d1
A_wire1 = math.pi * (d_wire1**2) / 4
R_coil1 = 11.8  # Measured primary coil resistance [Ω]

L_wire2 = n2 * math.pi * d2
A_wire2 = math.pi * (d_wire2**2) / 4
R_coil2 = 123.3  # Measured secondary coil resistance [Ω]

# b. Calculate inductance: L = μ₀ · N² · A / h
A_coil1 = math.pi * (d1**2) / 4
L_coil1 = 5.7e-3  # Measured primary coil inductance [H]

A_coil2 = math.pi * (d2**2) / 4
L_coil2 = 84.1e-3  # Measured secondary coil inductance [H]

# c. Magnetic field at the center of a finite primary coil
V_p = 1.0  # Input voltage Vₚ [V]
R_in = 50.0  # Signal generator internal resistance [Ω]

I_1 = V_p / (R_in + R_coil1)  # Voltage divider assuming low frequency / DC
B_1 = (MU_0 * n1 * I_1) / math.sqrt(h1**2 + d1**2)

# e. Transformation ratio: Vₛ/Vₚ = (N₂ · d₂²) / (N₁ · d₁²)
# The flux linked by each turn is proportional to its area.
ratio_Vs_Vp = (n2 * (d2**2)) / (n1 * (d1**2))


# ==========================================
# Question 3: Oven Heater
# ==========================================
V_oven = 40.0  # Oven voltage [V]
d_wire_oven = 3e-4  # Heating wire diameter [m] (corrected from 3e-3 to 0.3 mm for physical consistency)
n_oven = 76  # Number of turns around the oven
D_oven = 0.0167  # Oven diameter [m]
rho_kanthal = 1.45e-6  # Specific resistivity of Kanthal ρ [Ω·m]
rho_m_kanthal = 7.1e3  # Mass density ρ_m [kg/m³]
c_p_kanthal = 510.0  # Specific heat capacity c_p [J/(kg·K)]

# Power calculation: P = V² / R
L_wire_oven = math.pi * D_oven * n_oven
A_wire_oven = math.pi * (d_wire_oven**2) / 4
R_oven = rho_kanthal * L_wire_oven / A_wire_oven
P_oven = (V_oven**2) / R_oven

# Heating rate assuming no heat losses: dT/dt = P / (m · c_p)
m_wire = L_wire_oven * A_wire_oven * rho_m_kanthal
dT_dt = P_oven / (m_wire * c_p_kanthal)


# ==========================================
# Question 4: Newton's Cooling Law
# ==========================================
# Ceramic cylinder parameters (thermal resistance)
r_int = 0.0127 / 2
r_ext = 0.0315 / 2
h_oven_ceramic = 0.0995
kappa = 1.298  # Thermal conductivity κ [W/(m·K)]

# Thermal resistance of cylindrical shell: R_th = ln(r_ext / r_int) / (2 · π · κ · h)
R_th = math.log(r_ext / r_int) / (2 * math.pi * kappa * h_oven_ceramic)


# ==========================================
# Question 5: Water Kettle Heating Time
# ==========================================
m_water = 0.2  # Mass of water [kg]
T_start = 20.0  # Initial temperature [°C]
T_end = 100.0  # Final temperature [°C]
P_kettle = 2000.0  # Kettle power [W]
c_p_water = 4184.0  # Specific heat capacity of water c_p [J/(kg·K)]

# Heating time: t = m · c_p · ΔT / P
t_kettle = m_water * c_p_water * (T_end - T_start) / P_kettle


# ==========================================
# Question 6: Cooling Time
# ==========================================
T_0_q6 = 550.0  # Initial temperature T₀ [K]
T_env_q6 = 300.0  # Ambient temperature T_env [K]
k_q6 = 0.5  # Decay constant k [sec⁻¹]
T_target_q6 = 350.0  # Target temperature [K]

# T(t) = T_env + (T₀ - T_env) · exp(-kt)
# exp(-kt) = (T(t) - T_env) / (T₀ - T_env)
# t = -ln((T(t) - T_env) / (T₀ - T_env)) / k
t_target = -math.log((T_target_q6 - T_env_q6) / (T_0_q6 - T_env_q6)) / k_q6


# ==========================================
# Render Beautiful Rich Outputs
# ==========================================
console.print(
    Panel.fit(
        "[bold yellow]*** CURIE POINT EXPERIMENT - PREPARATION CALCULATIONS ***[/bold yellow]\n"
        "[dim]Analytical calculation of experimental coil, oven, and cooling characteristics[/dim]",
        border_style="bold gold1",
        padding=(1, 4),
        title="[bold green]Technion Physics Lab 4[/bold green]",
    )
)

# Table 1: Coil Parameters
q1_table = Table(
    title="\n[bold cyan]Question 1: Coil Parameters[/bold cyan]",
    show_header=True,
    header_style="bold magenta",
)
q1_table.add_column("Parameter", style="dim")
q1_table.add_column("Primary Coil (1)", justify="right")
q1_table.add_column("Secondary Coil (2)", justify="right")
q1_table.add_row("Resistance (R)", f"{R_coil1:.2f} Ω", f"{R_coil2:.2f} Ω")
q1_table.add_row(
    "Inductance (L)", f"{L_coil1 * 1000:.2f} mH", f"{L_coil2 * 1000:.2f} mH"
)
console.print(q1_table)

# Non-numbered list for single-value calculated constants
console.print("[bold cyan]Question 1: Calculated System Constants[/bold cyan]")
console.print(f" • Primary Current (I₁): [green]{I_1:.4f} A[/green]")
console.print(
    f" • Center Magnetic Field (B₁): [green]{B_1:.2e} T ({B_1 * 1e4:.3f} Gauss)[/green]"
)
console.print(
    f" • Ideal Transformation Ratio (Vₛ/Vₚ): [green]{ratio_Vs_Vp:.3f}[/green]"
)

# Table 3: Oven Heater
q3_table = Table(
    title="\n[bold cyan]Question 3: Oven Heater Characteristics[/bold cyan]",
    show_header=True,
    header_style="bold magenta",
)
q3_table.add_column("Parameter", style="dim")
q3_table.add_column("Calculated Value", justify="right", style="green")
q3_table.add_row("Heater Power (P)", f"{P_oven:.2f} W")
q3_table.add_row("Ideal Heating Rate (dT/dt)", f"{dT_dt:.2f} K/sec")
console.print(q3_table)


# Table 5 & 6: Heating/Cooling Scenarios
q56_table = Table(
    title="\n[bold cyan]Questions 5 & 6: Heating and Cooling Scenarios[/bold cyan]",
    show_header=True,
    header_style="bold magenta",
)
q56_table.add_column("Scenario", style="dim")
q56_table.add_column("Time Required", justify="right", style="green")
q56_table.add_row("Q5: Heat 0.2 kg water (20°C → 100°C) at 2 kW", f"{t_kettle:.2f} sec")
q56_table.add_row("Q6: Cool body (550 K → 350 K, k = 0.5 sec⁻¹)", f"{t_target:.2f} sec")
console.print(q56_table)

# Save console output to SVG
output_svg_path = Path(__file__).parent / "graphs" / "constants_output.svg"
console.save_svg(str(output_svg_path))

# ==========================================
# Generate JSON and Typst Constants Files
# ==========================================


# Define uncertainties/errors
# 1. Multimeter resistance accuracy (Agilent 34401A 6.5 digit DMM datasheet)
# Formula: ± (% of reading + % of range)
# 1 year spec for 100 Ohm and 1 kOhm range: 0.050% of reading + 0.008% of range
def calculate_dmm_resistance_error(reading, range_val):
    return (reading * 0.050 / 100) + (range_val * 0.008 / 100)


R_coil1_err = calculate_dmm_resistance_error(R_coil1, range_val=100.0)  # 100 Ohm range
R_coil2_err = calculate_dmm_resistance_error(R_coil2, range_val=1000.0)  # 1 kOhm range


# 2. LCR meter inductance accuracy (Amprobe LCR55A datasheet)
# Formula: ± (3.0% of reading + 20 digits)
# 20 mH range: resolution 0.01 mH, so 1 digit = 0.01 mH
# 200 mH range: resolution 0.1 mH, so 1 digit = 0.1 mH
def calculate_lcr_inductance_error(reading_henry, resolution_henry):
    return (reading_henry * 0.03) + (20 * resolution_henry)


L_coil1_err = calculate_lcr_inductance_error(
    L_coil1, resolution_henry=0.01e-3
)  # 20 mH range
L_coil2_err = calculate_lcr_inductance_error(
    L_coil2, resolution_henry=0.1e-3
)  # 200 mH range


errors = {
    'R_"coil1"': R_coil1_err,
    'L_"coil1"': L_coil1_err,
    'R_"coil2"': R_coil2_err,
    'L_"coil2"': L_coil2_err,
    "I_1": None,
    "B_1": None,
    "V_s / V_p": None,
    'R_"oven"': None,
    'P_"oven"': None,
    "dd(T)/dd(t)": None,
    'R_"th"': None,
    't_"cool"': None,
}


def format_val(val, err, fmt_spec, scale=1.0, suffix=""):
    v = val * scale
    if err is None:
        v_str = f"{v:{fmt_spec}}"
        if suffix:
            v_str = f"{v_str} {suffix}"
        return v_str
    e = err * scale
    v_str = f"{v:{fmt_spec}}"
    e_str = f"{e:{fmt_spec}}"
    if suffix:
        return f"({v_str} +- {e_str}) {suffix}"
    return f"{v_str} +- {e_str}"


raw_constants = [
    {
        "hebrew_name": "התנגדות סליל ראשי",
        "english_name": "Primary Coil Resistance",
        "hebrew_var": "התנגדות_סליל_ראשי",
        "english_var": "primary_coil_resistance",
        "symbol": 'R_"coil1"',
        "value": R_coil1,
        "error": errors['R_"coil1"'],
        "units": "Omega",
        "scale": 1.0,
        "fmt_spec": ".2f",
        "suffix": "",
    },
    {
        "hebrew_name": "השראות סליל ראשי",
        "english_name": "Primary Coil Inductance",
        "hebrew_var": "השראות_סליל_ראשי",
        "english_var": "primary_coil_inductance",
        "symbol": 'L_"coil1"',
        "value": L_coil1,
        "error": errors['L_"coil1"'],
        "units": '"H"',
        "scale": 1000.0,
        "fmt_spec": ".2f",
        "suffix": r"dot 10^(-3)",
    },
    {
        "hebrew_name": "התנגדות סליל משני",
        "english_name": "Secondary Coil Resistance",
        "hebrew_var": "התנגדות_סליל_משני",
        "english_var": "secondary_coil_resistance",
        "symbol": 'R_"coil2"',
        "value": R_coil2,
        "error": errors['R_"coil2"'],
        "units": "Omega",
        "scale": 1.0,
        "fmt_spec": ".2f",
        "suffix": "",
    },
    {
        "hebrew_name": "השראות סליל משני",
        "english_name": "Secondary Coil Inductance",
        "hebrew_var": "השראות_סליל_משני",
        "english_var": "secondary_coil_inductance",
        "symbol": 'L_"coil2"',
        "value": L_coil2,
        "error": errors['L_"coil2"'],
        "units": '"H"',
        "scale": 1000.0,
        "fmt_spec": ".2f",
        "suffix": r"dot 10^(-3)",
    },
    {
        "hebrew_name": "זרם בסליל הראשי",
        "english_name": "Primary Coil Current",
        "hebrew_var": "זרם_בסליל_הראשי",
        "english_var": "primary_coil_current",
        "symbol": "I_1",
        "value": I_1,
        "error": errors["I_1"],
        "units": '"A"',
        "scale": 1.0,
        "fmt_spec": ".4f",
        "suffix": "",
    },
    {
        "hebrew_name": "שדה מגנטי במרכז הסליל",
        "english_name": "Central Magnetic Field",
        "hebrew_var": "שדה_מגנטי_במרכז_הסליל",
        "english_var": "central_magnetic_field",
        "symbol": "B_1",
        "value": B_1,
        "error": errors["B_1"],
        "units": '"T"',
        "scale": 1e5,
        "fmt_spec": ".2f",
        "suffix": r"dot 10^(-5)",
    },
    {
        "hebrew_name": "יחס השנאה אידיאלי",
        "english_name": "Ideal Transformation Ratio",
        "hebrew_var": "יחס_השנאה_אידיאלי",
        "english_var": "ideal_transformation_ratio",
        "symbol": "V_s / V_p",
        "value": ratio_Vs_Vp,
        "error": errors["V_s / V_p"],
        "units": "",
        "scale": 1.0,
        "fmt_spec": ".3f",
        "suffix": "",
    },
    {
        "hebrew_name": "התנגדות חוט החימום",
        "english_name": "Oven Heater Resistance",
        "hebrew_var": "התנגדות_חוט_החימום",
        "english_var": "oven_heater_resistance",
        "symbol": 'R_"oven"',
        "value": R_oven,
        "error": errors['R_"oven"'],
        "units": "Omega",
        "scale": 1.0,
        "fmt_spec": ".2f",
        "suffix": "",
    },
    {
        "hebrew_name": "הספק התנור",
        "english_name": "Oven Heater Power",
        "hebrew_var": "הספק_התנור",
        "english_var": "oven_heater_power",
        "symbol": 'P_"oven"',
        "value": P_oven,
        "error": errors['P_"oven"'],
        "units": '"W"',
        "scale": 1.0,
        "fmt_spec": ".2f",
        "suffix": "",
    },
    {
        "hebrew_name": "קצב חימום אידיאלי",
        "english_name": "Ideal Heating Rate",
        "hebrew_var": "קצב_חימום_אידיאלי",
        "english_var": "ideal_heating_rate",
        "symbol": "dd(T)/dd(t)",
        "value": dT_dt,
        "error": errors["dd(T)/dd(t)"],
        "units": '"K" / "sec"',
        "scale": 1.0,
        "fmt_spec": ".2f",
        "suffix": "",
    },
    {
        "hebrew_name": "התנגדות תרמית של הגליל",
        "english_name": "Thermal Resistance",
        "hebrew_var": "התנגדות_תרמית_של_הגליל",
        "english_var": "thermal_resistance",
        "symbol": 'R_"th"',
        "value": R_th,
        "error": errors['R_"th"'],
        "units": '"K" / "W"',
        "scale": 1.0,
        "fmt_spec": ".3f",
        "suffix": "",
    },
    {
        "hebrew_name": "זמן התקררות ל-350 קלווין",
        "english_name": "Cooling Time to 350K",
        "hebrew_var": "זמן_התקררות_ל_350_קלווין",
        "english_var": "cooling_time_to_350k",
        "symbol": 't_"cool"',
        "value": t_target,
        "error": errors['t_"cool"'],
        "units": '"sec"',
        "scale": 1.0,
        "fmt_spec": ".2f",
        "suffix": "",
    },
]

# Generate formatted values and export constants to JSON/Typst
export_constants(raw_constants, Path(__file__).parent / "constants")
