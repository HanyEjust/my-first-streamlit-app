import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Report",
    page_icon  = "📈",
    layout     = "wide",
)

# ── Initialize session state (in case user lands here first) ──────────────────
if "subject"       not in st.session_state:
    st.session_state.subject       = "Mathematics"
if "num_students"  not in st.session_state:
    st.session_state.num_students  = 30
if "passing_score" not in st.session_state:
    st.session_state.passing_score = 60
if "dataframe"     not in st.session_state:
    st.session_state.dataframe     = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📈 Report Page")
    st.markdown("---")
    st.markdown("### Active Settings")
    st.write(f"**Subject      :** {st.session_state.subject}")
    st.write(f"**Students     :** {st.session_state.num_students}")
    st.write(f"**Passing Score:** {st.session_state.passing_score}")
    st.markdown("---")
    st.info("Data comes from the **Data** page.")

# ── Page Title ────────────────────────────────────────────────────────────────
st.title("📈 Class Report")
st.write(f"Full analysis of **{st.session_state.subject}** results.")
st.markdown("---")

# ── Guard: check data exists ──────────────────────────────────────────────────
if st.session_state.dataframe is None:
    st.warning("⚠️ No data found. Please generate data first.")
    st.info("👈 Go to the **Data** page and click **Generate Student Scores**.")
    st.stop()   # stop rendering the rest of the page

# ── Load Data ─────────────────────────────────────────────────────────────────
df         = st.session_state.dataframe
subject    = st.session_state.subject
passing    = st.session_state.passing_score
score_col  = f"{subject} Score"

passed_df  = df[df["Status"] == "Pass ✅"]
failed_df  = df[df["Status"] == "Fail ❌"]
pass_rate  = len(passed_df) / len(df) * 100

# ── Summary Metrics ───────────────────────────────────────────────────────────
st.subheader("📌 Key Metrics")

m1, m2, m3, m4, m5, m6 = st.columns(6)
with m1: st.metric("Total Students",  len(df))
with m2: st.metric("Passed",          len(passed_df),  delta=f"+{len(passed_df)}")
with m3: st.metric("Failed",          len(failed_df),  delta=f"-{len(failed_df)}", delta_color="inverse")
with m4: st.metric("Pass Rate",       f"{pass_rate:.1f}%")
with m5: st.metric("Class Average",   f"{df[score_col].mean():.1f}")
with m6: st.metric("Highest Score",   int(df[score_col].max()))

st.markdown("---")

# ── Charts in Tabs ────────────────────────────────────────────────────────────
st.subheader("📊 Charts")

tab1, tab2, tab3 = st.tabs(["📊 Score Distribution", "🥧 Pass / Fail", "🏅 Grade Breakdown"])

# ─────────────────────────────────────────────────────────
# Tab 1: Bar chart of all student scores
# ─────────────────────────────────────────────────────────
with tab1:
    st.write("Each bar is one student. Green = Pass, Red = Fail.")

    fig1, ax1 = plt.subplots(figsize=(14, 5))

    colors = ["green" if s >= passing else "red"
              for s in df[score_col]]

    bars = ax1.bar(df["Student Name"], df[score_col], color=colors, edgecolor="white")

    # Passing score line
    ax1.axhline(
        y     = passing,
        color = "black",
        linestyle = "--",
        linewidth = 1.5,
        label = f"Passing Score ({passing})",
    )

    ax1.set_title(f"{subject} Scores — All Students", fontsize=14)
    ax1.set_xlabel("Student")
    ax1.set_ylabel("Score")
    ax1.set_ylim(0, 110)
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    # Legend patches
    green_patch = mpatches.Patch(color="green", label="Pass")
    red_patch   = mpatches.Patch(color="red",   label="Fail")
    ax1.legend(handles=[green_patch, red_patch,
                        plt.Line2D([0],[0], color="black", linestyle="--",
                                   label=f"Passing Score ({passing})")])

    plt.tight_layout()
    st.pyplot(fig1)

