import streamlit as st
import zipfile
import shutil
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Image Classification App",
    page_icon  = "🧠",
    layout     = "wide",
)

# ── Initialize session state ──────────────────────────────────────────────────
if "dataset_path"          not in st.session_state:
    st.session_state.dataset_path          = None

if "img_size"              not in st.session_state:
    st.session_state.img_size              = 64

if "class_names"           not in st.session_state:
    st.session_state.class_names           = []

if "X_test"                not in st.session_state:
    st.session_state.X_test                = None

if "y_test"                not in st.session_state:
    st.session_state.y_test                = None

if "all_predictions"       not in st.session_state:
    st.session_state.all_predictions       = {}

if "all_accuracies"        not in st.session_state:
    st.session_state.all_accuracies        = {}

if "trained_model_objects" not in st.session_state:
    st.session_state.trained_model_objects = {}

if "models_trained"        not in st.session_state:
    st.session_state.models_trained        = False

if "X_test_224"            not in st.session_state:
    st.session_state.X_test_224            = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🧠 Image Classifier")
    st.markdown("---")

    st.markdown("### 📌 Pages")
    st.markdown("- 🏠 **Home** — Upload dataset here")
    st.markdown("- 🏋️ **Train Models** — Train all classifiers")
    st.markdown("- 🖼️ **Upload & Predict** — Classify one image")
    st.markdown("- 📊 **Results** — Compare all models")
    st.markdown("---")

    # ── Step 1: Upload ZIP ────────────────────────────────────────────────────
    st.markdown("### 📦 Step 1 — Upload Dataset ZIP")
    st.caption("ZIP must contain one subfolder per class.")

    uploaded_zip = st.file_uploader(
        "Choose your dataset ZIP",
        type = ["zip"],
        help = "Example: cats_vs_dogs.zip containing cat/ and dog/ folders"
    )

    # ── Step 2: Image size ────────────────────────────────────────────────────
    st.markdown("### 🖼️ Step 2 — Image Size")
    img_size = st.select_slider(
        "Resize images to (px)",
        options = [32, 64, 128],
        value   = st.session_state.img_size,
    )

    # ── Step 3: Extract and Save ──────────────────────────────────────────────
    st.markdown("### 💾 Step 3 — Extract & Save")

    if uploaded_zip is not None:
        if st.button("🚀 Extract Dataset", use_container_width=True, type="primary"):

            # Remove old dataset if it exists
            if os.path.exists("dataset/"):
                shutil.rmtree("dataset/")

            # Extract the uploaded ZIP file
            with zipfile.ZipFile(uploaded_zip, "r") as z:
                z.extractall("dataset/")

            # Find class folders (ignore hidden folders like __MACOSX)
            class_names = sorted([
                d for d in os.listdir("dataset/")
                if os.path.isdir(os.path.join("dataset/", d))
                and not d.startswith(".")
                and not d.startswith("__")
            ])

            # Save everything to session state
            st.session_state.dataset_path   = "dataset/"
            st.session_state.img_size       = img_size
            st.session_state.class_names    = class_names
            st.session_state.models_trained = False  # reset if new dataset

            st.success(f"✅ Done! Found {len(class_names)} classes.")

    else:
        st.info("👆 Upload a ZIP file first.")

    st.markdown("---")

    # ── Current Status ────────────────────────────────────────────────────────
    st.markdown("### 🔍 Status")
    dataset_ready = st.session_state.dataset_path is not None
    st.write(f"**Dataset :** {'✅ Ready' if dataset_ready else '❌ Not uploaded'}")
    st.write(f"**Classes :** {', '.join(st.session_state.class_names) if st.session_state.class_names else 'None'}")
    st.write(f"**Img size:** {st.session_state.img_size} × {st.session_state.img_size} px")
    st.write(f"**Models  :** {'✅ Trained' if st.session_state.models_trained else '❌ Not trained'}")


# ── Main Page ─────────────────────────────────────────────────────────────────
st.title("🧠 Image Classification App")
st.write("A complete machine learning pipeline — upload your dataset, train all models, and compare results.")
st.markdown("---")

# ── How to Prepare the Dataset ────────────────────────────────────────────────
st.header("📋 How to Use This App")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### Step 1")
    st.markdown("#### 📦 Upload Dataset")
    st.write("Pack your images as a ZIP file and upload it using the sidebar on the left.")
    st.success("✅ Done on this page")

with col2:
    st.markdown("### Step 2")
    st.markdown("#### 🏋️ Train Models")
    st.write("Go to **Train Models** to train SVM, KNN, Random Forest, ANN, CNN, and MobileNetV2.")
    st.info("👈 Use the sidebar to navigate")

with col3:
    st.markdown("### Step 3")
    st.markdown("#### 🖼️ Upload & Predict")
    st.write("Upload a single image and get a prediction with confidence scores from any trained model.")
    st.info("👈 Use the sidebar to navigate")

with col4:
    st.markdown("### Step 4")
    st.markdown("#### 📊 Results")
    st.write("See confusion matrices, accuracy bar charts, and a full model comparison table.")
    st.info("👈 Use the sidebar to navigate")

st.markdown("---")

# ── How to Prepare the ZIP ────────────────────────────────────────────────────
st.header("📦 How to Prepare Your Dataset ZIP")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    Your ZIP file must have **one subfolder per class**:

    ```
    my_dataset.zip
    ├── cat/
    │   ├── cat001.jpg
    │   ├── cat002.jpg
    │   └── cat003.jpg
    ├── dog/
    │   ├── dog001.jpg
    │   └── dog002.jpg
    └── bird/
        ├── bird001.jpg
        └── bird002.jpg
    ```
    """)

with col_right:
    st.markdown("""
    **How to create the ZIP:**

    **Windows:**
    1. Put all your class folders in one folder
    2. Select all class folders
    3. Right-click → *Send to* → *Compressed folder*

    **Mac:**
    1. Put all your class folders in one folder
    2. Select all class folders
    3. Right-click → *Compress*

    ⚠️ Make sure the **class folders are at the top level** of the ZIP,
    not inside an extra subfolder.
    """)

st.markdown("---")

# ── Models Included ───────────────────────────────────────────────────────────
st.header("🤖 Models Included")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### 📊 Classical ML")
    st.markdown("- ✅ Support Vector Machine (SVM)")
    st.markdown("- ✅ K-Nearest Neighbours (KNN)")
    st.markdown("- ✅ Random Forest")

with col_b:
    st.markdown("#### 🧠 Neural Networks")
    st.markdown("- ✅ Artificial Neural Network (ANN)")
    st.markdown("- ✅ Convolutional Neural Network (CNN)")

with col_c:
    st.markdown("#### 🚀 Pretrained Models")
    st.markdown("- ✅ MobileNetV2 (ImageNet weights)")

st.markdown("---")
st.caption("Example 12 — Image Classification App | Streamlit Tutorial Series")
