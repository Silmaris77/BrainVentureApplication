"""
Navigation utilities for the BrainVenture app.
"""
import streamlit as st
import os
from streamlit_option_menu import option_menu
from utils.theme_provider import ThemeProvider, UITheme

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
        
        # Main navigation menu
        selected = option_menu(
            "Menu",
            ["Dashboard", "Test", "Typy Neuroliderów", "Lekcje", "Profil"],
            icons=["speedometer2", "clipboard-check", "people", "book", "person"],
            menu_icon="brain",
            default_index=[
                "Dashboard", "Test", "Typy Neuroliderów", "Lekcje", "Profil"
            ].index(current_page) if current_page in ["Dashboard", "Test", "Typy Neuroliderów", "Lekcje", "Profil"] else 0,
            key=f"main_navigation_{current_page}",
            styles={
                "container": {"background-color": "#f0f0f0", "border-radius": "10px", "padding": "10px"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin":"0px 0px 8px 0px",  # Dodane marginesy między przyciskami
                    "padding": "8px 12px",  # Zwiększone wypełnienie
                    "border-radius": "8px",  # Bardziej zaokrąglone rogi
                    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",  # Dodany cień
                    "background-color": "#ffffff",  # Białe tło dla przycisków
                    "transition": "transform 0.2s, box-shadow 0.2s"  # Dodane animacje
                },
                "nav-link-selected": {
                    "background-color": "#4a4a4a", 
                    "color": "white",
                    "box-shadow": "0 3px 5px rgba(0,0,0,0.2)",  # Mocniejszy cień dla aktywnego elementu
                    "transform": "translateY(-2px)"  # Lekkie uniesienie przycisku
                },
                "nav-link:hover": {
                    "background-color": "#f8f8f8",  # Jaśniejsze tło przy najechaniu
                    "transform": "translateY(-2px)",  # Lekkie uniesienie przycisku
                    "box-shadow": "0 4px 6px rgba(0,0,0,0.15)"  # Mocniejszy cień przy najechaniu
                }
            }
        )
        
        # Handle navigation based on selection
        if selected != current_page:
            try:
                # Dla stron w katalogu pages/ używamy ścieżki "pages/nazwa_pliku.py"
                if selected == "Dashboard":
                    st.switch_page("pages/1_Dashboard.py")
                elif selected == "Test":
                    st.switch_page("pages/2_Neuroleader_Test.py")
                elif selected == "Typy Neuroliderów":
                    st.switch_page("pages/5_Typy_Neuroliderow.py")
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
    # Initialize ui_theme if not present in session_state
    ThemeProvider.initialize()
    
    st.markdown("### Wybierz layout (układ)")
    
    # Create container with 2 rows of 2 buttons for better UI
    row1, row2 = st.columns(2), st.columns(2)
    
    # Debug: show current theme
    st.markdown(f"Current theme: **{ThemeProvider.get_current_theme().name}**")
    
    # First row - Material3 and Fluent
    with row1[0]:
        if st.button("Material", use_container_width=True, 
                   type="primary" if ThemeProvider.get_current_theme() == UITheme.MATERIAL3 else "secondary",
                   key="btn_material"):
            ThemeProvider.set_theme(UITheme.MATERIAL3)
            st.rerun()
            
    with row1[1]:
        if st.button("Fluent", use_container_width=True, 
                   type="primary" if ThemeProvider.get_current_theme() == UITheme.FLUENT else "secondary",
                   key="btn_fluent"):
            ThemeProvider.set_theme(UITheme.FLUENT)
            st.rerun()
    
    # Second row - Default and Neuro
    with row2[0]:
        if st.button("Default", use_container_width=True, 
                   type="primary" if ThemeProvider.get_current_theme() == UITheme.DEFAULT else "secondary",
                   key="btn_default"):
            ThemeProvider.set_theme(UITheme.DEFAULT)
            st.rerun()
            
    with row2[1]:
        if st.button("Neuro", use_container_width=True, 
                   type="primary" if ThemeProvider.get_current_theme() == UITheme.NEURO else "secondary",
                   key="btn_neuro"):
            ThemeProvider.set_theme(UITheme.NEURO)
            st.rerun()
