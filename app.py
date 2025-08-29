import streamlit as st
from PIL import Image, ImageOps
import io
from pathlib import Path
from datetime import datetime
import os
from image_enhancement.image_enhancement import *
from constants import *
from image_enhancement.image_enhancement import *
from constants import *

def save_pair(input_img: Image.Image, output_img: Image.Image, base_dir: str = "data") -> Path:
    """
    Create data/<datetime-folder>/ and save input.png and output.png.
    Returns the folder Path.
    """
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)
    # timestamp with microseconds to ensure uniqueness
    ts = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    folder = base / ts
    folder.mkdir()
    # save as PNG
    input_path = folder / "input.png"
    output_path = folder / "output.png"
    input_img.save(str(input_path), format="PNG")
    output_img.save(str(output_path), format="PNG")
    return folder

st.set_page_config(page_title="Image Processing Playground", layout="wide")

st.title("Image Processing Playground")
st.write("Choose an algorithm, upload an image, then click Apply.")

# UI controls
algorithms = {
    NEGATIVE_IMAGE: NEGATIVE_IMAGE,
    THRESHOLDING: THRESHOLDING,
    LOG_FUNCTION_TRANSFORM: LOG_FUNCTION_TRANSFORM,
    INVERSE_LOG_FUNCTION_TRANSFORM: INVERSE_LOG_FUNCTION_TRANSFORM
}
col1, col2 = st.columns([1, 1])
params = {}
params = {}
with col1:
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    algorithm = st.selectbox("Algorithm", list(algorithms.keys()))    
    if algorithm == algorithms[THRESHOLDING]:
        threshold_value = st.number_input(label="Enter threshold value", min_value = 0, max_value=255)
        params = {}
        params[THRESHOLD_VALUE] = threshold_value
    # elif algorithm == algorithms[LOG_FUNCTION_TRANSFORM]:
    #     c_value = st.number_input(label="Enter constant c value", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    #     params = {}
    #     params[C_VALUE] = c_value

        

with col2:
    st.markdown("Preview / Result")
    original_placeholder = st.empty()
    result_placeholder = st.empty()

def apply_algorithm(img: Image.Image, name: str, param) -> Image.Image:
def apply_algorithm(img: Image.Image, name: str, param) -> Image.Image:
    """
    Replace or extend this function with your real implementations.
    It must return a PIL.Image.
    """
    if name == algorithms[NEGATIVE_IMAGE]:
    if name == algorithms[NEGATIVE_IMAGE]:
        return negative_image(img)
    elif name == algorithms[THRESHOLDING]:
        return thresholding(img, param[THRESHOLD_VALUE])
    elif name == algorithms[LOG_FUNCTION_TRANSFORM]:
        return log_function_transform(img)
    elif name == algorithms[INVERSE_LOG_FUNCTION_TRANSFORM]:
        return inverse_log_transform(img)
    return img

if uploaded is not None:
    # read image from uploaded file
    image = Image.open(io.BytesIO(uploaded.read())).convert("RGB")
    original_placeholder.image(image, caption="Original image", width="stretch")

    if st.button("Apply"):
        with st.spinner("Applying algorithm..."):
            output = apply_algorithm(image, algorithm, params)
            output = apply_algorithm(image, algorithm, params)
        result_placeholder.image(output, caption=f"Result — {algorithm}", width="stretch")

        # save pair
        try:
            saved_folder = save_pair(image, output, base_dir="data")
            st.success(f"Saved input/output pair to: {saved_folder}")
        except Exception as e:
            st.error(f"Failed to save images: {e}")
else:
    original_placeholder.info("No image uploaded yet.")
    result_placeholder.empty()