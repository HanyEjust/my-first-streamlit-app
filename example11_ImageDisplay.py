import streamlit as st
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageEnhance
import io

st.set_page_config(page_title="Example 11 — Image Display", layout="wide")

st.title("Example 11 — Image Display")
st.write("This example shows how to display and work with images in Streamlit.")
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — Display Image from a URL
# ─────────────────────────────────────────────────────────────────────────────
st.header("1 — Display Image from a URL")
st.write("Paste a URL of any image and Streamlit will display it directly.")

img_url = st.text_input(
    "Image URL",
    value="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
)

if img_url.strip():
    try:
        st.image(img_url, caption="Image from URL", width=400)
        st.success("✅ Image loaded successfully.")
    except Exception as e:
        st.error("❌ Could not load the image. Check the URL and try again.")

st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — Upload Your Own Image
# ─────────────────────────────────────────────────────────────────────────────
st.header("2 — Upload Your Own Image")
st.write("Upload a JPG or PNG image from your computer.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:

    # Open the uploaded image with PIL
    image = Image.open(uploaded_file)

    # Convert to RGB so all operations work correctly
    image = image.convert("RGB")

    # Convert to NumPy array to get pixel info
    img_array = np.array(image)

    # Show image info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Width",    f"{image.width} px")
    with col2:
        st.metric("Height",   f"{image.height} px")
    with col3:
        st.metric("Channels", img_array.shape[2])
    with col4:
        st.metric("Mode",     image.mode)

    # Show the image
    st.image(image, caption="Uploaded Image", width=400)

st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — Create a Sample Image with NumPy (no upload needed)
# ─────────────────────────────────────────────────────────────────────────────
st.header("3 — Sample Image Created with NumPy")
st.write("We build an image from scratch using a NumPy array — no file needed.")
st.write("This is exactly how Keras sees images internally.")

# Create a 200x300 image filled with a red-to-blue gradient
height = 200
width  = 300

# Start with a blank black image: shape = (height, width, 3 channels)
arr = np.zeros((height, width, 3), dtype=np.uint8)

# Fill each column with a colour that changes left to right
for x in range(width):
    red   = int(x / width * 255)          # increases left → right
    blue  = int((1 - x / width) * 255)    # decreases left → right
    green = 80                             # stays constant
    arr[:, x] = [red, green, blue]

sample_image = Image.fromarray(arr)

col_a, col_b = st.columns(2)
with col_a:
    st.image(sample_image, caption="Gradient image built with NumPy", use_column_width=True)
with col_b:
    st.write(f"**Array shape :** `{arr.shape}`  → (height, width, channels)")
    st.write(f"**dtype       :** `{arr.dtype}`")
    st.write(f"**Min pixel   :** `{arr.min()}`")
    st.write(f"**Max pixel   :** `{arr.max()}`")
    st.info("A NumPy array is just numbers. Streamlit and Keras both read images this way.")

st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — Image Operations
# ─────────────────────────────────────────────────────────────────────────────
st.header("4 — Image Operations")
st.write("Choose an operation to apply to the sample gradient image above.")

operation = st.selectbox("Select operation", [
    "Original",
    "Grayscale",
    "Flip Horizontal",
    "Flip Vertical",
    "Rotate 90°",
    "Rotate 180°",
    "Blur",
    "Sharpen",
    "Edge Detection",
    "Invert Colors",
])

# Apply the selected operation to the sample image
if operation == "Original":
    result_image = sample_image

elif operation == "Grayscale":
    result_image = ImageOps.grayscale(sample_image)

elif operation == "Flip Horizontal":
    result_image = ImageOps.mirror(sample_image)

elif operation == "Flip Vertical":
    result_image = ImageOps.flip(sample_image)

elif operation == "Rotate 90°":
    result_image = sample_image.rotate(90, expand=True)

elif operation == "Rotate 180°":
    result_image = sample_image.rotate(180)

elif operation == "Blur":
    result_image = sample_image.filter(ImageFilter.GaussianBlur(radius=4))

elif operation == "Sharpen":
    result_image = sample_image.filter(ImageFilter.SHARPEN)

elif operation == "Edge Detection":
    result_image = sample_image.filter(ImageFilter.FIND_EDGES)

elif operation == "Invert Colors":
    result_image = ImageOps.invert(sample_image)

# Show original and result side by side
col_left, col_right = st.columns(2)
with col_left:
    st.write("**Original**")
    st.image(sample_image, use_column_width=True)
with col_right:
    st.write(f"**{operation}**")
    st.image(result_image, use_column_width=True)

st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — Normalization (important for ML)
# ─────────────────────────────────────────────────────────────────────────────
st.header("5 — Normalization")
st.write("Neural networks need pixel values between 0.0 and 1.0, not 0–255.")

# Original array: values 0 to 255
original_arr = np.array(sample_image)

# Normalized array: values 0.0 to 1.0
normalized_arr = original_arr / 255.0

col1, col2 = st.columns(2)

with col1:
    st.subheader("Before Normalization")
    st.write(f"dtype : `{original_arr.dtype}`")
    st.write(f"Min   : `{original_arr.min()}`")
    st.write(f"Max   : `{original_arr.max()}`")
    st.image(original_arr, caption="uint8 — values 0 to 255", use_column_width=True)

with col2:
    st.subheader("After Normalization (÷ 255)")
    st.write(f"dtype : `{normalized_arr.dtype}`")
    st.write(f"Min   : `{normalized_arr.min():.3f}`")
    st.write(f"Max   : `{normalized_arr.max():.3f}`")
    st.image(normalized_arr, caption="float64 — values 0.0 to 1.0", use_column_width=True)

st.info("The images look identical — normalization only changes the number range, not the visual appearance.")

st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — Download a Processed Image
# ─────────────────────────────────────────────────────────────────────────────
st.header("6 — Download a Processed Image")
st.write("Apply an operation and download the result as a PNG file.")

download_op = st.selectbox("Choose operation to download", [
    "Grayscale",
    "Flip Horizontal",
    "Invert Colors",
    "Blur",
    "Edge Detection",
], key="download_select")

if download_op == "Grayscale":
    download_image = ImageOps.grayscale(sample_image)

elif download_op == "Flip Horizontal":
    download_image = ImageOps.mirror(sample_image)

elif download_op == "Invert Colors":
    download_image = ImageOps.invert(sample_image)

elif download_op == "Blur":
    download_image = sample_image.filter(ImageFilter.GaussianBlur(radius=4))

elif download_op == "Edge Detection":
    download_image = sample_image.filter(ImageFilter.FIND_EDGES)

# Convert PIL image to bytes so st.download_button can use it
buf = io.BytesIO()
download_image.save(buf, format="PNG")
buf.seek(0)

col_prev, col_btn = st.columns(2)
with col_prev:
    st.image(download_image, caption=f"Preview: {download_op}", use_column_width=True)
with col_btn:
    st.download_button(
        label     = f"⬇️ Download {download_op} image",
        data      = buf,
        file_name = "processed_image.png",
        mime      = "image/png",
    )

st.markdown("---")
st.caption("Example 11 — Image Display | Streamlit Tutorial Series")
