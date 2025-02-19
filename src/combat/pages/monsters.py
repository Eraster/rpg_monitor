import streamlit as st

from _game.entities.entities.monsters import PredefinedMonsters
from _game.entities.base.entity import Entity

def main_monsters():

    page = st.sidebar.selectbox("Monster Selection:", [''] + list(PredefinedMonsters.get_monster().keys()))

    if page == '':
        st.title('All Monsters')
        for race, enemy in PredefinedMonsters.get_monster().items():
            st.write(f"""{enemy.description_short()}   
                 
            {enemy.description()}""")

    elif page in PredefinedMonsters.get_monster():
        monster: Entity = PredefinedMonsters.get_monster(page)

        button_roll_stats = st.button("Roll stats")
        if button_roll_stats:
            monster.hit_points.roll_hit_points()

        # Monster info
        st.markdown(monster.get_html(), unsafe_allow_html=True)

    else:
        st.title(f"Monster allocation error.")
        st.write("Monster selection not found.")
