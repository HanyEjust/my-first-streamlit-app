import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    f1_score,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    matthews_corrcoef,
    cohen_kappa_score,
    log_loss,
)
from sklearn.preprocessing import label_binarize

st.set_page_config(
    page_title = "Results",
    page_icon  = "📊",
    layout     = "wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📊 Results")
    st.markdown("---")
    st.write(f"**Models :** {'✅ Trained' if st.session_state.get('models_trained') else '❌ Not trained'}")
    st.markdown("---")
    st.markdown("### 📌 Sections")
    st.markdown("1. Accuracy Summary")
    st.markdown("2. Accuracy Bar Chart")
    st.markdown("3. Confusion Matrix")
    st.markdown("4. All Confusion Matrices")
    st.markdown("5. ROC-AUC Curves")
    st.markdown("6. Precision-Recall Curves")
    st.markdown("7. Training Metrics per Class")
    st.markdown("8. Metrics Heatmap")
    st.markdown("9. Error Analysis")
    st.markdown("10. Final Summary Table")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("models_trained", False):
    st.title("📊 Results & Model Comparison")
    st.warning("⚠️ No results yet.")
    st.info("👈 Go to the **Train Models** page first.")
    st.stop()

# ── Load from session state ───────────────────────────────────────────────────
all_predictions = st.session_state.all_predictions
all_accuracies  = st.session_state.all_accuracies
y_test          = st.session_state.y_test
class_names     = st.session_state.class_names
num_classes     = len(class_names)
model_names     = list(all_predictions.keys())

sorted_models   = sorted(all_accuracies.items(), key=lambda x: x[1], reverse=True)
sorted_names    = [m[0] for m in sorted_models]
sorted_accs     = [m[1] * 100 for m in sorted_models]

# ── Binarize labels for multi-class ROC / PR curves ──────────────────────────
y_test_bin = label_binarize(y_test, classes=list(range(num_classes)))

# ── Get probability scores from neural models for ROC/PR ─────────────────────
# Classical ML only has hard predictions — we build fake probabilities from them
def get_proba(model_name):
    """
    Returns (N, num_classes) probability array.
    For classical ML: one-hot from hard prediction.
    For neural networks: real softmax probabilities stored in session state.
    """
    nn_proba = st.session_state.get("all_probabilities", {})
    if model_name in nn_proba:
        return np.array(nn_proba[model_name])
    # Fallback: build one-hot from hard predictions
    y_pred = all_predictions[model_name]
    proba  = np.zeros((len(y_pred), num_classes))
    for i, p in enumerate(y_pred):
        proba[i, p] = 1.0
    return proba

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("📊 Results & Model Comparison")
st.write("Complete evaluation of all trained models.")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Accuracy Summary Cards
# ═════════════════════════════════════════════════════════════════════════════
st.header("1 — Accuracy Summary")

cols = st.columns(len(sorted_models))
for i, (name, acc) in enumerate(sorted_models):
    with cols[i]:
        delta = "🥇 Best" if i == 0 else (f"−{(sorted_models[0][1]-acc)*100:.1f}%" if i > 0 else None)
        st.metric(name, f"{acc*100:.2f}%", delta=delta)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Accuracy Bar Chart
# ═════════════════════════════════════════════════════════════════════════════
st.header("2 — Accuracy Comparison Bar Chart")

fig_acc, ax_acc = plt.subplots(figsize=(12, 5))
bar_colors = ["gold" if i == 0 else "steelblue" for i in range(len(sorted_names))]
bars = ax_acc.bar(sorted_names, sorted_accs, color=bar_colors, edgecolor="white", width=0.5)

for bar, acc in zip(bars, sorted_accs):
    ax_acc.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{acc:.2f}%", ha="center", fontsize=11, fontweight="bold"
    )

ax_acc.set_title("Test Accuracy — All Models", fontsize=14)
ax_acc.set_ylabel("Test Accuracy (%)")
ax_acc.set_ylim(0, 115)
ax_acc.tick_params(axis="x", rotation=15)
ax_acc.grid(axis="y", alpha=0.3)
ax_acc.axhline(y=sum(sorted_accs)/len(sorted_accs), color="red",
               linestyle="--", alpha=0.6, label="Average")
