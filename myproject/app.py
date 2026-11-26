import os
import io
import wave
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_buzzer():
    t = np.linspace(0, 0.5, 11025, False)
    wave_data = (np.sign(np.sin(2 * np.pi * 150 * t)) * 12000).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(22050)
        w.writeframes(wave_data.tobytes())
    return buf.getvalue()  

def make_chime():
    rate = 22050
    parts = []
    for f in [523, 659, 784, 1047]:
        t = np.linspace(0, 0.15, int(rate * 0.15), False)
        parts.append(np.sin(2 * np.pi * f * t) * np.linspace(1, 0.6, t.size))
    data = (np.concatenate(parts) * 12000).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data.tobytes())
    return buf.getvalue()

# ---------- Page setup ----------
st.set_page_config(page_title="Carl Vincent O. Pilongo", page_icon="👤")
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #0B1F3A 0%, #12335c 50%, #050d1a 100%); background-attachment: fixed; }
    .stApp { background: radial-gradient(circle at top right, rgba(255,215,0,0.18), transparent 45%), linear-gradient(160deg, #0B1F3A, #050d1a); background-attachment: fixed; }
    .stApp { background-color: #0B1F3A; background-image: radial-gradient(rgba(255,215,0,0.3) 1.5px, transparent 1.5px); background-size: 30px 30px; }
    .stApp { background: repeating-linear-gradient(45deg, #0B1F3A, #0B1F3A 20px, #0e2747 20px, #0e2747 40px); }
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
    "Select Page", ["My Profile", "Data Explorer", "Contact", "Game", "Guess My Favorites"]
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
elif app_mode == "Guess My Favorites":
    st.title("Guess My Favorites")

    favorites = [
        {"category": "Color", "answers": ["blue"], "clue": "Number 5 in the rainbow"},
        {"category": "Dish", "answers": ["adobo"], "clue": "Soy sauce"},
        {"category": "Fruit", "answers": ["orange"], "clue": "Sharmaine"},
        {"category": "Game", "answers": ["mobile legends bang bang", "mobile legends", "mlbb"], "clue": "E-games"},
        {"category": "Dessert", "answers": ["mango float"], "clue": "Floating"},
        {"category": "Animal", "answers": ["bird"], "clue": "Can sing"},
        {"category": "Subject", "answers": ["recess"], "clue": "Lasts only 15 minutes"},
        {"category": "Drink", "answers": ["water"], "clue": "Water"},
        {"category": "Number", "answers": ["28"], "clue": "", "latex": r"\lim_{x \to 4} \dfrac{x^2 + 20x - 96}{x - 4}"},
        {"category": "Letter", "answers": ["c"], "clue": "(it's on you now)"},
    ]

    if "fav_i" not in st.session_state:
        st.session_state.fav_i = 0
        st.session_state.fav_score = 0
        st.session_state.fav_msg = ""
    if st.session_state.get("fav_celebrate"):
        st.balloons()
        st.audio(make_chime(), format="audio/wav", autoplay=True)
        st.session_state.fav_celebrate = False

    if st.session_state.fav_msg:
        st.info(st.session_state.fav_msg)
        st.session_state.fav_msg = ""

    i = st.session_state.fav_i
    if i >= len(favorites):
        st.success(f"Game over! Your score: {st.session_state.fav_score} / {len(favorites)}")
        st.balloons()
        if st.button("Play again"):
            st.session_state.fav_i = 0
            st.session_state.fav_score = 0
            st.rerun()
    else:
        item = favorites[i]
        st.subheader(f"{i + 1} of {len(favorites)}: My favorite {item['category']}")
        st.write("Clue:")
        if "latex" in item:
            st.latex(item["latex"])
        else:
            st.write(item["clue"])

        answer = st.text_input("Your answer", key=f"ans_{i}")
        col_a, col_b = st.columns(2)
        if col_a.button("Submit"):
            if answer.strip().lower() in item["answers"]:
                st.session_state.fav_score += 1
                st.session_state.fav_i += 1
                st.session_state.fav_msg = "Correct!"
                st.session_state.fav_celebrate = True
                st.rerun()
            else:
                st.warning("Not yet, try again!")
                st.audio(make_buzzer(), format="audio/wav", autoplay=True)
        if col_b.button("Skip"):
            st.session_state.fav_i += 1
            st.session_state.fav_msg = "The answer was: " + item["answers"][0].title()
            st.rerun()
        
