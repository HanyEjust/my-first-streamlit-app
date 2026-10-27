import streamlit as st
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import requests
from io import BytesIO

st.title("Example 11 — Image Display")
st.markdown("---")

# ────────────────────────────────────────────────────────
# 1. IMAGE FROM URL
# ────────────────────────────────────────────────────────
st.header("1 — Display Image from URL")

img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"

st.image(img_url, caption="A cute dog from Wikipedia", width=300)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. IMAGE FROM UPLOAD + DISPLAY OPTIONS
# ────────────────────────────────────────────────────────
st.header("2 — Upload & Display Image")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    image = Image.open(uploaded)
    img_array = np.array(image)

    # Info
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Width",    f"{image.width}px")
    with col2: st.metric("Height",   f"{image.height}px")
    with col3: st.metric("Channels", img_array.shape[2] if len(img_array.shape)==3 else 1)
    with col4: st.metric("Mode",     image.mode)

    # Display size control
    display_width = st.slider("Display width (px)", 100, 800, 400)
    st.image(image, caption="Uploaded Image", width=display_width)

    st.markdown("---")

    # ── Image Operations ─────────────────────────────────
    st.header("3 — Image Operations")
    st.write("Apply operations and see the result instantly.")

    operation = st.selectbox("Choose an operation", [
        "Original",
        "Grayscale",
        "Flip Horizontal",
        "Flip Vertical",
        "Rotate 90°",
        "Blur",
        "Edge Detection",
    ])

    if operation == "Original":
        result = image
    elif operation == "Grayscale":
        result = ImageOps.grayscale(image)
    elif operation == "Flip Horizontal":
        result = ImageOps.mirror(image)
    elif operation == "Flip Vertical":
        result = ImageOps.flip(image)
    elif operation == "Rotate 90°":
        result = image.rotate(90, expand=True)
    elif operation == "Blur":
        result = image.filter(ImageFilter.GaussianBlur(radius=3))
    elif operation == "Edge Detection":
        result = image.filter(ImageFilter.FIND_EDGES)

    # Show original and result side by side
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Original**")
        st.image(image, use_column_width=True)
    with c2:
        st.write(f"**{operation}**")
        st.image(result, use_column_width=True)

    st.markdown("---")

    # ── NumPy Array Display ──────────────────────────────
    st.header("4 — Display from NumPy Array")
    st.write("Streamlit can display NumPy arrays directly — important for ML!")

    with st.expander("Show pixel array"):
        st.write(f"Shape: `{img_array.shape}`")
        st.write(f"dtype: `{img_array.dtype}`")
        st.write(f"Min: `{img_array.min()}` | Max: `{img_array.max()}`")

    # Normalize array to 0–1 and display
    normalized = img_array / 255.0
    st.write("Displaying from **normalized NumPy array** (values 0.0–1.0):")
    st.image(normalized, caption="From NumPy array (normalized)", width=300)

    st.markdown("---")

    # ── Image Grid ───────────────────────────────────────
    st.header("5 — Image Grid")
    st.write("Display the same image with different operations in a grid.")

    operations = {
        "Original"   : image,
        "Grayscale"  : ImageOps.grayscale(image),
        "Flipped"    : ImageOps.mirror(image),
        "Rotated 90°": image.rotate(90, expand=True),
        "Blurred"    : image.filter(ImageFilter.GaussianBlur(3)),
        "Edges"      : image.filter(ImageFilter.FIND_EDGES),
    }

    grid_cols = st.columns(3)
    for i, (op_name, op_img) in enumerate(operations.items()):
        with grid_cols[i % 3]:
            st.image(op_img, caption=op_name, use_column_width=True)

else:
    st.info("👆 Upload an image to see display options and operations")
