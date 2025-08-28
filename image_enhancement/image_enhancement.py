from PIL import Image, ImageOps
import io
import numpy as np
def negative_image(image: Image.Image):
    gray = image.convert("L")
    arr = np.asarray(gray).astype(np.float32) / 255.0
    out = 1.0 - arr
    out_img = Image.fromarray((np.clip(out, 0.0, 1.0) * 255.0).round().astype(np.uint8), mode="L")
    return out_img