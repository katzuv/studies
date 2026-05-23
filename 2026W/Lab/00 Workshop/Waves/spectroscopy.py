import numpy as np
import pandas as pd
from prettytable import PrettyTable

data = pd.read_csv("spectroscopy.csv")

d = 1e-3 / 500
angle = np.deg2rad(data.grating_angle)
wavelengths = d * np.sin(angle)
print(wavelengths * 1e9)

table = PrettyTable(
    (
        "Line",
        "Grating angle [deg]",
        "Grating wavelength [nm]",
        "Color",
        "Prism angle [deg]",
    )
)
for i in range(len(data)):
    table.add_row(
        [
            i + 1,
            data.grating_angle[i],
            round(wavelengths[i] * 1e9, 3),  # convert to nm
            data.color[i],
            data.prism_angle[i],
        ]
    )
print(table)
