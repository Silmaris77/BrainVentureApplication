"""
Navigation utilities for the BrainVenture app.
"""
import streamlit as st
import os
from streamlit_option_menu import option_menu

def hide_streamlit_navigation():
    """Hide the default Streamlit navigation sidebar and top menu."""
    st.markdown("""
    <style>
        /* Hide all sidebar navigation items */
        [data-testid="stSidebarNavItems"] {
            display: none !important;
        }
        
        /* Hide the expand/collapse arrow button */
        .css-1n76uvr, .css-90vs21 {
            display: none !important;
        }
        
        /* Maintain sidebar width when default navigation is hidden */
        section[data-testid="stSidebar"] > div {
            width: 16rem !important;
        }
        
        /* Hide hamburger menu */
        .css-r698ls, .css-hxt7ib {
            display: none !important;
        }
        
        /* Hide top right menu */
        .css-18ni7ap {
            display: none !important;
        }
        
        /* Hide Made with Streamlit footer */
        footer {
            visibility: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)

def create_sidebar_navigation(current_page=None):
    """
    Creates a consistent navigation sidebar for all pages.
    
    Args:
        current_page: The current page name to highlight in the menu
    """
    # If current_page is not set, try to get it from the session state
    if current_page is None:
        current_page = st.session_state.get("current_page", "Home")
    
    # Store the current page in session state
    st.session_state["current_page"] = current_page
    
    with st.sidebar:
        # Show logo if available
        logo_path = os.path.join("static", "images", "brainventure_logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)
        else:
            st.title(" BrainVenture")
        
        # Main navigation menu
        selected = option_menu(
            "Menu",
            ["Home", "Dashboard", "Test", "Lekcje", "Profil"],
            icons=["house-fill", "speedometer2", "clipboard-check", "book", "person"],
            menu_icon="brain",
            default_index=[
                "Home", "Dashboard", "Test", "Lekcje", "Profil"
            ].index(current_page) if current_page in ["Home", "Dashboard", "Test", "Lekcje", "Profil"] else 0,
            key=f"main_navigation_{current_page}",
            styles={
                "container": {"background-color": "#f0f0f0", "border-radius": "10px", "padding": "10px"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "border-radius": "5px"},
                "nav-link-selected": {"background-color": "#4a4a4a", "color": "white"},
            }
        )
        
        # Handle navigation based on selection
        if selected != current_page:
            try:
                # Dla strony głównej
                if selected == "Home":
                    st.switch_page("Home.py")
                # Dla stron w katalogu pages/ używamy ścieżki "pages/nazwa_pliku.py"
                elif selected == "Dashboard":
                    st.switch_page("pages/1_Dashboard.py")
                elif selected == "Test":
                    st.switch_page("pages/2_Neuroleader_Test.py")
                elif selected == "Lekcje":
                    st.switch_page("pages/3_Lekcje.py")
                elif selected == "Profil":
                    st.switch_page("pages/4_Profil.py")
            except Exception as e:
                st.error(f"Nie można przejść do strony {selected}: {e}")
                
        # Only show filters for lessons page
        if current_page == "Lekcje":
            st.markdown("---")
            filtry = option_menu(
                "Filtruj lekcje",
                ["Wszystkie", "Ukończone", "Do zrobienia", "Zablokowane"],
                icons=["grid", "check-circle", "hourglass", "lock"],
                key=f"lekcje_filtry_{current_page}",
                default_index=0,
                styles={
                    "container": {"background-color": "#f0f0f0", "border-radius": "10px", "padding": "5px"},
                    "icon": {"color": "#4a4a4a", "font-size": "16px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "border-radius": "5px"},
                    "nav-link-selected": {"background-color": "orange", "color": "white"},
                }
            )
            
            # Create category filter for lessons
            kategoria = option_menu(
                "Kategorie",
                ["Neurobiologia", "Emocje", "Podejmowanie Decyzji"],
                icons=["diagram-3", "emoji-smile", "lightning"],
                key=f"lekcje_kategorie_{current_page}",
                default_index=0,
                styles={
                    "container": {"background-color": "#f0f0f0", "border-radius": "10px", "padding": "5px"},
                    "icon": {"color": "#4a4a4a", "font-size": "16px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "border-radius": "5px"},
                    "nav-link-selected": {"background-color": "orange", "color": "white"},
                }
            )
        
        # Add profile tabs if on Profile page
        elif current_page == "Profil":
            st.markdown("---")
            profil_tab = option_menu(
                "Sekcje profilu",
                ["Dane", "Postępy", "Certyfikaty", "Ustawienia"],
                icons=["person-circle", "graph-up", "award", "gear"],
                key=f"profil_sekcje_{current_page}",
                default_index=0,
                styles={
                    "container": {"background-color": "#f0f0f0", "border-radius": "10px", "padding": "5px"},
                    "icon": {"color": "#4a4a4a", "font-size": "16px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "border-radius": "5px"},
                    "nav-link-selected": {"background-color": "orange", "color": "white"},
                }
            )
            
        st.markdown("---")
        st.markdown("© 2025 BrainVenture")

def create_horizontal_submenu(title, options, icons, default_index=0):
    """
    Creates a horizontal submenu for pages.
    
    Args:
        title: The title of the menu (can be empty string for no title)
        options: List of menu options
        icons: List of icons for each option
        default_index: The default selected option index
        
    Returns:
        The selected option
    """
    # Używamy current_page do unikalności klucza
    current_page = st.session_state.get("current_page", "unknown")
    
    selected = option_menu(
        title,
        options,
        icons=icons,
        orientation="horizontal",
        key=f"horizontal_menu_{current_page}_{'-'.join(options).lower()}",
        default_index=default_index,
        styles={
            "container": {"padding": "0px", "margin": "0px 0px 10px 0px"},
            "icon": {"font-size": "16px"},
            "nav-link": {
                "font-size": "14px", 
                "text-align": "center", 
                "margin": "0px", 
                "padding": "10px", 
                "border-radius": "5px"
            },
            "nav-link-selected": {"background-color": "#4a4a4a", "color": "white"},
        }
    )
    
    return selected
