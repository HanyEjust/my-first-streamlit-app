import streamlit as st

st.title("Example 08 — Session State")
st.markdown("---")

# ────────────────────────────────────────────────────────
# 1. THE PROBLEM — without session state
# ────────────────────────────────────────────────────────
st.header("1 — The Problem (Without Session State)")
st.write("Every time you click the button, the count resets to 0 ❌")

count_broken = 0   # this resets every time the script reruns!

if st.button("Click to count (broken)"):
    count_broken += 1

st.write(f"Count: {count_broken}")   # always shows 0 or 1

st.markdown("---")

# ────────────────────────────────────────────────────────
# 2. THE SOLUTION — with session state
# ────────────────────────────────────────────────────────
st.header("2 — The Solution (With Session State)")
st.write("Session state remembers the value across reruns ✅")

# Step 1: Initialize the value if it doesn't exist yet
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Step 2: Buttons to change the value
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ Increment"):
        st.session_state.counter += 1
with col2:
    if st.button("➖ Decrement"):
        st.session_state.counter -= 1
with col3:
    if st.button("🔄 Reset"):
        st.session_state.counter = 0

# Step 3: Display the current value
st.metric("Current Count", st.session_state.counter)

st.markdown("---")

# ────────────────────────────────────────────────────────
# 3. TO-DO LIST — real use of session state
# ────────────────────────────────────────────────────────
st.header("3 — To-Do List App")
st.write("Session state keeps the list even after you add new items.")

# Initialize the list
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# Add a new item
new_task = st.text_input("Enter a new task")
if st.button("➕ Add Task"):
    if new_task.strip():   # only add if not empty
        st.session_state.todo_list.append(new_task.strip())
        st.success(f"Added: {new_task}")

# Show the list
if st.session_state.todo_list:
    st.subheader(f"Tasks ({len(st.session_state.todo_list)})")
    for i, task in enumerate(st.session_state.todo_list):
        col_task, col_del = st.columns([5, 1])
        with col_task:
            st.write(f"{i+1}. {task}")
        with col_del:
            if st.button("🗑️", key=f"del_{i}"):  # key must be unique!
                st.session_state.todo_list.pop(i)
                st.rerun()   # rerun immediately to refresh the list

    if st.button("🗑️ Clear All Tasks"):
        st.session_state.todo_list = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above!")

st.markdown("---")

# ────────────────────────────────────────────────────────
# 4. MULTI-STEP FORM — page-by-page wizard
# ────────────────────────────────────────────────────────
st.header("4 — Multi-Step Form (Wizard)")
st.write("Session state lets you build a step-by-step form.")

# Initialize step
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Progress indicator
st.progress(st.session_state.step / 3)
st.write(f"Step {st.session_state.step} of 3")

# Step 1: Personal Info
if st.session_state.step == 1:
    st.subheader("Step 1 — Personal Information")
    name = st.text_input("Full Name")
    age  = st.number_input("Age", 15, 80, 20)

    if st.button("Next ➡️"):
        if name.strip():
            st.session_state.user_data["name"] = name
            st.session_state.user_data["age"]  = age
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Please enter your name.")

# Step 2: Academic Info
elif st.session_state.step == 2:
    st.subheader("Step 2 — Academic Information")
    major  = st.selectbox("Major", ["AI", "CS", "Engineering", "Medicine"])
    year   = st.radio("Year", ["1st", "2nd", "3rd", "4th"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next ➡️"):
            st.session_state.user_data["major"] = major
            st.session_state.user_data["year"]  = year
            st.session_state.step = 3
            st.rerun()

# Step 3: Summary
elif st.session_state.step == 3:
    st.subheader("Step 3 — Confirm Your Information")
    data = st.session_state.user_data
    st.write(f"**Name  :** {data.get('name')}")
    st.write(f"**Age   :** {data.get('age')}")
    st.write(f"**Major :** {data.get('major')}")
    st.write(f"**Year  :** {data.get('year')}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("✅ Submit"):
            st.success("🎉 Registration complete!")
            st.balloons()
            st.session_state.step = 1
            st.session_state.user_data = {}