# ─────────────────────────────────────────────────────────
# Tab 2: Pie chart — pass vs fail
# ─────────────────────────────────────────────────────────
with tab2:
    st.write("Proportion of students who passed vs failed.")

    col_pie, col_info = st.columns([1, 1])

    with col_pie:
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        sizes  = [len(passed_df), len(failed_df)]
        labels = [f"Pass ({len(passed_df)})", f"Fail ({len(failed_df)})"]
        colors_pie = ["#2ecc71", "#e74c3c"]
        explode    = (0.05, 0.05)

        ax2.pie(
            sizes,
            labels    = labels,
            colors    = colors_pie,
            explode   = explode,
            autopct   = "%1.1f%%",
            startangle= 90,
            textprops = {"fontsize": 13},
        )
        ax2.set_title(f"Pass / Fail — {subject}", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig2)

    with col_info:
        st.markdown("### Result Summary")
        if pass_rate >= 80:
            st.success(f"🎉 Excellent! **{pass_rate:.1f}%** of students passed.")
        elif pass_rate >= 60:
            st.info(f"👍 Good. **{pass_rate:.1f}%** of students passed.")
        elif pass_rate >= 40:
            st.warning(f"⚠️ Needs improvement. Only **{pass_rate:.1f}%** passed.")
        else:
            st.error(f"❌ Critical. Only **{pass_rate:.1f}%** passed.")

        st.markdown("---")
        st.write(f"**Total students :** {len(df)}")
        st.write(f"**Passed         :** {len(passed_df)}")
        st.write(f"**Failed         :** {len(failed_df)}")
        st.write(f"**Average score  :** {df[score_col].mean():.1f}")
        st.write(f"**Highest score  :** {int(df[score_col].max())}")
        st.write(f"**Lowest score   :** {int(df[score_col].min())}")

# ─────────────────────────────────────────────────────────
# Tab 3: Grade breakdown bar chart
# ─────────────────────────────────────────────────────────
with tab3:
    st.write("Number of students in each grade (A, B, C, D, F).")

    grade_counts = df["Grade"].value_counts().sort_index()

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    grade_colors = {
        "A": "#2ecc71",
        "B": "#3498db",
        "C": "#f39c12",
        "D": "#e67e22",
        "F": "#e74c3c",
    }
    bar_colors = [grade_colors.get(g, "gray") for g in grade_counts.index]

    bars3 = ax3.bar(grade_counts.index, grade_counts.values,
                    color=bar_colors, edgecolor="white", width=0.5)

    # Add count labels on top of bars
    for bar, val in zip(bars3, grade_counts.values):
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            str(int(val)),
            ha="center", fontsize=12, fontweight="bold"
        )

    ax3.set_title(f"Grade Distribution — {subject}", fontsize=14)
    ax3.set_xlabel("Grade")
    ax3.set_ylabel("Number of Students")
    ax3.set_ylim(0, grade_counts.max() + 3)
    ax3.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig3)

    # Grade table
    st.markdown("#### Grade Ranges")
    grade_table = pd.DataFrame({
        "Grade": ["A", "B", "C", "D", "F"],
        "Score Range": ["80 – 100", "70 – 79", "60 – 69", "50 – 59", "0 – 49"],
        "Count": [int(grade_counts.get(g, 0)) for g in ["A","B","C","D","F"]],
    })
    st.table(grade_table)

st.markdown("---")

# ── Full Report Expander ──────────────────────────────────────────────────────
with st.expander("📄 Show Full Student Report Table"):
    st.dataframe(
        df.sort_values(score_col, ascending=False),
        use_container_width = True,
        hide_index          = True,
    )

# ── Written Summary ───────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📝 Written Summary")

st.markdown(f"""
**Subject:** {subject}  
**Total Students:** {len(df)}  
**Passing Score Threshold:** {passing}

Out of **{len(df)}** students, **{len(passed_df)}** passed and **{len(failed_df)}** failed,
giving a pass rate of **{pass_rate:.1f}%**.

The class average was **{df[score_col].mean():.1f}** points.
The highest score was **{int(df[score_col].max())}** and the lowest was **{int(df[score_col].min())}**.

{"The class performed well overall. 🎉" if pass_rate >= 70 else "There is room for improvement. More focus is needed. 📚"}
""")

st.markdown("---")
st.caption("📈 Report Page — Example 10 of the Streamlit Tutorial Series")
