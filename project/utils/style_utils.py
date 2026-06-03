import streamlit as st

# =========================================================
# GLOBAL STYLE SYSTEM
# =========================================================

def load_global_styles():

    st.markdown(
        """
        <style>

        /* =======================================================
           GLOBAL
        ======================================================= */

        .stApp {

            background:
                radial-gradient(
                    circle at top left,
                    #1f1147 0%,
                    #0b1020 45%,
                    #05070f 100%
                );

            color: white;
        }

        /* =======================================================
           REMOVE STREAMLIT UI
        ======================================================= */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        /* =======================================================
           AUTH
        ======================================================= */

        .auth-title {

            text-align: center;

            font-size: 72px;

            font-weight: 900;

            margin-top: 40px;

            margin-bottom: 15px;

            background:
                linear-gradient(
                    90deg,
                    #ff004c,
                    #7c3aed,
                    #00e5ff
                );

            -webkit-background-clip: text;

            -webkit-text-fill-color: transparent;

            letter-spacing: 2px;
        }

        .auth-subtitle {

            text-align: center;

            color: #94a3b8;

            font-size: 18px;

            margin-bottom: 45px;
        }

        /* =======================================================
           GLASS CARD
        ======================================================= */

        div[data-testid="stTabs"] {

            background:
                rgba(255,255,255,0.05);

            border:
                1px solid rgba(255,255,255,0.08);

            border-radius: 24px;

            padding: 24px;

            backdrop-filter: blur(24px);

            box-shadow:
                0 0 35px rgba(124,58,237,0.15);
        }

        /* =======================================================
           TABS
        ======================================================= */

        button[data-baseweb="tab"] {

            color: #cbd5e1 !important;

            font-weight: 700 !important;
        }

        /* =======================================================
           INPUT LABELS
        ======================================================= */

        .stTextInput label {

            color: #cbd5e1 !important;

            font-weight: 600 !important;
        }

        /* =======================================================
           INPUT ROOT
        ======================================================= */

        div[data-testid="stTextInputRootElement"] {

            background:
                rgba(255,255,255,0.06) !important;

            border:
                1px solid rgba(255,255,255,0.08) !important;

            border-radius: 14px !important;

            overflow: hidden !important;
        }

        /* =======================================================
           INPUT
        ======================================================= */

        div[data-testid="stTextInputRootElement"] input {

            background: transparent !important;

            color: white !important;

            -webkit-text-fill-color: white !important;

            caret-color: white !important;

            font-weight: 600 !important;
        }

        /* =======================================================
           PLACEHOLDER
        ======================================================= */

        div[data-testid="stTextInputRootElement"] input::placeholder {

            color: #94a3b8 !important;

            opacity: 1 !important;
        }

        /* =======================================================
           PASSWORD ICON
        ======================================================= */

        div[data-testid="stTextInputRootElement"] svg {

            fill: #cbd5e1 !important;
        }

        /* =======================================================
           BUTTONS
        ======================================================= */

        .stButton > button {

            width: 100%;

            border: none;

            border-radius: 14px;

            padding: 12px;

            font-weight: 700;

            background:
                linear-gradient(
                    90deg,
                    #7c3aed,
                    #00c2ff
                );

            color: white;

            transition: 0.2s;

            box-shadow:
                0 0 18px rgba(124,58,237,0.25);
        }

        .stButton > button:hover {

            transform: translateY(-2px);

            box-shadow:
                0 0 30px rgba(0,194,255,0.35);
        }

        /* =======================================================
           ALERTS
        ======================================================= */

        .stAlert {

            border-radius: 16px;
        }

        /* =======================================================
           SIDEBAR
        ======================================================= */

        section[data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    rgba(18,24,38,0.95),
                    rgba(9,12,20,0.98)
                );

            border-right:
                1px solid rgba(255,255,255,0.08);
        }

        /* =======================================================
           METRICS
        ======================================================= */

        div[data-testid="metric-container"] {

            background:
                rgba(255,255,255,0.04);

            border:
                1px solid rgba(255,255,255,0.05);

            padding: 10px;

            border-radius: 16px;
        }

        /* =======================================================
           ROLE TITLE
        ======================================================= */

        .role-title {

            text-align: center;

            font-size: 13px;

            font-weight: 700;

            color: #cbd5e1;

            margin-bottom: 8px;
        }

        /* =======================================================
           PICK SLOT
        ======================================================= */

        .pick-slot-small {

            height: 68px;

            border-radius: 14px;

            background:
                rgba(255,255,255,0.05);

            border:
                1px solid rgba(255,255,255,0.08);

            display: flex;

            align-items: center;

            justify-content: center;

            margin-bottom: 10px;

            color: #64748b;

            font-size: 12px;

            font-weight: 700;

            transition: 0.2s;
        }

        .pick-slot-small:hover {

            border:
                1px solid #7c3aed;

            box-shadow:
                0 0 15px rgba(124,58,237,0.25);
        }

        /* =======================================================
           HERO MINI CARD
        ======================================================= */

        .hero-mini-card {

            background:
                rgba(255,255,255,0.04);

            border:
                1px solid rgba(255,255,255,0.05);

            border-radius: 12px;

            padding: 6px;

            margin-bottom: 6px;

            transition: 0.2s;

            cursor: pointer;
        }

        .hero-mini-card:hover {

            border:
                1px solid #00c2ff;

            transform: translateY(-2px);

            box-shadow:
                0 0 12px rgba(0,194,255,0.18);
        }

        /* =======================================================
           HERO IMAGE
        ======================================================= */

        .hero-mini-image {

            width: 100%;

            height: 42px;

            border-radius: 8px;

            margin-bottom: 4px;

            background:
                linear-gradient(
                    135deg,
                    #7c3aed,
                    #00c2ff
                );
        }

        /* =======================================================
           HERO NAME
        ======================================================= */

        .hero-mini-name {

            font-size: 11px;

            font-weight: 700;

            color: white;
        }

        /* =======================================================
           HERO SCORE
        ======================================================= */

        .hero-mini-score {

            font-size: 10px;

            font-weight: 700;

            color: #00e676;
        }

        /* =======================================================
           SCROLLBAR
        ======================================================= */

        ::-webkit-scrollbar {

            width: 8px;
        }

        ::-webkit-scrollbar-thumb {

            background: #7c3aed;

            border-radius: 10px;
        }

        /* =======================================================
           AUTOFILL FIX
        ======================================================= */

        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus {

            -webkit-text-fill-color: white !important;

            transition:
                background-color 9999s ease-in-out 0s;

            box-shadow:
                0 0 0px 1000px transparent inset !important;
        }
                /* =======================================================
           DRAFT BOARD
        ======================================================= */

        .draft-team-title {

            font-size: 20px;

            font-weight: 800;

            text-align: center;

            margin-bottom: 10px;

            color: white;
        }

        /* =======================================================
           ROLE TITLE
        ======================================================= */

        .role-title {

            text-align: center;

            font-size: 12px;

            font-weight: 700;

            color: #cbd5e1;

            margin-bottom: 6px;
        }

        /* =======================================================
           PICK SLOT
        ======================================================= */

        .pick-slot-small {

            height: 68px;

            border-radius: 14px;

            background:
                rgba(255,255,255,0.05);

            border:
                1px solid rgba(255,255,255,0.08);

            display: flex;

            align-items: center;

            justify-content: center;

            margin-bottom: 8px;

            color: #64748b;

            font-size: 12px;

            font-weight: 700;

            transition: 0.2s;
        }

        .pick-slot-small:hover {

            border:
                1px solid #7c3aed;

            box-shadow:
                0 0 15px rgba(124,58,237,0.25);
        }

        /* =======================================================
           HERO MINI CARD
        ======================================================= */

        .hero-mini-card {

            background:
                rgba(255,255,255,0.04);

            border:
                1px solid rgba(255,255,255,0.05);

            border-radius: 10px;

            padding: 5px;

            margin-bottom: 5px;

            transition: 0.2s;

            cursor: pointer;
        }

        .hero-mini-card:hover {

            border:
                1px solid #00c2ff;

            transform: translateY(-2px);

            box-shadow:
                0 0 10px rgba(0,194,255,0.18);
        }

        /* =======================================================
           HERO IMAGE
        ======================================================= */

        .hero-mini-image {

            width: 100%;

            height: 40px;

            border-radius: 8px;

            margin-bottom: 4px;

            background:
                linear-gradient(
                    135deg,
                    #7c3aed,
                    #00c2ff
                );
        }

        /* =======================================================
           HERO NAME
        ======================================================= */

        .hero-mini-name {

            font-size: 10px;

            font-weight: 700;

            color: white;

            text-align: center;
        }

        /* =======================================================
           HERO SCORE
        ======================================================= */

        .hero-mini-score {

            font-size: 10px;

            font-weight: 700;

            color: #00e676;

            text-align: center;
        }

        /* =======================================================
           SEARCH INPUT COMPACT
        ======================================================= */

        div[data-testid="stTextInputRootElement"] {

            min-height: 40px !important;
        }

        div[data-testid="stTextInputRootElement"] input {

            padding-top: 8px !important;

            padding-bottom: 8px !important;

            font-size: 12px !important;
        }
                /* =======================================================
           MAIN TITLE
        ======================================================= */

        .main-title {

            font-size: 42px;

            font-weight: 900;

            color: white;

            margin-top: 10px;
        }

        /* =======================================================
           TEAM HEADERS
        ======================================================= */

        .team-header-radiant {

            text-align: center;

            font-size: 34px;

            font-weight: 900;

            color: #22ff88;

            margin-bottom: 30px;

            text-shadow:
                0 0 20px rgba(34,255,136,0.45);
        }

        .team-header-dire {

            text-align: center;

            font-size: 34px;

            font-weight: 900;

            color: #ff5c5c;

            margin-bottom: 30px;

            text-shadow:
                0 0 20px rgba(255,92,92,0.45);
        }

        /* =======================================================
           CENTER DIVIDER
        ======================================================= */

        .draft-divider {

            width: 2px;

            height: 100%;

            min-height: 700px;

            margin: auto;

            background:
                linear-gradient(
                    180deg,
                    rgba(0,0,0,0),
                    rgba(0,194,255,0.9),
                    rgba(0,0,0,0)
                );

            box-shadow:
                0 0 20px rgba(0,194,255,0.35);
        }

        /* =======================================================
           TEAM PANELS
        ======================================================= */

        div[data-testid="column"] {

            position: relative;
        }
        /* =======================================================
   HERO CARD INFO
======================================================= */

.hero-card-info {

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid rgba(255,255,255,0.05);

    border-top:none;

    border-radius:
        0 0 12px 12px;

    padding:8px;

    margin-bottom:12px;

    text-align:center;
}

/* =======================================================
   STREAMLIT IMAGE
======================================================= */

div[data-testid="stImage"] img {

    border-radius:12px 12px 0 0;

    transition:0.2s;
}

div[data-testid="stImage"] img:hover {

    transform:scale(1.02);

    box-shadow:
        0 0 18px rgba(0,194,255,0.35);
}
        /* =======================================================
           RECOMMENDATION SCROLL
        ======================================================= */

        .recommendation-scroll {

            max-height: 520px;

            overflow-y: auto;

            overflow-x: hidden;

            padding-right: 4px;
        }

        /* =======================================================
           SCROLLBAR
        ======================================================= */

        .recommendation-scroll::-webkit-scrollbar {

            width: 6px;
        }

        .recommendation-scroll::-webkit-scrollbar-thumb {

            background: #7c3aed;

            border-radius: 12px;
        }
        

        </style>
        """,
        unsafe_allow_html=True
    )