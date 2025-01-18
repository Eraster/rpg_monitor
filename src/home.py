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
    st.title(f"RPG campaign monitor")
    st.write("""
    The following should become support for DM's when playing NPC's.
    Goal is, to streamline the set up for encounters and the enemy health etc. management.
    Due to ongoing recalculations it would easily become possible to introduce debuff items such as 
    "Reduce Intelligence by 2" or equivalent.
    
    Check out the Battle Tracker!
    """)

if page == "Home":
    home()
elif page == "History":
    main_history()
elif page == "Combat":
    main_combat()
elif page == "Battle Tracker":
    main_battle_tracker()
