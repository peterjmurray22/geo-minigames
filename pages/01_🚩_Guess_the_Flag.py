import streamlit as st
import pathlib
import utils

def show_flag_question(round_data, multiple_choice=True):
    answer = round_data["answer"]
    st.session_state.correct = answer["name"]
    flag_dir = pathlib.Path(__file__).resolve().parents[1] / "assets" / "flags"
    flag_path = flag_dir / answer["flag_image"]
    if flag_path.exists():
        st.image(str(flag_path), width=450)
    else:
        st.warning(f"Flag image not found: {answer['flag_image']}")
    if multiple_choice:
        options = [c["name"] for c in round_data["options"]]
        submitted = utils.show_multiple_choice_options("Which country does this flag belong to?", options)
    else:
        submitted = utils.show_text_entry("Which country does this flag belong to?")
    return submitted

# --- App ---
st.title("🚩 Guess the Flag")

utils.init_game("flags")

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
    utils.run_game(st.session_state.pool, st.session_state.num_options, st.session_state.num_rounds, 'name', 'flag_distractors', show_flag_question)