ax_acc.legend()
plt.tight_layout()
st.pyplot(fig_acc)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Confusion Matrix (one model, interactive)
# ═════════════════════════════════════════════════════════════════════════════
st.header("3 — Confusion Matrix")
st.write("Rows = True labels | Columns = Predicted labels | Diagonal = Correct predictions")

selected_model  = st.selectbox("Select a model", sorted_names, key="cm_select")
y_pred_selected = all_predictions[selected_model]
cm              = confusion_matrix(y_test, y_pred_selected)

# Normalised version
cm_norm = cm.astype("float") / cm.sum(axis=1, keepdims=True)

show_norm = st.checkbox("Show normalised confusion matrix (percentages)", value=False)

col_cm, col_report = st.columns(2)

with col_cm:
    fig_cm, ax_cm = plt.subplots(figsize=(7, 6))
    if show_norm:
        sns.heatmap(cm_norm, annot=True, fmt=".2f", cmap="Blues",
                    xticklabels=class_names, yticklabels=class_names,
                    ax=ax_cm, linewidths=0.5)
        ax_cm.set_title(f"Normalised Confusion Matrix — {selected_model}", fontsize=12)
    else:
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=class_names, yticklabels=class_names,
                    ax=ax_cm, linewidths=0.5)
        ax_cm.set_title(f"Confusion Matrix — {selected_model}", fontsize=12)
    ax_cm.set_xlabel("Predicted Label")
    ax_cm.set_ylabel("True Label")
    plt.tight_layout()
    st.pyplot(fig_cm)

with col_report:
    st.subheader("Classification Report")
    report = classification_report(
        y_test, y_pred_selected,
        target_names=class_names, output_dict=True
    )
    report_df = pd.DataFrame(report).transpose().round(3)
    st.dataframe(report_df, use_container_width=True)

    acc = all_accuracies[selected_model]
    if acc >= 0.85:
        st.success(f"🎉 Excellent: **{acc*100:.2f}%**")
    elif acc >= 0.70:
        st.info(f"👍 Good: **{acc*100:.2f}%**")
    elif acc >= 0.50:
        st.warning(f"⚠️ Moderate: **{acc*100:.2f}%**")
    else:
        st.error(f"❌ Low: **{acc*100:.2f}%**")

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — All Confusion Matrices Grid
# ═════════════════════════════════════════════════════════════════════════════
st.header("4 — All Confusion Matrices")

with st.expander("📊 Show all confusion matrices at once"):
    grid_cols = st.columns(3)
    for i, (model_name, y_pred) in enumerate(all_predictions.items()):
        cm_i = confusion_matrix(y_test, y_pred)
        with grid_cols[i % 3]:
            fig_i, ax_i = plt.subplots(figsize=(5, 4))
            sns.heatmap(cm_i, annot=True, fmt="d", cmap="Blues",
                        xticklabels=class_names, yticklabels=class_names, ax=ax_i)
            ax_i.set_title(
                f"{model_name}\n({all_accuracies[model_name]*100:.1f}%)", fontsize=11
            )
            ax_i.set_xlabel("Predicted")
            ax_i.set_ylabel("True")
            plt.tight_layout()
            st.pyplot(fig_i)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — ROC-AUC Curves
# ═════════════════════════════════════════════════════════════════════════════
st.header("5 — ROC-AUC Curves")
st.write("""
**ROC curve** (Receiver Operating Characteristic) plots True Positive Rate vs False Positive Rate.
**AUC** (Area Under the Curve) = 1.0 is perfect. A random classifier scores 0.5 (dashed line).
""")

roc_model = st.selectbox("Select a model for ROC curve", sorted_names, key="roc_select")
y_proba   = get_proba(roc_model)

tab_roc1, tab_roc2 = st.tabs(["Per-Class ROC Curves", "All Models Macro-AUC"])

