import streamlit as st
import session

# set up config and redis connection
st.set_page_config(page_title="Geo Games", page_icon="🌍", layout="centered")
st.title("🌍 Geo Games")
session.setup_multiplayer_session()

st.markdown(
    "Welcome! Pick a game from the **sidebar**. Start with **Guess the Flag** to test your geography skills."
)
