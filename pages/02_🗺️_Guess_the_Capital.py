import streamlit as st
import game
import session

def show_capital_question(round_data, multiple_choice=True):
    answer = round_data["answer"]
    st.session_state.correct = answer["capital"]
    if multiple_choice:
        options = round_data["options"]
        submitted = game.show_multiple_choice_options(f"What is the capital of **{answer['name']}**?", options)
    else:
        submitted = game.show_text_entry(f"What is the capital of **{answer['name']}**?")
    return submitted

# --- App ---
st.title("🗺️ Guess the Capital")
session.setup_multiplayer_session()

game.init_game("Guess the Capital")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = game.load_countries()
if "game_started" not in st.session_state or not st.session_state.game_started:
    game.setup_screen(st.session_state.countries)
else:
    st.metric("Score", st.session_state.score_display)
    game.run_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'capital', 'capital_distractors', show_capital_question, verify_distractors=False)
