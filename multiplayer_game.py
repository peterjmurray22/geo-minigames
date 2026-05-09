import json
import uuid
import time
from typing import Dict, Any, List
import session
import streamlit as st

# Redis key patterns
GAME_KEY = "game:{game_id}"
GAME_PLAYERS = "game:{game_id}:players"
GAME_STATE = "game:{game_id}:state"
GAME_ROUND = "game:{game_id}:round"
GAME_ANSWERS = "game:{game_id}:answers"
RECENT_EVENTS = "recent_events"

def create_game(host_uid: str, host_name: str, options: Dict[str, Any]) -> str:
    """Host creates a lobby and becomes initial player."""
    r = session.get_redis_connection()
    game_id = str(uuid.uuid4())[:8]
    r.hset(GAME_KEY.format(game_id=game_id), mapping={
        "host": host_uid,
        "game_mode": st.session_state.current_game,
        "status": "lobby",
        "options": json.dumps(options),
        "created_at": int(time.time())
    })
    # add host to players hash
    r.hset(GAME_PLAYERS.format(game_id=game_id), host_uid, json.dumps({
        "name": host_name, "score": 0
    }))
    st.session_state.auto_refresh = True
    session.push_event({"event": "game_created", "game_mode": st.session_state.current_game, "game_id": game_id, "host_uid": host_uid, "host_name": host_name})
    return game_id

def list_lobbies() -> List[Dict[str, Any]]:
    """Return list of active lobbies in 'lobby' status."""
    r = session.get_redis_connection()
    keys = r.keys("game:*")
    lobbies = []
    seen = set()
    for k in keys:
        if ":" not in k.split("game:")[-1]:
            pass
    for key in r.keys("game:*"):
        if key.count(":") != 1:
            continue
        game_id = key.split(":")[1]
        if game_id in seen:
            continue
        seen.add(game_id)
        status = r.hget(key, "status")
        if status == "lobby" or status == "in_progress":
            options = json.loads(r.hget(key, "options") or "{}")
            game_mode = r.hget(key, "game_mode")
            host_uid = r.hget(key, "host")
            host_name = None
            if host_uid:
                p = r.hget(GAME_PLAYERS.format(game_id=game_id), host_uid)
                if p:
                    host_name = json.loads(p).get("name")
            lobbies.append({"game_id": game_id, "game_mode": game_mode, "host_name": host_name, "options": options})
    return lobbies

def join_game(game_id: str, uid: str, name: str) -> None:
    r = session.get_redis_connection()
    r.hset(GAME_PLAYERS.format(game_id=game_id), uid, json.dumps({"name": name, "score": 0}))
    session.push_event({"event": "player_joined_lobby", "game_id": game_id, "uid": uid, "name": name})
    st.session_state.auto_refresh = True

def start_game(game_id: str, host_uid: str, initial_pool: list, num_options:int, num_rounds:int) -> None:
    r = session.get_redis_connection()
    key = GAME_KEY.format(game_id=game_id)
    current_host = r.hget(key, "host")
    if current_host != host_uid:
        raise PermissionError("Only host can start the game")
    r.hset(key, "status", "in_progress")
    state = {
        "pool": json.dumps(initial_pool),
        "num_options": num_options,
        "num_rounds": num_rounds,
        "round_index": 0,
        "started_at": int(time.time())
    }
    r.set(GAME_STATE.format(game_id=game_id), json.dumps(state))
    # clear any previous round/answers
    r.delete(GAME_ROUND.format(game_id=game_id))
    r.delete(GAME_ANSWERS.format(game_id=game_id))
    session.push_event({"event": "game_started", "game_id": game_id})

def publish_round(game_id: str, round_data: dict) -> None:
    r = session.get_redis_connection()
    r.set(GAME_ROUND.format(game_id=game_id), json.dumps(round_data))
    # clear previous answers for this round
    r.delete(GAME_ANSWERS.format(game_id=game_id))

def submit_answer(game_id: str, uid: str, answer_value: str) -> None:
    r = session.get_redis_connection()
    r.hset(GAME_ANSWERS.format(game_id=game_id), uid, answer_value)

def collect_answers(game_id: str) -> Dict[str, str]:
    r = session.get_redis_connection()
    return r.hgetall(GAME_ANSWERS.format(game_id=game_id))

def award_scores(game_id: str, correct_answer: str) -> Dict[str,int]:
    """Host checks answers, updates player scores in players hash and returns updated scores dict."""
    r = session.get_redis_connection()
    answers = collect_answers(game_id)
    players = r.hgetall(GAME_PLAYERS.format(game_id=game_id))
    updated = {}
    for uid, pdata in players.items():
        p = json.loads(pdata)
        submitted = answers.get(uid)
        if submitted and submitted.strip().lower() == correct_answer.strip().lower():
            p["score"] = p.get("score", 0) + 1
            updated[uid] = p["score"]
        else:
            updated[uid] = p.get("score", 0)
        r.hset(GAME_PLAYERS.format(game_id=game_id), uid, json.dumps(p))
    session.push_event({"event": "round_scored", "game_id": game_id, "correct": correct_answer})
    return updated

