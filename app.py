import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import configuration
from config.app_config import APP_NAME, APP_DESCRIPTION, APP_ICON, UI_THEME
from config.security_config import ENABLE_AUTHENTICATION

# Import components
from components.navigation import sidebar_menu
from pages.dashboard import show_dashboard
from pages.neuroleader_test import show_neuroleader_test
from pages.lessons import show_lessons
from pages.profile import show_profile
from utils.ui import set_page_config

def main():
    set_page_config(
        page_title=f"{APP_NAME} | {APP_DESCRIPTION}",
        page_icon=APP_ICON,
        layout="wide"
    )

    # Apply custom CSS
    css_path = os.path.join("static", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at {css_path}")

    # Sidebar navigation
    selected = sidebar_menu()

    # Content based on selection
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Neuroleader Test":
        show_neuroleader_test()
    elif selected == "Lekcje":
        show_lessons()
    elif selected == "Profil":
        show_profile()

if __name__ == "__main__":
    main()
