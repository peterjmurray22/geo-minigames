import streamlit as st
import game
import pathlib
import session

def show_country_question(round_data, multiple_choice=True):
    return game.show_image_question(round_data, pathlib.Path(__file__).resolve().parents[1] / "assets" / "silhouettes", "silhouette", "Which country is this?", multiple_choice)


# --- App ---
st.title("🌎️ Guess the Country")
session.setup_multiplayer_session()

game.init_game("Guess the Country")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = game.load_countries()
if "game_started" not in st.session_state or not st.session_state.game_started:
    pool, input, num_options, num_rounds = game.setup_screen(st.session_state.countries)
    if "game_started" in st.session_state and st.session_state.game_started:
        st.session_state.pool = pool
        st.session_state.input = input
        st.session_state.num_options = num_options
        st.session_state.num_rounds = num_rounds
        st.rerun()
else:
    st.metric("Score", st.session_state.score_display)
    game.run_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'name', 'flag_distractors', show_country_question, verify_distractors=False)
