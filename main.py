import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2
def open_folder_gui():
    import numpy as np
    from tkinter import Toplevel

    def apply_and_replace(func):
        folder = filedialog.askdirectory()
        if not folder:
            return
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg', '.tif')):
                path = os.path.join(folder, filename)
                img = cv2.imread(path)
                if img is None:
                    continue
                processed = func(img)
                cv2.imwrite(path, processed)
        messagebox.showinfo("Done", "All images processed and saved.")

    def adjust_brightness_contrast(img, brightness=0, contrast=0):
        brightness = int((brightness / 100.0) * 255)
        contrast = (contrast + 100) / 100.0
        img = img.astype(np.float32)
        img = (img - 128) * contrast + 128 + brightness
        img = np.clip(img, 0, 255)
        return img.astype(np.uint8)

    def apply_denoising(img):
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    def apply_blur(img):
        return cv2.GaussianBlur(img, (5, 5), 0)

    def apply_edges(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(cv2.Canny(gray, 100, 200), cv2.COLOR_GRAY2BGR)

    def apply_orb(img):
        orb = cv2.ORB_create()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = orb.detectAndCompute(gray, None)
        return cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0), flags=0)

    
    folder_window = tk.Tk()
    folder_window.title("Batch Processing")
    folder_window.geometry("300x300")

    
    tk.Button(folder_window, text="🌫 Gaussian Blur", command=lambda: apply_and_replace(apply_blur)).pack(pady=5)
    tk.Button(folder_window, text="🧱 Canny Edges", command=lambda: apply_and_replace(apply_edges)).pack(pady=5)
    tk.Button(folder_window, text="🧹 Denoise", command=lambda: apply_and_replace(apply_denoising)).pack(pady=5)
    tk.Button(folder_window, text="🔍 Feature Extraction", command=lambda: apply_and_replace(apply_orb)).pack(pady=5)
    tk.Button(folder_window, text="☀ Brightness + Contrast", command=lambda: apply_and_replace(lambda img: adjust_brightness_contrast(img, 30, 30))).pack(pady=5)

    folder_window.mainloop()

# ====== Main Windooow ======
main_root = tk.Tk()
main_root.title("Select Mode")
main_root.geometry("400x400")

def open_single_image_gui():
    main_root.destroy()
    import single_image_gui

def open_folder_processing_gui():
    main_root.destroy()
    open_folder_gui()

tk.Button(main_root, text="📷 Single Image", width=20, height=2, command=open_single_image_gui).pack(pady=10)
tk.Button(main_root, text="🗂 Full Folder", width=20, height=2, command=open_folder_processing_gui).pack(pady=10)

main_root.mainloop()
