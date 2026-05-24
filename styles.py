import streamlit as st

def apply_geography_theme():
    """Apply clean, minimal design inspired by geography reference sites"""
    st.markdown("""
    <style>
    /* Import clean, professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Main app - light green background */
    .stApp {
        background: #E8F5E9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Headers - simple and clean */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #1a1a1a !important;
        font-weight: 700 !important;
        text-shadow: none;
    }

    h1 {
        font-size: 2rem !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.75rem;
    }

    h2 {
        font-size: 1.5rem !important;
        color: #374151 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
        color: #4b5563 !important;
    }

    /* Sidebar - clean gray */
    [data-testid="stSidebar"] {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #374151 !important;
        font-weight: 500 !important;
        text-shadow: none;
    }

    [data-testid="stSidebar"] a {
        color: #1f2937 !important;
        text-decoration: none;
        transition: color 0.2s ease;
        font-size: 0.95rem !important;
    }

    [data-testid="stSidebar"] a:hover {
        color: #059669 !important;
    }

    /* Buttons - clean and simple */
    .stButton > button {
        background: #059669 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.25rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease !important;
        cursor: pointer;
    }

    .stButton > button:hover {
        background: #047857 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    .stButton > button:disabled {
        background: #d1d5db !important;
        color: #9ca3af !important;
        cursor: not-allowed;
        box-shadow: none !important;
    }

    /* Radio buttons - minimal style */
    .stRadio > label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-shadow: none;
    }

    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }

    .stRadio [role="radiogroup"] label {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.25rem;
        border: 1px solid #d1d5db;
        transition: all 0.2s ease;
        cursor: pointer;
        font-weight: 500;
        color: #374151 !important;
    }

    .stRadio [role="radiogroup"] label:hover {
        background: #f9fafb;
        border-color: #059669;
    }

    .stRadio [role="radiogroup"] label[data-checked="true"] {
        background: #ecfdf5;
        color: #059669 !important;
        border-color: #059669;
        font-weight: 600;
    }

    /* Checkboxes */
    .stCheckbox > label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    .stCheckbox > div {
        background: white;
        padding: 0.5rem;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
    }

    /* Sliders */
    .stSlider > label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Text input */
    .stTextInput > label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    .stTextInput > div > div > input {
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.625rem 0.875rem !important;
        font-size: 0.95rem !important;
        background: white !important;
        color: #1f2937 !important;
        font-weight: 400 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1) !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
        text-shadow: none;
    }

    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Containers */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }

    /* Image containers - clean borders */
    [data-testid="stImage"] {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }

    /* Success/Error messages */
    .stSuccess {
        background: #ecfdf5 !important;
        color: #065f46 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border-left: 4px solid #059669 !important;
    }

    .stError {
        background: #fef2f2 !important;
        color: #991b1b !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border-left: 4px solid #dc2626 !important;
    }

    .stWarning {
        background: #fffbeb !important;
        color: #92400e !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border-left: 4px solid #f59e0b !important;
    }

    /* Columns */
    [data-testid="column"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }

    /* Custom list styling */
    .stMarkdown ul {
        list-style-type: none;
        padding-left: 0;
    }

    .stMarkdown ul li {
        background: white;
        padding: 0.875rem 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        font-weight: 500;
        color: #374151;
        transition: all 0.2s ease;
    }

    .stMarkdown ul li:hover {
        border-color: #d1d5db;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Remove any background textures */
    .stApp::before {
        display: none;
    }

    /* Clean text styling */
    p, span, div {
        color: #374151;
    }

    .stMarkdown {
        color: #374151 !important;
    }

    /* Remove text shadows */
    .main * {
        text-shadow: none;
    }

    /* Clean background */
    .main {
        background: #E8F5E9;
    }
    </style>
    """, unsafe_allow_html=True)


def add_geography_header(title, icon="🌍"):
    """Add a simple, clean header"""
    st.title(f"{icon} {title}")


def add_score_card(score_text):
    """Add a clean score display"""
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin: 1rem 0;
    ">
        <div style="
            color: #6b7280;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        ">Score</div>
        <div style="
            color: #1f2937;
            font-size: 2rem;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
        ">{score_text}</div>
    </div>
    """, unsafe_allow_html=True)


def add_lobby_card(game_id, host_name, num_players=1):
    """Add a clean lobby card"""
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin: 0.75rem 0;
    ">
        <div style="color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 600;">
            🎮 {host_name}'s Game
        </div>
        <div style="color: #6b7280; font-size: 0.875rem; font-weight: 400;">
            <strong>ID:</strong> {game_id} · <strong>Players:</strong> {num_players}
        </div>
    </div>
    """, unsafe_allow_html=True)


def add_geography_footer():
    """Add a clean footer"""
    st.markdown("""
    <div style="
        margin-top: 3rem;
        padding: 2rem;
        text-align: center;
        color: #9ca3af;
        font-size: 0.875rem;
        border-top: 1px solid #e5e7eb;
    ">
        Test your geography knowledge
    </div>
    """, unsafe_allow_html=True)


def show_leaderboard(leaderboard, current_uid=None):
    """Display a live leaderboard during multiplayer games"""
    st.markdown("""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin: 1rem 0;
    ">
        <div style="
            color: #1f2937;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e5e7eb;
        ">🏆 Leaderboard</div>
    """, unsafe_allow_html=True)

    for idx, player in enumerate(leaderboard):
        rank = idx + 1
        medal = ""
        if rank == 1:
            medal = "🥇 "
        elif rank == 2:
            medal = "🥈 "
        elif rank == 3:
            medal = "🥉 "

        is_current = player["uid"] == current_uid
        bg_color = "#ecfdf5" if is_current else "white"
        border_color = "#059669" if is_current else "#e5e7eb"
        font_weight = "700" if is_current else "500"

        st.markdown(f"""
        <div style="
            background: {bg_color};
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            border-radius: 6px;
            border: 1px solid {border_color};
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div style="color: #374151; font-weight: {font_weight};">
                {medal}<span style="color: #9ca3af; margin-right: 0.5rem;">#{rank}</span>{player['name']}
            </div>
            <div style="color: #059669; font-weight: 700; font-size: 1.1rem;">
                {player['score']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
