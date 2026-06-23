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
        font-size: 1.75rem !important; /* lowered from 2rem */
        margin-bottom: 1.25rem !important;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }

    h2 {
        font-size: 1.25rem !important; /* slightly smaller */
        color: #374151 !important;
        margin-top: 1rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
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

    /* Buttons - clean and simple. Ensure clickable area, reasonable size */
    .stButton > button {
        background: #059669 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important; /* slightly smaller */
        min-width: 120px !important; /* consistent clickable area */
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
        pointer-events: auto !important;
        z-index: 10 !important;
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

    /* Radio buttons - minimal style, ensure label is clickable */
    .stRadio > label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-shadow: none;
        cursor: pointer !important;
    }

    .stRadio > div {
        background: white;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }

    .stRadio [role="radiogroup"] label {
        background: white;
        padding: 0.6rem 0.9rem;
        border-radius: 6px;
        margin: 0.25rem;
        border: 1px solid #d1d5db;
        transition: all 0.15s ease;
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
        cursor: pointer !important;
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
        padding: 0.5rem 0.75rem !important;
        font-size: 0.95rem !important;
        background: white !important;
        color: #1f2937 !important;
        font-weight: 400 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #059669 !important;
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.08) !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important; /* reduced */
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
        text-shadow: none;
    }

    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="metric-container"] {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Containers */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: white;
        padding: 0.8rem;
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
        padding: 0.9rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        border-left: 4px solid #059669 !important;
    }

    .stError {
        background: #fef2f2 !important;
        color: #991b1b !important;
        border-radius: 8px !important;
        padding: 0.9rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        border-left: 4px solid #dc2626 !important;
    }

    .stWarning {
        background: #fffbeb !important;
        color: #92400e !important;
        border-radius: 8px !important;
        padding: 0.9rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        border-left: 4px solid #f59e0b !important;
    }

    /* Columns */
    [data-testid="column"] {
        background: white;
        padding: 0.9rem;
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
        padding: 0.75rem 0.9rem;
        margin: 0.4rem 0;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        font-weight: 500;
        color: #374151;
        transition: all 0.15s ease;
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


def apply_birthday_theme():
    """Apply a cheerful birthday theme with pastel colors and normal-sized UI elements."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #FFF1F8 0%, #FFF8E7 50%, #F0FFF4 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-attachment: fixed;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #0f172a !important;
        font-weight: 700 !important;
        text-shadow: none;
    }

    h1 { font-size: 1.8rem !important; margin-bottom: 1.2rem !important; }
    h2 { font-size: 1.3rem !important; color: #334155 !important; }
    h3 { font-size: 1.1rem !important; color: #475569 !important; }

    /* Fun header accent with balloons */
    .stTitle {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Buttons - birthday colors, normal size, friendly and easy to click */
    .stButton > button {
        background: linear-gradient(90deg, #FF8BA7 0%, #FFD6A5 100%) !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        min-width: 130px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 12px rgba(255,139,167,0.2) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        pointer-events: auto !important;
        z-index: 10 !important;
        height: auto !important;
        line-height: 1.2 !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(255,139,167,0.25) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    .stButton > button:disabled {
        background: linear-gradient(90deg, #f3e8ff 0%, #fce7f3 100%) !important;
        color: #9ca3af !important;
        box-shadow: none !important;
        cursor: not-allowed;
    }

    /* Radio buttons - birthday theme */
    .stRadio > label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
    }

    .stRadio > div {
        background: rgba(255,255,255,0.95);
        padding: 0.75rem;
        border-radius: 12px;
        border: 2px solid #FFD6A5;
    }

    .stRadio [role="radiogroup"] label {
        background: white;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin: 0.35rem;
        border: 2px solid #FFE8D1;
        transition: all 0.15s ease;
        cursor: pointer;
        font-weight: 600;
        color: #0f172a !important;
        font-size: 0.95rem !important;
    }

    .stRadio [role="radiogroup"] label:hover {
        background: #FFF5EB;
        border-color: #FF8BA7;
        transform: translateY(-2px);
    }

    .stRadio [role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #FFE8D1 0%, #FFD6A5 100%);
        color: #C2185B !important;
        border-color: #FF6B9D;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(255,139,167,0.2);
    }

    /* Checkboxes */
    .stCheckbox > label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        cursor: pointer !important;
    }

    .stCheckbox > div {
        background: rgba(255,255,255,0.9);
        padding: 0.6rem;
        border-radius: 8px;
        border: 2px solid #FFE8D1;
    }

    /* Sliders */
    .stSlider > label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Text input */
    .stTextInput > label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    .stTextInput > div > div > input {
        border: 2px solid #FFE8D1 !important;
        border-radius: 10px !important;
        padding: 0.6rem 0.8rem !important;
        font-size: 0.95rem !important;
        background: white !important;
        color: #0f172a !important;
        font-weight: 400 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #FF8BA7 !important;
        box-shadow: 0 0 0 3px rgba(255,139,167,0.12) !important;
    }

    /* Metrics - birthday themed */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        color: #FF6B9D !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.95);
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #FFD6A5;
        box-shadow: 0 2px 8px rgba(255,139,167,0.1);
    }

    /* Cards */
    .card-small {
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 2px solid #FFE8D1 !important;
        background: rgba(255,255,255,0.95) !important;
        box-shadow: 0 2px 8px rgba(255,139,167,0.08) !important;
    }

    /* Confetti accent (subtle) */
    .confetti {
        background-image: radial-gradient(circle at 10% 20%, rgba(255,203,164,0.4) 3px, transparent 4px),
                          radial-gradient(circle at 80% 30%, rgba(255,133,133,0.35) 3px, transparent 4px),
                          radial-gradient(circle at 40% 80%, rgba(167,139,250,0.3) 3px, transparent 4px);
        background-size: 150px 150px, 170px 170px, 130px 130px;
        background-repeat: repeat;
        opacity: 0.15;
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 0;
    }

    /* Columns/cards */
    [data-testid="column"] {
        background: rgba(255,255,255,0.95);
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 2px solid #FFE8D1 !important;
    }

    /* Success/Error messages */
    .stSuccess {
        background: #F0FFF4 !important;
        color: #065f46 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border-left: 4px solid #10b981 !important;
    }

    .stError {
        background: #FEE2E2 !important;
        color: #991b1b !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border-left: 4px solid #ef4444 !important;
    }

    .stWarning {
        background: #FFFBEB !important;
        color: #92400e !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        border-left: 4px solid #f59e0b !important;
    }

    /* Main container styling */
    .main {
        background: transparent;
    }

    </style>
    """, unsafe_allow_html=True)


