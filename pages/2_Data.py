import streamlit as st
import pandas as pd
import numpy as np

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "Data",
    page_icon  = "📊",
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

# ── Helper: Generate Student Data ─────────────────────────────────────────────
def generate_student_data(subject, num_students, passing_score, seed=42):
    """
    Creates a DataFrame of random student scores.
    The seed makes results reproducible for the same settings.
    """
    np.random.seed(seed)

    # Generate student names
    first_names = [
        "Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace",
        "Henry", "Iris", "Jack", "Karen", "Leo", "Mia", "Noah",
        "Olivia", "Paul", "Quinn", "Rita", "Sam", "Tina", "Uma",
        "Victor", "Wendy", "Xander", "Yara", "Zoe", "Ahmed", "Bella",
        "Carlos", "Diana", "Ethan", "Fatima", "George", "Hana",
        "Ibrahim", "Julia", "Khalid", "Layla", "Marcus", "Nora",
        "Omar", "Petra", "Rami", "Sara", "Tariq", "Ursula",
        "Vlad", "Wafa", "Xavier", "Yasmin", "Ziad", "Amira",
        "Badr", "Celine", "Dalia", "Emad", "Farida", "Ghassan",
        "Heba", "Imad", "Jana", "Kareem", "Lina", "Mohamad",
        "Nadia", "Osama", "Rania", "Sami", "Tamer", "Ula",
        "Walid", "Youssef", "Zeina", "Adam", "Bana", "Cyrus",
        "Dina", "Elias", "Faten", "Gala", "Hamid", "Ines",
        "Jad", "Kira", "Louay", "May", "Nasser", "Ola",
        "Petra", "Rabih", "Suha", "Tarek", "Udai", "Vera",
        "Wiam", "Yahya", "Zainab", "Adel", "Basma", "Chadi",
    ]

    names  = first_names[:num_students]
    scores = np.random.randint(30, 101, size=num_students)

    df = pd.DataFrame({
        "Student Name" : names,
        f"{subject} Score": scores,
        "Status"       : ["Pass ✅" if s >= passing_score else "Fail ❌" for s in scores],
        "Grade"        : pd.cut(
            scores,
            bins   = [0,  49,  59,  69,  79,  100],
            labels = ["F", "D", "C", "B", "A"],
        ),
    })

    return df

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📊 Data Page")
    st.markdown("---")
    st.markdown("### Active Settings")
    st.write(f"**Subject      :** {st.session_state.subject}")
    st.write(f"**Students     :** {st.session_state.num_students}")
    st.write(f"**Passing Score:** {st.session_state.passing_score}")
    st.markdown("---")
    st.info("Change these on the **Settings** page.")

# ── Page Title ────────────────────────────────────────────────────────────────
st.title("📊 Student Data")
st.write(f"Generate and explore **{st.session_state.subject}** scores for **{st.session_state.num_students}** students.")
st.markdown("---")

# ── Settings Summary ──────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Subject",       st.session_state.subject)
with col2:
    st.metric("Students",      st.session_state.num_students)
with col3:
    st.metric("Passing Score", st.session_state.passing_score)

st.markdown("---")

# ── Generate Button ───────────────────────────────────────────────────────────
if st.button("🎲 Generate Student Scores", use_container_width=True, type="primary"):
    df = generate_student_data(
        subject       = st.session_state.subject,
        num_students  = st.session_state.num_students,
        passing_score = st.session_state.passing_score,
    )
    # Save to session state so the Report page can use it
    st.session_state.dataframe = df
    st.success(f"✅ Generated scores for {st.session_state.num_students} students!")

# ── Show Data ─────────────────────────────────────────────────────────────────
if st.session_state.dataframe is not None:
    df = st.session_state.dataframe
    score_col = f"{st.session_state.subject} Score"

    st.markdown("---")

    # ── Quick Stats ───────────────────────────────────────────────────────────
    st.subheader("📌 Quick Statistics")

    passed = (df["Status"] == "Pass ✅").sum()
    failed = (df["Status"] == "Fail ❌").sum()

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Total",   len(df))
    with m2: st.metric("Passed",  int(passed))
    with m3: st.metric("Failed",  int(failed))
    with m4: st.metric("Average", f"{df[score_col].mean():.1f}")
    with m5: st.metric("Highest", int(df[score_col].max()))

    st.markdown("---")

    # ── Tabs for different views ───────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📋 Full Table", "✅ Passed", "❌ Failed"])

    with tab1:
        st.write(f"All **{len(df)}** students:")
        # Color code the Status column
        st.dataframe(
            df,
            use_container_width = True,
            hide_index          = True,
        )

    with tab2:
        passed_df = df[df["Status"] == "Pass ✅"]
        st.write(f"**{len(passed_df)}** students passed:")
        st.dataframe(passed_df, use_container_width=True, hide_index=True)

    with tab3:
        failed_df = df[df["Status"] == "Fail ❌"]
        st.write(f"**{len(failed_df)}** students failed:")
        st.dataframe(failed_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Filter ────────────────────────────────────────────────────────────────
    st.subheader("🔍 Filter Data")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        grade_filter  = st.multiselect(
            "Filter by Grade",
            options = df["Grade"].unique().tolist(),
            default = df["Grade"].unique().tolist(),
        )
    with col_f2:
        status_filter = st.multiselect(
            "Filter by Status",
            options = ["Pass ✅", "Fail ❌"],
            default = ["Pass ✅", "Fail ❌"],
        )

    filtered = df[
        df["Grade"].isin(grade_filter) &
        df["Status"].isin(status_filter)
    ]

    st.write(f"Showing **{len(filtered)}** of **{len(df)}** students:")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.info("👉 Go to the **Report** page to see charts and a full summary.")

else:
    st.warning("⚠️ No data yet. Click **Generate Student Scores** above.")
    st.info("💡 You can also go to the **Settings** page to change the subject or number of students first.")
