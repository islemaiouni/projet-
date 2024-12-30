import numpy as np

# Filtre Médian
def median_filter(image):
    padded_image = np.pad(image, 1, mode="edge")
    result = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = np.median(padded_image[i:i+3, j:j+3])
    return result

# Filtre Min
def min_filter(image):
    padded_image = np.pad(image, 1, mode="edge")
    result = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = np.min(padded_image[i:i+3, j:j+3])
    return result

# Filtre Max
def max_filter(image):
    padded_image = np.pad(image, 1, mode="edge")
    result = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = np.max(padded_image[i:i+3, j:j+3])
    return result