# ── Per-class ROC for one model ───────────────────────────────────────────────
with tab_roc1:
    fig_roc, ax_roc = plt.subplots(figsize=(9, 6))
    colors_roc = plt.cm.tab10(np.linspace(0, 1, num_classes))

    auc_scores = []
    for i in range(num_classes):
        if num_classes == 2:
            fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
        else:
            fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
        roc_auc = auc(fpr, tpr)
        auc_scores.append(roc_auc)
        ax_roc.plot(fpr, tpr, color=colors_roc[i], linewidth=2,
                    label=f"{class_names[i]} (AUC = {roc_auc:.3f})")

    # Macro-average
    all_fpr  = np.unique(np.concatenate([
        roc_curve(y_test_bin[:, i], y_proba[:, i])[0]
        for i in range(num_classes)
    ]))
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(num_classes):
        fpr_i, tpr_i, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
        mean_tpr += np.interp(all_fpr, fpr_i, tpr_i)
    mean_tpr /= num_classes
    macro_auc = auc(all_fpr, mean_tpr)
    ax_roc.plot(all_fpr, mean_tpr, color="black", linewidth=2.5, linestyle="--",
                label=f"Macro-average (AUC = {macro_auc:.3f})")

    ax_roc.plot([0, 1], [0, 1], color="grey", linestyle=":", linewidth=1.5, label="Random (AUC = 0.5)")
    ax_roc.set_xlim([0, 1])
    ax_roc.set_ylim([0, 1.05])
    ax_roc.set_xlabel("False Positive Rate", fontsize=12)
    ax_roc.set_ylabel("True Positive Rate", fontsize=12)
    ax_roc.set_title(f"ROC Curves — {roc_model}", fontsize=13)
    ax_roc.legend(loc="lower right", fontsize=9)
    ax_roc.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_roc)

    # AUC per class table
    auc_df = pd.DataFrame({
        "Class": class_names,
        "AUC Score": [round(a, 4) for a in auc_scores]
    })
    auc_df["Rating"] = auc_df["AUC Score"].apply(
        lambda x: "🟢 Excellent" if x >= 0.9 else ("🟡 Good" if x >= 0.8 else "🔴 Needs Work")
    )
    st.dataframe(auc_df, use_container_width=True, hide_index=True)

# ── Macro AUC comparison across all models ───────────────────────────────────
with tab_roc2:
    st.write("Macro-average AUC score for each model (one number per model).")

    macro_aucs = {}
    for mname in model_names:
        yp = get_proba(mname)
        all_fpr_m  = np.unique(np.concatenate([
            roc_curve(y_test_bin[:, i], yp[:, i])[0] for i in range(num_classes)
        ]))
        mean_tpr_m = np.zeros_like(all_fpr_m)
        for i in range(num_classes):
            fpr_i, tpr_i, _ = roc_curve(y_test_bin[:, i], yp[:, i])
            mean_tpr_m += np.interp(all_fpr_m, fpr_i, tpr_i)
        mean_tpr_m /= num_classes
        macro_aucs[mname] = round(auc(all_fpr_m, mean_tpr_m), 4)

    # Plot all macro ROC curves together
    fig_roc_all, ax_roc_all = plt.subplots(figsize=(9, 6))
    colors_all = plt.cm.tab10(np.linspace(0, 1, len(model_names)))

    for idx, mname in enumerate(model_names):
        yp = get_proba(mname)
        all_fpr_m  = np.unique(np.concatenate([
            roc_curve(y_test_bin[:, i], yp[:, i])[0] for i in range(num_classes)
        ]))
        mean_tpr_m = np.zeros_like(all_fpr_m)
        for i in range(num_classes):
            fpr_i, tpr_i, _ = roc_curve(y_test_bin[:, i], yp[:, i])
            mean_tpr_m += np.interp(all_fpr_m, fpr_i, tpr_i)
        mean_tpr_m /= num_classes
        m_auc = auc(all_fpr_m, mean_tpr_m)
        ax_roc_all.plot(all_fpr_m, mean_tpr_m, color=colors_all[idx],
                        linewidth=2, label=f"{mname} (AUC={m_auc:.3f})")

    ax_roc_all.plot([0, 1], [0, 1], "k:", linewidth=1.5, label="Random")
    ax_roc_all.set_xlim([0, 1])
    ax_roc_all.set_ylim([0, 1.05])
    ax_roc_all.set_xlabel("False Positive Rate", fontsize=12)
    ax_roc_all.set_ylabel("True Positive Rate", fontsize=12)
    ax_roc_all.set_title("Macro-Average ROC — All Models", fontsize=13)
    ax_roc_all.legend(loc="lower right", fontsize=9)
    ax_roc_all.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_roc_all)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Precision-Recall Curves
