import csv
import hashlib
import os
import requests
import pandas as pd

from utils.constants import *

# =========================================================
# HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

# =========================================================
# OPENDOTA
# =========================================================

def get_player_profile(account_id):

    url = f"https://api.opendota.com/api/players/{account_id}"

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        return response.json()

    except Exception:
        return None

# =========================================================
# VALIDATION
# =========================================================

def validate_account(account_id):

    profile = get_player_profile(account_id)

    if profile is None:
        return False

    return "profile" in profile

# =========================================================
# USERS
# =========================================================

def user_exists(account_id):

    if not USERS_FILE.exists():
        return False

    df = pd.read_csv(USERS_FILE)

    return int(account_id) in df["user_id"].values

# =========================================================
# REGISTER
# =========================================================

def create_user(account_id, password):

    profile = get_player_profile(account_id)

    if profile is None:
        return False, "OpenDota profile not found"

    username = profile["profile"]["personaname"]

    password_hash = hash_password(password)

    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            account_id,
            username,
            password_hash
        ])

    return True, username

# =========================================================
# LOGIN
# =========================================================

def login_user(account_id, password):

    if not USERS_FILE.exists():
        return False

    password_hash = hash_password(password)

    df = pd.read_csv(USERS_FILE)

    row = df[df["user_id"] == int(account_id)]

    if len(row) == 0:
        return False

    return (
        row.iloc[0]["password_hash"]
        == password_hash
    )

# =========================================================
# HEROES
# =========================================================

def get_player_heroes(account_id):

    url = f"https://api.opendota.com/api/players/{account_id}/heroes"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    result = []

    for hero in data:

        games = hero["games"]
        wins = hero["win"]

        result.append([

            account_id,

            hero["hero_id"],

            games,

            wins,

            wins / games if games > 0 else 0
        ])

    return result

# =========================================================
# SAVE HEROES
# =========================================================

def save_player_heroes(account_id):

    rows = get_player_heroes(account_id)

    if len(rows) == 0:
        return

    file_exists = USER_HEROES_FILE.exists()

    with open(
        USER_HEROES_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "user_id",
                "hero_id",
                "games",
                "wins",
                "winrate"
            ])

        writer.writerows(rows)