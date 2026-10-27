import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import importlib
import cv2

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

st.title("🖼️ Upload an Image & Get a Prediction")
st.write("Upload one image and any trained model will classify it with confidence scores.")
st.markdown("---")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("models_trained", False):
    st.warning("⚠️ No trained models found.")
    st.info("👈 Please go to the **Train Models** page first.")
    st.stop()

class_names           = st.session_state.class_names
img_size              = st.session_state.img_size
trained_model_objects = st.session_state.trained_model_objects

# Classical ML and neural network names
CLASSICAL_ML_NAMES = ["SVM", "KNN", "Random Forest"]

# Pretrained model info: maps class name → (module_name, input_size)
PRETRAINED_INFO = {
    "MobileNet"        : ("mobilenet",            224),
    "MobileNetV2"      : ("mobilenet_v2",         224),
    "MobileNetV3Small" : ("mobilenet_v3",         224),
    "MobileNetV3Large" : ("mobilenet_v3",         224),
    "EfficientNetB0"   : ("efficientnet",         224),
    "EfficientNetB1"   : ("efficientnet",         240),
    "EfficientNetB2"   : ("efficientnet",         260),
    "EfficientNetB3"   : ("efficientnet",         300),
    "EfficientNetB4"   : ("efficientnet",         380),
    "EfficientNetB5"   : ("efficientnet",         456),
    "EfficientNetB6"   : ("efficientnet",         528),
    "EfficientNetB7"   : ("efficientnet",         600),
    "EfficientNetV2B0" : ("efficientnet_v2",      224),
    "EfficientNetV2B1" : ("efficientnet_v2",      240),
    "EfficientNetV2B2" : ("efficientnet_v2",      260),
    "EfficientNetV2B3" : ("efficientnet_v2",      300),
    "EfficientNetV2S"  : ("efficientnet_v2",      384),
    "EfficientNetV2M"  : ("efficientnet_v2",      480),
    "EfficientNetV2L"  : ("efficientnet_v2",      480),
    "ResNet50"         : ("resnet",               224),
    "ResNet50V2"       : ("resnet_v2",            224),
    "ResNet101"        : ("resnet",               224),
    "ResNet101V2"      : ("resnet_v2",            224),
    "ResNet152"        : ("resnet",               224),
    "ResNet152V2"      : ("resnet_v2",            224),
    "VGG16"            : ("vgg16",                224),
    "VGG19"            : ("vgg19",                224),
    "InceptionV3"      : ("inception_v3",         299),
    "InceptionResNetV2": ("inception_resnet_v2",  299),
    "Xception"         : ("xception",             299),
    "DenseNet121"      : ("densenet",             224),
    "DenseNet169"      : ("densenet",             224),
    "DenseNet201"      : ("densenet",             224),
    "NASNetMobile"     : ("nasnet",               224),
    "NASNetLarge"      : ("nasnet",               331),
    "ConvNeXtTiny"     : ("convnext",             224),
    "ConvNeXtSmall"    : ("convnext",             224),
    "ConvNeXtBase"     : ("convnext",             224),
    "ConvNeXtLarge"    : ("convnext",             224),
    "ConvNeXtXLarge"   : ("convnext",             224),
}

# ── Step 1: Upload Image ──────────────────────────────────────────────────────
st.header("1 — Upload Your Image")

uploaded_file = st.file_uploader(
    "Choose an image to classify",
    type = ["jpg", "jpeg", "png", "bmp"],
)

if uploaded_file is None:
    st.info("👆 Upload an image to get started.")
    st.stop()

image = Image.open(uploaded_file).convert("RGB")

col_img, col_info = st.columns(2)
with col_img:
    st.image(image, caption="Uploaded Image", width=300)
with col_info:
    st.write(f"**File name     :** {uploaded_file.name}")
    st.write(f"**Original size :** {image.width} × {image.height} px")

st.markdown("---")

# ── Step 2: Choose Model ──────────────────────────────────────────────────────
st.header("2 — Choose a Model & Predict")

model_choice = st.selectbox("Select a trained model", list(trained_model_objects.keys()))

