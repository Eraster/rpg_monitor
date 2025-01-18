import streamlit as st

from game.entities.entities.monsters import ALL_MONSTERS
from game.entities.base.enemy_base_sheet import Enemy

def main_monsters():
    page = st.sidebar.selectbox("Monster Selection:", ['All'] + list(ALL_MONSTERS.keys()))

    if page == 'All':
        st.title('All Monsters')
        st.write(ALL_MONSTERS)

    elif page in ALL_MONSTERS:
        monster: Enemy = ALL_MONSTERS[page]

        button_roll_stats = st.button("Roll stats")
        if button_roll_stats:
            monster.hit_points.roll_hit_points()

        # Monster info
        st.markdown(monster.get_html(), unsafe_allow_html=True)
        st.write(monster.get_html)

    else:
        st.title(f"Monster allocation error.")
        st.write("Monster selection not found.")
