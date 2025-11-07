import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


image = plt.imread("acousto_near.tif")

plt.imshow(image)
plt.show()

x0, x1 = 600, 800
x = np.linspace(x0, x1, 400)
y0, y1 = 400, 600
y_near = image[y0, x0 : x0 + len(x), 0]
plt.plot(x, y_near, label="Intensity")

peaks, _ = signal.find_peaks(y_near, distance=40)
spacings = np.diff(peaks)
avg_dist = np.mean(spacings) * 5.2e-6
v = avg_dist * 2079e6
print(f"{v=}")
plt.plot(x[peaks], y_near[peaks], "^", label="Peaks")

plt.grid()
plt.legend()
plt.show()

image = plt.imread("acousto_far.tif")

plt.imshow(image)
plt.show()

x0, x1 = 750, 850
x = np.linspace(x0, x1, 100)
y0, y1 = 450, 550
y_far = image[y0, x0 : x0 + len(x), 0]
plt.plot(x, y_far, label="Intensity_far")

peaks, _ = signal.find_peaks(y_far, distance=1)
plt.plot(x[peaks], y_near[peaks], "^", label="Peaks")
brightest = sorted(peaks, key=lambda p: y_far[p], reverse=True)[:2]
distance = (brightest[1] - brightest[0]) * 5.2e-6
v = (2079e6 * 0.3 * 632.8e-9) / distance
print(f"{v=}")
plt.grid()
plt.legend()
plt.show()


# I don't know how to use FFT, we haven't studied this yet... also something in my data is off because the velocities I get make no sense.
