import streamlit as st

from utils.style_utils import load_global_styles
from utils.session_utils import initialize_session

from components.auth_components import render_auth_page

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Dota Draft AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# INIT
# =========================================================

load_global_styles()

initialize_session()

# =========================================================
# AUTH GATE
# =========================================================

if not st.session_state.logged_in:

    render_auth_page()

    st.stop()

# =========================================================
# MAIN APP
# =========================================================

st.sidebar.markdown(
    f"""
    ### 👤 {st.session_state.username}
    """
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.username = None

    st.session_state.guest_mode = False

    st.rerun()

# =========================================================
# TEMP PLACEHOLDER
# =========================================================

from components.draft_layout import (
    render_draft_layout
)

render_draft_layout()

st.success("Authentication system connected successfully")

st.write("Next step: Draft recommendation interface")