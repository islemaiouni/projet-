import tkinter as tk
from tkinter import filedialog
from utils.image_loader import load_image, display_image, update_image  # Ensure correct import
from filters.linear_filters import mean_filter_3x3, mean_filter_5x5, gaussian_filter
from filters.non_linear_filters import median_filter, min_filter, max_filter
from contrast.enhancement import quantifier, recadrage, egaliser  # Imported contrast enhancement functions
from seuillage.thresholding import manual_threshold, mean_threshold, median_threshold
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Global variables
image_original = None
image_processed = None
current_operation = None

def apply_transformation(transformation_func, title):
    global image_processed, current_operation
    if image_original is not None:
        # Apply the transformation
        image_processed = transformation_func(image_original)
        current_operation = title
        update_displayed_image_and_histogram(title)

def update_displayed_image_and_histogram(title):
    # Clear previous widgets
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    operation_label = tk.Label(canvas_frame, text=f"Operation: {title}", font=('Arial', 14))
    operation_label.grid(row=0, column=0, columnspan=2)

    original_image_label = tk.Label(canvas_frame, text="Original Image")
    original_image_label.grid(row=1, column=0)
    display_image_on_canvas(image_original, 0)
    display_histogram(image_original, 1)

    processed_image_label = tk.Label(canvas_frame, text="Processed Image")
    processed_image_label.grid(row=1, column=1)
    display_image_on_canvas(image_processed, 1)
    display_histogram(image_processed, 2)

def display_image_on_canvas(image, column):
    fig = plt.Figure(figsize=(5, 5), dpi=80)
    ax = fig.add_subplot(111)
    ax.imshow(image, cmap="gray")
    ax.axis('off')
    
    # Draw the image onto Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().grid(row=2, column=column, padx=5, pady=5)
    canvas.draw()

def display_histogram(image, column):
    fig = plt.Figure(figsize=(5, 2), dpi=80)
    ax = fig.add_subplot(111)
    ax.hist(image.ravel(), bins=256, histtype='step', color='black')
    ax.set_title("Histogram")
    
    # Draw the histogram onto Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().grid(row=3, column=column, padx=5, pady=5)
    canvas.draw()

def zoom_histogram(event, image, column):
    fig = plt.Figure(figsize=(5, 2), dpi=80)
    ax = fig.add_subplot(111)
    bins = 256
    if event.delta > 0:  # Zoom in
        bins = max(50, bins - 10)
    else:  # Zoom out
        bins = min(256, bins + 10)

    ax.hist(image.ravel(), bins=bins, histtype='step', color='black')
    ax.set_title("Histogram")
    
    # Redraw histogram with new bins
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().grid(row=3, column=column)
    canvas.draw()

# Main interface
root = tk.Tk()
root.title("Image Processing Project")

# Create scrollable frame
scrollable_frame = tk.Frame(root)
scrollable_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(scrollable_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", lambda event: zoom_histogram(event, image_processed, 2))

canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Load Image", command=lambda: load_image_to_global())
file_menu.add_command(label="Quit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

filter_menu = tk.Menu(menu_bar, tearoff=0)
filter_menu.add_command(label="Mean Filter 3x3", command=lambda: apply_transformation(mean_filter_3x3, "Mean Filter 3x3"))
filter_menu.add_command(label="Mean Filter 5x5", command=lambda: apply_transformation(mean_filter_5x5, "Mean Filter 5x5"))
filter_menu.add_command(label="Gaussian Filter", command=lambda: apply_transformation(gaussian_filter, "Gaussian Filter"))
menu_bar.add_cascade(label="Linear Filters", menu=filter_menu)

non_linear_menu = tk.Menu(menu_bar, tearoff=0)
non_linear_menu.add_command(label="Median Filter", command=lambda: apply_transformation(median_filter, "Median Filter"))
non_linear_menu.add_command(label="Min Filter", command=lambda: apply_transformation(min_filter, "Min Filter"))
non_linear_menu.add_command(label="Max Filter", command=lambda: apply_transformation(max_filter, "Max Filter"))
menu_bar.add_cascade(label="Non-Linear Filters", menu=non_linear_menu)

contrast_menu = tk.Menu(menu_bar, tearoff=0)
contrast_menu.add_command(label="Quantifier", command=lambda: apply_transformation(quantifier, "Quantifier"))
contrast_menu.add_command(label="Recadrage", command=lambda: apply_transformation(recadrage, "Recadrage"))
contrast_menu.add_command(label="Histogram Equalization", command=lambda: apply_transformation(egaliser, "Histogram Equalization"))
menu_bar.add_cascade(label="Contrast Enhancement", menu=contrast_menu)

seuillage_menu = tk.Menu(menu_bar, tearoff=0)
seuillage_menu.add_command(label="Manual Threshold", command=lambda: apply_transformation(manual_threshold, "Manual Threshold"))
seuillage_menu.add_command(label="Mean Threshold", command=lambda: apply_transformation(mean_threshold, "Mean Threshold"))
seuillage_menu.add_command(label="Median Threshold", command=lambda: apply_transformation(median_threshold, "Median Threshold"))
menu_bar.add_cascade(label="Thresholding", menu=seuillage_menu)

root.config(menu=menu_bar)

def load_image_to_global():
    global image_original
    file_path = filedialog.askopenfilename()
    if file_path:
        image_original = plt.imread(file_path)
        update_displayed_image_and_histogram("Image Loaded")

root.mainloop()
