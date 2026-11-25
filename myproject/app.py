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
    "Select Page", ["My Profile", "Home", "Exploration", "Prediction"]
)


# ---------- Cached data (tutorial: @st.cache_data) ----------
@st.cache_data
def load_data():
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "ApplicantIncome": rng.integers(1000, 10000, 100),
            "LoanAmount": rng.integers(50, 700, 100),
            "CreditHistory": rng.integers(0, 2, 100),
        }
    )


data = load_data()

# ---------- MAIN HEADER ----------
st.header("Carl Vincent O. Pilongo")

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
        st.write("**Section:** (edit this)")
        st.write("**School:** (edit this)")
        st.write("**About me:** (write one or two sentences here)")
