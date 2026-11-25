import streamlit as st

st.header("Carl Vincent O. Pilongo")
import numpy as np
import pandas as pd
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="My Streamlit App", page_icon="📊")

# ---------- Sidebar navigation (tutorial: sidebar + selectbox) ----------
st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Exploration", "Prediction"])


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

# ---------- Home ----------
if app_mode == "Home":
    st.title("Loan Prediction Demo")
    st.markdown("This app follows the DataCamp Streamlit tutorial.")
    st.caption("Sample dataset (randomly generated)")
    st.write(data.head())
    st.bar_chart(data[["ApplicantIncome", "LoanAmount"]].head(20))

# ---------- Exploration ----------
elif app_mode == "Exploration":
    st.title("Data Exploration")
    column = st.selectbox("Pick a variable", data.columns)
    st.line_chart(data[column])
    st.area_chart(data[[column]])
    st.write(data[column].describe())

# ---------- Prediction ----------
elif app_mode == "Prediction":
    st.title("Loan Prediction")
    income = st.sidebar.slider("ApplicantIncome", 0, 10000, 3000)
    loan = st.sidebar.slider("LoanAmount in K$", 9.0, 700.0, 200.0)
    credit = st.sidebar.radio("Credit History", ["No", "Yes"])

    if st.button("Predict"):
        # Simple rule-based stand-in for the tutorial's Random Forest model
        approved = credit == "Yes" and income * 0.05 > loan * 0.1
        if approved:
            st.success("Congratulations! You will get the loan.")
            st.balloons()
        else:
            st.error("According to our calculations, you will not get the loan.")
