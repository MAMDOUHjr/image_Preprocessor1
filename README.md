# Image Processing GUI Application

## Overview
This is a desktop application built with Python and Tkinter that provides a graphical user interface for image processing. It supports processing either a single image or an entire folder of images in batch mode.

---

## Features

- **Single Image Processing:**
  - Load and display an image.
  - Adjust brightness and contrast with Photoshop-style controls.
  - Apply filters such as Gaussian Blur, Canny Edge Detection, and Denoising.
  - Perform feature extraction using ORB (Oriented FAST and Rotated BRIEF).
  - Reset the image to its original state.
  - Save the processed image.

- **Folder Batch Processing:**
  - Select a folder containing multiple images.
  - Apply any of the above filters or processing techniques to all images in the folder.
  - Save the processed images automatically with the same filenames.

---

## Main Files

- `main.py`  
  The entry point of the application that allows the user to choose between single image processing or full folder batch processing.  
  Depending on the choice, it opens the corresponding GUI window.

- `single_image_gui.py` (or your second script)  
  Implements the single image processing interface with controls for brightness, contrast, filters, feature extraction, reset, and saving functionality.

---

## How to Use

1. Run the program:
   ```bash
   python main.py
