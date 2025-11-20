import streamlit as st
import random
import time
import json
import pathlib
import multiplayer_game as mg

@st.cache_data
def load_countries():
    data_path = pathlib.Path(__file__).resolve().parents[0] / "data" / "countries.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_round(pool, key_field: str, distractor_key: str, num_options: int = 4, verify_distractors=True):
    if not pool:
        return None

    pool = [c for c in pool if c[key_field] != ""]

    answer = random.choice(pool)

    # remove answer from pool
    remaining = [c for c in pool if c != answer and c[key_field] != ""]

    if st.session_state.input == "Text Entry":
        return {
            "answer": answer,
            "options": [],
            "key_field": key_field,
        }, remaining

    # sample distractors
    distractor_list = answer[distractor_key]
    distractors = []
    options = []
    if verify_distractors:
        distractors = [d for d in remaining if d[key_field] in distractor_list]
        distractors = random.sample(distractors, k=min(num_options - 1, len(distractors)))
        if len(distractors) < min(num_options - 1, len(remaining)):
            extend_list = [a for a in remaining if a not in distractors and a["name"] != answer["name"]]
            distractors.extend(random.sample(extend_list, k=(min(num_options - 1, len(remaining)) - len(distractors))))
        options = [d[key_field] for d in distractors] + [answer[key_field]]
    else:
        distractors = distractor_list
        distractors = random.sample(distractors, k=min(num_options - 1, len(distractors)))
        if len(distractors) < min(num_options - 1, len(remaining)):
            extend_list = [a[key_field] for a in remaining if a[key_field] not in distractors and a["name"] != answer["name"]]
            distractors.extend(random.sample(extend_list, k=(min(num_options - 1, len(remaining)) - len(distractors))))
        options = distractors + [answer[key_field]]

    return {
        "answer": answer,
        "options": options,
        "key_field": key_field,
    }, remaining

def setup_screen(countries):
    col1, col2 = st.columns([2, 1])
    with col1:  # game settings
        st.subheader("Game Settings")
        nations = st.checkbox("Nations", value=True)
        territories = st.checkbox("Territories", value=False)
        us_states = st.checkbox("US States", value=False)
        input = st.radio("Input type", ["Multiple Choice", "Text Entry"], index=0, horizontal=True)
        num_options = None
        if input == "Multiple Choice":
            num_options = st.slider("Number of choices", 2, 10, 4)
        num_rounds = st.slider("Number of rounds", 1, 50, 10)

        st.session_state.score = 0
        st.session_state.rounds = 0
        update_score()

        if st.button("Start Game", disabled=not nations and not territories and not us_states):
            pool = []
            if nations:
                pool.extend([c for c in countries if c["type"] == "nation"])
            if territories:
                pool.extend([c for c in countries if c["type"] == "territory"])
            if us_states:
                pool.extend([c for c in countries if c["type"] == "us_state"])
            st.session_state.game_started = True
            return pool, input, num_options, num_rounds
        elif st.button("Create Multiplayer Lobby", disabled=not nations and not territories and not us_states):
            sets = []
            if nations:
                sets.append("nations")
            if territories:
                sets.append("territories")
            if us_states:
                sets.append("us_states")
            options = {
                "sets": sets,
                "input": input,
                "num_options": num_options,
                "num_rounds": num_rounds
            }
            mg.create_game(st.session_state.uid, st.session_state.username, options)
            return None, None, None, None
    with col2:  # multiplayer lobbies
        st.subheader("Join Lobby")
        lobbies = mg.list_lobbies()
        for lobby in lobbies:
            if lobby['game_mode'] != st.session_state.current_game:
                continue
            if st.button(f"Join {lobby['host_name']}'s game", key=f"join_{lobby['game_id']}"):
                mg.join_game(lobby["game_id"], st.session_state.uid, st.session_state.username)
                st.session_state.current_game_id = lobby["game_id"]
                st.rerun()

    return None, None, None, None

def show_image_question(round_data, image_dir, image_key, question_text, multiple_choice=True):
    answer = round_data["answer"]
    st.session_state.correct = answer["name"]
    image_path = image_dir / answer[image_key]
    if not answer[image_key]:
        st.warning(f"No image specified for {answer['name']}")
    elif image_path.exists():
        with st.container(border=True, width=450):
            st.image(str(image_path), width=450)
    else:
        st.warning(f"Image not found: {answer[image_key]}")
    if multiple_choice:
        options = round_data["options"]
        submitted = show_multiple_choice_options(question_text, options)
    else:
        submitted = show_text_entry(question_text)
    return submitted

def update_score():
    st.session_state.score_display = f"{st.session_state.score} / {st.session_state.rounds} - {round(st.session_state.score/st.session_state.rounds * 100) if st.session_state.rounds > 0 else 0}%"

def init_game(game_title):
    if "current_game" not in st.session_state or st.session_state.current_game != game_title:
        st.session_state.game_started = False
        st.session_state.current_game = game_title
        if "round" in st.session_state:
            del st.session_state["round"]

def show_multiple_choice_options(question_text, options):
    choice = st.radio(question_text, sorted(options), index=None, key="multiple_choice")
    return choice

def show_text_entry(question_text):
    entry = st.text_input(question_text, key="text_entry")
    return entry

def submit_answer():
    if st.session_state.input == "Multiple Choice":
        st.session_state.submitted = st.session_state.multiple_choice
        st.session_state.multiple_choice = None
    else:
        st.session_state.submitted = st.session_state.text_entry
        st.session_state.text_entry = ""

def run_game(pool, num_options, num_rounds, key_field, distractor_key, show_question_fn, verify_distractors=True):
    if "round" not in st.session_state:
        round_data, pool = generate_round(pool, key_field, distractor_key, num_options, verify_distractors)
        st.session_state.round = round_data
        st.session_state.pool = pool

    current = st.session_state.round
    submitted = show_question_fn(current, st.session_state.input == "Multiple Choice")

    if st.button("Submit", disabled=submitted is None or submitted == "" or st.session_state.rounds == num_rounds, on_click=submit_answer):
        st.session_state.rounds += 1
        if st.session_state.submitted.lower().strip() == st.session_state.correct.lower().strip():
            st.session_state.score += 1
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect! The correct answer is **{st.session_state.correct}**.")

        update_score()
        if st.session_state.rounds < num_rounds and st.session_state.pool:
            round_data, pool = generate_round(st.session_state.pool, key_field, distractor_key, num_options, verify_distractors)
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
            "game_title",
            "correct"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
