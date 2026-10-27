import streamlit as st
import numpy as np
import os
from PIL import Image

st.set_page_config(
    page_title = "Train Models",
    page_icon  = "🏋️",
    layout     = "wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏋️ Train Models")
    st.markdown("---")
    dataset_ready = st.session_state.get("dataset_path") is not None
    st.write(f"**Dataset :** {'✅ Ready' if dataset_ready else '❌ Not uploaded'}")
    st.write(f"**Classes :** {', '.join(st.session_state.get('class_names', []))}")
    st.write(f"**Img size:** {st.session_state.get('img_size', 64)} px")
    st.markdown("---")
    st.info("Upload your dataset on the **Home** page first.")

# ── Page Title ────────────────────────────────────────────────────────────────
st.title("🏋️ Train All Models")
st.write("Load your dataset and train Classical ML, ANN, CNN, and any pretrained model.")
st.markdown("---")

# ── Guard ─────────────────────────────────────────────────────────────────────
if st.session_state.get("dataset_path") is None:
    st.warning("⚠️ No dataset found.")
    st.info("👈 Please go to the **Home** page and upload your dataset ZIP first.")
    st.stop()

DATASET_PATH = st.session_state.dataset_path
IMG_SIZE     = st.session_state.img_size
class_names  = st.session_state.class_names
num_classes  = len(class_names)

# ── Dataset Summary ───────────────────────────────────────────────────────────
st.header("1 — Dataset Summary")

class_counts = {}
for cls in class_names:
    folder = os.path.join(DATASET_PATH, cls)
    files  = [f for f in os.listdir(folder)
               if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]
    class_counts[cls] = len(files)

total_images = sum(class_counts.values())
st.success(f"✅ {num_classes} classes — {total_images} images total")

cols = st.columns(num_classes)
for i, (cls, cnt) in enumerate(class_counts.items()):
    with cols[i]:
        st.metric(cls, f"{cnt} images")

st.markdown("---")

# ── Training Settings ─────────────────────────────────────────────────────────
st.header("2 — Training Settings")

col1, col2 = st.columns(2)
with col1:
    epochs     = st.slider("Epochs (ANN / CNN)", 5, 50, 20)
with col2:
    batch_size = st.select_slider("Batch Size", options=[16, 32, 64], value=32)

st.markdown("---")

# ── Pretrained Model Selection ────────────────────────────────────────────────
st.header("3 — Select Pretrained Models")
st.write("Choose one or more pretrained models to include in training. All use ImageNet weights.")

