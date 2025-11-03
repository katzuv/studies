import numpy as np  # math functions
import pandas as pd  # handling data structures (loaded from files)
from sklearn.metrics import r2_score  # import function that calculates R^2 score

C = 1
a = 1
L = 3
N = 100
coord = np.linspace(-L, L, N)  # defines coordinates
coord_x, coord_y = np.meshgrid(coord, coord)
