import streamlit as st

st.title("Example 02 — Text & Markdown")

# ── Plain text ──────────────────────────────────────────
st.write("This is plain text using st.write()")

# ── Markdown: formatted text ────────────────────────────
# st.markdown() lets you use standard Markdown syntax
st.markdown("---")   # horizontal line

st.markdown("## This is a Markdown Header")
st.markdown("**This text is bold**")
st.markdown("*This text is italic*")
st.markdown("~~This text is crossed out~~")

# ── Bullet list ─────────────────────────────────────────
st.markdown("""
### Shopping List
- Apples
- Bananas
- Oranges
""")

# ── Numbered list ────────────────────────────────────────
st.markdown("""
### Steps
1. Install Streamlit
2. Create app.py
3. Run streamlit run app.py
""")

# ── Colored text using HTML ──────────────────────────────
# unsafe_allow_html=True lets you write real HTML inside markdown
st.markdown("<h3 style='color: red;'>This text is red</h3>",
            unsafe_allow_html=True)

st.markdown("<p style='color: green; font-size: 20px;'>This text is green and bigger</p>",
            unsafe_allow_html=True)

# ── Inline code and code blocks ──────────────────────────
st.markdown("To install, run `pip install streamlit`")

st.code("""
import streamlit as st
st.title("Hello!")
""", language="python")

# ── Info / Warning / Success / Error boxes ───────────────
st.markdown("---")
st.markdown("### Special Message Boxes")

st.info("ℹ️ This is an info message — use it for tips")
st.success("✅ This is a success message — use it for good news")
st.warning("⚠️ This is a warning message — use it for caution")
st.error("❌ This is an error message — use it for problems")
