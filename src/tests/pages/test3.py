import streamlit as st

# Initialize session state variables if not already set
if "level" not in st.session_state:
    st.session_state.level = "home"
    st.session_state.history = []

def home():
    st.title("Home Page")
    if st.button("Go to Categories"):
        st.session_state.level = "categories"
        st.session_state.history.append("home")

def categories():
    st.title("Categories")
    if st.button("Go to Category 1"):
        st.session_state.level = "category1"
        st.session_state.history.append("categories")
    if st.button("Go to Category 2"):
        st.session_state.level = "category2"
        st.session_state.history.append("categories")
    if st.button("Go back"):
        st.session_state.level = st.session_state.history.pop()

def category1():
    st.title("Category 1")
    if st.button("Go back"):
        st.session_state.level = st.session_state.history.pop()

def category2():
    st.title("Category 2")
    if st.button("Go back"):
        st.session_state.level = st.session_state.history.pop()

if st.session_state.level == "home":
    home()
elif st.session_state.level == "categories":
    categories()
elif st.session_state.level == "category1":
    category1()
elif st.session_state.level == "category2":
    category2()

st.sidebar.write("Current path:")
for item in st.session_state.history:
    st.sidebar.write("/".join(st.session_state.history))
