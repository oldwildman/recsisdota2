import streamlit as st

from utils.hero_utils import get_hero_image
from utils.loaders import load_heroes

from services.recommendation_service import (
    get_recommendations
)

# =========================================================
# SETTINGS
# =========================================================

MAX_VISIBLE_HEROES = 999

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
# INIT STATE
# =========================================================

def initialize_draft_state():

    if "draft_state" not in st.session_state:

        st.session_state["draft_state"] = {

            "radiant": {},

            "dire": {}
        }

# =========================================================
# HERO PARSER
# =========================================================

def parse_hero_row(row):

    row_dict = row.to_dict()

    # =====================================================
    # HERO ID
    # =====================================================

    hero_id = None

    for key in [

        "hero_id",
        "id",
        "HeroID",
        "heroid"
    ]:

        if key in row_dict:

            try:

                hero_id = int(
                    row_dict[key]
                )

                break

            except Exception:

                pass

    # =====================================================
    # FALLBACK ID
    # =====================================================

    if hero_id is None:

        for value in row_dict.values():

            if isinstance(
                value,
                (int, float)
            ):

                hero_id = int(value)

                break

    # =====================================================
    # HERO NAME
    # =====================================================

    hero_name = "Unknown"

    for key in [

        "localized_name",
        "hero_name",
        "name",
        "display_name"
    ]:

        if key in row_dict:

            hero_name = str(
                row_dict[key]
            )

            break

    # =====================================================
    # FALLBACK NAME
    # =====================================================

    if hero_name == "Unknown":

        for value in row_dict.values():

            if isinstance(value, str):

                if len(value) > 1:

                    hero_name = value

                    break

    return hero_id, hero_name

# =========================================================
# TOP METRICS
# =========================================================

def calculate_top_metrics():

    draft_state = st.session_state["draft_state"]

    radiant_picks = []

    dire_picks = []

    for hero in draft_state["radiant"].values():

        if hero:

            radiant_picks.append(
                hero["hero_id"]
            )

    for hero in draft_state["dire"].values():

        if hero:

            dire_picks.append(
                hero["hero_id"]
            )

    # =====================================================
    # LIVE METRICS
    # =====================================================

    synergy = min(
        len(radiant_picks) * 14,
        100
    )

    counter = min(
        len(dire_picks) * 11,
        100
    )

    winrate = 50 + (
        synergy - counter
    ) * 0.3

    winrate = round(

        max(
            1,
            min(winrate, 99)
        )
    )

    return {

        "winrate": f"{winrate}%",

        "synergy": synergy,

        "counter": counter
    }

# =========================================================
# MAIN LAYOUT
# =========================================================

