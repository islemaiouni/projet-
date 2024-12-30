import numpy as np

# Convolution function (handles multi-channel images)
def convolution(image, kernel):
    kernel_size = kernel.shape[0]
    pad = kernel_size // 2
    padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
    result = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for c in range(image.shape[2]):  # Process each channel (for RGB)
                region = padded_image[i:i+kernel_size, j:j+kernel_size, c]
                result[i, j, c] = np.sum(region * kernel)
    return result

# Filtre Moyenneur 3x3 (handles multi-channel images)
def mean_filter_3x3(image):
    kernel = np.ones((3, 3)) / 9
    return convolution(image, kernel)

# Filtre Moyenneur 5x5 (handles multi-channel images)
def mean_filter_5x5(image):
    kernel = np.ones((5, 5)) / 25
    return convolution(image, kernel)

# Filtre Gaussien (handles multi-channel images)
def gaussian_filter(image, sigma=1.0):
    size = int(2 * np.ceil(2 * sigma) + 1)
    kernel = np.zeros((size, size))
    center = size // 2
    for x in range(size):
        for y in range(size):
            dx, dy = x - center, y - center
            kernel[x, y] = np.exp(-(dx**2 + dy**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)
    return convolution(image, kernel)
