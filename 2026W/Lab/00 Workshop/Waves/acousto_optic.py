import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def process_image(image_path):
    image = plt.imread(image_path)

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
