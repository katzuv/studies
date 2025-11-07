import numpy as np
import pandas as pd

data = pd.read_csv("spectroscopy.csv")

d = 1e-3 / 500
angle = np.deg2rad(data.grating_angle)
wavelengths = d * np.sin(angle)
print(wavelengths * 1e9)
