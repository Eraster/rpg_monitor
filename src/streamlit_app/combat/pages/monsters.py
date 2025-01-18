import streamlit as st

from game.entities.entities.monsters import PredefinedMonsters
from game.entities.base.enemy_base_sheet import Enemy

def main_monsters():

    page = st.sidebar.selectbox("Monster Selection:", [''] + list(PredefinedMonsters.get_monster().keys()))

    if page == '':
        st.title('All Monsters')
        st.write(PredefinedMonsters.get_monster())

    elif page in PredefinedMonsters.get_monster():
        monster: Enemy = PredefinedMonsters.get_monster(page)

        button_roll_stats = st.button("Roll stats")
        if button_roll_stats:
            monster.hit_points.roll_hit_points()

        # Monster info
        st.markdown(monster.get_html(), unsafe_allow_html=True)
        st.write(monster.get_html)

    else:
        st.title(f"Monster allocation error.")
        st.write("Monster selection not found.")