if st.button("🔮 Predict", type="primary", use_container_width=True):

    model = trained_model_objects[model_choice]

    # ── Classical ML ─────────────────────────────────────────────────────────
    if model_choice in CLASSICAL_ML_NAMES:
        image_resized = image.resize((img_size, img_size))
        img_array     = np.array(image_resized) / 255.0
        img_flat      = img_array.flatten().reshape(1, -1)
        pred_index    = int(model.predict(img_flat)[0])
        pred_label    = class_names[pred_index]

        st.markdown("---")
        st.subheader("🎯 Prediction Result")
        st.success(f"**Model      :** {model_choice}")
        st.success(f"**Prediction :** {pred_label}")
        st.info("Classical ML models give one prediction — no probability scores.")

    # ── ANN / CNN ─────────────────────────────────────────────────────────────
    elif model_choice in ["ANN", "CNN"]:
        image_resized = image.resize((img_size, img_size))
        img_array     = np.array(image_resized) / 255.0
        img_input     = img_array.reshape(1, img_size, img_size, 3)
        probs         = model.predict(img_input, verbose=0)[0]
        pred_index    = int(np.argmax(probs))
        pred_label    = class_names[pred_index]
        confidence    = float(probs[pred_index]) * 100

        st.markdown("---")
        st.subheader("🎯 Prediction Result")

        col_result, col_chart = st.columns(2)
        with col_result:
            if confidence >= 70:
                st.success(f"**Predicted: {pred_label}**")
            elif confidence >= 40:
                st.warning(f"**Predicted: {pred_label}**")
            else:
                st.error(f"**Predicted: {pred_label}** (low confidence)")
            st.metric("Confidence", f"{confidence:.1f}%")
            st.write(f"**Model:** {model_choice}")
            st.markdown("**All probabilities:**")
            for i, cls in enumerate(class_names):
                st.write(f"- **{cls}** : {float(probs[i])*100:.1f}%")

        with col_chart:
            fig, ax = plt.subplots(figsize=(6, 4))
            colors  = ["green" if i == pred_index else "steelblue"
                       for i in range(len(class_names))]
            bars    = ax.barh(class_names, probs * 100, color=colors)
            for bar, prob in zip(bars, probs):
                ax.text(bar.get_width() + 0.5,
                        bar.get_y() + bar.get_height() / 2,
                        f"{prob*100:.1f}%", va="center", fontsize=10)
            ax.set_xlim(0, 115)
            ax.set_xlabel("Confidence (%)")
            ax.set_title(f"Prediction — {model_choice}")
            ax.axvline(x=50, color="red", linestyle="--", alpha=0.4)
            plt.tight_layout()
            st.pyplot(fig)

    # ── Any Pretrained Model ──────────────────────────────────────────────────
    else:
        mod_name, pt_size = PRETRAINED_INFO.get(model_choice, ("mobilenet_v2", 224))

        # Load matching preprocess_input for this model
        preprocess_mod = importlib.import_module(
            f"tensorflow.keras.applications.{mod_name}"
        )
        preprocess_fn  = getattr(preprocess_mod, "preprocess_input")

        # Resize and preprocess
        img_resized = cv2.resize(
            np.array(image.resize((pt_size, pt_size))).astype("uint8"),
            (pt_size, pt_size)
        )
        img_input   = preprocess_fn(
            img_resized.reshape(1, pt_size, pt_size, 3).astype("float32")
        )

        probs      = model.predict(img_input, verbose=0)[0]
        pred_index = int(np.argmax(probs))
        pred_label = class_names[pred_index]
        confidence = float(probs[pred_index]) * 100

        st.markdown("---")
        st.subheader("🎯 Prediction Result")

        col_result, col_chart = st.columns(2)
        with col_result:
            if confidence >= 70:
                st.success(f"**Predicted: {pred_label}**")
            elif confidence >= 40:
                st.warning(f"**Predicted: {pred_label}**")
            else:
                st.error(f"**Predicted: {pred_label}** (low confidence)")
            st.metric("Confidence", f"{confidence:.1f}%")
            st.write(f"**Model    :** {model_choice}")
            st.write(f"**Input    :** {pt_size}×{pt_size} px")
            st.markdown("**All probabilities:**")
            for i, cls in enumerate(class_names):
                st.write(f"- **{cls}** : {float(probs[i])*100:.1f}%")

        with col_chart:
            fig, ax = plt.subplots(figsize=(6, 4))
            colors  = ["green" if i == pred_index else "steelblue"
                       for i in range(len(class_names))]
            bars    = ax.barh(class_names, probs * 100, color=colors)
            for bar, prob in zip(bars, probs):
                ax.text(bar.get_width() + 0.5,
                        bar.get_y() + bar.get_height() / 2,
                        f"{prob*100:.1f}%", va="center", fontsize=10)
            ax.set_xlim(0, 115)
            ax.set_xlabel("Confidence (%)")
            ax.set_title(f"Prediction — {model_choice}")
            ax.axvline(x=50, color="red", linestyle="--", alpha=0.4)
            plt.tight_layout()
            st.pyplot(fig)

st.markdown("---")
st.caption("Page 1 — Upload & Predict | Example 12")
