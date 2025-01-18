import streamlit as st

# Top-level navigation
main_menu = st.sidebar.radio("Main Menu", ["Home", "Features", "Settings"])

if main_menu == "Home":
    st.title("Welcome to Home Page")
    st.write("This is the main dashboard.")
    # Print the list of lines
    uploaded_file = st.file_uploader("history_data", type="txt")

    # Check if the file is uploaded
    if uploaded_file is not None:
        # Read the content of the file
        content = uploaded_file.read().decode("utf-8")  # Decode the binary content to string
        st.text_area("File Content", content, height=300)
elif main_menu == "Features":
    # Submenu for Features
    feature_menu = st.sidebar.radio("Features Menu", ["Feature 1", "Feature 2", "Feature 3"])

    if feature_menu == "Feature 1":
        st.title("Feature 1 Page")
        st.write("Details about Feature 1.")
    elif feature_menu == "Feature 2":
        st.title("Feature 2 Page")
        st.write("Details about Feature 2.")
    elif feature_menu == "Feature 3":
        st.title("Feature 3 Page")
        st.write("Details about Feature 3.")
elif main_menu == "Settings":
    # Submenu for Settings
    settings_menu = st.sidebar.radio("Settings Menu", ["Profile", "Preferences", "About"])

    if settings_menu == "Profile":
        st.title("Profile Settings")
        st.write("Manage your profile here.")
    elif settings_menu == "Preferences":
        st.title("Preferences")
        st.write("Set your preferences here.")
    elif settings_menu == "About":
        st.title("About")
        st.write("Learn more about this app.")
