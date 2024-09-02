from skimage.io import imread, imsave

def read_image(path, is_gray=False):
    """
    Reads an image from the specified path.

    Args:
        path (str): The path to the image file.
        is_gray (bool): Whether to read the image as grayscale. Defaults to False.

    Returns:
        ndarray: The image read from the file.
    """
    image = imread(path, as_gray=is_gray)
    return image

def save_image(image, path):
    """
    Saves an image to the specified path.

    Args:
        image (ndarray): The image to be saved.
        path (str): The path where the image will be saved.
    """
    imsave(path, image)
