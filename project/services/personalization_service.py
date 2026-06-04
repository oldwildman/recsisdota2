import pandas as pd
import streamlit as st


def get_personal_score(hero_id):

    user_id = st.session_state.get("user_id")


    if user_id is None:
        
        return 0

    try:

        from pathlib import Path

        BASE_DIR = Path(__file__).resolve().parent.parent

        CSV_PATH = (
            BASE_DIR
            / "data"
            / "processed"
            / "user_heroes.csv"
        )

        df = pd.read_csv(CSV_PATH)


        df["user_id"] = pd.to_numeric(
            df["user_id"],
            errors="coerce"
        )

        df["hero_id"] = pd.to_numeric(
            df["hero_id"],
            errors="coerce"
        )

        user_id = int(user_id)
        hero_id = int(hero_id)

        user_rows = df[
            df["user_id"] == user_id
        ]

    

        hero_row = df[
            (df["user_id"] == user_id)
            &
            (df["hero_id"] == hero_id)
        ]


        if hero_row.empty:
      
            return 0

        games = float(
            hero_row.iloc[0]["games"]
        )

        winrate = float(
            hero_row.iloc[0]["winrate"]
        )

        personal_score = (
            games * 0.003
            +
            winrate * 1
        )



        return round(
            personal_score,
            2
        )

    except Exception as e:



        import traceback


        return 0