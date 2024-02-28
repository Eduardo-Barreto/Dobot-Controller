import streamlit as st

from dobotController import DobotController
import pages

st.title("Dobot Robot Controller")


def get_dobot():
    if 'dobot' not in st.session_state:
        st.session_state.dobot = DobotController()
    return st.session_state.dobot

dobot = get_dobot()

page_selector = st.sidebar.selectbox(
    "Select an option:",
    pages.pages.keys(),
)

pages.pages[page_selector](dobot)
