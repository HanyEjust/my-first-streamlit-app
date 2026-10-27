import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(
    page_title = "Upload & Predict",
    page_icon  = "🖼️",
    layout     = "wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🖼️ Upload & Predict")
    st.markdown("---")
    st.write(f"**Classes :** {', '.join(st.session_state.get('class_names', []))}")
    st.write(f"**Img size:** {st.session_state.get('img_size', 64)} px")
    st.write(f"**Models  :** {'✅ Trained' if st.session_state.get('models_trained') else '❌ Not trained'}")
    st.markdown("---")
    st.info("Train models first on the **Train Models** page.")

# ── Page Title ────────────────────────────────────────────────────────────────
st.title("🖼️ Upload an Image & Get a Prediction")
st.write("Upload one image and the trained model will classify it and show confidence scores.")
st.markdown("---")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("models_trained", False):
    st.warning("⚠️ No trained models found.")
    st.info("👈 Please go to the **Train Models** page first.")
    st.stop()

class_names           = st.session_state.class_names
img_size              = st.session_state.img_size
trained_model_objects = st.session_state.trained_model_objects

# ── Step 1: Upload Image ──────────────────────────────────────────────────────
st.header("1 — Upload Your Image")

uploaded_file = st.file_uploader(
    "Choose an image to classify",
    type = ["jpg", "jpeg", "png", "bmp"],
)

if uploaded_file is None:
    st.info("👆 Upload an image to get started.")
    st.stop()

# Open uploaded image
image = Image.open(uploaded_file).convert("RGB")

col_img, col_info = st.columns(2)
with col_img:
    st.image(image, caption="Uploaded Image", width=300)
with col_info:
    st.write(f"**File name     :** {uploaded_file.name}")
    st.write(f"**Original size :** {image.width} × {image.height} px")
    st.write(f"**Resized to    :** {img_size} × {img_size} px for prediction")

st.markdown("---")

# ── Step 2: Preprocess ────────────────────────────────────────────────────────
st.header("2 — Preprocessing")
st.write("The image is resized and normalized exactly the same way as during training.")

# Resize and normalize
image_resized = image.resize((img_size, img_size))
img_array     = np.array(image_resized) / 255.0       # shape: (H, W, 3)
img_flat      = img_array.flatten().reshape(1, -1)     # for classical ML
img_nn        = img_array.reshape(1, img_size, img_size, 3)  # for ANN / CNN

col_prev, col_shapes = st.columns(2)
with col_prev:
    st.image(image_resized, caption=f"After resize: {img_size}×{img_size}", width=150)
with col_shapes:
    st.write(f"**Shape for SVM / KNN / RF :** `{img_flat.shape}`")
    st.write(f"**Shape for ANN / CNN      :** `{img_nn.shape}`")
    st.write(f"**Pixel range              :** 0.0 – 1.0 (normalized)")

st.markdown("---")

# ── Step 3: Choose Model ──────────────────────────────────────────────────────
st.header("3 — Choose a Model & Predict")

model_choice = st.selectbox("Select a trained model", list(trained_model_objects.keys()))

if st.button("🔮 Predict", type="primary", use_container_width=True):

    model = trained_model_objects[model_choice]

    # ── Classical ML: uses flat input, returns class index directly ──────────
    if model_choice in ["SVM", "KNN", "Random Forest"]:

        pred_index = int(model.predict(img_flat)[0])
        pred_label = class_names[pred_index]

        st.markdown("---")
        st.subheader("🎯 Prediction Result")
        st.success(f"**Model      :** {model_choice}")
        st.success(f"**Prediction :** {pred_label}")
        st.info("Classical ML models give one prediction only — no probability scores.")

    # ── Neural Networks: uses (1, H, W, 3) input, returns probabilities ──────
    else:
        if model_choice == "MobileNetV2":
            import cv2
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
            img_224   = cv2.resize(
                (img_array * 255).astype("uint8"), (224, 224)
            )
            img_input = preprocess_input(
                img_224.reshape(1, 224, 224, 3).astype("float32")
            )
        else:
            img_input = img_nn

        probs      = model.predict(img_input, verbose=0)[0]   # probabilities for each class
        pred_index = int(np.argmax(probs))
        pred_label = class_names[pred_index]
        confidence = float(probs[pred_index]) * 100

        st.markdown("---")
        st.subheader("🎯 Prediction Result")

        col_result, col_chart = st.columns(2)

        with col_result:
            # Show result with color depending on confidence
            if confidence >= 70:
                st.success(f"**Predicted class : {pred_label}**")
            elif confidence >= 40:
                st.warning(f"**Predicted class : {pred_label}**")
            else:
                st.error(f"**Predicted class : {pred_label}** (low confidence)")

            st.metric("Confidence", f"{confidence:.1f}%")
            st.write(f"**Model used :** {model_choice}")

            st.markdown("**All class probabilities:**")
            for i, cls in enumerate(class_names):
                pct = float(probs[i]) * 100
                st.write(f"- **{cls}** : {pct:.1f}%")

        with col_chart:
            # Horizontal bar chart of probabilities
            fig, ax = plt.subplots(figsize=(6, 4))

            colors = [
                "green" if i == pred_index else "steelblue"
                for i in range(len(class_names))
            ]
            bars = ax.barh(class_names, probs * 100, color=colors)

            for bar, prob in zip(bars, probs):
                ax.text(
                    bar.get_width() + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{prob*100:.1f}%",
                    va    = "center",
                    fontsize = 10
                )

            ax.set_xlim(0, 115)
            ax.set_xlabel("Confidence (%)")
            ax.set_title(f"Prediction Probabilities — {model_choice}")
            ax.axvline(x=50, color="red", linestyle="--", alpha=0.4, label="50%")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)

st.markdown("---")
st.caption("Page 1 — Upload & Predict | Example 12")
