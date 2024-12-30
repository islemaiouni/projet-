from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from skimage.color import rgb2gray  # If you're using scikit-image for color conversion

def load_image_to_global():
    global image_original
    file_path = filedialog.askopenfilename()
    if file_path:
        image_original = plt.imread(file_path)  # Assuming the image is loaded using matplotlib

        # If the image is RGB, convert it to grayscale
        if len(image_original.shape) == 3:  # Check if the image is RGB
            image_original = rgb2gray(image_original)

        update_displayed_image_and_histogram("Image Loaded")

image_original = None
image_processed = None
canvas_frame = None


# Charger une image
def load_image():
    global image_original, image_processed
    filename = filedialog.askopenfilename(title="Charger une image", filetypes=[("Images", "*.jpg *.png *.bmp *.jpeg")])
    if filename:
        image_original = Image.open(filename).convert("L")
        image_processed = np.array(image_original)
        display_image(image_processed, "Image Originale")

# Function to update the image and display it with the histogram
def update_image(image_array):
    global canvas_frame
    # Convert the image to displayable format (PIL image)
    img = Image.fromarray(image_array)
    img = ImageTk.PhotoImage(img)

    # Update the processed image label
    processed_image_label = tk.Label(canvas_frame, image=img)
    processed_image_label.grid(row=1, column=1)
    processed_image_label.image = img

    # Update histogram for processed image
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(image_array, cmap="gray")
    axes[1].hist(image_array.flatten(), bins=256, range=(0, 256), color="gray")
    axes[0].set_title("Image Traité")
    axes[1].set_title("Histogramme de l'Image Traité")
    plt.show()

# Function to display the original image and its histogram
def display_image(image_array, title):
    global canvas_frame
    # Convert the image to displayable format (PIL image)
    img = Image.fromarray(image_array)
    img = ImageTk.PhotoImage(img)

    # Display the original image
    original_image_label = tk.Label(canvas_frame, image=img)
    original_image_label.grid(row=1, column=0)
    original_image_label.image = img

    # Display histogram for original image
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(image_array, cmap="gray")
    axes[1].hist(image_array.flatten(), bins=256, range=(0, 256), color="gray")
    axes[0].set_title("Image Originale")
    axes[1].set_title("Histogramme de l'Image Originale")
    plt.show()