# ═════════════════════════════════════════════════════════════════════════════
st.header("6 — Precision-Recall Curves")
st.write("""
**Precision** = of all predicted positives, how many were actually positive?
**Recall** = of all actual positives, how many did we find?
Precision-Recall curves are especially useful for **imbalanced datasets**.
""")

pr_model = st.selectbox("Select a model for PR curve", sorted_names, key="pr_select")
y_proba_pr = get_proba(pr_model)

tab_pr1, tab_pr2 = st.tabs(["Per-Class PR Curves", "All Models AP Comparison"])

# ── Per-class PR for one model ────────────────────────────────────────────────
with tab_pr1:
    fig_pr, ax_pr = plt.subplots(figsize=(9, 6))
    colors_pr = plt.cm.tab10(np.linspace(0, 1, num_classes))
    ap_scores  = []

    for i in range(num_classes):
        precision_i, recall_i, _ = precision_recall_curve(y_test_bin[:, i], y_proba_pr[:, i])
        ap_i = average_precision_score(y_test_bin[:, i], y_proba_pr[:, i])
        ap_scores.append(ap_i)
        ax_pr.plot(recall_i, precision_i, color=colors_pr[i], linewidth=2,
                   label=f"{class_names[i]} (AP = {ap_i:.3f})")

    # Baseline (random classifier)
    baseline = y_test_bin.sum(axis=0) / len(y_test)
    ax_pr.axhline(y=baseline.mean(), color="grey", linestyle=":", linewidth=1.5,
                  label=f"Baseline (random = {baseline.mean():.2f})")

    ax_pr.set_xlim([0, 1])
    ax_pr.set_ylim([0, 1.05])
    ax_pr.set_xlabel("Recall", fontsize=12)
    ax_pr.set_ylabel("Precision", fontsize=12)
    ax_pr.set_title(f"Precision-Recall Curves — {pr_model}", fontsize=13)
    ax_pr.legend(loc="lower left", fontsize=9)
    ax_pr.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_pr)

    ap_df = pd.DataFrame({
        "Class"              : class_names,
        "Average Precision"  : [round(a, 4) for a in ap_scores]
    })
    ap_df["Rating"] = ap_df["Average Precision"].apply(
        lambda x: "🟢 Excellent" if x >= 0.9 else ("🟡 Good" if x >= 0.7 else "🔴 Needs Work")
    )
    st.dataframe(ap_df, use_container_width=True, hide_index=True)

# ── Mean AP comparison across all models ──────────────────────────────────────
with tab_pr2:
    st.write("Mean Average Precision (mAP) for each model.")

    map_scores = {}
    for mname in model_names:
        yp  = get_proba(mname)
        aps = [average_precision_score(y_test_bin[:, i], yp[:, i]) for i in range(num_classes)]
        map_scores[mname] = round(np.mean(aps), 4)

    fig_map, ax_map = plt.subplots(figsize=(10, 4))
    map_names  = sorted(map_scores, key=map_scores.get, reverse=True)
    map_values = [map_scores[m] * 100 for m in map_names]
    bar_colors_map = ["gold" if i == 0 else "steelblue" for i in range(len(map_names))]
    bars_map = ax_map.bar(map_names, map_values, color=bar_colors_map, edgecolor="white")
    for bar, val in zip(bars_map, map_values):
        ax_map.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f"{val:.2f}%", ha="center", fontsize=10, fontweight="bold")
    ax_map.set_title("Mean Average Precision (mAP) — All Models", fontsize=13)
    ax_map.set_ylabel("mAP (%)")
    ax_map.set_ylim(0, 115)
    ax_map.tick_params(axis="x", rotation=15)
    ax_map.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_map)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 7 — Per-Class Metrics Bar Chart
