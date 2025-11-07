import pandas as pd

data = pd.read_csv("microwave.csv")
theta = np.deg2rad(data["theta(deg)"])
intensity1 = data["power_1"]
intensity2 = data["power_2"]
