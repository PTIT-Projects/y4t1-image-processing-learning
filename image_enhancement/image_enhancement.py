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

def histogram_equalization(image: Image.Image):
    gray = image.convert("L")
    arr = np.array(gray)
    hist, _ = np.histogram(arr.flatten(), bins = 256, range = (0, 256))
    cdf = hist.cumsum()
    cdf_masked = np.ma.masked_equal(cdf, 0)
    cdf_masked = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
    cdf = np.ma.filled(cdf_masked, 0).astype('uint8')
    out = cdf[arr]
    return Image.fromarray(out, mode="L")

def median_filter(image: Image.Image, filter_size: int = 3):
    gray = image.convert("L")
    arr = np.array(gray)
    height, width = arr.shape
    result = np.zeros_like(arr)
    pad = filter_size // 2
    padded_arr = np.pad(arr, pad_width=pad, mode='constant')
    for i in range(height):
        for j in range(width):
            window = padded_arr[i:i+filter_size, j:j+filter_size]
            result[i, j] = np.median(window)
    return Image.fromarray(result, mode="L")


