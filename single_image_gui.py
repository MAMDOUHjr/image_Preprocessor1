import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# ================== Global Variables ==================
original_image = None
processed_image = None
image_label = None

brightness_val = 0  
contrast_val = 0  

# ================== Image Processing Functions ==================
def adjust_brightness_contrast(img, brightness=0, contrast=0):
    """
    Adjust brightness and contrast similar to Photoshop style.

    brightness: -100 to 100
    contrast: -100 to 100
    """
    
    brightness = int((brightness / 100.0) * 255)
    contrast = (contrast + 100) / 100.0  
    img = img.astype(np.float32)

    
    img = (img - 128) * contrast + 128 + brightness

    
    img = np.clip(img, 0, 255)

    return img.astype(np.uint8)

def apply_gaussian_blur(img):
    return cv2.GaussianBlur(img, (5, 5), 0)

def apply_canny_edge_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(cv2.Canny(gray, 100, 200), cv2.COLOR_GRAY2BGR)

def apply_denoising(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

# ================== Utility Functions ==================
def open_image():
    global original_image, processed_image, brightness_val, contrast_val
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.tif")])
    if not file_path:
        return
    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Failed to load image.")
        return
    original_image = img
    processed_image = img.copy()
    brightness_val = 0
    contrast_val = 0
    show_image(processed_image)

def show_image(img):
    global image_label
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img_pil)

    if image_label is None:
        image_label = tk.Label(root, image=img_tk)
        image_label.image = img_tk
        image_label.pack()
    else:
        image_label.configure(image=img_tk)
        image_label.image = img_tk

def update_brightness(val):
    global brightness_val
    brightness_val += val
    brightness_val = max(-100, min(100, brightness_val))
    apply_brightness_contrast()

def update_contrast(val):
    global contrast_val
    contrast_val += val
    contrast_val = max(-100, min(100, contrast_val))
    apply_brightness_contrast()

def apply_brightness_contrast():
    global processed_image, original_image, brightness_val, contrast_val
    if original_image is None:
        messagebox.showwarning("No Image", "Please load an image first.")
        return
    processed_image = adjust_brightness_contrast(original_image, brightness=brightness_val, contrast=contrast_val)
    show_image(processed_image)

def apply_technique(func):
    global processed_image
    if processed_image is None:
        messagebox.showwarning("No Image", "Please load an image first.")
        return
    processed_image = func(processed_image)
    show_image(processed_image)

def reset_image():
    global processed_image, brightness_val, contrast_val
    if original_image is not None:
        brightness_val = 0
        contrast_val = 0
        processed_image = original_image.copy()
        show_image(processed_image)


def extract_features_with_orb(img):
    orb = cv2.ORB_create()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    
    img_with_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0), flags=0)
    
    
    print(f"[INFO] Keypoints: {len(keypoints)}, Descriptors shape: {descriptors.shape if descriptors is not None else 'None'}")

    return img_with_keypoints

def save_image():
    if processed_image is None:
        messagebox.showwarning("No Image", "No processed image to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
             filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, processed_image)
        messagebox.showinfo("Saved", f"Image saved successfully to:\n{file_path}")
# ================== GUI Setup ==================
root = tk.Tk()
root.title("Image Processing GUI")
root.geometry("500x750")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# ========== Row 0: Load and Save ==========
btn_load = tk.Button(btn_frame, text="📂 Load Image", command=open_image)
btn_load.grid(row=0, column=0, padx=5, pady=5)

btn_save = tk.Button(btn_frame, text="💾 Save Image", command=save_image)
btn_save.grid(row=0, column=1, padx=5, pady=5)

btn_reset = tk.Button(btn_frame, text="🔄 Reset", command=reset_image)
btn_reset.grid(row=0, column=2, padx=5, pady=5)

# ========== Row 1: Brightness ==========
tk.Label(btn_frame, text="Brightness").grid(row=1, column=0, pady=5)
btn_bright_dec = tk.Button(btn_frame, text="-", width=3, command=lambda: update_brightness(-10))
btn_bright_dec.grid(row=1, column=1, padx=2)
btn_bright_inc = tk.Button(btn_frame, text="+", width=3, command=lambda: update_brightness(10))
btn_bright_inc.grid(row=1, column=2, padx=2)

# ========== Row 2: Contrast ==========
tk.Label(btn_frame, text="Contrast").grid(row=2, column=0, pady=5)
btn_contrast_dec = tk.Button(btn_frame, text="-", width=3, command=lambda: update_contrast(-10))
btn_contrast_dec.grid(row=2, column=1, padx=2)
btn_contrast_inc = tk.Button(btn_frame, text="+", width=3, command=lambda: update_contrast(10))
btn_contrast_inc.grid(row=2, column=2, padx=2)

# ========== Row 3: Filters ==========
btn_blur = tk.Button(btn_frame, text="🌫 Gaussian Blur", command=lambda: apply_technique(apply_gaussian_blur))
btn_blur.grid(row=3, column=0, padx=5, pady=5)

btn_edge = tk.Button(btn_frame, text="🧱 Canny Edges", command=lambda: apply_technique(apply_canny_edge_detection))
btn_edge.grid(row=3, column=1, padx=5, pady=5)

btn_denoise = tk.Button(btn_frame, text="🧹 Denoise", command=lambda: apply_technique(apply_denoising))
btn_denoise.grid(row=3, column=2, padx=5, pady=5)

# ========== Row 4: Feature Extraction ==========
btn_features = tk.Button(btn_frame, text="🔍 Feature Extraction", command=lambda: apply_technique(extract_features_with_orb))
btn_features.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()

