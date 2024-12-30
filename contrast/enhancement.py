import numpy as np
import cv2

# Convert the image to grayscale if it's not already
def to_grayscale(image):
    if len(image.shape) == 3:  # If the image is not already grayscale
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

# Étirement du Contraste
def contrast_stretching(image):
    image = to_grayscale(image)  # Ensure the image is grayscale
    min_val, max_val = np.min(image), np.max(image)
    return ((image - min_val) * 255 / (max_val - min_val)).astype(np.uint8)

# Égalisation d'Histogramme
def histogram_equalization(image):
    image = to_grayscale(image)  # Ensure the image is grayscale
    hist, bins = np.histogram(image.flatten(), bins=256, range=(0, 256))
    cdf = hist.cumsum()
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    result = np.interp(image.flatten(), bins[:-1], cdf_normalized).reshape(image.shape)
    return result.astype(np.uint8)

# Quantification function: maps pixel values to quantized values based on a LUT
def LUTcreat1():
    LUT = {}
    for i in range(7):
        LUT[str(i)] = '0'
    for i in range(7, 10):
        LUT[str(i)] = '20'
    for i in range(10, 20):
        LUT[str(i)] = '40'
    return LUT

def quantifier(image):
    image = to_grayscale(image)  # Ensure the image is grayscale
    imr = np.copy(image)
    LUT = LUTcreat1()
    for i in range(imr.shape[0]):
        for j in range(imr.shape[1]):
            imr[i, j] = int(LUT.get(str(imr[i, j]), 0))  # Handle KeyError with default value
    return imr

# Recadrage function: rescales pixel values based on min/max of the image
def LUTcreat2(maxm1, minm1):
    LUT = {}
    min2 = 0
    max2 = 40
    for i in range(20):
        a = (max2 - min2) / (maxm1 - minm1)
        b = (min2 * maxm1 - max2 * minm1) / (maxm1 - minm1)
        x = int(round(a * i + b))
        LUT[str(i)] = str(x)
    return LUT

def recadrage(image):
    image = to_grayscale(image)  # Ensure the image is grayscale
    imr = np.copy(image)
    minn = np.min(imr)
    maxn = np.max(imr)
    LUT = LUTcreat2(maxn, minn)
    for i in range(imr.shape[0]):
        for j in range(imr.shape[1]):
            imr[i, j] = int(LUT.get(str(imr[i, j]), 0))  # Handle KeyError with default value
    return imr

# Histogram Equalization function
def hiscuml(hist):
    hisc = np.copy(hist)
    for i in range(1, len(hisc)):
        hisc[i] = hisc[i] + hisc[i - 1]
    return hisc

def histogramme(image):
    image = to_grayscale(image)  # Ensure the image is grayscale
    hist = np.zeros(256)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            hist[image[i, j]] += 1
    return hist

def LUTcreat3(image, marge):
    hist_cum = hiscuml(histogramme(image))  # Cumulative histogram of the image
    n = image.size
    LUT = {}
    for i in range(len(hist_cum)):
        v = (hist_cum[i] * marge) // n
        LUT[str(i)] = str(int(v))
    return LUT

def egaliser(image):
    image = to_grayscale(image)  # Ensure the image is grayscale
    imr = np.copy(image)
    marge = 40
    LUT = LUTcreat3(image, marge)
    for i in range(imr.shape[0]):
        for j in range(imr.shape[1]):
            imr[i, j] = int(LUT.get(str(imr[i, j]), 0))  # Handle KeyError with default value
    return imr

