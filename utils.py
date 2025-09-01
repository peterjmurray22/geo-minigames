import streamlit as st
import random
import time
import json
import pathlib

@st.cache_data
def load_countries():
    data_path = pathlib.Path(__file__).resolve().parents[0] / "data" / "countries.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_round(pool, key_field: str, distractor_key: str, num_options: int = 4):
    """
    pool: list of dicts (e.g., countries)
    key_field: the field used for correct answer ("name", "capital", etc.)
    """
    if not pool:
        return None

    answer = random.choice(pool)

    # remove answer from pool
    remaining = [c for c in pool if c != answer]

    # sample distractors
    distractor_list = answer[distractor_key]
    distractors = [d for d in remaining if d["name"] in distractor_list]
    distractors = random.sample(distractors, k=min(num_options - 1, len(distractors)))
    if len(distractors) < min(num_options - 1, len(remaining)):
        extend_list = [a for a in remaining if a not in distractors and a["name"] != answer["name"]]
        distractors.extend(random.sample(extend_list, k=(min(num_options - 1, len(remaining)) - len(distractors))))
    options = distractors + [answer]

    return {
        "answer": answer,
        "options": options,
        "key_field": key_field,
    }, remaining

def setup_screen(countries):
    nations = st.checkbox("Nations", value=True)
    territories = st.checkbox("Territories", value=True)
    num_options = st.slider("Number of choices", 2, 10, 4)
    num_rounds = st.slider("Number of rounds", 1, 50, 10)

    st.session_state.score = 0
    st.session_state.rounds = 0
    update_score()

    if st.button("Start Game", disabled=not nations and not territories):
        pool = []
        if nations:
            pool.extend([c for c in countries if c["type"] == "nation"])
        if territories:
            pool.extend([c for c in countries if c["type"] == "territory"])
        st.session_state.game_started = True
        return pool, num_options, num_rounds
    return None, None, None

def update_score():
    st.session_state.score_display = f"{st.session_state.score} / {st.session_state.rounds} - {round(st.session_state.score/st.session_state.rounds * 100) if st.session_state.rounds > 0 else 0}%"

def init_game(game_title):
    if "current_game" not in st.session_state or st.session_state.current_game != game_title:
        st.session_state.game_started = False
        st.session_state.current_game = game_title
        if "round" in st.session_state:
            del st.session_state["round"]

def run_multiple_choice_game(pool, num_options, num_rounds, key_field, distractor_key, show_question_fn):
    if "round" not in st.session_state:
        round_data, pool = generate_round(pool, key_field, distractor_key, num_options)
        st.session_state.round = round_data
        st.session_state.pool = pool

    current = st.session_state.round
    choice, correct = show_question_fn(current)

    if st.button("Submit", disabled=choice is None or st.session_state.rounds == num_rounds):
        st.session_state.rounds += 1
        if choice == correct:
            st.session_state.score += 1
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect! The correct answer is **{correct}**.")

        update_score()
        if st.session_state.rounds < num_rounds and st.session_state.pool:
            round_data, pool = generate_round(st.session_state.pool, key_field, distractor_key, num_options)
            st.session_state.round = round_data
            st.session_state.pool = pool
        else:
            st.success(f"Game over! Final score: {st.session_state.score}/{st.session_state.rounds}")
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
            "countries",
            "score_display",
            "current_game",
            "round",
            "game_title"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

