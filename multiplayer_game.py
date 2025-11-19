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
        "name": host_name, "ready": False, "score": 0
    }))
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
        if status == "lobby":
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
    r.hset(GAME_PLAYERS.format(game_id=game_id), uid, json.dumps({"name": name, "ready": False, "score": 0}))
    session.push_event({"event": "player_joined_lobby", "game_id": game_id, "uid": uid, "name": name})

def set_ready(game_id: str, uid: str, ready: bool) -> None:
    r = session.get_redis_connection()
    p_raw = r.hget(GAME_PLAYERS.format(game_id=game_id), uid)
    if not p_raw:
        return
    p = json.loads(p_raw)
    p["ready"] = bool(ready)
    r.hset(GAME_PLAYERS.format(game_id=game_id), uid, json.dumps(p))
    session.push_event({"event": "player_ready", "game_id": game_id, "uid": uid, "ready": p["ready"]})

def all_ready(game_id: str) -> bool:
    r = session.get_redis_connection()
    players = r.hgetall(GAME_PLAYERS.format(game_id=game_id))
    if not players:
        return False
    for v in players.values():
        if not json.loads(v).get("ready"):
            return False
    return True

def start_game(game_id: str, host_uid: str, initial_pool: list, num_options:int, num_rounds:int) -> None:
    """Host initializes shared game state and marks game in-progress."""
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
    """Host publishes a new round (round_data is JSON-serializable) — all clients read GAME_ROUND."""
    r = session.get_redis_connection()
    r.set(GAME_ROUND.format(game_id=game_id), json.dumps(round_data))
    # clear previous answers for this round
    r.delete(GAME_ANSWERS.format(game_id=game_id))
    session.push_event({"event": "round_published", "game_id": game_id})

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
