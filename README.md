# 🎓 Streamlit Tutorial Series
### A Step-by-Step Guide for Students — From Basics to Image Classification

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 What Is This?

This repository contains a complete **Streamlit tutorial series** designed for students who already know Python basics (NumPy, pandas) but have never used Streamlit before.

The tutorial goes **step by step** — each example builds on the previous one — starting from displaying a simple title all the way to building a full image classification web app connected to Keras models.

---

## 🗂️ Repository Structure

```
📦 streamlit-tutorial/
│
├── 📄 README.md                        ← You are here
├── 📄 requirements.txt                 ← All required packages
│
├── 📁 01_hello_streamlit/
│   └── app.py
│
├── 📁 02_text_markdown/
│   └── app.py
│
├── 📁 03_widgets_basics/
│   └── app.py
│
├── 📁 04_layout/
│   └── app.py
│
├── 📁 05_displaying_data/
│   └── app.py
│
├── 📁 06_charts_plots/
│   └── app.py
│
├── 📁 07_file_upload/
│   └── app.py
│
├── 📁 08_session_state/
│   └── app.py
│
├── 📁 09_forms/
│   └── app.py
│
├── 📁 10_multipage_app/
│   ├── app.py                          ← Main entry point (run this)
│   └── pages/
│       ├── 1_Settings.py
│       ├── 2_Data.py
│       └── 3_Report.py
│
├── 📁 11_image_display/
│   └── app.py
│
└── 📁 12_image_classification_app/
    ├── app.py                          ← Full Keras + Streamlit app
    ├── pages/
    │   ├── 1_Upload_Image.py
    │   ├── 2_Train_Model.py
    │   └── 3_Results.py
    └── models/                         ← Saved Keras models go here
```

---

## 📚 Tutorial Examples

| # | Example | What You Learn |
|---|---------|---------------|
| 01 | **Hello Streamlit** | What Streamlit is, how to run it, `st.title`, `st.write`, `st.header` |
| 02 | **Text & Markdown** | Formatted text, bold, italic, lists, colored text, message boxes |
| 03 | **Widgets Basics** | Button, slider, text input, checkbox, radio, selectbox, number input |
| 04 | **Layout** | Columns, sidebar, expander, container, tabs |
| 05 | **Displaying Data** | DataFrames, tables, metrics, filtering, `st.json` |
| 06 | **Charts & Plots** | Built-in charts, Matplotlib, Seaborn, live charts connected to widgets |
| 07 | **File Upload** | Upload CSV, upload image, multiple files, read into pandas / NumPy |
| 08 | **Session State** | Remember values across reruns, counter, to-do list, multi-step form |
| 09 | **Forms** | Group widgets, submit button, login form, search form, model config |
| 10 | **Multi-Page App** | Pages folder, sidebar navigation, sharing data between pages |
| 11 | **Image Display** | Show images from URL / upload / NumPy, image operations, grid |
| 12 | **Image Classification App** | Full app connecting Keras models with Streamlit |

---

## ⚙️ Requirements

### Python Version
```
Python 3.8 or higher
```

### Required Packages
All packages are listed in `requirements.txt`:

```
streamlit
pandas
numpy
matplotlib
seaborn
Pillow
scikit-learn
tensorflow
opencv-python-headless
```

---

## 🚀 How to Run Locally

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/streamlit-tutorial.git
cd streamlit-tutorial
```

### Step 2 — Install Requirements
```bash
pip install -r requirements.txt
```

### Step 3 — Run Any Example
```bash
# Run a single-file example
streamlit run 01_hello_streamlit/app.py

# Run the multi-page app (Example 10)
streamlit run 10_multipage_app/app.py
```

### Step 4 — Open in Browser
Streamlit opens automatically at:
```
http://localhost:8501
```

---

## ☁️ How to Deploy on Streamlit Cloud

### Step 1 — Push Your Code to GitHub
```bash
git add .
git commit -m "Add Streamlit tutorial"
git push origin main
```

### Step 2 — Go to Streamlit Cloud
Visit [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

### Step 3 — Deploy Your App
1. Click **"New app"**
2. Select your GitHub repository
3. Set the **Main file path** to the app you want to deploy, for example:
   ```
   10_multipage_app/app.py
   ```
4. Click **"Deploy"**

### Step 4 — Wait for Build
Streamlit Cloud will:
- Read your `requirements.txt`
- Install all packages automatically
- Launch your app at a public URL like:
  ```
  https://your-username-streamlit-tutorial-app-xxxx.streamlit.app
  ```

> ⚠️ **Important:** Always make sure `requirements.txt` lists every library you import.
> If you see a `ModuleNotFoundError` on Streamlit Cloud, add the missing package to `requirements.txt` and push again.

---

## 🔑 Key Concepts Quick Reference

### How Streamlit Works
```python
import streamlit as st

