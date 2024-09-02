import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def find_difference(image1, image2):
    """
    Compares two images by calculating their structural similarity.

    Args:
        image1 (ndarray): The first image.
        image2 (ndarray): The second image.

    Returns:
        ndarray: The normalized difference image.
    """
    assert image1.shape == image2.shape, "Specify 2 images with the same shape."
    
    # Convert images to grayscale
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)
    
    # Compute structural similarity
    score, difference_image = structural_similarity(gray_image1, gray_image2, full=True)
    print("Similarity of the images:", score)
    
    # Normalize the difference image
    normalized_difference_image = (difference_image - np.min(difference_image)) / (np.max(difference_image) - np.min(difference_image))
    
    return normalized_difference_image

def transfer_histogram(image1, image2):
    """
    Transfers the histogram of image1 to image2.

    Args:
        image1 (ndarray): The reference image.
        image2 (ndarray): The image whose histogram will be adjusted.

    Returns:
        ndarray: The histogram-matched image.
    """
    matched_image = match_histograms(image1, image2, multichannel=True)
    return matched_image
