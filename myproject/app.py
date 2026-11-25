import os

import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Page setup ----------
st.set_page_config(page_title="Carl Vincent O. Pilongo", page_icon="👤")

# ---------- Sidebar navigation ----------
st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox(
    "Select Page", ["My Profile", "Data Explorer", "Contact"]
)

# ---------- MAIN HEADER ----------
st.header("Carl Vincent O. Pilongo")


# ---------- Cached data (tutorial: @st.cache_data) ----------
@st.cache_data
def load_data():
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "Day": np.arange(1, 31),
            "Study Hours": rng.integers(1, 9, 30),
            "Sleep Hours": rng.integers(4, 10, 30),
        }
    )


# ---------- My Profile ----------
if app_mode == "My Profile":
    st.title("My Profile")

    image_path = os.path.join(BASE_DIR, "profile.jpg")  # your photo file name
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists(image_path):
            st.image(image_path, width=220)
        else:
            st.info("Upload profile.jpg next to app.py to show your photo.")
    with col2:
        st.subheader("Carl Vincent O. Pilongo")
        st.write("**Course:** BES 212")
        st.write("**Section:** (BSME 2B)")
        st.write("**School:** (NEMSU Bislig)")
        st.write("**About me:** (An irregular student, fighting to survive for the future. HUSS! HUSS! HUSS! HUSS!)")

# ---------- Data Explorer ----------
elif app_mode == "Data Explorer":
    st.title("Data Explorer")
    st.caption("Sample data (randomly generated)")
    data = load_data()
    st.write(data.head())

    column = st.selectbox("Pick a variable", ["Study Hours", "Sleep Hours"])
    st.line_chart(data.set_index("Day")[column])
    st.bar_chart(data.set_index("Day")[[column]])
    st.write(data[column].describe())

# ---------- Contact ----------
elif app_mode == "Contact":
    st.title("Contact")
    st.write("**Email:** carlvincentpilongo@gmail.com")
    st.link_button("My GitHub", "https://github.com/carlvincentpilongo-dot")
    
