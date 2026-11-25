import os

import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Page setup ----------
st.set_page_config(page_title="Carl Vincent O. Pilongo", page_icon="👤")
st.markdown(
    """
    <style>
    .stApp { background-color: #0B1F3A; }
    [data-testid="stSidebar"] { background-color: #08162B; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p,
    .stApp label, .stApp span, .stApp li,
    [data-testid="stMarkdownContainer"] * { color: #FFD700 !important; }
    [data-testid="stHeader"] { background-color: #0B1F3A; }.stApp, .stApp * { font-style: italic !important; }
    [data-testid="stImage"] img { border: 6px solid #FFD700; border-radius: 16px; box-shadow: 0 0 20px #FFD700; }
    </style>
    """,
    unsafe_allow_html=True,
)
# ---------- Sidebar navigation ----------
st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox(
    "Select Page", ["My Profile", "Data Explorer", "Contact", "Game"]
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

    image_files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f)) and f not in ("app.py", "requirements.txt")]
    image_path = os.path.join(BASE_DIR, image_files[0]) if image_files else ""
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
elif app_mode == "Game":
    st.title("Guess the Number")
    if "secret" not in st.session_state:
        st.session_state.secret = int(np.random.randint(1, 21))
        st.session_state.tries = 0

    guess = st.number_input("Pick a number from 1 to 20", 1, 20, 10)
    if st.button("Guess"):
        st.session_state.tries += 1
        if guess == st.session_state.secret:
            st.success(f"Correct! You got it in {st.session_state.tries} tries.")
            st.balloons()
        elif guess < st.session_state.secret:
            st.warning("Too low!")
        else:
            st.warning("Too high!")

    if st.button("New game"):
        st.session_state.secret = int(np.random.randint(1, 21))
        st.session_state.tries = 0
        st.rerun()
