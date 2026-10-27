import streamlit as st

st.set_page_config(
    page_title="My Multi-Page App",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Home Page")
st.write("Welcome to the multi-page app!")
st.info("👈 Use the sidebar to navigate between pages.")

st.markdown("""
### What this app contains:
- **Page 1 — Home:** This page
- **Page 2 — Data Explorer:** Upload and explore a dataset
- **Page 3 — Results:** View model results
""")
