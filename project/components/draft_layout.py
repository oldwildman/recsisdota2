import streamlit as st

from utils.hero_utils import get_hero_image
from utils.loaders import load_heroes
from services.recommendation_service import (
    calculate_hero_scores
)

from services.recommendation_service import (
    load_synergy_matrix,
    load_counter_matrix
)

from services.hero_role_service import (
    get_role_score
)
from services.recommendation_service import (
    get_recommendations
)
from services.personalization_service import (
    get_personal_score
)

# =========================================================
# SETTINGS
# =========================================================

MAX_VISIBLE_HEROES = 129

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

    synergy_df = load_synergy_matrix()
    counter_df = load_counter_matrix()

    radiant_ids = []
    dire_ids = []

    # =====================================
    # BUILD TEAMS
    # =====================================

    for hero_data in draft_state["radiant"].values():

        if hero_data:

            radiant_ids.append(
                hero_data["hero_id"]
            )

    for hero_data in draft_state["dire"].values():

        if hero_data:

            dire_ids.append(
                hero_data["hero_id"]
            )

    # =====================================
    # RADIANT SCORE
    # =====================================

    radiant_score = 0

    for hero_id in radiant_ids:

        allies = [
            h for h in radiant_ids
            if h != hero_id
        ]

        role_score = 1

        scores = calculate_hero_scores(

            candidate_hero=hero_id,

            ally_picks=allies,

            enemy_picks=dire_ids,

            synergy_df=synergy_df,

            counter_df=counter_df,

            role_score=role_score
        )

        radiant_score += scores["score"]

    # =====================================
    # DIRE SCORE
    # =====================================

    dire_score = 0

    for hero_id in dire_ids:

        allies = [
            h for h in dire_ids
            if h != hero_id
        ]

        role_score = 1

        scores = calculate_hero_scores(

            candidate_hero=hero_id,

            ally_picks=allies,

            enemy_picks=radiant_ids,

            synergy_df=synergy_df,

            counter_df=counter_df,

            role_score=role_score
        )

        dire_score += scores["score"]

    # =====================================
    # NORMALIZATION
    # =====================================

    total = radiant_score + dire_score

    if total > 0:

        radiant_percent = round(
            radiant_score / total * 100,
            1
        )

        dire_percent = round(
            dire_score / total * 100,
            1
        )

    else:

        radiant_percent = 50
        dire_percent = 50

    return {

        "radiant_score": round(
            radiant_score,
            2
        ),

        "dire_score": round(
            dire_score,
            2
        ),

        "radiant_percent": radiant_percent,

        "dire_percent": dire_percent
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

    radiant_score = metrics["radiant_score"]

    dire_score = metrics["dire_score"]

    radiant_percent = metrics["radiant_percent"]

    dire_percent = metrics["dire_percent"]

    title_col, stat1, stat2, stat3, reset_col = st.columns(
        [4, 1, 1, 1, 2]
    )

    # =====================================================
    # TITLE
    # =====================================================

    # =====================================================
    # WIN RATE
    # =====================================================

    with stat1:

        st.metric(
            "Radiant",
            f"{radiant_score}"
        )

    with stat2:

        st.metric(
            "Dire",
            f"{dire_score}"
        )
    # =====================================================
    # RESET
    # =====================================================

    with reset_col:

        if st.button(
            "Сбросить драфт",
            use_container_width=True
        ):

            st.session_state["draft_state"] = {
                "radiant": {},
                "dire": {}
            }

            st.rerun()

    # =====================================================
    # PROGRESS BAR
    # =====================================================

    left, center, right = st.columns(
        [2, 4, 2]
    )

    with center:

        st.progress(
            radiant_percent / 100
        )   

    st.markdown("<br>", unsafe_allow_html=True)

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

    heroes = heroes

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
                "sort_score",
                0
            ),

        reverse=True
    )
    # =====================================================
    # SCROLL
    # =====================================================

    with st.container(height=420):

        for i, hero in enumerate(heroes):

            hero_id = hero["hero_id"]
            hero_name = hero["hero_name"]

            image_path = get_hero_image(hero_id)

            hero_score = recommendation_map.get(
                hero_id,
                {}
            ).get(
                "score",
                0
            )

            if image_path:
                st.image(
                    image_path,
                    use_container_width=True
                )

            if st.button(
                "Выбрать",
                key=f"hero_{side}_{role}_{hero_id}_{idx}_{i}",
                use_container_width=True
            ):

                st.session_state["draft_state"][side][role] = {
                    "hero_id": hero_id,
                    "hero_name": hero_name
                }

                st.rerun()


