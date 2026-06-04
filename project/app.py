import base64
import streamlit as st

from utils.style_utils import load_global_styles
from utils.session_utils import initialize_session

from components.auth_components import render_auth_page

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Рекомендательная система Dota 2",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BACKGROUND
# =========================================================

def set_background():

    image_path = "project/assets/backgrounds/background1.jpg"

    with open(image_path, "rb") as image_file:

        encoded = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{

            background:
                linear-gradient(
                    rgba(0, 0, 0, 0.65),
                    rgba(0, 0, 0, 0.65)
                ),
                url("data:image/jpg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# INIT
# =========================================================

set_background()

load_global_styles()

initialize_session()

# =========================================================
# AUTH GATE
# =========================================================

if not st.session_state.logged_in:

    render_auth_page()

    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    f"""
    ### 👤 {st.session_state.username}
    """
)

if st.sidebar.button("Выйти"):

    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.username = None

    st.session_state.guest_mode = False

    st.rerun()

# =========================================================
# MAIN APP
# =========================================================

st.markdown(
    """
    <h1 class="main-title">
        Рекомендательная система выбора героев Dota 2
    </h1>
    """,
    unsafe_allow_html=True
)
# =========================================================
# DRAFT INTERFACE
# =========================================================

from components.draft_layout import (
    render_draft_layout
)

render_draft_layout()

# =========================================================
# STATUS
# =========================================================

st.success(
    "Система успешно запущена"
)
