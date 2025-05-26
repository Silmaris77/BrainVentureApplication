"""
Navigation utilities for the BrainVenture app.
"""
import streamlit as st
import os
from streamlit_option_menu import option_menu
from utils.theme_provider import ThemeProvider, UITheme
from components.theme_switcher import get_current_theme, get_current_layout

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
            width: 20rem !important;
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
        current_page = st.session_state.get("current_page", "Dashboard")
    
    # Store the current page in session state
    st.session_state["current_page"] = current_page
    
    with st.sidebar:
        # Show logo if available
        logo_path = os.path.join("static", "images", "brainventure_logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)
        else:
            st.title(" BrainVenture")
        
        # Main navigation menu - usunięto "Lekcje" i "Ustawienia"
        selected = option_menu(
            "Menu",
            ["Dashboard", "Profil", "Typy Neuroliderów", "Struktura Kursu"],
            icons=["speedometer2", "person-circle", "lightbulb", "list-check"],
            menu_icon="brain",
            default_index=[
                "Dashboard", "Profil", "Typy Neuroliderów", "Struktura Kursu"
            ].index(current_page) if current_page in ["Dashboard", "Profil", "Typy Neuroliderów", "Struktura Kursu"] else 0,
            key=f"main_navigation_{current_page}",
            styles={
                "container": {"background-color": "#f0f0f0", "border-radius": "10px", "padding": "10px"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin":"0px 0px 8px 0px",
                    "padding": "8px 12px",
                    "border-radius": "8px",
                    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "background-color": "#ffffff",
                    "transition": "transform 0.2s, box-shadow 0.2s"
                },
                "nav-link-selected": {
                    "background-color": "#4a4a4a", 
                    "color": "white",
                    "box-shadow": "0 3px 5px rgba(0,0,0,0.2)",
                    "transform": "translateY(-2px)"
                },
                "nav-link:hover": {
                    "background-color": "#f8f8f8",
                    "transform": "translateY(-2px)",
                    "box-shadow": "0 4px 6px rgba(0,0,0,0.15)"
                }
            }
        )
        
        # Handle navigation based on selection
        if selected != current_page:
            try:
                # Dla stron w katalogu pages/ używamy ścieżki "pages/nazwa_pliku.py"
                if selected == "Dashboard":
                    st.switch_page("pages/1_Dashboard.py")
                elif selected == "Profil":
                    st.switch_page("pages/4_Profil.py")
                elif selected == "Typy Neuroliderów":
                    st.switch_page("pages/5_Typy_Neuroliderow.py")
                elif selected == "Struktura Kursu":
                    st.switch_page("pages/8_Struktura_Kursu.py")
            except Exception as e:
                st.error(f"Nie można przejść do strony {selected}: {e}")
        
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
                    "nav-link": {
                        "font-size": "14px", 
                        "text-align": "left", 
                        "margin":"0px 0px 6px 0px", 
                        "padding": "6px 10px", 
                        "border-radius": "6px", 
                        "background-color": "#ffffff",
                        "box-shadow": "0 1px 3px rgba(0,0,0,0.05)",
                        "transition": "all 0.2s"
                    },
                    "nav-link-selected": {
                        "background-color": "orange", 
                        "color": "white",
                        "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "transform": "translateY(-1px)"
                    },
                    "nav-link:hover": {
                        "background-color": "#fffaf0",
                        "transform": "translateY(-1px)"
                    }
                }
            )
            
        # Add theme layout switcher at the bottom of the sidebar
        st.markdown("---")
        create_layout_switcher()
        
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
                "margin": "0px 3px", 
                "padding": "10px", 
                "border-radius": "8px",
                "background-color": "#f8f8f8",
                "transition": "all 0.2s ease",
                "box-shadow": "0 1px 3px rgba(0,0,0,0.05)"
            },
            "nav-link-selected": {
                "background-color": "#4a4a4a", 
                "color": "white",
                "box-shadow": "0 2px 4px rgba(0,0,0,0.2)"
            },
            "nav-link:hover": {
                "background-color": "#f0f0f0",
                "transform": "translateY(-1px)",
                "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
            }
        }
    )
    
    return selected

def create_layout_switcher():
    """
    Creates a layout switcher interface in the sidebar.
    Allows users to switch between different UI layouts (Material3, Fluent, etc.)
    """
    theme = get_current_theme()
    layout = get_current_layout()
    
    st.markdown(f"Aktualny motyw: **{theme}**")
    st.markdown(f"Aktualny układ: **{layout}**")
    
    # Create container with 2 rows of 2 buttons for better UI
    row1, row2 = st.columns(2), st.columns(2)
    
    # First row - Material3 and Fluent
    with row1[0]:
        if st.button("Material", use_container_width=True, 
                   type="primary" if layout == "material3" else "secondary",
                   key="btn_material"):
            # ThemeProvider.set_theme(UITheme.MATERIAL3)  # stara wersja
            st.session_state.layout = "material3"  # nowa wersja
            st.session_state.theme_just_changed = True
            st.rerun()
            
    with row1[1]:
        if st.button("Fluent", use_container_width=True, 
                   type="primary" if layout == "fluent" else "secondary",
                   key="btn_fluent"):
            # ThemeProvider.set_theme(UITheme.FLUENT)  # stara wersja
            st.session_state.layout = "fluent"  # nowa wersja
            st.session_state.theme_just_changed = True
            st.rerun()
    
    # Second row - Default and Neuro
    with row2[0]:
        if st.button("Default", use_container_width=True, 
                   type="primary" if layout == "default" else "secondary",
                   key="btn_default"):
            # ThemeProvider.set_theme(UITheme.DEFAULT)  # stara wersja
            st.session_state.layout = "default"  # nowa wersja
            st.session_state.theme_just_changed = True
            st.rerun()
            
    with row2[1]:
        if st.button("Neuro", use_container_width=True, 
                   type="primary" if layout == "neuro" else "secondary",
                   key="btn_neuro"):
            # ThemeProvider.set_theme(UITheme.NEURO)  # stara wersja
            st.session_state.layout = "neuro"  # nowa wersja
            st.session_state.theme_just_changed = True
            st.rerun()
