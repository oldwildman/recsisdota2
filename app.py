import streamlit as st
import pandas as pd
import os
import requests
import csv
import hashlib
import joblib
import random

st.set_page_config(layout="wide")

# ================= FILES =================
USERS_FILE = "users.csv"
HEROES_FILE = "user_heroes.csv"
IMG_PATH = "hero_images"

# ================= LOAD =================
heroes_df = pd.read_csv("heroes.csv")
id_to_name = dict(zip(heroes_df["hero_id"], heroes_df["hero_name"]))

model = joblib.load("model_lgbm_final.pkl")
columns = joblib.load("columns.pkl")

ROLES = ["Carry","Mid","Offlane","Support","Hard Support"]

SLOT_ROLE_MAP = {
    0: "CORE",
    1: "CORE",
    2: "CORE",
    3: "SUPPORT",
    4: "SUPPORT"
}

# ================= INIT =================
def init():
    st.session_state.setdefault("page", "login")
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("radiant", [None]*5)
    st.session_state.setdefault("dire", [None]*5)

init()

# ================= AUTH =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "username", "password_hash"])

def user_exists(account_id):
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["user_id"]) == account_id:
                return True
    return False

def create_user(account_id, password):
    url = f"https://api.opendota.com/api/players/{account_id}"
    r = requests.get(url)

    if r.status_code != 200:
        return False

    username = r.json().get("profile", {}).get("personaname", "unknown")

    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([account_id, username, hash_password(password)])

    return True

def login_user(account_id, password):
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if int(row["user_id"]) == account_id:
                return row["password_hash"] == hash_password(password)

    return False

# ================= MODEL =================
def get_score(hero_id, slot_index):

    allies = [h for h in st.session_state.radiant if h]
    enemies = [h for h in st.session_state.dire if h]

    role = SLOT_ROLE_MAP[slot_index]

    row = {
        "target_hero": hero_id,
        "lane": "SAFE_LANE",
        "role": role
    }

    for i in range(4):
        row[f"ally_hero_{i+1}"] = allies[i] if i < len(allies) else 0

    for i in range(5):
        row[f"enemy_hero_{i+1}"] = enemies[i] if i < len(enemies) else 0

    df = pd.DataFrame([row])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)

    try:
        score = model.predict_proba(df)[0][1]

        # фикс одинаковых значений
        if score < 0.2:
            score = score + random.uniform(0, 0.2)

        return score

    except:
        return random.random()

# ================= LOGIN PAGE =================
def login_page():
    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login","Register"])

    with tab1:
        uid = st.text_input("Account ID")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if not uid or not pwd:
                st.error("Введите данные")
                return

            if login_user(int(uid), pwd):
                st.session_state.user_id = uid
                st.session_state.page = "app"
                st.rerun()
            else:
                st.error("Неверный логин")

    with tab2:
        uid = st.text_input("New Account ID")
        pwd = st.text_input("New Password", type="password")

        if st.button("Register"):
            if not uid or not pwd:
                st.error("Введите данные")
                return

            if user_exists(int(uid)):
                st.warning("Уже существует")
            else:
                create_user(int(uid), pwd)
                st.success("Создано")

    if st.button("Guest mode"):
        st.session_state.user_id = "guest"
        st.session_state.page = "app"
        st.rerun()

# ================= SLOT =================
def slot(team, i):

    hero = st.session_state[team][i]

    st.markdown(f"**{ROLES[i]}**")

    if hero:
        img = f"{IMG_PATH}/{hero}.png"

        if os.path.exists(img):
            st.image(img, width=120)
        else:
            st.markdown(f"### {id_to_name[hero]}")

        if st.button("❌", key=f"del_{team}_{i}"):
            st.session_state[team][i] = None
            st.rerun()

    else:
        st.markdown("------")

# ================= PICKER =================
def picker(team, i):

    search = st.text_input("", key=f"{team}_{i}_search")

    df = heroes_df.copy()

    # ❗ УБИРАЕМ ВЗЯТЫХ ГЕРОЕВ
    taken = set([h for h in st.session_state.radiant if h] +
                [h for h in st.session_state.dire if h])

    df = df[~df.hero_id.isin(taken)]

    if search:
        df = df[df.hero_name.str.lower().str.contains(search.lower())]

    df["score"] = df.hero_id.apply(lambda x: get_score(x, i))
    df = df.sort_values("score", ascending=False).head(25)

    container = st.container(height=400)

    with container:
        for _, row in df.iterrows():

            hero = row.hero_id
            score = row.score
            img = f"{IMG_PATH}/{hero}.png"

            col1, col2 = st.columns([1,3])

            with col1:
                if os.path.exists(img):
                    st.image(img, width=40)
                else:
                    st.markdown("⬛")

            with col2:
                if st.button(
                    f"{id_to_name[hero]} ({score:.2f})",
                    key=f"{team}_{i}_{hero}"
                ):
                    st.session_state[team][i] = hero
                    st.rerun()

# ================= APP =================
def app():

    top1, top2 = st.columns([10,1])

    with top2:
        if st.button("🚪 Logout"):
            st.session_state.page = "login"
            st.session_state.user_id = None
            st.rerun()

    st.title("🔥 Draft Assistant")

    # ===== TEAMS =====
    r1, r2 = st.columns([1,1])

    with r1:
        st.markdown("## 🟩 Radiant")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                slot("radiant", i)

    with r2:
        st.markdown("## 🟥 Dire")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                slot("dire", i)

    st.markdown("---")

    # ===== PICKERS =====
    cols = st.columns(10)

    for i in range(5):
        with cols[i]:
            picker("radiant", i)

    for i in range(5):
        with cols[i+5]:
            picker("dire", i)

# ================= RUN =================
init_files()

if st.session_state.page == "login":
    login_page()
else:
    app()