import streamlit as st
import json, random, pathlib
import time

@st.cache_data
def load_countries():
    data_path = pathlib.Path(__file__).resolve().parents[1] / "data" / "countries.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def new_round(num_options: int = 4):
    pool = st.session_state.pool
    if not pool:
        st.warning("No more countries left!")
        st.stop()

    # pick the answer
    answer = random.choice(pool)

    # remove the answer from the pool so it won't appear again
    st.session_state.pool = [c for c in pool if c["code"] != answer["code"]]

    # pick unique distractors from the remaining pool
    distractors = random.sample(st.session_state.pool, k=min(num_options - 1, len(st.session_state.pool)))
    options = distractors + [answer]
    random.shuffle(options)

    # store current question
    st.session_state.current = {
        "answer": answer,
        "options": options,
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

if "game_started" not in st.session_state:
    nations = st.checkbox(label="Nations", value=True)
    territories = st.checkbox(label="Territories", value=True)
    
    num_options = st.slider("Number of choices", 2, 10, 4)

    if st.button(label="Start Game", disabled=not nations and not territories):
        st.session_state.pool = []
        if nations:
            st.session_state.pool.extend([c for c in st.session_state.countries if c["type"] == "nation"])
        if territories:
            st.session_state.pool.extend([c for c in st.session_state.countries if c["type"] == "territory"])
    
        st.session_state.num_options = num_options
        st.session_state.score = 0
        st.session_state.rounds = 0
        st.session_state.game_started = True

        st.rerun()
else:
    if "current" not in st.session_state:
        new_round(st.session_state.num_options)

    current = st.session_state.current
    current["submitted"] = False
    answer = current["answer"]

    st.metric("Score", f"{st.session_state.score} / {st.session_state.rounds} - {round(st.session_state.score/st.session_state.rounds * 100) if st.session_state.rounds > 0 else 0}%")

    flag_dir = pathlib.Path(__file__).resolve().parents[1] / "assets" / "flags"
    flag_path = flag_dir / answer["flag_image"]

    if flag_path.exists():
        st.image(str(flag_path), width=550)
    else:
        st.warning(f"Flag image not found: {answer['flag_image']}")

    options = sorted([c["name"] for c in current["options"]])
    choice = st.radio("Which country's flag is this?", options, index=None)

    cols = st.columns(2)
    submit = cols[0].button("Submit", type="primary", disabled=choice is None or current['submitted'])

    if submit and not current["submitted"]:
        current["submitted"] = True
        current["selected"] = choice
        st.session_state.rounds += 1
        if choice == answer["name"]:
            st.session_state.score += 1
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect! The correct answer is **{answer['name']}**.")
        new_round(st.session_state.num_options)
        time.sleep(3)
        st.rerun()
    
    if st.button("Reset Game"):
        keys_to_clear = [
            "game_started",
            "pool",
            "num_options",
            "num_rounds",
            "score",
            "rounds",
            "current",
            "countries"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