# ═════════════════════════════════════════════════════════════════════════════
st.header("7 — Per-Class Metrics")
st.write("Precision, Recall, and F1-Score for each class for the selected model.")

pc_model   = st.selectbox("Select a model", sorted_names, key="pc_select")
y_pred_pc  = all_predictions[pc_model]

prec_list  = precision_score(y_test, y_pred_pc, average=None, zero_division=0)
rec_list   = recall_score(y_test, y_pred_pc, average=None, zero_division=0)
f1_list    = f1_score(y_test, y_pred_pc, average=None, zero_division=0)

x          = np.arange(len(class_names))
width      = 0.25

fig_pc, ax_pc = plt.subplots(figsize=(10, 5))
ax_pc.bar(x - width, prec_list, width, label="Precision", color="steelblue")
ax_pc.bar(x,         rec_list,  width, label="Recall",    color="orange")
ax_pc.bar(x + width, f1_list,   width, label="F1-Score",  color="green")

ax_pc.set_xticks(x)
ax_pc.set_xticklabels(class_names, rotation=15)
ax_pc.set_ylim(0, 1.15)
ax_pc.set_ylabel("Score")
ax_pc.set_title(f"Per-Class Precision / Recall / F1 — {pc_model}", fontsize=13)
ax_pc.legend()
ax_pc.grid(axis="y", alpha=0.3)

for i in range(len(class_names)):
    ax_pc.text(x[i] - width, prec_list[i] + 0.02, f"{prec_list[i]:.2f}", ha="center", fontsize=8)
    ax_pc.text(x[i],         rec_list[i]  + 0.02, f"{rec_list[i]:.2f}",  ha="center", fontsize=8)
    ax_pc.text(x[i] + width, f1_list[i]   + 0.02, f"{f1_list[i]:.2f}",   ha="center", fontsize=8)

plt.tight_layout()
st.pyplot(fig_pc)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 8 — Metrics Heatmap (all models × all metrics)
# ═════════════════════════════════════════════════════════════════════════════
st.header("8 — Metrics Heatmap")
st.write("One glance comparison of all models across all key metrics.")

rows = []
for mname in model_names:
    yp  = all_predictions[mname]
    ypr = get_proba(mname)

    aps_list  = [average_precision_score(y_test_bin[:, i], ypr[:, i]) for i in range(num_classes)]

    all_fpr_h  = np.unique(np.concatenate([
        roc_curve(y_test_bin[:, i], ypr[:, i])[0] for i in range(num_classes)
    ]))
    mean_tpr_h = np.zeros_like(all_fpr_h)
    for i in range(num_classes):
        fpr_i, tpr_i, _ = roc_curve(y_test_bin[:, i], ypr[:, i])
        mean_tpr_h += np.interp(all_fpr_h, fpr_i, tpr_i)
    mean_tpr_h /= num_classes
    macro_auc_h = auc(all_fpr_h, mean_tpr_h)

    rows.append({
        "Model"      : mname,
        "Accuracy"   : round(accuracy_score(y_test, yp), 4),
        "Precision"  : round(precision_score(y_test, yp, average="weighted", zero_division=0), 4),
        "Recall"     : round(recall_score(y_test, yp, average="weighted", zero_division=0), 4),
        "F1-Score"   : round(f1_score(y_test, yp, average="weighted", zero_division=0), 4),
        "ROC-AUC"    : round(macro_auc_h, 4),
        "mAP"        : round(np.mean(aps_list), 4),
        "Kappa"      : round(cohen_kappa_score(y_test, yp), 4),
        "MCC"        : round(matthews_corrcoef(y_test, yp), 4),
    })

