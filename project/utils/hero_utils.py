from pathlib import Path

# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

HERO_IMAGES_DIR = BASE_DIR.parent / "hero_images"

# =========================================================
# HERO IMAGE
# =========================================================

def get_hero_image(hero_id):

    image_path = HERO_IMAGES_DIR / f"{hero_id}.png"

    if image_path.exists():

        return str(image_path)

    return None