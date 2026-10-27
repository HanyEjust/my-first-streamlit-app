import streamlit as st

st.title("Example 03 — Widgets Basics")
st.markdown("---")

# ────────────────────────────────────────────────────────
# 1. BUTTON
# ────────────────────────────────────────────────────────
st.header("1 — Button")
st.write("A button returns True when clicked, False otherwise.")

# st.button() returns True only at the moment it is clicked
if st.button("Click Me!"):
    st.success("✅ You clicked the button!")
else:
    st.info("👆 Press the button above")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. SLIDER
# ────────────────────────────────────────────────────────
st.header("2 — Slider")
st.write("A slider lets the user pick a number by dragging.")

# st.slider("label", min, max, default_value)
age = st.slider("Select your age", 0, 100, 25)
# The third argument (25) is the starting value

st.write(f"You selected: **{age}** years old")

# Slider with a float (decimal number)
temperature = st.slider("Select temperature (°C)", 0.0, 50.0, 25.0, step=0.5)
st.write(f"Temperature: **{temperature}°C**")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 3. TEXT INPUT
# ────────────────────────────────────────────────────────
st.header("3 — Text Input")
st.write("Lets the user type a short piece of text.")

# st.text_input("label", "default text")
name = st.text_input("Enter your name", "Type here...")

if name and name != "Type here...":
    st.success(f"Hello, **{name}**! 👋")

# Text area: for longer text (multiple lines)
st.write("For longer text, use st.text_area():")
message = st.text_area("Write a short message", height=100)

if message:
    st.info(f"Your message: *{message}*")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 4. CHECKBOX
# ────────────────────────────────────────────────────────
st.header("4 — Checkbox")
st.write("A checkbox returns True when ticked, False when not.")

agree = st.checkbox("I agree to the terms and conditions")

if agree:
    st.success("✅ Thank you for agreeing!")
else:
    st.warning("⚠️ Please tick the checkbox to continue")

# Checkbox to show/hide content
show_secret = st.checkbox("Show secret message")
if show_secret:
    st.info("🔐 The secret is: Streamlit is awesome!")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 5. RADIO BUTTON
# ────────────────────────────────────────────────────────
st.header("5 — Radio Button")
st.write("Radio buttons let the user pick exactly ONE option from a list.")

# st.radio("label", ["option1", "option2", ...])
favourite = st.radio(
    "What is your favourite subject?",
    ["Mathematics", "Computer Science", "Physics", "Biology"]
)

st.write(f"You chose: **{favourite}**")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 6. SELECTBOX (Dropdown)
# ────────────────────────────────────────────────────────
st.header("6 — Selectbox (Dropdown)")
st.write("A dropdown menu — good when there are many options.")

# st.selectbox("label", ["option1", "option2", ...])
city = st.selectbox(
    "Select your city",
    ["Cairo", "Alexandria", "Riyadh", "Dubai", "London", "New York"]
)

st.write(f"You selected: **{city}**")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 7. NUMBER INPUT
# ────────────────────────────────────────────────────────
st.header("7 — Number Input")
st.write("Lets the user type or click arrows to pick a precise number.")

# st.number_input("label", min, max, default)
score = st.number_input("Enter your score", min_value=0, max_value=100, value=50)
st.write(f"Your score: **{score}**")

# ────────────────────────────────────────────────────────
# 8. PUTTING IT ALL TOGETHER — Mini Profile Card
# ────────────────────────────────────────────────────────
st.markdown("---")
st.header("8 — Mini App: Build Your Profile")

name2    = st.text_input("Your name")
age2     = st.slider("Your age", 15, 80, 20)
subject2 = st.selectbox("Your major", ["AI", "Computer Science", "Engineering", "Medicine"])
hobby2   = st.radio("Favourite hobby", ["Reading", "Gaming", "Sports", "Coding"])
student  = st.checkbox("I am a student")

if st.button("Generate Profile Card"):
    st.markdown("---")
    st.subheader("📋 Your Profile Card")
    st.write(f"**Name:**    {name2}")
    st.write(f"**Age:**     {age2}")
    st.write(f"**Major:**   {subject2}")
    st.write(f"**Hobby:**   {hobby2}")
    st.write(f"**Student:** {'Yes ✅' if student else 'No'}")
    st.success("Profile created successfully!")