# Every widget returns a value
name = st.text_input("Enter your name")

# Use the value immediately
st.write(f"Hello, {name}!")

# The script reruns from top to bottom on every interaction
```

### Session State (remembering values)
```python
# Initialize
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Update
st.session_state.counter += 1

# Read
st.write(st.session_state.counter)
```

### Multi-Page App Structure
```
my_app/
├── app.py           ← run this file
└── pages/
    ├── 1_Page_A.py  ← appears in sidebar automatically
    ├── 2_Page_B.py
    └── 3_Page_C.py
```
> Streamlit detects the `pages/` folder automatically and adds navigation links to the sidebar. You do NOT write navigation code yourself.

### Layout Cheatsheet
```python
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Left")
with col2:
    st.write("Right")

# Sidebar
with st.sidebar:
    st.write("This appears on the left panel")

# Tabs
tab1, tab2 = st.tabs(["Tab A", "Tab B"])
with tab1:
    st.write("Tab A content")

# Expander
with st.expander("Click to expand"):
    st.write("Hidden content")
```

### Display Cheatsheet
```python
st.title("Big Title")
st.header("Header")
st.subheader("Subheader")
st.write("General text or data")
st.markdown("**Bold**, *italic*, `code`")
st.code("x = 1 + 1", language="python")
st.dataframe(df)
st.image(img)
st.pyplot(fig)
st.metric("Label", value, delta)
st.info("Blue box")
st.success("Green box")
st.warning("Yellow box")
st.error("Red box")
```

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` on Streamlit Cloud | Package not in `requirements.txt` | Add it to `requirements.txt` and push |
| Navigation not showing | `pages/` folder in wrong location | Put `pages/` next to `app.py` |
| Session state value lost | Variable not stored in `st.session_state` | Use `st.session_state.key = value` |
| Button only works once | No session state | Store result in `st.session_state` |
| App reruns while typing | Widget outside a form | Wrap inputs in `st.form()` |
| Image not displaying | Wrong file path or missing Pillow | Check path and add `Pillow` to requirements |

---

## 🎯 Learning Path

```
Start here
    │
    ▼
01 Hello Streamlit        ← understand the basics
    │
    ▼
02 Text & Markdown         ← format your output
    │
    ▼
03 Widgets                 ← make it interactive
    │
    ▼
04 Layout                  ← organize the page
    │
    ▼
05 Displaying Data         ← show tables and numbers
    │
    ▼
06 Charts & Plots          ← visualize data
    │
    ▼
07 File Upload             ← accept user files
    │
    ▼
08 Session State           ← remember values
    │
    ▼
09 Forms                   ← group inputs cleanly
    │
    ▼
10 Multi-Page App          ← build a real app
    │
    ▼
11 Image Display           ← work with images
    │
    ▼
12 Image Classification    ← connect to Keras models 🚀
```

---

## 👨‍🏫 For the Instructor

- Each example is **self-contained** — students can run any example independently
- Each example follows the same structure:
  - 🎯 What we need from this example
  - 🤔 Why we need it
  - 🛠️ How we do it
  - 📄 Complete working code
  - ✏️ Student exercise
- Examples increase in complexity gradually
- Example 12 connects everything to the **Keras image classification notebooks**

---

## 📜 License

This project is licensed under the MIT License — feel free to use, modify, and share it for educational purposes.

---

## 🙏 Acknowledgements

- [Streamlit Documentation](https://docs.streamlit.io)
- [TensorFlow / Keras Documentation](https://www.tensorflow.org)
- [scikit-learn Documentation](https://scikit-learn.org)

---

*Built with ❤️ for students learning AI and web development*
