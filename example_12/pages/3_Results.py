import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, f1_score

st.set_page_config(
    page_title = "Results",
    page_icon  = "📊",
    layout     = "wide",
)

with st.sidebar:
    st.title("📊 Results")
    st.markdown("---")
    trained = st.session_state.get("models_trained", False)
    st.write(f"**Models trained:** {'✅ Yes' if trained else '❌ No'}")
    st.markdown("---")
    st.info("Train models first on the **Train Models** page.")

st.title("📊 Results & Model Comparison")
st.write("View confusion matrices, accuracy charts, and a full summary for all trained models.")
st.markdown("---")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("models_trained", False):
    st.warning("⚠️ No results yet.")
    st.info("👈 Go to the **Train Models** page first.")
    st.stop()

# ── Load from session state ───────────────────────────────────────────────────
all_predictions = st.session_state.all_predictions
all_accuracies  = st.session_state.all_accuracies
y_test          = st.session_state.y_test
class_names     = st.session_state.class_names

# ── SECTION 1: Summary Metrics ────────────────────────────────────────────────
st.header("1 — Accuracy Summary")

sorted_models = sorted(all_accuracies.items(), key=lambda x: x[1], reverse=True)
model_names   = [m[0] for m in sorted_models]
accuracies    = [m[1] * 100 for m in sorted_models]

# Metric cards
cols = st.columns(len(sorted_models))
for i, (name, acc) in enumerate(sorted_models):
    with cols[i]:
        st.metric(name, f"{acc*100:.2f}%")

st.markdown("---")

# ── SECTION 2: Accuracy Bar Chart ─────────────────────────────────────────────
st.header("2 — Accuracy Comparison Chart")

fig1, ax1 = plt.subplots(figsize=(12, 5))

bar_colors = ["gold" if name == model_names[0] else "steelblue" for name in model_names]
bars       = ax1.bar(model_names, accuracies, color=bar_colors, edgecolor="white", width=0.5)

for bar, acc in zip(bars, accuracies):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{acc:.2f}%",
        ha="center", fontsize=11, fontweight="bold"
    )

ax1.set_title("Test Accuracy — All Models", fontsize=14)
ax1.set_ylabel("Test Accuracy (%)")
ax1.set_ylim(0, 115)
ax1.tick_params(axis="x", rotation=15)
ax1.grid(axis="y", alpha=0.3)
ax1.set_facecolor("#f9f9f9")
plt.tight_layout()
st.pyplot(fig1)

st.markdown("---")

# ── SECTION 3: Confusion Matrix for each model ────────────────────────────────
st.header("3 — Confusion Matrices")
st.write("Each matrix shows how many images were correctly classified (diagonal) vs misclassified (off-diagonal).")

# Let user choose which model's confusion matrix to view
selected_model = st.selectbox("Select a model to view its confusion matrix", model_names)

y_pred_selected = all_predictions[selected_model]
cm              = confusion_matrix(y_test, y_pred_selected)

col_cm, col_report = st.columns(2)

with col_cm:
    fig2, ax2 = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        cm,
        annot        = True,
        fmt          = "d",
        cmap         = "Blues",
        xticklabels  = class_names,
        yticklabels  = class_names,
        ax           = ax2,
        linewidths   = 0.5,
    )
    ax2.set_title(f"Confusion Matrix — {selected_model}", fontsize=13)
    ax2.set_xlabel("Predicted Label")
    ax2.set_ylabel("True Label")
    plt.tight_layout()
    st.pyplot(fig2)

with col_report:
    st.subheader(f"Classification Report — {selected_model}")
    report = classification_report(
        y_test,
        y_pred_selected,
        target_names = class_names,
        output_dict  = True
    )
    report_df = pd.DataFrame(report).transpose().round(3)
    st.dataframe(report_df, use_container_width=True)

    acc = all_accuracies[selected_model]
    if acc >= 0.85:
        st.success(f"🎉 Excellent accuracy: **{acc*100:.2f}%**")
    elif acc >= 0.70:
        st.info(f"👍 Good accuracy: **{acc*100:.2f}%**")
    elif acc >= 0.50:
        st.warning(f"⚠️ Moderate accuracy: **{acc*100:.2f}%**")
    else:
        st.error(f"❌ Low accuracy: **{acc*100:.2f}%**")

st.markdown("---")

# ── SECTION 4: All Confusion Matrices Grid ────────────────────────────────────
st.header("4 — All Confusion Matrices")

with st.expander("📊 Click to show all confusion matrices at once"):

    num_models = len(all_predictions)
    grid_cols  = st.columns(3)

    for i, (model_name, y_pred) in enumerate(all_predictions.items()):
        cm_i = confusion_matrix(y_test, y_pred)
        with grid_cols[i % 3]:
            fig_i, ax_i = plt.subplots(figsize=(5, 4))
            sns.heatmap(
                cm_i,
                annot       = True,
                fmt         = "d",
                cmap        = "Blues",
                xticklabels = class_names,
                yticklabels = class_names,
                ax          = ax_i,
            )
            ax_i.set_title(f"{model_name}\n({all_accuracies[model_name]*100:.1f}%)", fontsize=11)
            ax_i.set_xlabel("Predicted")
            ax_i.set_ylabel("True")
            plt.tight_layout()
            st.pyplot(fig_i)

st.markdown("---")

# ── SECTION 5: Summary Table ──────────────────────────────────────────────────
st.header("5 — Final Summary Table")

summary_rows = []
for name, y_pred in all_predictions.items():
    acc = all_accuracies[name]
    f1  = f1_score(y_test, y_pred, average="weighted")
    summary_rows.append({
        "Model"             : name,
        "Test Accuracy (%)" : round(acc * 100, 2),
        "Weighted F1 Score" : round(f1, 4),
        "Rank"              : 0,
    })

summary_df = pd.DataFrame(summary_rows)
summary_df = summary_df.sort_values("Test Accuracy (%)", ascending=False)
summary_df["Rank"] = range(1, len(summary_df) + 1)
summary_df = summary_df[["Rank", "Model", "Test Accuracy (%)", "Weighted F1 Score"]]
summary_df = summary_df.reset_index(drop=True)

st.dataframe(summary_df, use_container_width=True, hide_index=True)

best_model = summary_df.iloc[0]["Model"]
best_acc   = summary_df.iloc[0]["Test Accuracy (%)"]
st.success(f"🥇 Best model: **{best_model}** with **{best_acc}%** test accuracy")

st.markdown("---")
st.caption("Page 3 — Results | Example 12")
