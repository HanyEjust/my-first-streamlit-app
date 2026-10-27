import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Example 06 — Charts & Plots")
st.markdown("---")

# ── Sample data ──────────────────────────────────────────
np.random.seed(42)
epochs     = list(range(1, 21))
train_acc  = np.linspace(0.5, 0.95, 20) + np.random.normal(0, 0.02, 20)
val_acc    = np.linspace(0.45, 0.88, 20) + np.random.normal(0, 0.03, 20)
train_loss = np.linspace(1.2, 0.2, 20) + np.random.normal(0, 0.05, 20)
val_loss   = np.linspace(1.3, 0.35, 20) + np.random.normal(0, 0.05, 20)

history_df = pd.DataFrame({
    "Epoch"           : epochs,
    "Train Accuracy"  : train_acc.clip(0, 1),
    "Val Accuracy"    : val_acc.clip(0, 1),
    "Train Loss"      : train_loss.clip(0),
    "Val Loss"        : val_loss.clip(0),
}).set_index("Epoch")

# ────────────────────────────────────────────────────────
# 1. BUILT-IN LINE CHART
# ────────────────────────────────────────────────────────
st.header("1 — Built-in Line Chart")
st.write("One line of code — great for quick plots.")

st.line_chart(history_df[["Train Accuracy", "Val Accuracy"]])

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. BUILT-IN BAR CHART
# ────────────────────────────────────────────────────────
st.header("2 — Built-in Bar Chart")

model_results = pd.DataFrame({
    "Accuracy": [0.72, 0.68, 0.75, 0.83, 0.91]
}, index=["SVM", "KNN", "Random Forest", "CNN", "MobileNetV2"])

st.bar_chart(model_results)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 3. BUILT-IN AREA CHART
# ────────────────────────────────────────────────────────
st.header("3 — Built-in Area Chart")

st.area_chart(history_df[["Train Loss", "Val Loss"]])

st.markdown("---")

# ────────────────────────────────────────────────────────
# 4. MATPLOTLIB FIGURE
# ────────────────────────────────────────────────────────
st.header("4 — Matplotlib Figure")
st.write("Use Matplotlib when you need full control over the chart style.")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left: Accuracy
axes[0].plot(epochs, train_acc, label="Train",      color="blue",  linewidth=2)
axes[0].plot(epochs, val_acc,   label="Validation", color="orange", linewidth=2, linestyle="--")
axes[0].set_title("Model Accuracy")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Accuracy")
axes[0].legend()
axes[0].grid(True)

# Right: Loss
axes[1].plot(epochs, train_loss, label="Train",      color="blue",  linewidth=2)
axes[1].plot(epochs, val_loss,   label="Validation", color="orange", linewidth=2, linestyle="--")
axes[1].set_title("Model Loss")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Loss")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
st.pyplot(fig)   # <-- this is how you show a matplotlib figure in Streamlit

st.markdown("---")

# ────────────────────────────────────────────────────────
# 5. SEABORN FIGURE
# ────────────────────────────────────────────────────────
st.header("5 — Seaborn Figure")
st.write("Seaborn works exactly like Matplotlib — create fig, then st.pyplot(fig).")

scores_df = pd.DataFrame({
    "Model"   : ["SVM", "KNN", "Random Forest", "CNN", "MobileNetV2"],
    "Accuracy": [72, 68, 75, 83, 91],
})

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=scores_df, x="Model", y="Accuracy",
            palette="Blues_d", ax=ax2)
ax2.set_title("Model Accuracy Comparison", fontsize=14)
ax2.set_ylabel("Test Accuracy (%)")
ax2.set_ylim(0, 100)

# Add value labels on bars
for bar, acc in zip(ax2.patches, scores_df["Accuracy"]):
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             f"{acc}%", ha="center", fontsize=11)

plt.tight_layout()
st.pyplot(fig2)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 6. LIVE CHART — Connected to a Widget
# ────────────────────────────────────────────────────────
st.header("6 — Live Chart Connected to Widgets")
st.write("Move the sliders and watch the chart update instantly.")

col1, col2 = st.columns(2)
with col1:
    num_epochs = st.slider("Number of epochs to show", 1, 20, 20)
with col2:
    chart_type = st.radio("Chart type", ["Accuracy", "Loss"])

# Filter data based on slider
filtered = history_df.head(num_epochs)

if chart_type == "Accuracy":
    st.line_chart(filtered[["Train Accuracy", "Val Accuracy"]])
else:
    st.line_chart(filtered[["Train Loss", "Val Loss"]])