def advance_round(game_id: str) -> Dict[str, Any]:
    """Advance round_index and return new state (or None if finished). Host should call generate_round locally
       and use publish_round to send the round_data."""
    r = session.get_redis_connection()
    state_raw = r.get(GAME_STATE.format(game_id=game_id))
    if not state_raw:
        return None
    state = json.loads(state_raw)
    state["round_index"] += 1
    r.set(GAME_STATE.format(game_id=game_id), json.dumps(state))
    return state

def lobby_screen(game_id: str):
    r = session.get_redis_connection()
    current_host = get_game_host_uid(game_id)
    players = r.hgetall(GAME_PLAYERS.format(game_id=game_id))
    if r.hget(GAME_KEY.format(game_id=game_id), "status") == "lobby":
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #FCE4EC 50%, #FFFFFF 100%);
            padding: 2.5rem;
            border-radius: 25px;
            border: 4px solid #EC407A;
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(236, 64, 122, 0.3);
        ">
            <h2 style="color: #C2185B !important; text-align: center; margin-bottom: 2rem !important; font-size: 2.2rem !important; font-weight: 700 !important; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">🎮 Players in Lobby</h2>
        """, unsafe_allow_html=True)

        for uid, pdata in players.items():
            p = json.loads(pdata)
            is_host = "👑 " if uid == current_host else ""
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #FFFFFF 0%, #E8F5E9 100%);
                padding: 1.25rem 2rem;
                margin: 0.75rem 0;
                border-radius: 15px;
                border: 3px solid #4CAF50;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
                color: #2E7D32;
                font-weight: 700;
                font-size: 1.1rem;
                text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
            ">
                {is_host}{p['name']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        if current_host == st.session_state.uid:
            if st.button("Start Game"):
                options_raw = r.hget(GAME_KEY.format(game_id=game_id), "options")
                options = json.loads(options_raw)
                initial_pool = options.get("initial_pool", [])
                num_options = options.get("num_options", 4)
                num_rounds = options.get("num_rounds", 5)
                start_game(game_id, st.session_state.uid, initial_pool, num_options, num_rounds)
                st.session_state.game_started = True
                st.rerun()
        else:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #FFA726 0%, #FFB74D 100%);
                padding: 1.5rem;
                border-radius: 20px;
                text-align: center;
                color: white;
                font-weight: 700;
                font-size: 1.2rem;
                margin: 1.5rem 0;
                border: 3px solid white;
                box-shadow: 0 6px 20px rgba(255, 167, 38, 0.4);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">
                ⏳ Waiting for host to start the game...
            </div>
            """, unsafe_allow_html=True)

def get_game_host_uid(game_id: str) -> str:
    r = session.get_redis_connection()
    key = GAME_KEY.format(game_id=game_id)
    return r.hget(key, "host")

def pull_question_data(game_id: str) -> Dict[str, Any]:
    r = session.get_redis_connection()
    round_raw = r.get(GAME_ROUND.format(game_id=game_id))
    if not round_raw:
        return None
    return json.loads(round_raw)

def get_game_status(game_id: str) -> str:
    r = session.get_redis_connection()
    key = GAME_KEY.format(game_id=game_id)
    return r.hget(key, "status")

def get_game_options(game_id: str) -> Dict[str, Any]:
    r = session.get_redis_connection()
    return json.loads(r.hget(GAME_KEY.format(game_id=game_id), "options"))

def check_all_answers_submitted(game_id: str) -> bool:
    r = session.get_redis_connection()
    answers = collect_answers(game_id)
    players = r.hgetall(GAME_PLAYERS.format(game_id=game_id))
    return len(answers) == len(players)

def end_game(game_id: str) -> None:
    r = session.get_redis_connection()
    r.hset(GAME_KEY.format(game_id=game_id), "status", "finished")
    r.delete(GAME_PLAYERS.format(game_id=game_id))
    r.delete(GAME_ROUND.format(game_id=game_id))
    r.delete(GAME_ANSWERS.format(game_id=game_id))
    r.delete(GAME_STATE.format(game_id=game_id))
    session.push_event({"event": "game_ended", "game_id": game_id})
    st.session_state.game_started = False

def get_leaderboard(game_id: str) -> List[Dict[str, Any]]:
    """Get sorted leaderboard of players with their scores."""
    r = session.get_redis_connection()
    players = r.hgetall(GAME_PLAYERS.format(game_id=game_id))
    leaderboard = []
    for uid, pdata in players.items():
        p = json.loads(pdata)
        leaderboard.append({
            "name": p["name"],
            "score": p.get("score", 0),
            "uid": uid
        })
    # Sort by score descending
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard
