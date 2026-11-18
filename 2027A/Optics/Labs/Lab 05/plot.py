import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Uncertainties
SIGMA_V = 0.005  # V
SIGMA_THETA = 0.5  # deg


def malus_model(
    theta_deg: np.ndarray, V0: float, theta0_deg: float, offset: float
) -> np.ndarray:
    """Malus's Law: V_net(theta) = V0 * cos^2(theta - theta0) + offset"""
    rad = np.deg2rad(theta_deg - theta0_deg)
    return V0 * (np.cos(rad) ** 2) + offset


def fit_and_plot(
    df: pd.DataFrame,
    title: str,
    data_label: str,
    data_color: str,
    fit_color: str,
    marker: str,
    out_filename: str,
) -> None:
    theta = df["theta_deg"].to_numpy()
    v_net = df["V_net"].to_numpy()
    sigma = np.full_like(v_net, SIGMA_V, dtype=float)

    p0 = [v_net.max() - v_net.min(), 0.0, v_net.min()]

    popt, pcov = curve_fit(
        malus_model,
        theta,
        v_net,
        p0=p0,
        sigma=sigma,
        absolute_sigma=True,
        maxfev=10000,
    )
    perr = np.sqrt(np.diag(pcov))

    residuals = v_net - malus_model(theta, *popt)
    dof = len(v_net) - len(popt)
    chi2_red = np.sum((residuals / sigma) ** 2) / dof

    print(f"\n--- {title} Fit Results ---")
    print(f"V0      = {popt[0]:.4f} ± {perr[0]:.4f} V")
    print(f"theta_0 = {popt[1]:.2f} ± {perr[1]:.2f} deg")
    print(f"offset  = {popt[2]:.4f} ± {perr[2]:.4f} V")
    print(f"Reduced chi^2 = {chi2_red:.2f} (dof = {dof})")

    theta_grid = np.linspace(0, 360, 500)

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.errorbar(
        theta,
        v_net,
        yerr=SIGMA_V,
        xerr=SIGMA_THETA,
        fmt=marker,
        color=data_color,
        ecolor=data_color,
        elinewidth=1.2,
        capsize=3,
        markersize=5,
        label=data_label,
    )
    ax.plot(
        theta_grid,
        malus_model(theta_grid, *popt),
        "-",
        color=fit_color,
        linewidth=2.0,
        label=rf"Fit: $V_0 \cos^2(\theta - \theta_0) + C$ ($\chi^2_\nu = {chi2_red:.2f}$)",
    )

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel(r"Polarizer Angle $\theta$ [deg]", fontsize=11)
    ax.set_ylabel(r"Net Photodiode Voltage $V - V_{\mathrm{bg}}$ [V]", fontsize=11)
    ax.set_xlim(-5, 365)
    ax.set_xticks(np.arange(0, 361, 45))
    ax.grid(True, linestyle="--", alpha=0.45)
    ax.legend(loc="upper right", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_filename, format="svg", bbox_inches="tight")
    print(f"Saved {out_filename}")
    plt.show()


def main() -> None:
    df_h = pd.read_csv("malus_horizontal.csv")
    df_v = pd.read_csv("malus_vertical.csv")

    fit_and_plot(
        df=df_h,
        title="Horizontal Input Polarization ($H$)",
        data_label=r"Measured $V_H - V_{\mathrm{bg}}$",
        data_color="#1f77b4",
        fit_color="#d62728",
        marker="o",
        out_filename="q2_horizontal.svg",
    )

    fit_and_plot(
        df=df_v,
        title="Vertical Input Polarization ($V$)",
        data_label=r"Measured $V_V - V_{\mathrm{bg}}$",
        data_color="#2ca02c",
        fit_color="#ff7f0e",
        marker="s",
        out_filename="q2_vertical.svg",
    )


if __name__ == "__main__":
    main()
