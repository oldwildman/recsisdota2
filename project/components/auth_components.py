import streamlit as st
import time

from services.auth_service import (
    create_user,
    login_user,
    user_exists,
    validate_account,
    save_player_heroes,
    get_player_profile
)

# =========================================================
# AUTH PAGE
# =========================================================

def render_auth_page():

    render_auth_header()

    col1, col2, col3 = st.columns([1, 1.15, 1])

    with col2:

        tabs = st.tabs([
            "Вход в аккаунт",
            "Регистрация",
            "Гостевой режим"
        ])

        # =====================================================
        # LOGIN
        # =====================================================

        with tabs[0]:

            st.markdown("### Добро Поажловать")

            login_id = st.text_input(
                "Steam/OpenDota Account ID",
                key="login_id"
            )

            login_password = st.text_input(
                "Пароль",
                type="password",
                key="login_password"
            )

            if st.button(
                "Логин",
                use_container_width=True
            ):

                # -----------------------------
                # VALIDATION
                # -----------------------------

                if not login_id or not login_password:

                    st.error(
                        "Fill all fields"
                    )

                elif not login_id.isdigit():

                    st.error(
                        "Account ID must be numeric"
                    )

                else:

                    with st.spinner(
                        "Authorizing..."
                    ):

                        time.sleep(1)

                        success = login_user(
                            int(login_id),
                            login_password
                        )

                        if success:

                            profile = get_player_profile(
                                int(login_id)
                            )

                            username = (
                                profile["profile"]
                                ["personaname"]
                            )

                            st.session_state.logged_in = True

                            st.session_state.user_id = int(login_id)

                            st.session_state.username = username

                            st.success(
                                f"Welcome back, {username}"
                            )

                            time.sleep(1)

                            st.rerun()

                        else:

                            st.error(
                                "Wrong credentials"
                            )

        # =====================================================
        # REGISTER
        # =====================================================

        with tabs[1]:

            st.markdown("### Создать аккаунт")

            register_id = st.text_input(
                "Steam/OpenDota Account ID",
                key="register_id"
            )

            register_password = st.text_input(
                "Придумайте пароль",
                type="password",
                key="register_password"
            )

            if st.button(
                "Создать Аккаунт",
                use_container_width=True
            ):

                # -----------------------------
                # VALIDATION
                # -----------------------------

                if not register_id or not register_password:

                    st.error(
                        "Fill all fields"
                    )

                elif not register_id.isdigit():

                    st.error(
                        "Account ID must be numeric"
                    )

                elif len(register_password) < 6:

                    st.error(
                        "Пароль слишком короткий"
                    )

                elif user_exists(int(register_id)):

                    st.error(
                        "Пользователь уже сущестует"
                    )

                else:

                    with st.spinner(
                        "Validating OpenDota account..."
                    ):

                        valid = validate_account(
                            int(register_id)
                        )

                        if not valid:

                            st.error(
                                "OpenDota profile not found"
                            )

                        else:

                            # -----------------
                            # CREATE USER
                            # -----------------

                            success, username = create_user(
                                int(register_id),
                                register_password
                            )

                            if success:

                                # -----------------
                                # LOAD HEROES
                                # -----------------

                                with st.spinner(
                                    "Loading player heroes..."
                                ):

                                    save_player_heroes(
                                        int(register_id)
                                    )

                                st.success(
                                    f"Account created for {username}"
                                )

                                st.info(
                                    "You can now login"
                                )

                            else:

                                st.error(
                                    username
                                )

        # =====================================================
        # GUEST MODE
        # =====================================================

        with tabs[2]:

            st.markdown("### Продолжить без авторизации")

            st.markdown(
            '''
            Доступные возможности:

            ✅ Рекомендации героев

            ✅ Анализ синергии

            ✅ Анализ контрпиков

            ✅ Поиск похожих героев

            ⚠️ Персональные рекомендации недоступны
            '''
        )

            if st.button(
                "Продолжить как гость",
                use_container_width=True
            ):

                st.session_state.logged_in = True

                st.session_state.guest_mode = True

                st.session_state.username = "Guest"

                st.success(
                    "Entering guest mode..."
                )

                time.sleep(1)

                st.rerun()

# =========================================================
# HEADER
# =========================================================

def render_auth_header():

    st.markdown(
        """
        <div class="auth-title">
            Рекомендательная система выбора героев Dota 2
        </div>
        """,
        unsafe_allow_html=True
    )