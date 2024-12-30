import numpy as np

def histogram(image):
    hist = np.zeros(256)
    for value in image.flatten():
        hist[value] += 1
    return hist

# Seuillage Manuel
def manual_threshold(image, threshold=128):
    return (image >= threshold).astype(np.uint8) * 255

# Seuillage Moyenne
def mean_threshold(image):
    mean_val = np.mean(image)
    return manual_threshold(image, threshold=mean_val)

# Seuillage Médiane
def median_threshold(image):
    median_val = np.median(image)
    return manual_threshold(image, threshold=median_val)
