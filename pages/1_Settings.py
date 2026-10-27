import streamlit as st

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Settings",
    page_icon  = "⚙️",
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
    st.title("⚙️ Settings Page")
    st.markdown("---")
    st.markdown("Configure your class details here, then click **Save Settings**.")
    st.markdown("---")
    st.markdown("### Current Values")
    st.write(f"**Subject      :** {st.session_state.subject}")
    st.write(f"**Students     :** {st.session_state.num_students}")
    st.write(f"**Passing Score:** {st.session_state.passing_score}")

# ── Page Title ────────────────────────────────────────────────────────────────
st.title("⚙️ Settings")
st.write("Configure your class before generating data. All settings are saved and shared with other pages.")
st.markdown("---")

# ── Settings Form ─────────────────────────────────────────────────────────────
# We use a form so the app only reruns when Save is clicked — not on every change
with st.form("settings_form"):

    st.subheader("📚 Class Configuration")

    col1, col2 = st.columns(2)

    with col1:
        subject = st.selectbox(
            "Subject",
            ["Mathematics", "Science", "English", "Computer Science", "Physics"],
            index=["Mathematics", "Science", "English",
                   "Computer Science", "Physics"].index(st.session_state.subject),
            help="The subject these student scores belong to"
        )

        num_students = st.slider(
            "Number of Students",
            min_value  = 5,
            max_value  = 100,
            value      = st.session_state.num_students,
            step       = 5,
            help       = "How many students to generate scores for"
        )

    with col2:
        passing_score = st.slider(
            "Passing Score Threshold",
            min_value  = 40,
            max_value  = 80,
            value      = st.session_state.passing_score,
            step       = 5,
            help       = "Students scoring at or above this value are considered passing"
        )

        st.markdown("#### Preview")
        st.info(f"""
        - Subject       : **{subject}**
        - Students      : **{num_students}**
        - Passing score : **{passing_score}**
        """)

    st.markdown("---")

    # Submit button
    saved = st.form_submit_button("💾 Save Settings", use_container_width=True)

# ── Handle Save ───────────────────────────────────────────────────────────────
if saved:
    # Store everything in session state so other pages can read it
    st.session_state.subject       = subject
    st.session_state.num_students  = num_students
    st.session_state.passing_score = passing_score

    # Reset data so the Data page generates fresh data with new settings
    st.session_state.dataframe = None

    st.success("✅ Settings saved successfully!")
    st.info("👉 Now go to the **Data** page to generate student scores.")

    # Show what was saved
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Subject",       st.session_state.subject)
    with col_b:
        st.metric("Students",      st.session_state.num_students)
    with col_c:
        st.metric("Passing Score", st.session_state.passing_score)

st.markdown("---")

# ── Explanation for students ──────────────────────────────────────────────────
with st.expander("💡 How does this page share data with other pages?"):
    st.markdown("""
    **Session State** is the key.

    When you click **Save Settings**, we run:
    ```python
    st.session_state.subject       = subject
    st.session_state.num_students  = num_students
    st.session_state.passing_score = passing_score
    ```

    These values live in `st.session_state` — a dictionary that persists across
    all pages of the app. When you navigate to the **Data** or **Report** page,
    they read from the same `st.session_state` and get the values you saved here.
    """)
