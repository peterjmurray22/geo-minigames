import streamlit as st

st.set_page_config(page_title="Geo Games", page_icon="🌍", layout="centered")

st.title("🌍 Geo Games")
st.markdown(
    "Welcome! Pick a game from the **sidebar**. Start with **Guess the Flag** to test your geography skills."
)

with st.expander("How it works"):
    st.write(
        "- Each game is a separate **page** under the `pages/` folder.\n"
        "- Streamlit reruns the script top-to-bottom whenever you interact.\n"
        "- Use `st.session_state` to keep score and persist state across reruns."
    )

st.divider()
st.subheader("Tips")
st.write(
    "- Add more minigames by creating new files in the `pages/` folder.\n"
    "- Use `st.cache_data` for loading static data (e.g., country list).\n"
    "- Keep UI snappy with columns, buttons, and feedback messages."
)