# ── Full model catalogue ──────────────────────────────────────────────────────
# Format: display_name : (keras_class_name, preprocess_module, input_size, size_mb, imagenet_top1)
MODEL_CATALOGUE = {
    # ── MobileNet family (small & fast) ──────────────────────────────────────
    "MobileNet          (224px | 16 MB  | 70.4%)" : ("MobileNet",         "mobilenet",            224, 16,   70.4),
    "MobileNetV2        (224px | 14 MB  | 71.3%)" : ("MobileNetV2",       "mobilenet_v2",         224, 14,   71.3),
    "MobileNetV3Small   (224px | 10 MB  | 67.4%)" : ("MobileNetV3Small",  "mobilenet_v3",         224, 10,   67.4),
    "MobileNetV3Large   (224px | 22 MB  | 75.6%)" : ("MobileNetV3Large",  "mobilenet_v3",         224, 22,   75.6),
    # ── EfficientNet family (best accuracy/size tradeoff) ────────────────────
    "EfficientNetB0     (224px | 29 MB  | 77.1%)" : ("EfficientNetB0",    "efficientnet",         224, 29,   77.1),
    "EfficientNetB1     (240px | 31 MB  | 79.1%)" : ("EfficientNetB1",    "efficientnet",         240, 31,   79.1),
    "EfficientNetB2     (260px | 36 MB  | 80.1%)" : ("EfficientNetB2",    "efficientnet",         260, 36,   80.1),
    "EfficientNetB3     (300px | 48 MB  | 81.6%)" : ("EfficientNetB3",    "efficientnet",         300, 48,   81.6),
    "EfficientNetB4     (380px | 75 MB  | 82.9%)" : ("EfficientNetB4",    "efficientnet",         380, 75,   82.9),
    "EfficientNetB5     (456px | 118 MB | 83.6%)" : ("EfficientNetB5",    "efficientnet",         456, 118,  83.6),
    "EfficientNetB6     (528px | 166 MB | 84.0%)" : ("EfficientNetB6",    "efficientnet",         528, 166,  84.0),
    "EfficientNetB7     (600px | 256 MB | 84.3%)" : ("EfficientNetB7",    "efficientnet",         600, 256,  84.3),
    "EfficientNetV2B0   (224px | 29 MB  | 78.7%)" : ("EfficientNetV2B0",  "efficientnet_v2",      224, 29,   78.7),
    "EfficientNetV2B1   (240px | 34 MB  | 79.8%)" : ("EfficientNetV2B1",  "efficientnet_v2",      240, 34,   79.8),
    "EfficientNetV2B2   (260px | 42 MB  | 80.5%)" : ("EfficientNetV2B2",  "efficientnet_v2",      260, 42,   80.5),
    "EfficientNetV2B3   (300px | 59 MB  | 82.0%)" : ("EfficientNetV2B3",  "efficientnet_v2",      300, 59,   82.0),
    "EfficientNetV2S    (384px | 88 MB  | 83.9%)" : ("EfficientNetV2S",   "efficientnet_v2",      384, 88,   83.9),
    "EfficientNetV2M    (480px | 220 MB | 85.3%)" : ("EfficientNetV2M",   "efficientnet_v2",      480, 220,  85.3),
    "EfficientNetV2L    (480px | 479 MB | 86.8%)" : ("EfficientNetV2L",   "efficientnet_v2",      480, 479,  86.8),
    # ── ResNet family ─────────────────────────────────────────────────────────
    "ResNet50           (224px | 98 MB  | 74.9%)" : ("ResNet50",          "resnet",               224, 98,   74.9),
    "ResNet50V2         (224px | 98 MB  | 76.0%)" : ("ResNet50V2",        "resnet_v2",            224, 98,   76.0),
    "ResNet101          (224px | 171 MB | 76.4%)" : ("ResNet101",         "resnet",               224, 171,  76.4),
    "ResNet101V2        (224px | 171 MB | 77.2%)" : ("ResNet101V2",       "resnet_v2",            224, 171,  77.2),
    "ResNet152          (224px | 232 MB | 76.6%)" : ("ResNet152",         "resnet",               224, 232,  76.6),
    "ResNet152V2        (224px | 232 MB | 78.0%)" : ("ResNet152V2",       "resnet_v2",            224, 232,  78.0),
    # ── VGG family ────────────────────────────────────────────────────────────
    "VGG16              (224px | 528 MB | 71.3%)" : ("VGG16",             "vgg16",                224, 528,  71.3),
    "VGG19              (224px | 549 MB | 71.3%)" : ("VGG19",             "vgg19",                224, 549,  71.3),
    # ── Inception family ──────────────────────────────────────────────────────
    "InceptionV3        (299px | 92 MB  | 77.9%)" : ("InceptionV3",       "inception_v3",         299, 92,   77.9),
    "InceptionResNetV2  (299px | 215 MB | 80.3%)" : ("InceptionResNetV2", "inception_resnet_v2",  299, 215,  80.3),
    "Xception           (299px | 88 MB  | 79.0%)" : ("Xception",          "xception",             299, 88,   79.0),
    # ── DenseNet family ───────────────────────────────────────────────────────
    "DenseNet121        (224px | 33 MB  | 75.0%)" : ("DenseNet121",       "densenet",             224, 33,   75.0),
    "DenseNet169        (224px | 57 MB  | 76.2%)" : ("DenseNet169",       "densenet",             224, 57,   76.2),
    "DenseNet201        (224px | 80 MB  | 77.3%)" : ("DenseNet201",       "densenet",             224, 80,   77.3),
    # ── NASNet family ─────────────────────────────────────────────────────────
    "NASNetMobile       (224px | 23 MB  | 74.4%)" : ("NASNetMobile",      "nasnet",               224, 23,   74.4),
    "NASNetLarge        (331px | 343 MB | 82.5%)" : ("NASNetLarge",       "nasnet",               331, 343,  82.5),
    # ── ConvNeXt family (modern, high accuracy) ───────────────────────────────
    "ConvNeXtTiny       (224px | 109 MB | 81.3%)" : ("ConvNeXtTiny",      "convnext",             224, 109,  81.3),
    "ConvNeXtSmall      (224px | 192 MB | 83.1%)" : ("ConvNeXtSmall",     "convnext",             224, 192,  83.1),
    "ConvNeXtBase       (224px | 338 MB | 85.3%)" : ("ConvNeXtBase",      "convnext",             224, 338,  85.3),
    "ConvNeXtLarge      (224px | 755 MB | 86.3%)" : ("ConvNeXtLarge",     "convnext",             224, 755,  86.3),
    "ConvNeXtXLarge     (224px | 1310 MB| 87.0%)" : ("ConvNeXtXLarge",    "convnext",             224, 1310, 87.0),
}

