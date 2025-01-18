import streamlit as st

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Gallery", "Counter", "input"])

if page == "Home":
    st.title("Welcome to the Home Page")
    st.write("This is the home page of our app.")
elif page == "Gallery":
    st.title("Image Gallery")
    img = Image.open("path_to_image.jpg")
    st.image(img, caption="A cool image", use_column_width=True)
elif page == "Counter":
    st.title("Counter Example")
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if st.button("Add 1"):
        st.session_state.counter += 1
    st.write(f"Counter: {st.session_state.counter}")
elif page == "input":
    name = st.text_input("Enter your name:")
    if name:
        st.write(f"Hello, {name}!")