heat_df       = pd.DataFrame(rows).set_index("Model")
heat_numeric  = heat_df.select_dtypes(include="number")

fig_heat, ax_heat = plt.subplots(figsize=(12, max(4, len(model_names) * 0.7 + 2)))
sns.heatmap(
    heat_numeric,
    annot      = True,
    fmt        = ".3f",
    cmap       = "YlGn",
    linewidths = 0.5,
    ax         = ax_heat,
    vmin       = 0,
    vmax       = 1,
)
ax_heat.set_title("All Models × All Metrics Heatmap", fontsize=13)
ax_heat.set_xticklabels(ax_heat.get_xticklabels(), rotation=30, ha="right")
plt.tight_layout()
st.pyplot(fig_heat)

st.dataframe(heat_df.round(4), use_container_width=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 9 — Error Analysis
# ═════════════════════════════════════════════════════════════════════════════
st.header("9 — Error Analysis")
st.write("Where does each model make mistakes? Which classes are most confused with each other?")

err_model  = st.selectbox("Select a model", sorted_names, key="err_select")
y_pred_err = all_predictions[err_model]

tab_e1, tab_e2, tab_e3 = st.tabs([
    "Misclassification Rate per Class",
    "Most Confused Class Pairs",
    "Prediction Distribution",
])

# ── Misclassification rate per class ─────────────────────────────────────────
with tab_e1:
    cm_err     = confusion_matrix(y_test, y_pred_err)
    total_true = cm_err.sum(axis=1)
    correct    = np.diag(cm_err)
    error_rate = (total_true - correct) / total_true * 100

    fig_err, ax_err = plt.subplots(figsize=(8, 4))
    colors_err = ["red" if e > 30 else ("orange" if e > 10 else "green") for e in error_rate]
    bars_err   = ax_err.bar(class_names, error_rate, color=colors_err, edgecolor="white")

    for bar, rate in zip(bars_err, error_rate):
        ax_err.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.5,
                    f"{rate:.1f}%", ha="center", fontsize=11)

    ax_err.set_title(f"Misclassification Rate per Class — {err_model}", fontsize=12)
    ax_err.set_ylabel("Error Rate (%)")
    ax_err.set_ylim(0, max(error_rate) * 1.25 + 5)
    ax_err.grid(axis="y", alpha=0.3)

    green_p = mpatches.Patch(color="green",  label="≤ 10% error")
    orange_p= mpatches.Patch(color="orange", label="10–30% error")
    red_p   = mpatches.Patch(color="red",    label="> 30% error")
    ax_err.legend(handles=[green_p, orange_p, red_p])
    plt.tight_layout()
    st.pyplot(fig_err)

# ── Most confused class pairs ─────────────────────────────────────────────────
with tab_e2:
    cm_e2 = confusion_matrix(y_test, y_pred_err)
    pairs = []
    for i in range(num_classes):
        for j in range(num_classes):
            if i != j and cm_e2[i, j] > 0:
                pairs.append({
                    "True Class"      : class_names[i],
                    "Predicted As"    : class_names[j],
                    "Count"           : int(cm_e2[i, j]),
                    "% of True Class" : round(cm_e2[i, j] / cm_e2[i].sum() * 100, 1),
                })

    if pairs:
        pairs_df = pd.DataFrame(pairs).sort_values("Count", ascending=False)
        pairs_df.index = range(1, len(pairs_df) + 1)
        st.dataframe(pairs_df, use_container_width=True)

        # Bar chart of top confused pairs
        top_pairs = pairs_df.head(10)
        labels_p  = [f"{r['True Class']} → {r['Predicted As']}" for _, r in top_pairs.iterrows()]
        counts_p  = top_pairs["Count"].tolist()

        fig_pairs, ax_pairs = plt.subplots(figsize=(9, 4))
        ax_pairs.barh(labels_p[::-1], counts_p[::-1], color="salmon", edgecolor="white")
        ax_pairs.set_xlabel("Number of Misclassifications")
        ax_pairs.set_title(f"Top Confused Class Pairs — {err_model}", fontsize=12)
        ax_pairs.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig_pairs)
    else:
        st.success("🎉 No misclassifications found!")

