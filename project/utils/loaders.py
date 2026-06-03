import pandas as pd

from pathlib import Path

import streamlit as st

# =========================================================
# BASE DIR
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# DATA DIR
# =========================================================

DATA_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)

# =========================================================
# HERO REGISTRY
# =========================================================

@st.cache_data
def load_heroes():

    heroes_path = (
        DATA_DIR
        / "hero_registry.csv"
    )

    print("\n=== LOADING HEROES ===")

    print(heroes_path)

    df = pd.read_csv(
        heroes_path
    )

    print(df.head())

    print(df.columns)

    return df

# =========================================================
# HERO STATS
# =========================================================

@st.cache_data
def load_hero_stats():

    stats_path = (
        DATA_DIR
        / "hero_stats.csv"
    )

    print("\n=== LOADING HERO STATS ===")

    print(stats_path)

    df = pd.read_csv(
        stats_path
    )

    print(df.head())

    print(df.columns)

    return df

# =========================================================
# HERO SYNERGY MATRIX
# =========================================================

@st.cache_data
@st.cache_data
def load_synergy_matrix():

    path = DATA_DIR / "hero_synergy_matrix.csv"

    return pd.read_csv(path)
# =========================================================
# HERO COUNTER MATRIX
# =========================================================

@st.cache_data
@st.cache_data
def load_counter_matrix():

    path = DATA_DIR / "hero_counter_matrix.csv"

    return pd.read_csv(path)

# =========================================================
# HERO EMBEDDINGS
# =========================================================

@st.cache_data
def load_embeddings():

    embeddings_path = (
        DATA_DIR
        / "hero_embeddings_v6.csv"
    )

    print("\n=== LOADING EMBEDDINGS ===")

    print(embeddings_path)

    df = pd.read_csv(
        embeddings_path
    )

    print(df.shape)

    return df

# =========================================================
# HERO GRAPH FEATURES
# =========================================================

@st.cache_data
def load_graph_features():

    graph_path = (
        DATA_DIR
        / "hero_graph_features.csv"
    )

    print("\n=== LOADING GRAPH FEATURES ===")

    print(graph_path)

    df = pd.read_csv(
        graph_path
    )

    print(df.shape)

    return df