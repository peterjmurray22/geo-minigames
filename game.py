import streamlit as st
import random
import time
import json
import pathlib
import multiplayer_game as mg
import styles
from streamlit_autorefresh import st_autorefresh

@st.cache_data
def load_countries():
    data_path = pathlib.Path(__file__).resolve().parents[0] / "data" / "countries.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_round(pool, key_field: str, distractor_key: str, num_options: int = 4, verify_distractors=True, publish_to_game_id: str = None):
    if not pool:
        return None

    pool = [c for c in pool if c[key_field] != ""]

    answer = random.choice(pool)

    # remove answer from pool
    remaining = [c for c in pool if c != answer and c[key_field] != ""]

    if st.session_state.input == "Text Entry":
        if publish_to_game_id:
            mg.publish_round(publish_to_game_id, {
                "answer": answer,
                "options": [],
                "key_field": key_field,
            })
        return {
            "answer": answer,
            "options": [],
            "key_field": key_field,
        }, remaining
    else:
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
    
    if publish_to_game_id:
        mg.publish_round(publish_to_game_id, {
            "answer": answer,
            "options": options,
            "key_field": key_field,
        })
    return {
        "answer": answer,
        "options": options,
        "key_field": key_field,
    }, remaining

def setup_screen(countries):
    col1, col2 = st.columns([2, 1], gap="large")
    game_id = None
    with col1:  # game settings
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
            padding: 2rem;
            border-radius: 25px;
            border: 4px solid white;
            margin-bottom: 1.5rem;
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        ">
            <h2 style="color: white !important; margin: 0 !important; font-size: 2rem !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">⚙️ Game Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        nations = st.checkbox("Nations", value=True, disabled="current_game_id" in st.session_state)
        territories = st.checkbox("Territories", value=False, disabled="current_game_id" in st.session_state)
        us_states = st.checkbox("US States", value=False, disabled="current_game_id" in st.session_state)
        input = st.radio("Input type", ["Multiple Choice", "Text Entry"], index=0, horizontal=True, disabled="current_game_id" in st.session_state)
        num_options = None
        if input == "Multiple Choice":
            num_options = st.slider("Number of choices", 2, 10, 4, disabled="current_game_id" in st.session_state)
        num_rounds = st.slider("Number of rounds", 1, 50, 10, disabled="current_game_id" in st.session_state)

        st.session_state.score = 0
        st.session_state.rounds = 0
        update_score()

        if st.button("Start Singleplayer Game", disabled="current_game_id" in st.session_state or (not nations and not territories and not us_states)):
            pool = []
            if nations:
                pool.extend([c for c in countries if c["type"] == "nation"])
            if territories:
                pool.extend([c for c in countries if c["type"] == "territory"])
            if us_states:
                pool.extend([c for c in countries if c["type"] == "us_state"])
            st.session_state.game_started = True
            st.session_state.pool = pool
            st.session_state.input = input
            st.session_state.num_options = num_options
            st.session_state.num_rounds = num_rounds
            st.rerun()

        elif st.button("Create Multiplayer Lobby", disabled="current_game_id" in st.session_state or (not nations and not territories and not us_states)):
            pool = []
            if nations:
                pool.extend([c for c in countries if c["type"] == "nation"])
            if territories:
                pool.extend([c for c in countries if c["type"] == "territory"])
            if us_states:
                pool.extend([c for c in countries if c["type"] == "us_state"])
            options = {
                "pool": pool,
                "input": input,
                "num_options": num_options,
                "num_rounds": num_rounds
            }
            game_id = mg.create_game(st.session_state.uid, st.session_state.username, options)
            st.session_state.current_game_id = game_id
            st.session_state.pool = pool
            st.session_state.input = input
            st.session_state.num_options = num_options
            st.session_state.num_rounds = num_rounds
            st.rerun()

    with col2:  # multiplayer lobbies
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #EC407A 0%, #F06292 100%);
            padding: 2rem;
            border-radius: 25px;
            border: 4px solid white;
            margin-bottom: 1.5rem;
            box-shadow: 0 6px 20px rgba(236, 64, 122, 0.3);
        ">
            <h2 style="color: white !important; margin: 0 !important; font-size: 2rem !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎮 Join Lobby</h2>
        </div>
        """, unsafe_allow_html=True)
        lobbies = mg.list_lobbies()
        for lobby in lobbies:
            if lobby['game_mode'] != st.session_state.current_game:
                continue
            if st.button(f"Join {lobby['host_name']}'s game", key=f"join_{lobby['game_id']}"):
                mg.join_game(lobby["game_id"], st.session_state.uid, st.session_state.username)
                st.session_state.current_game_id = lobby["game_id"]
                st.rerun()

def show_image_question(round_data, image_dir, image_key, question_text, answer_key="name", multiple_choice=True):
    if round_data is None:
        st.rerun()
    answer = round_data["answer"]
    st.session_state.correct = answer[answer_key]
    image_path = image_dir / answer[image_key]

    # Create centered container for image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not answer[image_key]:
            st.warning(f"No image specified for {answer['name']}")
        elif image_path.exists():
            st.markdown("""
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 25px;
                border: 5px solid transparent;
                background: linear-gradient(white, white) padding-box,
                            linear-gradient(135deg, #4CAF50 0%, #EC407A 100%) border-box;
                box-shadow: 0 10px 30px rgba(236, 64, 122, 0.3);
                margin: 2rem 0;
            ">
            """, unsafe_allow_html=True)
            st.image(str(image_path), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
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
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FFFFFF 0%, #FCE4EC 100%);
        padding: 2rem;
        border-radius: 25px;
        border: 4px solid #EC407A;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(236, 64, 122, 0.3);
    ">
        <h3 style="color: #C2185B !important; text-align: center; margin: 0 !important; font-size: 1.8rem !important; font-weight: 700 !important; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">{question_text}</h3>
    </div>
    """, unsafe_allow_html=True)
    choice = st.radio("Select your answer:", sorted(options), index=None, key="multiple_choice", label_visibility="collapsed")
    return choice

