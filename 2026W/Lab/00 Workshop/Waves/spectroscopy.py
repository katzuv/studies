import numpy as np
import pandas as pd
from prettytable import PrettyTable

data = pd.read_csv("spectroscopy.csv")

d = 1e-3 / 500
angle = np.deg2rad(data.grating_angle)
wavelengths = d * np.sin(angle)
print(wavelengths * 1e9)

lines = {
    f"Line {n+1}": (data.grating_angle[n], wavelengths[n], data.color[n])
    for n in range(len(angle))
}
table = PrettyTable(("Grating angle [deg]", "Grating wavelength [nm]", "Color"))
table.add_row((data.grating_angle, wavelengths, data.color))
