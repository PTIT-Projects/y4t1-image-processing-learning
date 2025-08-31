from PIL import Image, ImageOps
import io
import numpy as np
def negative_image(image: Image.Image):
    gray = image.convert("L")
    arr = np.asarray(gray).astype(np.float32) / 255.0
    out = 1.0 - arr
    out_img = Image.fromarray((np.clip(out, 0.0, 1.0) * 255.0).round().astype(np.uint8), mode="L")
    return out_img

def thresholding(image: Image.Image, threshold_value: int):
    gray = image.convert("L")
    arr = np.asarray(gray).astype(np.float32)
    arr[arr < threshold_value] = 0
    arr[arr >= threshold_value] = 255
    out_img = Image.fromarray(arr.astype(np.uint8), mode="L")
    return out_img

def log_function_transform(image: Image.Image):
    gray = image.convert("L")
    arr = np.asarray(gray).astype(np.float64)  
    c = 255.0 / (np.log(1 + np.max(arr)))
    out = c * np.log1p(arr)
    out_img = Image.fromarray(np.round(out).astype(np.uint8), mode="L")
    return out_img

def inverse_log_transform(image: Image.Image):
    gray = image.convert("L")
    arr = np.asarray(gray).astype(np.float64)
    c = 255.0 / (np.log(1 + np.max(arr)))
    # Inverse of log transform: arr = c * log1p(x) -> x = expm1(arr / c)
    out = np.expm1(arr / c)
    out = np.clip(out, 0, 255)
    out_img = Image.fromarray(np.round(out).astype(np.uint8), mode="L")
    return out_img

def power_law_transform(image: Image.Image, gamma: float):
    gray = image.convert("L")
    arr = np.asarray(gray).astype(np.float64) / 255.0
    out = np.power(arr, gamma)
    out_img = Image.fromarray((np.clip(out, 0.0, 1.0) * 255.0).round().astype(np.uint8), mode="L")
    return out_img