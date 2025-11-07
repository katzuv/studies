import matplotlib.pyplot as plt
import numpy as np


def process_image(image_path):
    image = plt.imread(image_path)

    area = image[400:600, 600:800, :]
    x = np.arange(area.shape[1])

    y_intensity = area[:, :, :].mean(axis=2)
    plt.plot(x, y_intensity)

    plt.xlabel("Pixel X in selected area")
    plt.xlabel("Average intensity (red channel)")

    plt.imshow(image)
    plt.show()
