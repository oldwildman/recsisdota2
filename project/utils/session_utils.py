import streamlit as st

# =========================================================
# SESSION INITIALIZATION
# =========================================================

def initialize_session():

    defaults = {

        # AUTH
        "logged_in": False,
        "guest_mode": False,

        "user_id": None,
        "username": None,

        # DRAFT
        "radiant_picks": [None] * 5,
        "dire_picks": [None] * 5,

        "banned_heroes": [],

        "ban_mode": False,

        # UI
        "selected_role": None,

        # RECOMMENDATIONS
        "recommendations": {},
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value