import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


image = plt.imread("acousto_near.tif")

plt.imshow(image)
plt.show()

x0, x1 = 600, 800
x = np.linspace(x0, x1, 400)
y0, y1 = 400, 600
y = image[y0, x0 : x0 + len(x), 0]
plt.plot(x, y, label="Intensity")

peaks, _ = signal.find_peaks(y, distance=40)
plt.plot(x[peaks], y[peaks], "^", label="Peaks")

plt.grid()
plt.legend()
plt.show()

image = plt.imread("acousto_far.tif")

plt.imshow(image)
plt.show()

x0, x1 = 750, 850
x = np.linspace(x0, x1, 100)
y0, y1 = 450, 550
y = image[y0, x0 : x0 + len(x), 0]
plt.plot(x, y, label="Intensity")

peaks, _ = signal.find_peaks(y, distance=4)
plt.plot(x[peaks], y[peaks], "^", label="Peaks")

plt.grid()
plt.legend()
plt.show()
