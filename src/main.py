import os

if __name__ == '__main__':
    script_name = os.path.join("streamlit_app", "home.py")
    os.system(f"streamlit run {script_name}")
