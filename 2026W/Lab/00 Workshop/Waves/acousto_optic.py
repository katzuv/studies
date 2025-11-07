import matplotlib.pyplot as plt


def process_image(image_path):
    image = plt.imread(image_path)

    plt.imshow(image)
    plt.show()