# ── Prediction Distribution ───────────────────────────────────────────────────
with tab_e3:
    st.write("How many images did the model predict for each class vs actual count?")

    actual_counts    = [np.sum(y_test == i) for i in range(num_classes)]
    predicted_counts = [np.sum(y_pred_err == i) for i in range(num_classes)]

    x_dist = np.arange(num_classes)
    w_dist = 0.35

    fig_dist, ax_dist = plt.subplots(figsize=(9, 4))
    ax_dist.bar(x_dist - w_dist/2, actual_counts,    w_dist, label="Actual",    color="steelblue")
    ax_dist.bar(x_dist + w_dist/2, predicted_counts, w_dist, label="Predicted", color="orange")
    ax_dist.set_xticks(x_dist)
    ax_dist.set_xticklabels(class_names, rotation=15)
    ax_dist.set_ylabel("Number of Images")
    ax_dist.set_title(f"Actual vs Predicted Distribution — {err_model}", fontsize=12)
    ax_dist.legend()
    ax_dist.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_dist)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 10 — Final Summary Table
# ═════════════════════════════════════════════════════════════════════════════
st.header("10 — Final Summary Table")

summary_rows = []
for mname in model_names:
    yp  = all_predictions[mname]
    ypr = get_proba(mname)

    aps_s = [average_precision_score(y_test_bin[:, i], ypr[:, i]) for i in range(num_classes)]
    all_fpr_s  = np.unique(np.concatenate([
        roc_curve(y_test_bin[:, i], ypr[:, i])[0] for i in range(num_classes)
    ]))
    mean_tpr_s = np.zeros_like(all_fpr_s)
    for i in range(num_classes):
        fpr_i, tpr_i, _ = roc_curve(y_test_bin[:, i], ypr[:, i])
        mean_tpr_s += np.interp(all_fpr_s, fpr_i, tpr_i)
    mean_tpr_s /= num_classes

    summary_rows.append({
        "Model"            : mname,
        "Accuracy (%)"     : round(accuracy_score(y_test, yp) * 100, 2),
        "Weighted F1"      : round(f1_score(y_test, yp, average="weighted", zero_division=0), 4),
        "ROC-AUC (Macro)"  : round(auc(all_fpr_s, mean_tpr_s), 4),
        "mAP"              : round(np.mean(aps_s), 4),
        "Cohen Kappa"      : round(cohen_kappa_score(y_test, yp), 4),
        "MCC"              : round(matthews_corrcoef(y_test, yp), 4),
    })

summary_df = pd.DataFrame(summary_rows)
summary_df = summary_df.sort_values("Accuracy (%)", ascending=False)
summary_df.insert(0, "Rank", range(1, len(summary_df) + 1))
summary_df = summary_df.reset_index(drop=True)

st.dataframe(summary_df, use_container_width=True, hide_index=True)

best_model = summary_df.iloc[0]["Model"]
best_acc   = summary_df.iloc[0]["Accuracy (%)"]
best_auc   = summary_df.iloc[0]["ROC-AUC (Macro)"]
st.success(f"🥇 Best model: **{best_model}** — Accuracy: **{best_acc}%** | ROC-AUC: **{best_auc}**")

with st.expander("📖 Metric Definitions"):
    st.markdown("""
    | Metric | What it measures |
    |--------|-----------------|
    | **Accuracy** | % of correctly classified images |
    | **Weighted F1** | Harmonic mean of Precision & Recall, weighted by class size |
    | **ROC-AUC** | Area under the ROC curve — 1.0 = perfect, 0.5 = random |
    | **mAP** | Mean Average Precision — summary of Precision-Recall curve |
    | **Cohen Kappa** | Agreement between predictions and true labels (1.0 = perfect, 0 = random) |
    | **MCC** | Matthews Correlation Coefficient — balanced metric even for imbalanced classes |
    """)

st.markdown("---")
st.caption("Page 3 — Results | Example 12")