def render_draft_layout():

    initialize_draft_state()

    render_top_bar()

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    # =====================================================
    # BOARD
    # =====================================================

    left_side, divider, right_side = st.columns(
        [5, 0.08, 5]
    )

    # =====================================================
    # RADIANT
    # =====================================================

    with left_side:

        st.markdown(
            """
            <div class="team-header-radiant">
                ✦ RADIANT ✦
            </div>
            """,
            unsafe_allow_html=True
        )

        radiant_cols = st.columns(5)

        for i in range(5):

            with radiant_cols[i]:

                render_slot(

                    side="radiant",

                    role=ROLES[i],

                    idx=i
                )

    # =====================================================
    # DIVIDER
    # =====================================================

    with divider:

        st.markdown(
            """
            <div class="draft-divider"></div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # DIRE
    # =====================================================

    with right_side:

        st.markdown(
            """
            <div class="team-header-dire">
                ✦ DIRE ✦
            </div>
            """,
            unsafe_allow_html=True
        )

        dire_cols = st.columns(5)

        for i in range(5):

            with dire_cols[i]:

                render_slot(

                    side="dire",

                    role=ROLES[i],

                    idx=i
                )

# =========================================================
# TOP BAR
# =========================================================

def render_top_bar():

    metrics = calculate_top_metrics()

    col1, col2, col3, col4, col5 = st.columns(
        [2, 1, 1, 1, 1.5]
    )

    # =====================================================
    # TITLE
    # =====================================================

    with col1:

        st.markdown(
            """
            <div class="main-title">
                Draft Arena
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # METRICS
    # =====================================================

    with col2:

        st.metric(
            "Win Chance",
            metrics["winrate"]
        )

    with col3:

        st.metric(
            "Synergy",
            metrics["synergy"]
        )

    with col4:

        st.metric(
            "Counter",
            metrics["counter"]
        )

    # =====================================================
    # RESET
    # =====================================================

    with col5:

        if st.button(
            "RESET DRAFT",
            use_container_width=True
        ):

            st.session_state["draft_state"] = {

                "radiant": {},

                "dire": {}
            }

            st.rerun()

# =========================================================
# SLOT
# =========================================================

def render_slot(

    side,
    role,
    idx
):

    # =====================================================
    # ROLE
    # =====================================================

    st.markdown(
        f"""
        <div class="role-title">
            {role}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CURRENT PICK
    # =====================================================

    current_pick = (
        st.session_state["draft_state"]
        .get(side, {})
        .get(role)
    )

    # =====================================================
    # PICK SLOT
    # =====================================================

    if current_pick:

        image_path = get_hero_image(
            current_pick["hero_id"]
        )

        if image_path:

            st.image(
                image_path,
                width=90
            )

        st.success(
            current_pick["hero_name"]
        )

    else:

        st.markdown(
            """
            <div class="pick-slot-small">
                PICK
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # SEARCH
    # =====================================================

    search_value = st.text_input(

        "",

        placeholder="Hero...",

        key=f"{side}_{idx}"
    )

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    render_recommendation_row(

        side=side,

        role=role,

        idx=idx,

        search_value=search_value
    )

# =========================================================
# RECOMMENDATIONS
# =========================================================

def render_recommendation_row(

    side,
    role,
    idx,
    search_value=""
):

    # =====================================================
    # LOAD HEROES
    # =====================================================

    try:

        heroes_df = load_heroes()

    except Exception as e:

        st.error(
            f"Heroes loading error: {e}"
        )

        return

    # =====================================================
    # DRAFT STATE
    # =====================================================

    draft_state = st.session_state["draft_state"]

    if side == "radiant":

        ally_team = draft_state["radiant"]

        enemy_team = draft_state["dire"]

    else:

        ally_team = draft_state["dire"]

        enemy_team = draft_state["radiant"]

    # =====================================================
    # PICKS
    # =====================================================

    ally_picks = []

    enemy_picks = []

    for hero_data in ally_team.values():

        if hero_data:

            ally_picks.append(
                hero_data["hero_id"]
            )

    for hero_data in enemy_team.values():

        if hero_data:

            enemy_picks.append(
                hero_data["hero_id"]
            )

    # =====================================================
    # HEROES
    # =====================================================

    heroes = []

    for _, row in heroes_df.iterrows():

        try:

            hero_id, hero_name = parse_hero_row(row)

            heroes.append({

                "hero_id": hero_id,

                "hero_name": hero_name
            })

        except Exception:

            continue

    # =====================================================
    # REMOVE PICKED HEROES
    # =====================================================

    picked_ids = []

    for team_name in [

        "radiant",
        "dire"
    ]:

        for hero_data in draft_state[team_name].values():

            if hero_data:

                picked_ids.append(
                    hero_data["hero_id"]
                )

    heroes = [

        hero for hero in heroes

        if hero["hero_id"] not in picked_ids
    ]

    # =====================================================
    # SEARCH
    # =====================================================

    if search_value:

        heroes = [

            hero for hero in heroes

            if search_value.lower()
            in hero["hero_name"].lower()
        ]

    # =====================================================
    # LIMIT
    # =====================================================

    heroes = heroes[:MAX_VISIBLE_HEROES]

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    candidate_ids = [

        hero["hero_id"]

        for hero in heroes
    ]

    recommendations = get_recommendations(

        candidate_heroes=candidate_ids,

        ally_picks=ally_picks,

        enemy_picks=enemy_picks,

        role=role
    )

    # =====================================================
    # MAP
    # =====================================================

    recommendation_map = {

        rec["hero_id"]: rec

        for rec in recommendations
    }

    # =====================================================
    # SORT HEROES BY SCORE
    # =====================================================

    heroes = sorted(

        heroes,

        key=lambda hero:

            recommendation_map.get(
                hero["hero_id"],
                {}
            ).get(
                "score",
                0
            ),

        reverse=True
    )

    # =====================================================
    # SCROLL
    # =====================================================

    with st.container(height=420):

        for hero in heroes:

            hero_id = hero["hero_id"]

            hero_name = hero["hero_name"]

            recommendation = recommendation_map.get(
                hero_id,
                {}
            )

            score = recommendation.get(
                "score",
                0
            )

            synergy = recommendation.get(
                "synergy",
                0
            )

            counter = recommendation.get(
                "counter",
                0
            )

            role_score = recommendation.get(
                "role_score",
                0
            )

            image_path = get_hero_image(
                hero_id
            )

            # =================================================
            # CARD
            # =================================================

            with st.container():

                card_col1, card_col2 = st.columns(
                    [1, 2]
                )

                # =============================================
                # IMAGE
                # =============================================

                with card_col1:

                    if image_path:

                        st.image(
                            image_path,
                            width=70
                        )

                # =============================================
                # INFO
                # =============================================

                with card_col2:

                    st.markdown(
                        f"""
                        ### {hero_name}

                        **Score:** {score}

                        **Role:** {role_score}

                        **Synergy:** {synergy}

                        **Counter:** {counter}
                        """
                    )

                    # =========================================
                    # PICK BUTTON
                    # =========================================

                    if st.button(

                        f"PICK {hero_name}",

                        key=f"pick_{side}_{role}_{hero_id}"
                    ):

                        st.session_state["draft_state"][side][role] = {

                            "hero_id": hero_id,

                            "hero_name": hero_name
                        }

                        st.rerun()

                st.markdown("---")