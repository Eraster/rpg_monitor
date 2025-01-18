import streamlit as st
import os

from streamlit_app.combat.pages.monsters import main_monsters

CURRENT_DIRECTORY = os.path.join("streamlit_app", "combat", "pages")

def main_combat():
    page = st.sidebar.selectbox("Combat Features", ['Main', 'Monsters'])

    if page == 'Main':
        st.title("Combat Features")
        st.write("All combat related information can be found here. Select Combat Feature in Sidebar.")

    elif page == 'Monsters':
        main_monsters()


