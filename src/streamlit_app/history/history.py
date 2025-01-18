import streamlit as st
import os


def main_history():
    st.title("Hello World 2")
    st.write("Hello, World! 2")
    st.write("wup eup")

    file_path = os.path.join("streamlit_app", "history", "pages", "history_data")

    # Open the file if it exists
    with open(file_path, "r") as file:
        content = file.read()
    st.text_area("File Content", content, height=300)  # Display content in a text area
