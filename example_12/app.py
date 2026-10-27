import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Image Classification App",
    page_icon  = "🧠",
    layout     = "wide",
)

# ── Initialize session state ──────────────────────────────────────────────────
# These variables are shared across all pages

if "dataset_path"   not in st.session_state:
    st.session_state.dataset_path   = "dataset/"

if "img_size"       not in st.session_state:
    st.session_state.img_size       = 64

if "class_names"    not in st.session_state:
    st.session_state.class_names    = []

if "X_test"         not in st.session_state:
    st.session_state.X_test         = None

if "y_test"         not in st.session_state:
    st.session_state.y_test         = None

if "all_predictions" not in st.session_state:
    st.session_state.all_predictions = {}

if "all_accuracies"  not in st.session_state:
    st.session_state.all_accuracies  = {}

if "models_trained"  not in st.session_state:
    st.session_state.models_trained  = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🧠 Image Classifier")
    st.markdown("---")
    st.markdown("### 📌 Pages")
    st.markdown("- 🏠 **Home** — You are here")
    st.markdown("- 🖼️ **Upload & Predict** — Classify one image")
    st.markdown("- 🏋️ **Train Models** — Train all classifiers")
    st.markdown("- 📊 **Results** — Compare all models")
    st.markdown("---")

    # Dataset settings in sidebar — available on all pages
    st.markdown("### ⚙️ Dataset Settings")
    dataset_path = st.text_input(
        "Dataset folder path",
        value = st.session_state.dataset_path,
        help  = "Folder with one subfolder per class"
    )
    img_size = st.select_slider(
        "Image size (px)",
        options = [32, 64, 128],
        value   = st.session_state.img_size,
    )

    if st.button("💾 Save Settings"):
        st.session_state.dataset_path = dataset_path
        st.session_state.img_size     = img_size
        st.session_state.models_trained = False   # reset when settings change
        st.success("Settings saved!")

    st.markdown("---")
    status = "✅ Trained" if st.session_state.models_trained else "❌ Not trained yet"
    st.metric("Models", status)

# ── Home Page ─────────────────────────────────────────────────────────────────
st.title("🧠 Image Classification App")
st.write("A complete machine learning pipeline — from raw images to model comparison.")
st.markdown("---")

# Workflow steps
st.header("📋 How to Use This App")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### Step 1")
    st.markdown("#### ⚙️ Settings")
    st.write("Set your dataset folder path and image size in the **sidebar** on the left.")
    st.info("👈 Use the sidebar")

with col2:
    st.markdown("### Step 2")
    st.markdown("#### 🏋️ Train Models")
    st.write("Go to **Train Models** to load your dataset and train all classifiers.")
    st.info("SVM · KNN · Random Forest · ANN · CNN · MobileNetV2")

with col3:
    st.markdown("### Step 3")
    st.markdown("#### 🖼️ Upload & Predict")
    st.write("Go to **Upload & Predict** to upload a single image and get a prediction from any trained model.")
    st.info("Upload → Choose model → See result")

with col4:
    st.markdown("### Step 4")
    st.markdown("#### 📊 Results")
    st.write("Go to **Results** to see confusion matrices, accuracy charts, and a full comparison table.")
    st.info("Charts · Confusion Matrix · Summary Table")

st.markdown("---")

# What models are included
st.header("🤖 Models Included")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### Classical ML")
    st.markdown("""
    - ✅ Support Vector Machine (SVM)
    - ✅ K-Nearest Neighbours (KNN)
    - ✅ Random Forest
    """)

with col_b:
    st.markdown("#### Neural Networks")
    st.markdown("""
    - ✅ Artificial Neural Network (ANN)
    - ✅ Convolutional Neural Network (CNN)
    """)

with col_c:
    st.markdown("#### Pretrained Models")
    st.markdown("""
    - ✅ MobileNetV2 (ImageNet)
    """)

st.markdown("---")

# Current status
st.header("🔍 Current Status")

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.metric("Dataset Path",   st.session_state.dataset_path)
with s2:
    st.metric("Image Size",     f"{st.session_state.img_size}×{st.session_state.img_size}")
with s3:
    num_classes = len(st.session_state.class_names)
    st.metric("Classes Found",  num_classes if num_classes > 0 else "Not loaded yet")
with s4:
    st.metric("Models Trained", "✅ Yes" if st.session_state.models_trained else "❌ No")

st.markdown("---")
st.caption("Example 12 — Image Classification App | Streamlit Tutorial Series")
