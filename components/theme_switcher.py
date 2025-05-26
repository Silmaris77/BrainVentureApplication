"""
Moduł zarządzający motywami (theme) w aplikacji BrainVenture.
"""
import streamlit as st
from utils.theme_provider import ThemeProvider, UITheme

def initialize_theme():
    """Initialize the theme in the session state"""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "layout" not in st.session_state:
        st.session_state.layout = "material3"
    if "theme_just_changed" not in st.session_state:
        st.session_state.theme_just_changed = False

def get_current_theme():
    """Get the current theme from session state"""
    return st.session_state.get("theme", "light")

def get_current_layout():
    """Get the current layout from session state"""
    return st.session_state.get("layout", "material3")

def set_theme(theme):
    """Set the theme in session state"""
    st.session_state.theme = theme
    st.session_state.theme_just_changed = True

def set_layout(layout):
    """Set the layout in session state"""
    st.session_state.layout = layout
    st.session_state.theme_just_changed = True

def create_theme_switcher(container=None):
    """
    Create a theme switcher component.
    Returns True if theme was changed.
    """
    if container is None:
        container = st

    theme_changed = False
    
    # Kolor motywu (Jasny/Ciemny)
    container.markdown("#### Wybierz motyw")
    theme_cols = container.columns(2)
    
    with theme_cols[0]:
        if st.button("🌞 Jasny", use_container_width=True, 
                   type="primary" if st.session_state.theme == "light" else "secondary"):
            set_theme("light")
            theme_changed = True
            
    with theme_cols[1]:
        if st.button("🌙 Ciemny", use_container_width=True,
                   type="primary" if st.session_state.theme == "dark" else "secondary"):
            set_theme("dark")
            theme_changed = True
    
    # Layout (Material/Fluent)
    container.markdown("#### Wybierz layout (układ)")
    layout_cols = container.columns(2)
    
    with layout_cols[0]:
        if st.button("Material 3", use_container_width=True,
                   type="primary" if st.session_state.layout == "material3" else "secondary"):
            set_layout("material3")
            theme_changed = True
            
    with layout_cols[1]:
        if st.button("Fluent", use_container_width=True,
                   type="primary" if st.session_state.layout == "fluent" else "secondary"):
            set_layout("fluent")
            theme_changed = True
    
    return theme_changed
