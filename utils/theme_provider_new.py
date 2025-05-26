import streamlit as st
from enum import Enum
from components.theme_switcher import apply_theme as apply_color_theme, get_current_theme as get_current_color_theme

class UITheme(Enum):
    MATERIAL3 = "material3"
    FLUENT = "fluent"
    DEFAULT = "default"
    NEURO = "neuro"  # Example of a new layout

class ThemeProvider:
    @staticmethod
    def initialize():
        """Initialize the UI theme system."""
        # Set default theme if not already set
        if "ui_theme" not in st.session_state:
            st.session_state.ui_theme = UITheme.DEFAULT
        
        # Add JS for theme persistence across page loads
        ThemeProvider._add_theme_persistence_js()

    @staticmethod
    def _add_theme_persistence_js():
        """Add JavaScript to handle theme persistence using localStorage."""
        st.markdown("""
        <script>
        // On page load, check for stored theme
        document.addEventListener('DOMContentLoaded', function() {
            const storedTheme = localStorage.getItem('brainventure_ui_theme');
            if (storedTheme) {
                console.log("Loading stored theme: " + storedTheme);
                // We'll handle the actual theme loading in Python
            }
        });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def set_theme(theme):
        """Set the UI theme and handle persistence."""
        # Save previous theme for comparison
        previous_theme = st.session_state.ui_theme if "ui_theme" in st.session_state else None
        
        # Set new theme
        st.session_state.ui_theme = theme
        
        # If theme changed, force reload
        if previous_theme is not None and previous_theme != theme:
            # Store theme in browser localStorage for persistence
            js_code = f"""
            <script>
            // Store theme for persistence
            localStorage.setItem('brainventure_ui_theme', '{theme.value}');
            
            // Wait a moment to apply changes
            setTimeout(function() {{
                // Force full page reload to apply theme across all components
                window.parent.location.reload();
            }}, 200);
            </script>
            """
            st.markdown(js_code, unsafe_allow_html=True)
            
            # Apply theme immediately
            ThemeProvider.apply_theme()
    
    @staticmethod
    def get_current_theme():
        """Get the current UI theme."""
        return st.session_state.ui_theme
    
    @staticmethod
    def apply_theme():
        """Apply the current theme to the UI."""
        # Debug info
        st.sidebar.text(f"Applying theme: {ThemeProvider.get_current_theme().name}")
        
        # Apply color theme first (light, dark, etc.)
        color_theme = get_current_color_theme()
        apply_color_theme(color_theme)
        
        # Then apply layout theme (Material3, Fluent, etc.)
        theme = ThemeProvider.get_current_theme()
        
        if theme == UITheme.MATERIAL3:
            ThemeProvider._apply_material3_theme()
        elif theme == UITheme.FLUENT:
            ThemeProvider._apply_fluent_theme()
        elif theme == UITheme.NEURO:
            ThemeProvider._apply_neuro_theme()
        else:
            ThemeProvider._apply_default_theme()
    
    @staticmethod
    def _apply_material3_theme():
        """Apply Material 3 design theme."""
        st.markdown("""
        <style>
        /* Material 3 Design System - BARDZIEJ WYRAZISTE */
        body {
            background-color: #E8F0FE !important;
        }
        
        .stApp {
            background-color: #E8F0FE !important;
        }
        
        .main .block-container {
            background-color: white;
            padding: 3rem;
            border-radius: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            margin: 1rem;
        }
        
        /* Apply Material 3 styles */
        .stButton > button {
            background-color: #6750A4 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 24px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
            font-weight: 500 !important;
        }
        
        h1, h2, h3 {
            color: #6750A4 !important;
        }
        
        div[data-testid="stSidebar"] > div {
            background-color: #F5EEFF !important;
            border-radius: 16px;
            margin: 10px;
            padding: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_fluent_theme():
        """Apply Fluent design theme."""
        st.markdown("""
        <style>
        /* Fluent Design System - BARDZIEJ WYRAZISTE */
        body {
            background-color: #FAFAFA !important;
        }
        
        .stApp {
            background-color: #FAFAFA !important;
        }
        
        .main .block-container {
            background-color: white;
            padding: 2rem;
            border-radius: 2px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem;
        }
        
        /* Apply Fluent styles */
        .stButton > button {
            background-color: #0078D4 !important;
            color: white !important;
            border-radius: 2px !important;
            border: none !important;
            padding: 8px 16px !important;
            font-weight: 400 !important;
        }
        
        h1, h2, h3 {
            color: #0078D4 !important;
        }
        
        div[data-testid="stSidebar"] > div {
            background-color: #F3F2F1 !important;
            border-right: 1px solid rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_default_theme():
        """Apply default Streamlit theme."""
        st.markdown("""
        <style>
        /* Reset to default styles */
        body {
            background-color: white !important;
        }
        
        .stApp {
            background-color: white !important;
        }
        
        .main .block-container {
            background-color: white;
            padding: 1rem;
            border-radius: 0px;
            box-shadow: none;
            margin: 0;
        }
        
        .stButton > button {
            /* Reset button styles to default */
            background-color: #f63366 !important;
            border-radius: 4px !important;
        }
        
        h1, h2, h3 {
            color: #262730 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def _apply_neuro_theme():
        """Apply Neuro design theme."""
        st.markdown("""
        <style>
        /* Neuro Design System - BARDZIEJ WYRAZISTE */
        body {
            background-color: #FBE9E7 !important;
        }
        
        .stApp {
            background-color: #FBE9E7 !important;
        }
        
        .main .block-container {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            margin: 1rem;
        }
        
        /* Apply Neuro styles */
        .stButton > button {
            background-color: #FF5722 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
        }
        
        h1, h2, h3 {
            color: #FF5722 !important;
        }
        
        div[data-testid="stSidebar"] > div {
            background-color: #FFCCBC !important;
            border-radius: 12px;
            padding: 15px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_layout_switcher():
        """Create a UI for switching between layout themes."""
        with st.sidebar:
            st.markdown("### Wybierz layout")
            cols = st.columns(len(UITheme))
            
            for idx, theme in enumerate(UITheme):
                with cols[idx]:
                    if st.button(
                        theme.name.capitalize(), 
                        use_container_width=True, 
                        type="primary" if st.session_state.ui_theme == theme else "secondary",
                        key=f"layout_btn_{theme.name.lower()}"
                    ):
                        ThemeProvider.set_theme(theme)
                        st.rerun()
