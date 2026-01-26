import streamlit as st
import game
import pathlib
import session
import multiplayer_game as mg


def show_capital_question(round_data, multiple_choice=True):
    answer = round_data["answer"]
    st.session_state.correct = answer["capital"]
    return game.show_image_question(round_data, pathlib.Path(__file__).resolve().parents[1] / "assets" / "silhouettes", "silhouette", f"What is the capital of **{answer['name']}**?", "capital", multiple_choice)

game.conditional_autorefresh()

# --- App ---
st.title("🗺️ Guess the Capital")
r, uid, username = session.setup_multiplayer_session()
session.heartbeat()

game.init_game("Guess the Capital")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = game.load_countries()
if "current_game_id" in st.session_state:
    if mg.get_game_status(st.session_state.current_game_id) == "in_progress" and mg.get_game_host_uid(st.session_state.current_game_id) != uid:
        options = mg.get_game_options(st.session_state.current_game_id)
        st.session_state.game_started = True
        st.session_state.pool = options.get("pool", [])
        st.session_state.num_options = options["num_options"]
        st.session_state.num_rounds = options["num_rounds"]
        st.session_state.input = options["input"]
    mg.lobby_screen(st.session_state.current_game_id)
if "game_started" not in st.session_state or not st.session_state.game_started:
    game.setup_screen(st.session_state.countries)
else:
    st.metric("Score", st.session_state.score_display)
    game.run_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'capital', 'capital_distractors', show_capital_question, verify_distractors=False)
