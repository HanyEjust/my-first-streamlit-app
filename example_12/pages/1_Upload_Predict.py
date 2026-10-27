import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(
    page_title = "Upload & Predict",
    page_icon  = "🖼️",
    layout     = "wide",
)

# ── Guard ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🖼️ Upload & Predict")
    st.markdown("---")
    st.write(f"**Dataset :** {st.session_state.get('dataset_path', 'Not set')}")
    st.write(f"**Img size:** {st.session_state.get('img_size', 64)}×{st.session_state.get('img_size', 64)}")
    st.markdown("---")
    st.info("Train models first on the **Train Models** page.")

st.title("🖼️ Upload an Image & Get a Prediction")
st.write("Upload one image and the trained model will classify it.")
st.markdown("---")

# ── Check if models are trained ───────────────────────────────────────────────
if not st.session_state.get("models_trained", False):
    st.warning("⚠️ No trained models found.")
    st.info("👈 Please go to the **Train Models** page first and train the models.")
    st.stop()

# ── Upload Image ──────────────────────────────────────────────────────────────
st.header("1 — Upload Your Image")

uploaded_file = st.file_uploader(
    "Choose an image to classify",
    type = ["jpg", "jpeg", "png", "bmp"],
)

if uploaded_file is None:
    st.info("👆 Upload an image to get a prediction.")
    st.stop()

# Open and display the image
image     = Image.open(uploaded_file).convert("RGB")
img_size  = st.session_state.img_size

col_img, col_info = st.columns(2)
with col_img:
    st.image(image, caption="Uploaded Image", width=300)
with col_info:
    st.write(f"**File name :** {uploaded_file.name}")
    st.write(f"**Original size :** {image.width} × {image.height} px")
    st.write(f"**Will be resized to :** {img_size} × {img_size} px")

st.markdown("---")

# ── Preprocess the image ──────────────────────────────────────────────────────
st.header("2 — Preprocessing")
st.write(f"Resizing to {img_size}×{img_size} and normalizing pixel values to 0–1.")

# Resize and normalize — same steps used during training
image_resized  = image.resize((img_size, img_size))
img_array      = np.array(image_resized) / 255.0          # shape: (img_size, img_size, 3)
img_flat       = img_array.flatten().reshape(1, -1)        # shape: (1, img_size*img_size*3) for classical ML
img_nn         = img_array.reshape(1, img_size, img_size, 3)  # shape: (1, H, W, 3) for ANN/CNN

st.image(image_resized, caption=f"Resized to {img_size}×{img_size}", width=150)
st.write(f"Array shape for classical ML : `{img_flat.shape}`")
st.write(f"Array shape for ANN / CNN    : `{img_nn.shape}`")

st.markdown("---")

# ── Choose Model and Predict ──────────────────────────────────────────────────
st.header("3 — Choose a Model & Predict")

class_names     = st.session_state.class_names
trained_models  = st.session_state.get("trained_model_objects", {})

if not trained_models:
    st.error("No model objects found. Please retrain on the Train Models page.")
    st.stop()

model_choice = st.selectbox("Select a model", list(trained_models.keys()))

if st.button("🔮 Predict", type="primary", use_container_width=True):

    model = trained_models[model_choice]

    # Classical ML models expect flat input
    if model_choice in ["SVM", "KNN", "Random Forest"]:
        pred_index = int(model.predict(img_flat)[0])
        pred_label = class_names[pred_index]

        # These models don't give probabilities easily — show just the prediction
        st.markdown("---")
        st.subheader("🎯 Prediction Result")
        st.success(f"**Model:** {model_choice}  \n**Prediction: {pred_label}**")

    # Neural network models expect (1, H, W, 3) input
    else:
        # For pretrained models, resize to 224×224
        if model_choice == "MobileNetV2":
            import cv2
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
            img_224      = cv2.resize(
                (img_array * 255).astype("uint8"), (224, 224)
            )
            img_input    = preprocess_input(
                img_224.reshape(1, 224, 224, 3).astype("float32")
            )
        else:
            img_input = img_nn

        probs       = model.predict(img_input)[0]   # array of probabilities
        pred_index  = int(np.argmax(probs))
        pred_label  = class_names[pred_index]
        confidence  = float(probs[pred_index]) * 100

        st.markdown("---")
        st.subheader("🎯 Prediction Result")

        # Show top prediction
        col_res, col_chart = st.columns(2)

        with col_res:
            if confidence >= 70:
                st.success(f"**Predicted class : {pred_label}**")
            elif confidence >= 40:
                st.warning(f"**Predicted class : {pred_label}**")
            else:
                st.error(f"**Predicted class : {pred_label}** (low confidence)")

            st.metric("Confidence", f"{confidence:.1f}%")
            st.write(f"**Model used:** {model_choice}")

            # Show all class probabilities
            st.markdown("**All class probabilities:**")
            for i, cls in enumerate(class_names):
                pct = float(probs[i]) * 100
                st.write(f"- {cls}: **{pct:.1f}%**")

        with col_chart:
            # Bar chart of probabilities
            fig, ax = plt.subplots(figsize=(6, 4))
            colors  = ["green" if i == pred_index else "steelblue"
                       for i in range(len(class_names))]
            bars    = ax.barh(class_names, probs * 100, color=colors)

            for bar, prob in zip(bars, probs):
                ax.text(
                    bar.get_width() + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{prob*100:.1f}%",
                    va="center", fontsize=10
                )

            ax.set_xlim(0, 115)
            ax.set_xlabel("Confidence (%)")
            ax.set_title(f"Prediction — {model_choice}")
            ax.axvline(x=50, color="red", linestyle="--", alpha=0.4, label="50% threshold")
            plt.tight_layout()
            st.pyplot(fig)

st.markdown("---")
st.caption("Page 1 — Upload & Predict | Example 12")
