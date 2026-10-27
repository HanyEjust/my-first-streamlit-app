import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io

st.title("Example 07 — File Upload")
st.markdown("---")

# ────────────────────────────────────────────────────────
# 1. UPLOAD A CSV FILE
# ────────────────────────────────────────────────────────
st.header("1 — Upload a CSV File")
st.write("The user uploads a CSV file and we display and analyze it.")

csv_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"],               # only allow CSV files
    help="Upload any CSV file to see it displayed as a table"
)

if csv_file is not None:
    # Show file info
    st.success(f"✅ File uploaded: **{csv_file.name}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("File Name", csv_file.name)
    with col2:
        size_kb = csv_file.size / 1024
        st.metric("File Size", f"{size_kb:.1f} KB")

    # Read into pandas
    df = pd.read_csv(csv_file)

    st.subheader("Preview (first 5 rows)")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Dataset Info")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Rows",    df.shape[0])
    with col_b:
        st.metric("Columns", df.shape[1])
    with col_c:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    with st.expander("📊 Show Column Statistics"):
        st.dataframe(df.describe(), use_container_width=True)

    with st.expander("🔍 Show Full Dataset"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👆 Upload a CSV file to get started")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. UPLOAD AN IMAGE
# ────────────────────────────────────────────────────────
st.header("2 — Upload an Image")
st.write("The user uploads an image and we display it with information.")

img_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "bmp"],
    help="Upload any image file"
)

if img_file is not None:
    # Open image with PIL
    image = Image.open(img_file)

    st.success(f"✅ Image uploaded: **{img_file.name}**")

    # Show image info in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Width",  f"{image.width} px")
    with col2:
        st.metric("Height", f"{image.height} px")
    with col3:
        st.metric("Mode", image.mode)   # RGB, RGBA, L (grayscale), etc.

    # Display options
    display_option = st.radio(
        "Display option",
        ["Original size", "Fixed width 300px", "Fixed width 600px"]
    )

    if display_option == "Original size":
        st.image(image, caption=img_file.name)
    elif display_option == "Fixed width 300px":
        st.image(image, caption=img_file.name, width=300)
    else:
        st.image(image, caption=img_file.name, width=600)

    # Convert to NumPy and show pixel info
    with st.expander("🔢 Show Pixel Array Info"):
        img_array = np.array(image)
        st.write(f"Array shape : `{img_array.shape}`")
        st.write(f"Data type   : `{img_array.dtype}`")
        st.write(f"Min pixel   : `{img_array.min()}`")
        st.write(f"Max pixel   : `{img_array.max()}`")
        st.write(f"Mean pixel  : `{img_array.mean():.2f}`")

else:
    st.info("👆 Upload an image file to see it displayed")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 3. UPLOAD MULTIPLE FILES
# ────────────────────────────────────────────────────────
st.header("3 — Upload Multiple Images")
st.write("Use accept_multiple_files=True to let the user upload many files at once.")

multi_files = st.file_uploader(
    "Upload multiple images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True   # <-- allows selecting multiple files
)

if multi_files:
    st.success(f"✅ {len(multi_files)} images uploaded")

    # Display all images in a grid using columns
    cols = st.columns(3)   # 3 images per row
    for i, file in enumerate(multi_files):
        img = Image.open(file)
        with cols[i % 3]:   # cycle through columns: 0, 1, 2, 0, 1, 2 ...
            st.image(img, caption=file.name, use_column_width=True)
else:
    st.info("👆 Upload multiple images to display them in a grid")
