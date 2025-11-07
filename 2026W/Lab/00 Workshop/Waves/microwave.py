import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv("microwave.csv")
theta = np.deg2rad(data["theta(deg)"])
intensity1 = data["power_1"]
intensity2 = data["power_2"]

for intensity in (intensity1, intensity2):
    plt.polar(theta, intensity)

plt.show()
