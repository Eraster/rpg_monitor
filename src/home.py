import streamlit as st

from battle_tracker.battle_tracker import main_battle_tracker
from history.history import main_history
from combat.combat import main_combat

# Sidebar to select page

st.set_page_config(
    page_title="Full Screen App",
    layout="wide"
)

if "counter" not in st.session_state:
    st.session_state.counter = 0

page = st.sidebar.selectbox("Type", ["Home", "History", "Combat", "Battle Tracker"])

def home():
    st.title(f"DND 5e campaign monitor")
    st.subheader(f"TODO")
    st.write()

if page == "Home":
    home()
elif page == "History":
    main_history()
elif page == "Combat":
    main_combat()
elif page == "Battle Tracker":
    main_battle_tracker()