# ── Show the model table for reference ───────────────────────────────────────
with st.expander("📊 Show all available pretrained models"):
    import pandas as pd
    table_rows = []
    for label, (cls, mod, size, mb, acc) in MODEL_CATALOGUE.items():
        family = cls.replace("V2","").replace("V3","")
        family = ''.join([c for c in family if not c.isdigit()])
        table_rows.append({
            "Model"              : cls,
            "Input Size (px)"    : size,
            "Weights Size (MB)"  : mb,
            "ImageNet Top-1 (%)" : acc,
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

# ── Recommended defaults ──────────────────────────────────────────────────────
st.markdown("**💡 Recommended for students:** Start with MobileNetV2 (fast) and EfficientNetB0 (accurate).")

default_selections = [
    "MobileNetV2        (224px | 14 MB  | 71.3%)",
    "EfficientNetB0     (224px | 29 MB  | 77.1%)",
]

selected_pt_labels = st.multiselect(
    "Choose pretrained models to train",
    options  = list(MODEL_CATALOGUE.keys()),
    default  = default_selections,
    help     = "You can select multiple models. Each will be trained and compared."
)

if not selected_pt_labels:
    st.warning("⚠️ No pretrained model selected. At least one is recommended.")

st.markdown("---")

# ── Train Button ──────────────────────────────────────────────────────────────
st.header("4 — Train All Models")

if st.button("🚀 Start Training", type="primary", use_container_width=True):

    # ── LOAD IMAGES ───────────────────────────────────────────────────────────
    st.subheader("Loading images...")
    progress_bar = st.progress(0)
    images, labels = [], []
    total  = sum(class_counts.values())
    loaded = 0

    for class_index, class_name in enumerate(class_names):
        folder = os.path.join(DATASET_PATH, class_name)
        for fname in os.listdir(folder):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                continue
            img = Image.open(os.path.join(folder, fname)).convert("RGB")
            img = img.resize((IMG_SIZE, IMG_SIZE))
            arr = np.array(img) / 255.0
            images.append(arr)
            labels.append(class_index)
            loaded += 1
            progress_bar.progress(loaded / total)

    images = np.array(images)
    labels = np.array(labels)
    st.success(f"✅ Loaded {len(images)} images — shape: {images.shape}")

    # ── SPLIT ─────────────────────────────────────────────────────────────────
    from sklearn.model_selection import train_test_split

    X_temp, X_test, y_temp, y_test = train_test_split(
        images, labels, test_size=0.15, stratify=labels, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.176, stratify=y_temp, random_state=42
    )
    st.write(f"**Train:** {len(X_train)}  |  **Val:** {len(X_val)}  |  **Test:** {len(X_test)}")

    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat  = X_test.reshape(X_test.shape[0],  -1)

    all_predictions       = {}
    all_accuracies        = {}
    trained_model_objects = {}

    from sklearn.metrics import accuracy_score

    # ── CLASSICAL ML ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Classical Machine Learning")

    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier

    for name, clf in [
        ("SVM",           SVC(kernel="rbf", random_state=42)),
        ("KNN",           KNeighborsClassifier(n_neighbors=5)),
        ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42)),
    ]:
        with st.spinner(f"Training {name}..."):
            clf.fit(X_train_flat, y_train)
            y_pred = clf.predict(X_test_flat)
            acc    = accuracy_score(y_test, y_pred)
        all_predictions[name]       = y_pred
        all_accuracies[name]        = acc
        trained_model_objects[name] = clf
        st.success(f"✅ {name} — **{acc*100:.2f}%**")

    # ── ANN ───────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Artificial Neural Network (ANN)")

    import tensorflow as tf

    ann = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ], name="ANN")

    ann.compile(
        optimizer = "adam",
        loss      = "sparse_categorical_crossentropy",
        metrics   = ["accuracy"]
    )

    with st.spinner("Training ANN..."):
        ann.fit(
            X_train, y_train,
            validation_data = (X_val, y_val),
            epochs          = epochs,
            batch_size      = batch_size,
            verbose         = 0,
            callbacks       = [tf.keras.callbacks.EarlyStopping(
                patience=5, restore_best_weights=True
            )]
        )

    _, ann_acc = ann.evaluate(X_test, y_test, verbose=0)
    ann_proba  = ann.predict(X_test, verbose=0)
    y_pred_ann = np.argmax(ann_proba, axis=1)
    all_predictions["ANN"]       = y_pred_ann
    all_accuracies["ANN"]        = ann_acc
    trained_model_objects["ANN"] = ann
    st.success(f"✅ ANN — **{ann_acc*100:.2f}%**")

    # ── CNN ───────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Convolutional Neural Network (CNN)")

    cnn = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal", input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.Conv2D(32,  (3, 3), activation="relu", padding="same"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64,  (3, 3), activation="relu", padding="same"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ], name="CNN")

    cnn.compile(
        optimizer = "adam",
        loss      = "sparse_categorical_crossentropy",
        metrics   = ["accuracy"]
    )

    with st.spinner("Training CNN..."):
        cnn.fit(
            X_train, y_train,
            validation_data = (X_val, y_val),
            epochs          = epochs,
            batch_size      = batch_size,
            verbose         = 0,
            callbacks       = [tf.keras.callbacks.EarlyStopping(
                patience=5, restore_best_weights=True
            )]
        )

    _, cnn_acc = cnn.evaluate(X_test, y_test, verbose=0)
    cnn_proba  = cnn.predict(X_test, verbose=0)
    y_pred_cnn = np.argmax(cnn_proba, axis=1)
    all_predictions["CNN"]       = y_pred_cnn
    all_accuracies["CNN"]        = cnn_acc
    trained_model_objects["CNN"] = cnn
    st.success(f"✅ CNN — **{cnn_acc*100:.2f}%**")

    # ── PRETRAINED MODELS ─────────────────────────────────────────────────────
    if selected_pt_labels:
        st.markdown("---")
        st.subheader("Pretrained Models (Transfer Learning)")

        import cv2
        import importlib

        for label in selected_pt_labels:
            cls_name, mod_name, pt_size, pt_mb, pt_acc_ref = MODEL_CATALOGUE[label]

            st.markdown(f"**Training {cls_name}** (input: {pt_size}×{pt_size}, weights: {pt_mb} MB)")

            # ── Dynamically import the model class and preprocess_input ──────
            keras_apps   = importlib.import_module("tensorflow.keras.applications")
            model_class  = getattr(keras_apps, cls_name)

            preprocess_mod = importlib.import_module(
                f"tensorflow.keras.applications.{mod_name}"
            )
            preprocess_fn  = getattr(preprocess_mod, "preprocess_input")

            # ── Resize images to this model's required input size ─────────────
            with st.spinner(f"Resizing images to {pt_size}×{pt_size}..."):
                X_train_pt = np.array([
                    cv2.resize((img * 255).astype("uint8"), (pt_size, pt_size))
                    for img in X_train
                ], dtype="float32")
                X_val_pt   = np.array([
                    cv2.resize((img * 255).astype("uint8"), (pt_size, pt_size))
                    for img in X_val
                ], dtype="float32")
                X_test_pt  = np.array([
                    cv2.resize((img * 255).astype("uint8"), (pt_size, pt_size))
                    for img in X_test
                ], dtype="float32")

                X_train_pt = preprocess_fn(X_train_pt)
                X_val_pt   = preprocess_fn(X_val_pt)
                X_test_pt  = preprocess_fn(X_test_pt)

            # ── Build model with frozen backbone ─────────────────────────────
            base = model_class(
                input_shape = (pt_size, pt_size, 3),
                include_top = False,
                weights     = "imagenet"
            )
            base.trainable = False

            inp = tf.keras.Input(shape=(pt_size, pt_size, 3))
            x   = base(inp, training=False)
            x   = tf.keras.layers.GlobalAveragePooling2D()(x)
            x   = tf.keras.layers.Dropout(0.2)(x)
            out = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
            pt_model = tf.keras.Model(inp, out, name=cls_name)

            pt_model.compile(
                optimizer = tf.keras.optimizers.Adam(1e-3),
                loss      = "sparse_categorical_crossentropy",
                metrics   = ["accuracy"]
            )

            # ── Train ─────────────────────────────────────────────────────────
            with st.spinner(f"Training {cls_name}..."):
                pt_model.fit(
                    X_train_pt, y_train,
                    validation_data = (X_val_pt, y_val),
                    epochs          = 10,
                    batch_size      = batch_size,
                    verbose         = 0,
                    callbacks       = [tf.keras.callbacks.EarlyStopping(
                        patience=3, restore_best_weights=True
                    )]
                )

            _, pt_acc  = pt_model.evaluate(X_test_pt, y_test, verbose=0)
            pt_proba   = pt_model.predict(X_test_pt, verbose=0)
            y_pred_pt  = np.argmax(pt_proba, axis=1)

            all_predictions[cls_name]       = y_pred_pt
            all_accuracies[cls_name]        = pt_acc
            trained_model_objects[cls_name] = pt_model

            # Save test data for this model (needed for predict page)
            if "pt_test_data" not in st.session_state:
                st.session_state.pt_test_data = {}
            st.session_state.pt_test_data[cls_name] = {
                "X_test_pt"    : X_test_pt,
                "preprocess_fn": preprocess_fn,
                "pt_size"      : pt_size,
            }

            st.success(f"✅ {cls_name} — **{pt_acc*100:.2f}%**")

    # Collect all probability arrays for ROC / PR curves
    all_probabilities = {}
    all_probabilities["ANN"] = ann_proba.tolist()
    all_probabilities["CNN"] = cnn_proba.tolist()

    # ── SAVE TO SESSION STATE ─────────────────────────────────────────────────
    st.session_state.all_probabilities     = all_probabilities
    st.session_state.X_test                = X_test
    st.session_state.y_test                = y_test
    st.session_state.all_predictions       = all_predictions
    st.session_state.all_accuracies        = all_accuracies
    st.session_state.trained_model_objects = trained_model_objects
    st.session_state.models_trained        = True

    # ── FINAL SUMMARY ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🏆 Training Complete — Summary")

    import pandas as pd

    summary = pd.DataFrame([
        {"Model": name, "Test Accuracy (%)": round(acc * 100, 2)}
        for name, acc in sorted(all_accuracies.items(), key=lambda x: x[1], reverse=True)
    ])
    summary.index = range(1, len(summary) + 1)
    st.dataframe(summary, use_container_width=True)

    best_model = max(all_accuracies, key=all_accuracies.get)
    best_acc   = all_accuracies[best_model] * 100
    st.success(f"🥇 Best model: **{best_model}** — **{best_acc:.2f}%** accuracy")
    st.info("👉 Go to **Upload & Predict** or **Results** to explore further.")

st.markdown("---")
st.caption("Page 2 — Train Models | Example 12")