def show_text_entry(question_text):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FFFFFF 0%, #FCE4EC 100%);
        padding: 2rem;
        border-radius: 25px;
        border: 4px solid #EC407A;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(236, 64, 122, 0.3);
    ">
        <h3 style="color: #C2185B !important; text-align: center; margin: 0 !important; font-size: 1.8rem !important; font-weight: 700 !important; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">{question_text}</h3>
    </div>
    """, unsafe_allow_html=True)
    entry = st.text_input("Type your answer:", key="text_entry", label_visibility="visible")
    return entry

def submit_answer():
    if st.session_state.input == "Multiple Choice":
        st.session_state.submitted = st.session_state.multiple_choice
        st.session_state.multiple_choice = None
    else:
        st.session_state.submitted = st.session_state.text_entry
        st.session_state.text_entry = ""
    mg.submit_answer(st.session_state.get("current_game_id", ""), st.session_state.uid, st.session_state.submitted)

def run_game(pool, num_options, num_rounds, key_field, distractor_key, show_question_fn, verify_distractors=True):
    if "round" not in st.session_state or st.session_state.round is None:
        if mg.get_game_host_uid(st.session_state.get("current_game_id", "")) is not None and mg.get_game_host_uid(st.session_state.get("current_game_id", "")) != st.session_state.uid:
            round_data = mg.pull_question_data(st.session_state.get("current_game_id", ""))
        else:
            round_data, pool = generate_round(pool, key_field, distractor_key, num_options, verify_distractors, publish_to_game_id=st.session_state.get("current_game_id") if mg.get_game_host_uid(st.session_state.get("current_game_id", "")) == st.session_state.uid else None)
            st.session_state.pool = pool
        st.session_state.round = round_data

    # Show leaderboard for multiplayer games
    if "current_game_id" in st.session_state and st.session_state.current_game_id:
        leaderboard = mg.get_leaderboard(st.session_state.current_game_id)
        if len(leaderboard) > 1:  # Only show if there are multiple players
            styles.show_leaderboard(leaderboard, st.session_state.uid)

    # Show round counter
    st.markdown(f"""
    <div style="
        text-align: center;
        background: linear-gradient(135deg, #4CAF50 0%, #EC407A 100%);
        color: white;
        font-weight: 700;
        font-size: 1.3rem;
        margin: 1.5rem 0;
        padding: 1rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(236, 64, 122, 0.3);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    ">
        🌸 Round {st.session_state.rounds + 1} of {num_rounds} 🌸
    </div>
    """, unsafe_allow_html=True)

    current = st.session_state.round
    submitted = show_question_fn(current, st.session_state.input == "Multiple Choice")

    # Center the submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit Answer", disabled=submitted is None or submitted == "" or st.session_state.rounds == num_rounds, on_click=submit_answer, use_container_width=True):
            st.rerun()
    
    if "submitted" in st.session_state and st.session_state.submitted is not None:
        check_correct_answer()
        update_score()
        if st.session_state.rounds < num_rounds and st.session_state.pool:
            if mg.get_game_host_uid(st.session_state.get("current_game_id", "")) is not None and mg.get_game_host_uid(st.session_state.get("current_game_id", "")) != st.session_state.uid:
                round_data = mg.pull_question_data(st.session_state.get("current_game_id", ""))
            else:
                round_data, pool = generate_round(pool, key_field, distractor_key, num_options, verify_distractors, publish_to_game_id=st.session_state.get("current_game_id") if mg.get_game_host_uid(st.session_state.get("current_game_id", "")) == st.session_state.uid else None)
                st.session_state.pool = pool
            st.session_state.round = round_data
        else:
            percentage = round(st.session_state.score/st.session_state.rounds * 100) if st.session_state.rounds > 0 else 0

            # Determine emoji and message based on performance
            if percentage >= 90:
                emoji = "🏆"
                message = "Outstanding! Geography Master!"
            elif percentage >= 75:
                emoji = "🌟"
                message = "Excellent work! Great knowledge!"
            elif percentage >= 60:
                emoji = "👍"
                message = "Good job! Keep it up!"
            elif percentage >= 40:
                emoji = "📚"
                message = "Not bad! Keep learning!"
            else:
                emoji = "💪"
                message = "Keep practicing!"

            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 25%, #EC407A 75%, #F06292 100%);
                padding: 4rem;
                border-radius: 30px;
                border: 6px solid white;
                box-shadow: 0 15px 40px rgba(236, 64, 122, 0.5);
                text-align: center;
                margin: 3rem 0;
            ">
                <div style="font-size: 6rem; margin-bottom: 1.5rem; animation: float 3s ease-in-out infinite;">{emoji}</div>
                <h2 style="color: white !important; margin: 0 0 2rem 0 !important; font-size: 3.5rem !important; text-shadow: 3px 3px 6px rgba(0,0,0,0.3); font-weight: 700;">Game Over!</h2>
                <div style="
                    background: rgba(255,255,255,0.3);
                    padding: 2.5rem;
                    border-radius: 20px;
                    margin: 2rem 0;
                    border: 3px solid white;
                ">
                    <div style="color: white; font-size: 4rem; font-weight: 700; text-shadow: 3px 3px 6px rgba(0,0,0,0.3);">
                        {st.session_state.score} / {st.session_state.rounds}
                    </div>
                    <div style="color: white; font-size: 2.5rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        {percentage}%
                    </div>
                </div>
                <div style="color: white; font-size: 1.8rem; font-weight: 700; margin-top: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    {message}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if mg.get_game_host_uid(st.session_state.get("current_game_id", "")) == st.session_state.uid:
                mg.end_game(st.session_state.get("current_game_id", ""))
            st.session_state.game_started = False
            st.session_state.pop("current_game_id", None)
        time.sleep(3)
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Reset Game", disabled=mg.get_game_host_uid(st.session_state.get("current_game_id", "")) is not None and mg.get_game_host_uid(st.session_state.get("current_game_id", "")) != st.session_state.uid, use_container_width=True):
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

def check_correct_answer():
    while (not mg.check_all_answers_submitted(st.session_state.get("current_game_id", "")) and
           mg.get_game_host_uid(st.session_state.get("current_game_id", "")) == st.session_state.uid and
           not st.button("Proceed")) or (
               mg.get_game_host_uid(st.session_state.get("current_game_id", "")) != st.session_state.uid and
               mg.pull_question_data(st.session_state.get("current_game_id", "")) == st.session_state.round and
               mg.get_game_status(st.session_state.get("current_game_id", "")) != "finished"):
        st.warning("Waiting for all players to submit their answers...")
        st.rerun()

    st.session_state.rounds += 1

    # Check if correct
    is_correct = st.session_state.submitted.lower().strip() == st.session_state.correct.lower().strip()

    if is_correct:
        st.session_state.score += 1
        st.success("Correct! 🎉")
    else:
        st.error(f"Incorrect! The correct answer is **{st.session_state.correct}**.")

    # Update multiplayer scores if in a game
    if "current_game_id" in st.session_state and st.session_state.current_game_id:
        # Host awards scores to all players
        if mg.get_game_host_uid(st.session_state.get("current_game_id", "")) == st.session_state.uid:
            mg.award_scores(st.session_state.current_game_id, st.session_state.correct)

    st.session_state.submitted = None
    st.session_state.round = None

def conditional_autorefresh():
    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = False

    if st.session_state.auto_refresh:
        st_autorefresh(interval=5000, key="page_refresh")
