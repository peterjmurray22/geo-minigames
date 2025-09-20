
import streamlit as st
import utils

def show_capital_question(round_data, multiple_choice=True):
    answer = round_data["answer"]
    st.session_state.correct = answer["capital"]
    if multiple_choice:
        options = round_data["options"]
        submitted = utils.show_multiple_choice_options(f"What is the capital of **{answer['name']}**?", options)
    else:
        submitted = utils.show_text_entry(f"What is the capital of **{answer['name']}**?")
    return submitted

# --- App ---
st.title("🗺️ Guess the Capital")

utils.init_game("captials")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = utils.load_countries()
if "game_started" not in st.session_state or not st.session_state.game_started:
    pool, input, num_options, num_rounds = utils.setup_screen(st.session_state.countries)
    if "game_started" in st.session_state and st.session_state.game_started:
        st.session_state.pool = pool
        st.session_state.input = input
        st.session_state.num_options = num_options
        st.session_state.num_rounds = num_rounds
        st.rerun()
else:
    st.metric("Score", st.session_state.score_display)
    utils.run_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'capital', 'capital_distractors', show_capital_question, verify_distractors=False)
