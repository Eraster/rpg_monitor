import streamlit as st


def main_test():
    st.title("Test Instance")

    # Define available pages
    PAGES = {
        "Home": lambda: st.write("Welcome to the Home Page!"),
        "Page 1": lambda: st.write("Welcome to Page 1!"),
        "Page 2": lambda: st.write("Welcome to Page 2!"),
    }

    # Initialize session state for the page if not already set
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # Sidebar (or use a hidden navigation)
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox("Select a page:", options=PAGES.keys())

    # Logic to change the page via the sidebar
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page

    # Button-based navigation
    if st.button("Go to Page 1"):
        st.session_state.current_page = "Page 1"

    if st.button("Go to Page 2"):
        st.session_state.current_page = "Page 2"

    # Display the current page
    current_page_func = PAGES[st.session_state.current_page]
    current_page_func()
