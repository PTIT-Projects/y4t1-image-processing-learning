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

def save_pair(input_img: Image.Image, output_img: Image.Image, algorithm: str = "", base_dir: str = "data") -> Path:
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
    input_path = folder / f"input_{algorithm}.png"
    output_path = folder / f"output_{algorithm}.png"
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
    INVERSE_LOG_FUNCTION_TRANSFORM: INVERSE_LOG_FUNCTION_TRANSFORM,
    POWER_LAW_TRANSFORM: POWER_LAW_TRANSFORM,
    HISTOGRAM_EQUALIZATION: HISTOGRAM_EQUALIZATION,
    MEDIAN_FILTER: MEDIAN_FILTER,
    MEAN_FILTER: MEAN_FILTER,
    MEAN_WEIGHTED_FILTER: MEAN_WEIGHTED_FILTER,
    NEAREST_NEIGHBOR_MEAN_FILTER: NEAREST_NEIGHBOR_MEAN_FILTER,
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
    elif algorithm == algorithms[POWER_LAW_TRANSFORM]:
        gamma_value = st.number_input(label="Enter gamma value")
        params = {}
        params[GAMMA_VALUE] = gamma_value
    elif algorithm == algorithms[NEAREST_NEIGHBOR_MEAN_FILTER]:
        k = st.number_input(label="Enter k", min_value=1, step=1)
        theta_str = st.text_input(label="Enter theta (float)", value="10.0")
        try:
            theta = float(theta_str)
        except ValueError:
            st.warning("Please enter a valid number for theta.")
            theta = 10.0  # fallback default
        params = {}
        params[K_VALUE] = k
        params[THETA_VALUE] = theta

        

with col2:
    st.markdown("Preview / Result")
    original_placeholder = st.empty()
    result_placeholder = st.empty()

def apply_algorithm(img: Image.Image, name: str, param) -> Image.Image:
    """
    Replace or extend this function with your real implementations.
    It must return a PIL.Image.
    """
    if name == algorithms[NEGATIVE_IMAGE]:
        return negative_image(img)
    elif name == algorithms[THRESHOLDING]:
        return thresholding(img, param[THRESHOLD_VALUE])
    elif name == algorithms[LOG_FUNCTION_TRANSFORM]:
        return log_function_transform(img)
    elif name == algorithms[INVERSE_LOG_FUNCTION_TRANSFORM]:
        return inverse_log_transform(img)
    elif name == algorithms[POWER_LAW_TRANSFORM]:
        return power_law_transform(img, param[GAMMA_VALUE])
    elif name == algorithms[HISTOGRAM_EQUALIZATION]:
        return histogram_equalization(img)
    elif name == algorithms[MEDIAN_FILTER]:
        return median_filter(img, filter_size=3)
    elif name == algorithms[MEAN_FILTER]:
        return mean_filter(img, filter_size=3)
    elif name == algorithms[MEAN_WEIGHTED_FILTER]:
        return mean_weighted_filter(img, filter_size=3)
    elif name == algorithms[NEAREST_NEIGHBOR_MEAN_FILTER]:
        return k_nearest_neighbor_mean_filter(img, filter_size=3, k=param[K_VALUE], theta=param[THETA_VALUE])
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
            saved_folder = save_pair(image, output, algorithm, base_dir="data")
            st.success(f"Saved input/output pair to: {saved_folder}")
        except Exception as e:
            st.error(f"Failed to save images: {e}")
else:
    original_placeholder.info("No image uploaded yet.")
    result_placeholder.empty()