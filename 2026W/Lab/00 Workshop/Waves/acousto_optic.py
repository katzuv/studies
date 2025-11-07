import matplotlib.pyplot as plt
from scipy import ndimage


def process_image(image_path):
    image = plt.imread(image_path)

    image = ndimage.rotate(image, 90, reshape=True)

    plt.imshow(image)
    plt.show()
