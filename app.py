import streamlit as st
import session
import styles

# set up config and redis connection
st.set_page_config(page_title="Geo Games", page_icon="🌍", layout="wide")
session.setup_multiplayer_session()

# Apply custom geography theme
styles.apply_birthday_theme()

# Add custom header
styles.add_geography_header("Geo Games", "🌍")

st.markdown("""
<div style="
    background: white;
    padding: 2rem;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
">
    <h2 style="
        color: #1f2937 !important;
        margin-bottom: 1rem !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    ">Welcome to Geo Games</h2>
    <p style="
        color: #6b7280;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    ">
        Choose a game from the sidebar to test your geography knowledge solo or with friends in multiplayer mode.
    </p>
    <div style="
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    ">
        <div style="
            padding: 1.5rem;
            background: white;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            text-align: center;
            transition: all 0.2s ease;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🚩</div>
            <div style="color: #374151; font-weight: 600; font-size: 1rem;">Guess the Flag</div>
        </div>
        <div style="
            padding: 1.5rem;
            background: white;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            text-align: center;
            transition: all 0.2s ease;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🗺️</div>
            <div style="color: #374151; font-weight: 600; font-size: 1rem;">Guess the Capital</div>
        </div>
        <div style="
            padding: 1.5rem;
            background: white;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            text-align: center;
            transition: all 0.2s ease;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🌎</div>
            <div style="color: #374151; font-weight: 600; font-size: 1rem;">Guess the Country</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

styles.add_geography_footer()
