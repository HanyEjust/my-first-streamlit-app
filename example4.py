import streamlit as st

st.title("Example 04 — Layout")
st.write("This example shows how to organize your app professionally.")
st.markdown("---")

# ────────────────────────────────────────────────────────
# 1. COLUMNS — side by side content
# ────────────────────────────────────────────────────────
st.header("1 — Columns")
st.write("Use columns to place content side by side.")

# Create 2 equal columns
col1, col2 = st.columns(2)

# Put content inside each column using 'with'
with col1:
    st.subheader("Left Column")
    st.write("This is the left side.")
    st.success("✅ Column 1")

with col2:
    st.subheader("Right Column")
    st.write("This is the right side.")
    st.info("ℹ️ Column 2")

st.markdown("---")

# 3 columns with different widths
# The numbers are relative sizes: 1, 2, 1 means middle is twice as wide
st.write("Three columns with different widths [1, 2, 1]:")
col_a, col_b, col_c = st.columns([1, 2, 1])

with col_a:
    st.metric(label="Students", value="120")
    # st.metric shows a number with a label — great for dashboards

with col_b:
    st.metric(label="Average Score", value="87.5", delta="+ 3.2")
    # delta shows a change (green if positive, red if negative)

with col_c:
    st.metric(label="Pass Rate", value="94%", delta="-1%")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. SIDEBAR — controls panel on the left
# ────────────────────────────────────────────────────────
st.header("2 — Sidebar")
st.write("The sidebar keeps controls separate from the main content.")

# Everything inside 'with st.sidebar:' appears on the left panel
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Move controls here to keep the main page clean.")

    # Any widget works inside the sidebar
    student_name = st.text_input("Your name")
    grade        = st.selectbox("Your grade", ["Grade 1", "Grade 2", "Grade 3"])
    dark_mode    = st.checkbox("Dark mode (visual only)")

    st.markdown("---")
    st.info("All controls are in the sidebar!")

# Use the sidebar values in the main page
if student_name:
    st.success(f"Welcome, **{student_name}** from **{grade}**! 👋")
else:
    st.warning("👈 Enter your name in the sidebar")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 3. EXPANDER — collapsible sections
# ────────────────────────────────────────────────────────
st.header("3 — Expander")
st.write("Use expanders to hide details until the user wants to see them.")

with st.expander("📖 Click to see the explanation"):
    st.write("""
    An expander is like a drawer that opens and closes.
    Use it for:
    - Extra details that not everyone needs
    - Help text or instructions
    - Raw data or debug information
    """)
    st.code("st.expander('label')", language="python")

with st.expander("📊 Click to see sample data"):
    import pandas as pd
    data = pd.DataFrame({
        "Name" : ["Alice", "Bob", "Carol"],
        "Score": [90, 85, 92]
    })
    st.dataframe(data)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 4. CONTAINER — group elements together
# ────────────────────────────────────────────────────────
st.header("4 — Container")
st.write("A container groups elements and lets you control their order.")

# Create a container
box = st.container()

# You can write to the container out of order!
st.write("👆 This line appears AFTER the container in the code...")

with box:
    st.info("...but this container appears BEFORE it on the page!")
    st.write("Containers are useful for reserving a spot on the page.")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 5. TABS — organize into clickable tabs
# ────────────────────────────────────────────────────────
st.header("5 — Tabs")
st.write("Tabs let you organize content into separate clickable sections.")

tab1, tab2, tab3 = st.tabs(["📋 About", "📊 Data", "⚙️ Settings"])

with tab1:
    st.subheader("About This App")
    st.write("This is the About tab. Use tabs to separate different views.")
    st.success("You are on the About tab!")

with tab2:
    st.subheader("Data Tab")
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(
        np.random.randint(0, 100, size=(5, 3)),
        columns=["Math", "Science", "English"]
    )
    st.dataframe(df)
    st.write("Random student scores table.")

with tab3:
    st.subheader("Settings Tab")
    font_size = st.slider("Font size", 10, 30, 16)
    show_grid = st.checkbox("Show grid lines")
    st.write(f"Font size selected: **{font_size}**")
    st.write(f"Grid lines: **{'On' if show_grid else 'Off'}**")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 6. PUTTING IT ALL TOGETHER — Dashboard Layout
# ────────────────────────────────────────────────────────
st.header("6 — Mini Dashboard")

# Sidebar controls
with st.sidebar:
    st.markdown("---")
    st.header("📊 Dashboard Controls")
    num_students = st.slider("Number of students", 10, 100, 30)
    subject      = st.selectbox("Subject", ["Math", "Science", "English"])

# Main area: metrics in columns
st.subheader(f"📈 {subject} Results for {num_students} Students")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total",   num_students)
with m2:
    st.metric("Passed",  int(num_students * 0.85), delta="+5")
with m3:
    st.metric("Failed",  int(num_students * 0.15), delta="-5")
with m4:
    st.metric("Average", "78.4%")

# Tabs for details
t1, t2 = st.tabs(["📋 Summary", "ℹ️ Info"])
with t1:
    st.write(f"Showing results for **{subject}** with **{num_students}** students.")
    with st.expander("See full breakdown"):
        st.write("- Top score: 98")
        st.write("- Lowest score: 42")
        st.write("- Median: 76")
with t2:
    st.info("This dashboard updates automatically when you change the sidebar settings.")
