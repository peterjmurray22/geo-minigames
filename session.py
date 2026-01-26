import streamlit as st
import uuid
import redis
import os
import time
import json

# config
RECENT_EVENTS_KEY = "recent_events"
RECENT_EVENTS_LIMIT = 10
HEARTBEAT_TIMEOUT = 60 * 20  # seconds
EVENT_TTL = 300  # seconds

def push_event(event):
    r = get_redis_connection()
    event.update({"timestamp": int(time.time())})
    r.lpush(RECENT_EVENTS_KEY, json.dumps(event))
    r.ltrim(RECENT_EVENTS_KEY, 0, RECENT_EVENTS_LIMIT - 1)

def setup_multiplayer_session():
    r = get_redis_connection()
    uid, username = prompt_username()
    heartbeat()
    show_recent_events(r, uid)
    return r, uid, username

@st.cache_resource
def get_redis_connection():
    cfg = st.secrets[os.getenv("ENV", "redis-cloud")]
    return redis.Redis(
        host=cfg["REDIS_HOST"],
        port=int(cfg["REDIS_PORT"]),
        password=cfg.get("REDIS_PASSWORD", ""),
        decode_responses=True,
    )

def prompt_username():
    if "uid" not in st.session_state:
        st.session_state.uid = str(uuid.uuid4())[:8]

    uid = st.session_state.uid

    if "username" not in st.session_state:
        name = st.text_input("Enter your name:", key="name_input")
        if name:
            st.session_state.username = name
            r = get_redis_connection()
            r.hset(f"user:{uid}", mapping={"name": name})
            push_event({"event": "player_joined", "uid": uid, "name": name})
            st.rerun()
        st.stop()
    
    st.write(f"Your name: {st.session_state.get('username', 'Not set')}")
    return uid, st.session_state.username

def heartbeat():
    if "uid" not in st.session_state:
        return

    uid = st.session_state.uid
    r = get_redis_connection()

    # Update heartbeat in a shared hash
    r.hset("last_active", uid, int(time.time()))

    # Cleanup inactive users
    for user_id, last_active in r.hgetall("last_active").items():
        if int(time.time()) - int(last_active) > HEARTBEAT_TIMEOUT:
            push_event({"event": "player_left", "uid": user_id, "name": r.hget(f"user:{user_id}", "name")})
            # Cleanup games hosted by user
            for key in r.scan_iter("game:*"):
                if key.count(":") == 1 and r.hget(key, "host") == user_id:
                    r.delete(key)
                    r.delete(f"{key}:players")
                    r.delete(f"{key}:round")
                    r.delete(f"{key}:answers")
                    r.delete(f"{key}:state")
            r.delete(f"user:{user_id}")
            r.hdel("last_active", user_id)

def show_recent_events(r, uid):
    if "seen_events" not in st.session_state:
        st.session_state.seen_events = set()

    events = r.lrange(RECENT_EVENTS_KEY, 0, -1)
    for e_json in reversed(events):
        if e_json in st.session_state.seen_events:
            continue
        data = json.loads(e_json)
        # Ignore self events and old events
        if data.get("uid") == uid or data.get("timestamp") < time.time() - EVENT_TTL:
            continue
        st.session_state.seen_events.add(e_json)

        # Event handlers
        if data["event"] == "player_joined":
            st.toast(f"{data['name']} logged in!", icon="🎉")
        elif data["event"] == "player_left":
            st.toast(f"{data['name']} left.", icon="⚠️")
        elif data["event"] == "game_created":
            st.toast(f"Game lobby for {data['game_mode']} created by {data['host_name']}.", icon="🕹️")
        elif data["event"] == "game_started":
            st.toast(f"Game started!", icon="🚀")
