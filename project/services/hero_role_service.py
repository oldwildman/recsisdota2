import ast

import streamlit as st

from utils.loaders import load_hero_stats

# =========================================================
# ROLE MAP
# =========================================================

ROLE_MAP = {

    "Carry": [
        "Carry"
    ],

    "Mid": [
        "Nuker",
        "Carry"
    ],

    "Off": [
        "Initiator",
        "Durable"
    ],

    "Soft": [
        "Support",
        "Disabler"
    ],

    "Hard": [
        "Support"
    ]
}

# =========================================================
# LOAD HERO ROLES
# =========================================================

@st.cache_data
def build_role_database():

    df = load_hero_stats()

    role_db = {}

    for _, row in df.iterrows():

        try:

            hero_id = int(row["id"])

            roles_raw = row["roles"]

            roles = ast.literal_eval(
                roles_raw
            )

            role_db[hero_id] = roles

        except Exception:

            continue

    return role_db

# =========================================================
# ROLE SCORE
# =========================================================

def get_role_score(
    hero_id,
    role
):

    role_db = build_role_database()

    hero_roles = role_db.get(
        hero_id,
        []
    )

    target_roles = ROLE_MAP.get(
        role,
        []
    )

    matches = 0

    for r in target_roles:

        if r in hero_roles:

            matches += 1

    # =====================================================
    # SCORE
    # =====================================================

    if len(target_roles) == 0:

        return 0

    return matches / len(target_roles)

# =========================================================
# VALID ROLE PICK
# =========================================================

def is_valid_role_pick(
    hero_id,
    role
):

    score = get_role_score(
        hero_id,
        role
    )

    return score >= 0.5