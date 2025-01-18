import streamlit as st

from src.streamlit_app.battle_tracker.battle_tracker import main_battle_tracker
from src.streamlit_app.history.history import main_history
from src.streamlit_app.combat.combat import main_combat
from src.streamlit_app.tests.test import main_test

# Sidebar to select page

st.set_page_config(
    page_title="Full Screen App",
    layout="wide"
)

if "counter" not in st.session_state:
    st.session_state.counter = 0

page = st.sidebar.selectbox("Type", ["Home", "History", "Combat", "Battle Tracker", "Tests"])

def home():
    st.title(f"DND 5e campaign monitor")
    st.subheader(f"TODO")
    st.write(f"""
    
    Add method to add new enemys to initiative without reroll.
    def roll_initiative_for_added_entities(self):
        raise NotImplementedError()
    
    def mutate_initiative_rolls(self):
        raise NotImplementedError()
    
    add possibility to mutate rolls.
        
        
    
    # @TODO: Always write functions for game manipulations
    
    - implement two_handed property
    Two-Handed. This weapon requires two hands to use. This property is relevant only when you attack with the weapon, not when you simply hold it.
    - Light weapon
    When you take the Attack action and attack with a light melee weapon that you're holding in one hand, you can use a bonus action to attack with a different light melee weapon that you're holding in the other hand. You don't add your ability modifier to the damage of the bonus attack, unless that modifier is negative.


    """)

if page == "Home":
    home()
elif page == "History":
    main_history()
elif page == "Combat":
    main_combat()
elif page == "Battle Tracker":
    main_battle_tracker()
elif page == "Tests":
    main_test()
