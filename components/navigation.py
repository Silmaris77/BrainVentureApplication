import streamlit as st
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
        st.markdown("### Menu Główne")
        
        # Define menu options with icons using emoji or Unicode symbols
        menu_options = {
            "Dashboard": "🏠",
            "Neuroleader Test": "📋",
            "Lekcje": "📚",
            "Profil": "👤"
        }
        
        # Create navigation buttons
        for page_name, icon in menu_options.items():
            btn_style = "font-weight: bold; color: #FF4B4B;" if st.session_state.page == page_name else ""
            if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True, 
                        help=f"Przejdź do {page_name}"):
                st.session_state.page = page_name
                st.rerun()  # Force app to rerun with the new page
        
        st.markdown("---")
        st.markdown("© 2025 BrainVenture")
