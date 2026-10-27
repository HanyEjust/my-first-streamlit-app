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
st.write("This page loads your dataset and trains all 6 classifiers one by one.")
st.markdown("---")

# ── Guard: dataset must be uploaded first ─────────────────────────────────────
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

col1, col2, col3 = st.columns(3)
with col1:
    epochs     = st.slider("Epochs (ANN / CNN)", 5, 50, 20)
with col2:
    batch_size = st.select_slider("Batch Size", options=[16, 32, 64], value=32)
with col3:
    st.metric("Image Size", f"{IMG_SIZE} × {IMG_SIZE} px")

st.markdown("---")

# ── Train Button ──────────────────────────────────────────────────────────────
st.header("3 — Train All Models")

if st.button("🚀 Start Training All Models", type="primary", use_container_width=True):

    # ── LOAD IMAGES ───────────────────────────────────────────────────────────
    st.subheader("Loading images...")
    progress_bar = st.progress(0)

    images, labels = [], []
    total = sum(class_counts.values())
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

    # Flatten for classical ML
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat  = X_test.reshape(X_test.shape[0],  -1)

    # Containers for results
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
        st.success(f"✅ {name} — Test Accuracy: **{acc*100:.2f}%**")

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
    y_pred_ann = np.argmax(ann.predict(X_test, verbose=0), axis=1)

    all_predictions["ANN"]       = y_pred_ann
    all_accuracies["ANN"]        = ann_acc
    trained_model_objects["ANN"] = ann
    st.success(f"✅ ANN — Test Accuracy: **{ann_acc*100:.2f}%**")

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
    y_pred_cnn = np.argmax(cnn.predict(X_test, verbose=0), axis=1)

    all_predictions["CNN"]       = y_pred_cnn
    all_accuracies["CNN"]        = cnn_acc
    trained_model_objects["CNN"] = cnn
    st.success(f"✅ CNN — Test Accuracy: **{cnn_acc*100:.2f}%**")

    # ── MOBILENETV2 ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Pretrained Model — MobileNetV2")

    import cv2
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    with st.spinner("Resizing images to 224×224 for MobileNetV2..."):
        X_train_224 = np.array([
            cv2.resize((img * 255).astype("uint8"), (224, 224))
            for img in X_train
        ], dtype="float32")
        X_val_224 = np.array([
            cv2.resize((img * 255).astype("uint8"), (224, 224))
            for img in X_val
        ], dtype="float32")
        X_test_224 = np.array([
            cv2.resize((img * 255).astype("uint8"), (224, 224))
            for img in X_test
        ], dtype="float32")

        X_train_224 = preprocess_input(X_train_224)
        X_val_224   = preprocess_input(X_val_224)
        X_test_224  = preprocess_input(X_test_224)

    base = MobileNetV2(
        input_shape = (224, 224, 3),
        include_top = False,
        weights     = "imagenet"
    )
    base.trainable = False

    inp  = tf.keras.Input(shape=(224, 224, 3))
    x    = base(inp, training=False)
    x    = tf.keras.layers.GlobalAveragePooling2D()(x)
    x    = tf.keras.layers.Dropout(0.2)(x)
    out  = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    pt   = tf.keras.Model(inp, out, name="MobileNetV2")

    pt.compile(
        optimizer = tf.keras.optimizers.Adam(1e-3),
        loss      = "sparse_categorical_crossentropy",
        metrics   = ["accuracy"]
    )

    with st.spinner("Training MobileNetV2..."):
        pt.fit(
            X_train_224, y_train,
            validation_data = (X_val_224, y_val),
            epochs          = 10,
            batch_size      = batch_size,
            verbose         = 0,
            callbacks       = [tf.keras.callbacks.EarlyStopping(
                patience=3, restore_best_weights=True
            )]
        )

    _, pt_acc  = pt.evaluate(X_test_224, y_test, verbose=0)
    y_pred_pt  = np.argmax(pt.predict(X_test_224, verbose=0), axis=1)

    all_predictions["MobileNetV2"]       = y_pred_pt
    all_accuracies["MobileNetV2"]        = pt_acc
    trained_model_objects["MobileNetV2"] = pt
    st.success(f"✅ MobileNetV2 — Test Accuracy: **{pt_acc*100:.2f}%**")

    # ── SAVE TO SESSION STATE ─────────────────────────────────────────────────
    st.session_state.X_test                = X_test
    st.session_state.y_test                = y_test
    st.session_state.X_test_224            = X_test_224
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
    st.info("👉 Go to **Upload & Predict** to classify a new image, or **Results** to see full charts.")

st.markdown("---")
st.caption("Page 2 — Train Models | Example 12")