def add_geography_header(title, icon="🌍"):
    """Add a simple, clean header"""
    st.title(f"{icon} {title}")


def add_birthday_header(title, icon="🎉"):
    """Add a birthday-style header with confetti background"""
    st.markdown(f"""
    <div style="position: relative; margin-bottom: 2rem;">
      <div class="confetti"></div>
      <div style="position: relative; z-index: 1;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem; text-align: center;">{icon}</div>
        <h1 style="text-align: center; margin: 0; color: #FF6B9D;">{title}</h1>
      </div>
    </div>
    """, unsafe_allow_html=True)


def add_score_card(score_text):
    """Add a clean score display"""
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.95);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #FFD6A5;
        box-shadow: 0 2px 8px rgba(255,139,167,0.1);
        margin: 1rem 0;
    ">
        <div style="
            color: #9ca3af;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        ">Score</div>
        <div style="
            color: #FF6B9D;
            font-size: 1.8rem;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
        ">{score_text}</div>
    </div>
    """, unsafe_allow_html=True)


def add_lobby_card(game_id, host_name, num_players=1):
    """Add a clean lobby card"""
    st.markdown(f"""
    <div class="card-small" style="
        margin: 0.75rem 0;
    ">
        <div style="color: #0f172a; margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 700;">
            🎮 {host_name}'s Game
        </div>
        <div style="color: #6b7280; font-size: 0.9rem; font-weight: 600;">
            <strong>ID:</strong> {game_id} · <strong>Players:</strong> {num_players}
        </div>
    </div>
    """, unsafe_allow_html=True)


def add_geography_footer():
    """Add a clean footer"""
    st.markdown("""
    <div style="
        margin-top: 2rem;
        padding: 1.25rem;
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
        background: rgba(255,255,255,0.95);
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #FFD6A5;
        box-shadow: 0 2px 8px rgba(255,139,167,0.1);
        margin: 1rem 0;
    ">
        <div style="
            color: #FF6B9D;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #FFE8D1;
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
        bg_color = "#FFE8D1" if is_current else "white"
        border_color = "#FF6B9D" if is_current else "#FFD6A5"
        font_weight = "700" if is_current else "600"

        st.markdown(f"""
        <div style="
            background: {bg_color};
            padding: 0.8rem 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border: 2px solid {border_color};
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div style="color: #0f172a; font-weight: {font_weight}; font-size: 1rem;">
                {medal}<span style="color: #9ca3af; margin-right: 0.75rem;">#{rank}</span>{player['name']}
            </div>
            <div style="color: #FF6B9D; font-weight: 700; font-size: 1.1rem;">
                {player['score']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
