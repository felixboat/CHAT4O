import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    # Function to get the API key for a logged-in user
    def get_api_key(username):
        api_keys = st.secrets["apikeys"]
        return api_keys.get(username, None)

    def password_entered():
        # global user_chat, api_key
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state["user_chat"] = st.session_state["username"]
            # print(user_chat)
            st.session_state["api_key"] = get_api_key(st.session_state["user_chat"])
            # print(api_key)
            del st.session_state["password"]  # Don't store the username or password.
            # del st.session_state["username"]
            return st.session_state["user_chat"], st.session_state["api_key"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


