import streamlit as st
import os


def main_history():
    st.title("World History")

    file_path = os.path.join("history", "pages", "history_data")

    # Open the file if it exists
    if st.button("Only Click as Dungeon Master!!!"):
        st.write(f"""
        
        --- debug grabbing weapons from environment
        
        - implement movement action, grapling etc.
        - implement two_handed property properly -> allow entities to select carried weapon
        Two-Handed. This weapon requires two hands to use. This property is relevant only when you attack with the weapon, not when you simply hold it.
        - Light weapon
        When you take the Attack action and attack with a light melee weapon that you're holding in one hand, you can use a bonus action to attack with a different light melee weapon that you're holding in the other hand. You don't add your ability modifier to the damage of the bonus attack, unless that modifier is negative.  
        - implement action handling (movement, action, bonus action) all separate as step by step todo's
        - implement action suggestion.
        
        - action pick up weapon: allow only once per turn (or display that it should not be possible anymore)
        
        
        
        -action costs -> for finesse etc.
        -reactions
        -bonus actions
        
        
        - add mongo db for data storage
        """)



















        st.write("")



        with open(file_path, "r") as file:
            content = file.read()
        st.text_area("File Content", content, height=300)  # Display content in a text area
