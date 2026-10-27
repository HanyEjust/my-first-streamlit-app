import streamlit as st
import pandas as pd
import numpy as np

st.title("Example 05 — Displaying Data")
st.markdown("---")

# ────────────────────────────────────────────────────────
# 1. CREATE SAMPLE DATA
# ────────────────────────────────────────────────────────
st.header("1 — Sample Dataset")

# Create a sample student scores dataframe
np.random.seed(42)
df = pd.DataFrame({
    "Name"      : ["Alice", "Bob", "Carol", "David", "Eve",
                   "Frank", "Grace", "Henry", "Iris", "Jack"],
    "Math"      : np.random.randint(50, 100, 10),
    "Science"   : np.random.randint(50, 100, 10),
    "English"   : np.random.randint(50, 100, 10),
    "Grade"     : np.random.choice(["A", "B", "C"], 10),
    "Passed"    : np.random.choice([True, False], 10),
})

# Add average column
df["Average"] = ((df["Math"] + df["Science"] + df["English"]) / 3).round(1)

st.write("Here is our sample dataset:")
st.write(df)   # st.write() auto-detects a dataframe and displays it nicely

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. st.dataframe() — Interactive Table
# ────────────────────────────────────────────────────────
st.header("2 — Interactive Table: st.dataframe()")
st.write("The user can **sort columns** by clicking the header, and **scroll** through rows.")

st.dataframe(
    df,
    use_container_width=True,   # stretch to full page width
    height=300,                 # set a fixed height with scroll
)

# Highlight the maximum value in each column
st.write("With color highlighting on numeric columns:")
st.dataframe(
    df[["Name", "Math", "Science", "English", "Average"]]
    .style.highlight_max(axis=0, color="lightgreen")
           .highlight_min(axis=0, color="lightsalmon"),
    use_container_width=True,
)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 3. st.table() — Static Table
# ────────────────────────────────────────────────────────
st.header("3 — Static Table: st.table()")
st.write("A clean, fixed table — no scrolling, no sorting. Good for small tables.")

# Show only top 5 rows
st.table(df[["Name", "Math", "Science", "English", "Average"]].head(5))

st.markdown("---")

# ────────────────────────────────────────────────────────
# 4. st.metric() — Single Value Cards
# ────────────────────────────────────────────────────────
st.header("4 — Metric Cards: st.metric()")
st.write("Use metric cards to highlight key numbers at the top of a dashboard.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Students",
        value=len(df),
    )
with col2:
    passed = df["Passed"].sum()
    st.metric(
        label="Passed",
        value=int(passed),
        delta=f"+{int(passed)} this term",   # green because positive
    )
with col3:
    st.metric(
        label="Class Average",
        value=f"{df['Average'].mean():.1f}",
        delta="+2.3 vs last term",
    )
with col4:
    st.metric(
        label="Highest Score",
        value=int(df["Average"].max()),
        delta="-1 vs last term",             # red because negative
    )

st.markdown("---")

# ────────────────────────────────────────────────────────
# 5. FILTERING DATA INTERACTIVELY
# ────────────────────────────────────────────────────────
st.header("5 — Interactive Filtering")
st.write("Combine widgets with dataframes to let users filter data.")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Data")
    grade_filter = st.multiselect(
        "Filter by Grade",
        options=df["Grade"].unique(),
        default=df["Grade"].unique()    # all selected by default
    )
    min_avg = st.slider(
        "Minimum Average Score",
        min_value=50, max_value=100, value=50
    )
    passed_only = st.checkbox("Show passed students only")

# Apply filters
filtered_df = df[df["Grade"].isin(grade_filter)]
filtered_df = filtered_df[filtered_df["Average"] >= min_avg]
if passed_only:
    filtered_df = filtered_df[filtered_df["Passed"] == True]

# Show filtered result
st.write(f"Showing **{len(filtered_df)}** of **{len(df)}** students:")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 6. st.json() — Display Dictionary / JSON
# ────────────────────────────────────────────────────────
st.header("6 — JSON Display: st.json()")
st.write("Useful for showing model configs, API results, or any dictionary.")

model_config = {
    "model_name"  : "CNN",
    "input_size"  : [64, 64, 3],
    "num_classes" : 5,
    "optimizer"   : "adam",
    "learning_rate": 0.001,
    "epochs"      : 30,
    "batch_size"  : 32,
}

st.json(model_config)
