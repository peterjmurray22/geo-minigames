
import streamlit as st
import utils

def show_capital_question(round_data):
    answer = round_data["answer"]
    options = [c["capital"] for c in round_data["options"]]
    st.write(f"🌍 What is the capital of **{answer['name']}**?")
    choice = st.radio("Choose the capital:", options, index=None)
    return choice, answer["capital"]

# --- App ---
st.title("🗺️ Guess the Capital")

utils.init_game("captials")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = utils.load_countries()
if "game_started" not in st.session_state or not st.session_state.game_started:
    pool, num_options, num_rounds = utils.setup_screen(st.session_state.countries)
    if "game_started" in st.session_state and st.session_state.game_started:
        st.session_state.pool = pool
        st.session_state.num_options = num_options
        st.session_state.num_rounds = num_rounds
        st.rerun()
else:
    st.metric("Score", st.session_state.score_display)
    utils.run_multiple_choice_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'name', show_capital_question)
