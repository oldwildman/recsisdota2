import streamlit as st

# =========================================================
# ROLES
# =========================================================

ROLES = [
    "Carry",
    "Mid",
    "Off",
    "Soft",
    "Hard"
]

# =========================================================
# FORCE RESET INVALID STATE
# =========================================================

def force_reset_state():

    st.session_state.radiant_picks = {
        role: None
        for role in ROLES
    }

    st.session_state.dire_picks = {
        role: None
        for role in ROLES
    }

    st.session_state.picked_heroes = set()

    st.session_state.banned_heroes = set()

    st.session_state.ban_mode = False

# =========================================================
# INIT STATE
# =========================================================

def init_draft_state():

    # =====================================================
    # INVALID OLD STATE FIX
    # =====================================================

    if (
        "radiant_picks" in st.session_state
        and isinstance(
            st.session_state.radiant_picks,
            list
        )
    ):

        force_reset_state()

    # =====================================================
    # INIT RADIANT
    # =====================================================

    if "radiant_picks" not in st.session_state:

        st.session_state.radiant_picks = {

            role: None

            for role in ROLES
        }

    # =====================================================
    # INIT DIRE
    # =====================================================

    if "dire_picks" not in st.session_state:

        st.session_state.dire_picks = {

            role: None

            for role in ROLES
        }

    # =====================================================
    # INIT PICKED
    # =====================================================

    if "picked_heroes" not in st.session_state:

        st.session_state.picked_heroes = set()

    # =====================================================
    # INIT BANNED
    # =====================================================

    if "banned_heroes" not in st.session_state:

        st.session_state.banned_heroes = set()

    # =====================================================
    # INIT BAN MODE
    # =====================================================

    if "ban_mode" not in st.session_state:

        st.session_state.ban_mode = False

# =========================================================
# PICK HERO
# =========================================================

def pick_hero(
    side,
    role,
    hero_id
):

    if hero_id in st.session_state.banned_heroes:

        return

    # =====================================================
    # OLD HERO
    # =====================================================

    old_hero = None

    if side == "radiant":

        old_hero = (
            st.session_state
            .radiant_picks[role]
        )

    else:

        old_hero = (
            st.session_state
            .dire_picks[role]
        )

    # =====================================================
    # REMOVE OLD
    # =====================================================

    if old_hero is not None:

        st.session_state.picked_heroes.discard(
            old_hero
        )

    # =====================================================
    # SAVE
    # =====================================================

    if side == "radiant":

        st.session_state.radiant_picks[role] = hero_id

    else:

        st.session_state.dire_picks[role] = hero_id

    # =====================================================
    # REGISTER
    # =====================================================

    st.session_state.picked_heroes.add(
        hero_id
    )

# =========================================================
# BAN HERO
# =========================================================

def ban_hero(hero_id):

    st.session_state.banned_heroes.add(
        hero_id
    )

# =========================================================
# RESET
# =========================================================

def reset_draft():

    force_reset_state()

# =========================================================
# TOGGLE BAN MODE
# =========================================================

def toggle_ban_mode():

    st.session_state.ban_mode = (
        not st.session_state.ban_mode
    )

# =========================================================
# HERO AVAILABLE
# =========================================================

def is_hero_available(hero_id):

    if hero_id in st.session_state.picked_heroes:

        return False

    if hero_id in st.session_state.banned_heroes:

        return False

    return True