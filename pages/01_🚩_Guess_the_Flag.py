import streamlit as st
import pathlib
import utils

def show_flag_question(round_data):
    answer = round_data["answer"]
    options = [c["name"] for c in round_data["options"]]
    flag_dir = pathlib.Path(__file__).resolve().parents[1] / "assets" / "flags"
    flag_path = flag_dir / answer["flag_image"]
    if flag_path.exists():
        st.image(str(flag_path), width=450)
    else:
        st.warning(f"Flag image not found: {answer['flag_image']}")
    choice = st.radio("Which country's flag is this?", options, index=None)
    return choice, answer["name"]

# --- App ---
st.title("🚩 Guess the Flag")

utils.init_game("flags")

# init global state
if "countries" not in st.session_state:
    st.session_state.countries = utils.load_countries()
if "game_started" not in st.session_state or not st.session_state.game_started:
    pool, num_options, num_rounds = utils.setup_screen(st.session_state.countries)
    st.session_state.pool = pool
    st.session_state.num_options = num_options
    st.session_state.num_rounds = num_rounds
    st.rerun()
else:
    st.metric("Score", st.session_state.score_display)
    utils.run_multiple_choice_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'name', show_flag_question)
