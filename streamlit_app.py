import streamlit as st

st.set_page_config(page_title="My First Streamlit App", page_icon="🎈")

st.title("🎈 Hello from Streamlit Cloud!")
st.write("This is a simple example app.")

name = st.text_input("What's your name?")
if name:
    st.success(f"Hello, {name}! 👋")

number = st.slider("Pick a number", 0, 100, 50)
st.write(f"You selected: **{number}**")
st.write(f"Squared: **{number ** 2}**")
