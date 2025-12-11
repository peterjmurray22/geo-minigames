import streamlit as st
import pathlib
import game
import session
import multiplayer_game as mg

def show_flag_question(round_data, multiple_choice=True):
    return game.show_image_question(round_data, pathlib.Path(__file__).resolve().parents[1] / "assets" / "flags", "flag_image", "Which country does this flag belong to?", "name", multiple_choice)

game.conditional_autorefresh()

# --- App ---
st.title("🚩 Guess the Flag")
r, uid, username = session.setup_multiplayer_session()
session.heartbeat()

game.init_game("Guess the Flag")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = game.load_countries()
if "current_game_id" in st.session_state:
    mg.lobby_screen(st.session_state.current_game_id)
if "game_started" not in st.session_state or not st.session_state.game_started:
    game.setup_screen(st.session_state.countries)
else:
    st.metric("Score", st.session_state.score_display)
    game.run_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'name', 'flag_distractors', show_flag_question)
