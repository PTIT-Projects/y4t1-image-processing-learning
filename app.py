import streamlit as st
from PIL import Image, ImageOps
import io
from pathlib import Path
from datetime import datetime
import os

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
algorithms = [
    "None (show original)",
    "Grayscale (stub)",
    "Gaussian Blur (stub)",
    "Edge Detect (stub)",
    "Custom - your implementation"
]
col1, col2 = st.columns([1, 1])

with col1:
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    algorithm = st.selectbox("Algorithm", algorithms)
    # example parameter (you can add more or remove)
    param = st.slider("Parameter (example)", 0, 100, 10)

with col2:
    st.markdown("Preview / Result")
    original_placeholder = st.empty()
    result_placeholder = st.empty()

def apply_algorithm(img: Image.Image, name: str, param: int) -> Image.Image:
    """
    Replace or extend this function with your real implementations.
    It must return a PIL.Image.
    """
    if name == "None (show original)":
        return img
    if name == "Grayscale (stub)":
        return ImageOps.grayscale(img).convert("RGB")
    if name == "Gaussian Blur (stub)":
        # stub: just return original (replace with actual blur)
        return img
    if name == "Edge Detect (stub)":
        # stub: just return original (replace with actual edge detection)
        return img
    if name.startswith("Custom"):
        # keep original until you implement your custom algorithm
        return img
    return img

if uploaded is not None:
    # read image from uploaded file
    image = Image.open(io.BytesIO(uploaded.read())).convert("RGB")
    original_placeholder.image(image, caption="Original image", width="stretch")

    if st.button("Apply"):
        with st.spinner("Applying algorithm..."):
            output = apply_algorithm(image, algorithm, param)
        result_placeholder.image(output, caption=f"Result — {algorithm}", width="stretch")

        # save pair
        try:
            saved_folder = save_pair(image, output, base_dir="data")
            st.success(f"Saved input/output pair to: {saved_folder}")
        except Exception as e:
            st.error(f"Failed to save images: {e}")

        # optional: provide download
        buf = io.BytesIO()
        output.save(buf, format="PNG")
        st.download_button("Download result (PNG)", data=buf.getvalue(), file_name="result.png", mime="image/png")
else:
    original_placeholder.info("No image uploaded yet.")
    result_placeholder.empty()