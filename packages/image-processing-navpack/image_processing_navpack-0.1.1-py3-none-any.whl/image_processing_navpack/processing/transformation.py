from skimage.transform import resize

def resize_image(image, proportion):
    """
    Resizes an image by a specified proportion.

    Args:
        image (ndarray): The image to be resized.
        proportion (float): The proportion to resize the image. Should be between 0 and 1.

    Returns:
        ndarray: The resized image.
    """
    assert 0 <= proportion <= 1, "Specify a valid proportion between 0 and 1."
    
    # Calculate new dimensions
    height = round(image.shape[0] * proportion)
    width = round(image.shape[1] * proportion)
    
    # Resize the image
    image_resized = resize(image, (height, width), anti_aliasing=True)
    
    return image_resized
