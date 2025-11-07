import matplotlib.pyplot as plt
import numpy as np


def process_image(image_path):
    image = plt.imread(image_path)

    plt.imshow(image)
    plt.show()

    x0, x1 = 600, 800
    x = np.linspace(x0, x1, 400)
    y0, y1 = 400, 600
    y = image[y0, x0 : x0 + len(x), 0]
    plt.plot(x, y, label="Intensity")

    plt.grid()
    plt.legend()
    plt.show()
