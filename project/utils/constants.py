from pathlib import Path

# ROOT
ROOT_DIR = Path(__file__).resolve().parent.parent

# DATA
DATA_DIR = ROOT_DIR.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# MODELS
MODELS_DIR = ROOT_DIR.parent / "models"

# HERO ASSETS
HERO_IMAGES_DIR = ROOT_DIR.parent / "hero_images"
HERO_FACES_DIR = ROOT_DIR.parent / "hero_faces"

# STREAMLIT
STREAMLIT_ARTIFACTS_DIR = ROOT_DIR.parent / "streamlit_artifacts"

# USER FILES
USERS_FILE = ROOT_DIR.parent / "users.csv"
USER_HEROES_FILE = ROOT_DIR.parent / "user_heroes.csv"

# CSV FILES
HEROES_CSV = ROOT_DIR.parent / "heroes.csv"
HERO_ROLES_CSV = ROOT_DIR.parent / "heroes_roles.csv"
HERO_COUNTERS_CSV = ROOT_DIR.parent / "hero_counters.csv"
HERO_STATS_CSV = ROOT_DIR.parent / "hero_games_stats.csv"
HERO_PAIRS_CSV = ROOT_DIR.parent / "hero_pairs.csv"

# PROCESSED FILES
EMBEDDINGS_FILE = PROCESSED_DIR / "hero_embeddings_v6.csv"

SYNERGY_MATRIX = PROCESSED_DIR / "hero_synergy_matrix.csv"
COUNTER_MATRIX = PROCESSED_DIR / "hero_counter_matrix.csv"

TSNE_IMAGE = PROCESSED_DIR / "hero_embeddings_tsne_communities.png"
PCA_IMAGE = PROCESSED_DIR / "hero_embeddings_pca_communities.png"

ROC_IMAGE = PROCESSED_DIR / "hard_roc_curve.png"
PR_IMAGE = PROCESSED_DIR / "hard_pr_curve.png"

CONFUSION_IMAGE = PROCESSED_DIR / "hard_confusion_matrix.png"
FEATURE_IMPORTANCE_IMAGE = PROCESSED_DIR / "hard_feature_importance.png"