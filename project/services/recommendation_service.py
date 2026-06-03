import pandas as pd

from utils.loaders import (
    load_synergy_matrix,
    load_counter_matrix
)

from services.hero_role_service import (
    get_role_score
)

# =========================================================
# EDGE LOOKUP
# =========================================================

def get_synergy_value(
    synergy_df,
    hero_a,
    hero_b
):

    try:

        row = synergy_df[

            (
                (synergy_df["hero_1"] == hero_a)
                &
                (synergy_df["hero_2"] == hero_b)
            )

            |

            (
                (synergy_df["hero_1"] == hero_b)
                &
                (synergy_df["hero_2"] == hero_a)
            )
        ]

        if len(row) == 0:

            return 0.15

        return float(
            row.iloc[0][
                "synergy_score_norm"
            ]
        )

    except Exception:

        return 0.15

# =========================================================
# COUNTER LOOKUP
# =========================================================

def get_counter_value(
    counter_df,
    hero_a,
    hero_b
):

    try:

        row = counter_df[

            (
                (counter_df["hero_id"] == hero_a)
                &
                (
                    counter_df["enemy_hero_id"]
                    == hero_b
                )
            )
        ]

        if len(row) == 0:

            return 0.15

        return float(
            row.iloc[0][
                "counter_score_norm"
            ]
        )

    except Exception:

        return 0.15

# =========================================================
# HERO SCORE
# =========================================================

def calculate_hero_scores(

    candidate_hero,

    ally_picks,

    enemy_picks,

    synergy_df,

    counter_df,

    role_score
):

    # =====================================================
    # SYNERGY
    # =====================================================

    synergy_score = 0.0

    for ally in ally_picks:

        synergy_score += get_synergy_value(

            synergy_df,

            candidate_hero,

            ally
        )

    # =====================================================
    # COUNTER
    # =====================================================

    counter_score = 0.0

    for enemy in enemy_picks:

        counter_score += get_counter_value(

            counter_df,

            candidate_hero,

            enemy
        )

    # =====================================================
    # ROLE WEIGHT
    # =====================================================

    role_component = role_score * 3

    # =====================================================
    # FINAL
    # =====================================================

    final_score = (

        synergy_score * 4
        +
        counter_score * 4
        +
        role_component
    )

    return {

        "score": round(
            final_score,
            2
        ),

        "synergy": round(
            synergy_score,
            2
        ),

        "counter": round(
            counter_score,
            2
        ),

        "role_score": round(
            role_score,
            2
        )
    }

# =========================================================
# MAIN RECOMMENDATION
# =========================================================

def get_recommendations(

    candidate_heroes,

    ally_picks,

    enemy_picks,

    role
):

    # =====================================================
    # LOAD DATA
    # =====================================================

    synergy_df = load_synergy_matrix()

    counter_df = load_counter_matrix()

    # =====================================================
    # BUILD
    # =====================================================

    recommendations = []

    for hero_id in candidate_heroes:

        role_score = get_role_score(
            hero_id,
            role
        )

        scores = calculate_hero_scores(

            candidate_hero=hero_id,

            ally_picks=ally_picks,

            enemy_picks=enemy_picks,

            synergy_df=synergy_df,

            counter_df=counter_df,

            role_score=role_score
        )

        recommendations.append({

            "hero_id": hero_id,

            "score": scores["score"],

            "synergy": scores["synergy"],

            "counter": scores["counter"],

            "role_score": scores["role_score"]
        })

    # =====================================================
    # SORT
    # =====================================================

    recommendations = sorted(

        recommendations,

        key=lambda x: x["score"],

        reverse=True
    )

    return recommendations