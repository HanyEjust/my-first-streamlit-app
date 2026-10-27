import streamlit as st

# ── Page Configuration ────────────────────────────────────────────────────────
# This must be the FIRST Streamlit command in the file
st.set_page_config(
    page_title = "Student Portal",
    page_icon  = "🎓",
    layout     = "wide",
)

# ── Initialize session state ──────────────────────────────────────────────────
# We set default values here so all pages can read them safely
if "subject"        not in st.session_state:
    st.session_state.subject        = "Mathematics"
if "num_students"   not in st.session_state:
    st.session_state.num_students   = 30
if "passing_score"  not in st.session_state:
    st.session_state.passing_score  = 60
if "dataframe"      not in st.session_state:
    st.session_state.dataframe      = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/110px-Python-logo-notext.svg.png", width=60)
    st.title("🎓 Student Portal")
    st.markdown("---")
    st.markdown("### 📌 Navigation")
    st.markdown("Use the **pages** above to navigate:")
    st.markdown("- 🏠 **Home** — You are here")
    st.markdown("- ⚙️ **Settings** — Configure subject & students")
    st.markdown("- 📊 **Data** — View generated student scores")
    st.markdown("- 📈 **Report** — See results & charts")
    st.markdown("---")
    st.info("💡 Start by going to **Settings** to configure your class.")

# ── Main Page Content ─────────────────────────────────────────────────────────
st.title("🏠 Welcome to the Student Portal")
st.markdown("This is a **multi-page Streamlit app** that demonstrates how to:")
st.markdown("""
- Split an app into multiple pages
- Share data between pages using **session state**
- Build a complete mini workflow: Settings → Data → Report
""")

st.markdown("---")

# ── How to Use ────────────────────────────────────────────────────────────────
st.header("📋 How to Use This App")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Step 1 — ⚙️ Settings")
    st.markdown("""
    Go to the **Settings** page and:
    - Choose a subject
    - Set the number of students
    - Set the passing score threshold
    - Click **Save Settings**
    """)
    st.success("👈 Go to Settings in the sidebar")

with col2:
    st.markdown("### Step 2 — 📊 Data")
    st.markdown("""
    Go to the **Data** page to:
    - Generate random student scores
    - View the full data table
    - See basic statistics
    - Click **Generate Data**
    """)
    st.info("👈 Go to Data in the sidebar")

with col3:
    st.markdown("### Step 3 — 📈 Report")
    st.markdown("""
    Go to the **Report** page to:
    - See pass / fail counts
    - View a bar chart of scores
    - Read a full summary
    """)
    st.warning("👈 Go to Report in the sidebar")

st.markdown("---")

# ── Current Session State Summary ─────────────────────────────────────────────
st.header("🔍 Current App Status")

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.metric("Subject",      st.session_state.subject)
with col_b:
    st.metric("Students",     st.session_state.num_students)
with col_c:
    st.metric("Passing Score", st.session_state.passing_score)
with col_d:
    data_status = "✅ Ready" if st.session_state.dataframe is not None else "❌ Not generated"
    st.metric("Data",         data_status)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit — Example 10 of the Streamlit Tutorial Series")
