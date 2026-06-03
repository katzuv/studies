import numpy as np
import pandas as pd

import physlab

# --- Nuclear Specific Constants ---
RHO_AIR = 1.204e-3  # g/cm^3 (at room temp)
RHO_AL = 2.70       # g/cm^3
SIGMA_GM_WINDOW = 2.0e-3 # g/cm^2 (typical Geiger-Muller window density)

# Manual Background Measurement: 52 counts in 100 seconds
BG_RATE = 0.52  # cps
BG_ERR = np.sqrt(52) / 100  # cps



def load_gm(path, header=9):
    """Specialized loader for Geiger-Muller TSV files."""
    df = pd.read_csv(path, header=header, sep="\t+", engine="python")
    df["counts_err"] = np.sqrt(df["Counts"])
    df["rate"] = df["Counts"] / df["Time"]
    # Error propagation for rate (R = N/t) -> sigma_R = sqrt(N)/t
    df["rate_err"] = df["counts_err"] / df["Time"]
    return df


def subtract_bg(rate, rate_err, bg, bg_err):
    """Substracts background and propagates error."""
    corrected = rate - bg
    err = np.sqrt(rate_err**2 + bg_err**2)
    return corrected, err


def fit_linear_tvl(x, y, y_err):
    """
    Fits y = slope * x + intercept.
    TVL (Tenth Value Layer) is where R(x) = R(0)/10.
    Intercept + slope*TVL = Intercept/10 -> slope*TVL = -0.9*Intercept
    TVL = 0.9 * Intercept / |slope|
    """
    def model(x, slope, intercept):
        return slope * x + intercept

    # Heuristic p0
    slope_guess = (y[-1] - y[0]) / (x[-1] - x[0]) if len(x) > 1 else -1.0
    intercept_guess = y[0]

    res = physlab.physics_fit(model, x, y, y_err, p0=[slope_guess, intercept_guess])

    slope, intercept = res.params
    slope_err, intercept_err = res.errors

    # TVL calculation
    tvl = 0.9 * intercept / np.abs(slope)

    # Error propagation for TVL
    tvl_err = physlab.propagate_error(
        lambda s, i: 0.9 * i / np.abs(s), (slope, intercept), (slope_err, intercept_err)
    )

    return res, tvl, tvl_err


def fit_exponential(x, y, y_err, p0=None):
    """Fits y = A * exp(-mu * x) and returns TVL (Tenth Value Layer)."""
    # Heuristic p0 if not provided
    if p0 is None:
        A_guess = y[0]
        # mu = ln(y1/y2) / (x2-x1)
        mu_guess = np.log(y[0] / y[-1]) / (x[-1] - x[0]) if len(y) > 1 else 0.001
        p0 = [A_guess, mu_guess]

    def model(x, A, mu):
        return A * np.exp(-mu * x)
    res = physlab.physics_fit(model, x, y, y_err, p0=p0)

    A, mu = res.params
    A_err, mu_err = res.errors

    # TLV is thickness where intensity drops by 10
    # 1/10 = exp(-mu * TLV) -> TLV = ln(10) / mu
    tlv = np.log(10) / mu
    tlv_err = physlab.propagate_error(lambda m: np.log(10) / m, (mu,), (mu_err,))

    return res, tlv, tlv_err
