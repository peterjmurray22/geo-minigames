
import streamlit as st
import json, random, pathlib

@st.cache_data
def load_countries():
    data_path = pathlib.Path(__file__).resolve().parents[1] / "data" / "countries.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def flag_from_iso(code: str) -> str:
    # Convert ISO country code to flag emoji
    code = code.upper()
    base = 127397  # regional indicator base
    return "".join(chr(base + ord(c)) for c in code)

def new_round(num_options: int = 4):
    countries = st.session_state.countries
    answer = random.choice(countries)
    # pick unique distractors
    pool = [c for c in countries if c["code"] != answer["code"]]
    distractors = random.sample(pool, k=min(num_options - 1, len(pool)))
    options = distractors + [answer]
    random.shuffle(options)
    st.session_state.current = {
        "answer": answer,
        "options": options,
        "submitted": False,
        "selected": None,
    }

# --- App ---
st.title("🚩 Guess the Flag")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = load_countries()
if "score" not in st.session_state:
    st.session_state.score = 0
if "rounds" not in st.session_state:
    st.session_state.rounds = 0
if "current" not in st.session_state:
    new_round()

with st.sidebar:
    st.header("Settings")
    num_options = st.slider("Choices per question", 3, 6, 4, 1)
    if st.button("🔄 New Question"):
        new_round(num_options)
    if st.button("🧹 Reset Score"):
        st.session_state.score = 0
        st.session_state.rounds = 0
        st.success("Scoreboard reset.")

current = st.session_state.current
answer = current["answer"]

st.metric("Score", f"{st.session_state.score} / {st.session_state.rounds}")

st.markdown(
    f"<div style='font-size: 8rem; line-height: 1;'>{flag_from_iso(answer['code'])}</div>",
    unsafe_allow_html=True,
)

options = [c["name"] for c in current["options"]]
choice = st.radio("Which country's flag is this?", options, index=None)

cols = st.columns(2)
submit = cols[0].button("Submit", type="primary", disabled=choice is None or current['submitted'])
nextq = cols[1].button("Next")

if submit and not current["submitted"]:
    current["submitted"] = True
    current["selected"] = choice
    st.session_state.rounds += 1
    if choice == answer["name"]:
        st.session_state.score += 1
        st.success("Correct! 🎉")
    else:
        st.error(f"Not quite. The correct answer is **{answer['name']}**.")

if nextq:
    new_round(num_options)

with st.expander("About this game"):
    st.write(
        "Flags are displayed using **emoji** generated from ISO country codes. "
        "Add or edit countries in `data/countries.json`. "
        "For image-based flags, place PNG/SVG files in an `assets/flags` folder "
        "and display them with `st.image()`."
    )
