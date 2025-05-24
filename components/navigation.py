import streamlit as st
from streamlit_option_menu import option_menu
import os

def sidebar_menu():
    """Display the sidebar navigation menu."""
    with st.sidebar:
        logo_path = os.path.join("static", "images", "brainventure_logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)
        else:
            st.title("BrainVenture")
            
        st.markdown("## BrainVenture")
        st.markdown("### Program dla Neuroliderów")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Menu Główne",
            options=["Dashboard", "Neuroleader Test", "Lekcje", "Profil"],
            icons=["house", "clipboard-check", "book", "person"],
            menu_icon="cast",
            default_index=0,
        )
        
        st.markdown("---")
        st.markdown("© 2025 BrainVenture")
        
    return selected
