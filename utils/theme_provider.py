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
        # Check if we need to load theme from localStorage
        try_load_from_storage = False
        
        # Set default theme if not already set
        if "ui_theme" not in st.session_state:
            try_load_from_storage = True
            st.session_state.ui_theme = UITheme.DEFAULT
        
        # Add JavaScript for checking localStorage and storing/retrieving themes
        st.markdown(
            """
            <script>
            // Function to handle theme persistence
            function setupThemeSystem() {
                const storedTheme = localStorage.getItem('brainventure_ui_theme');
                if (storedTheme) {
                    console.log("Found stored theme: " + storedTheme);
                    
                    // Try to apply theme from storage
                    try {
                        // Note: We can't directly modify Streamlit's session state from JS
                        // The theme will be retrieved in Python during the next reload
                        console.log("Theme will be applied on next page load: " + storedTheme);
                    } catch (e) {
                        console.error("Error applying theme:", e);
                    }
                }
            }
            
            // Run when the page loads
            if (document.readyState === 'complete') {
                setupThemeSystem();
            } else {
                window.addEventListener('load', setupThemeSystem);
            }
            </script>            """,
            unsafe_allow_html=True
        )
    @staticmethod
    def set_theme(theme):
        """Set the UI theme and handle persistence."""
        # Save previous theme for comparison
        previous_theme = st.session_state.ui_theme if "ui_theme" in st.session_state else None
        
        # Set new theme
        st.session_state.ui_theme = theme
        
        # If theme changed, force reload
        if previous_theme is not None and previous_theme != theme:
            # Add a flag to indicate theme was just changed
            st.session_state.theme_just_changed = True
            
            # Apply theme immediately
            ThemeProvider.apply_theme()
            
            # Add JavaScript to save theme in localStorage and force reload
            st.markdown(
                f"""
                <script>
                // Store current theme in localStorage for persistence
                localStorage.setItem('brainventure_ui_theme', '{theme.value}');
                
                // Set a flag in localStorage to indicate theme was just changed
                localStorage.setItem('brainventure_theme_changed', 'true');
                
                // Wait a moment before reloading to ensure styles are applied
                setTimeout(function() {{
                    // Force full page reload to apply theme across all components
                    window.parent.location.reload();
                }}, 200);
                </script>
                """,
                unsafe_allow_html=True
            )
        
    @staticmethod
    def get_current_theme():
        return st.session_state.ui_theme
    
    @staticmethod
    def apply_theme():
        # Debug info
        st.sidebar.text(f"Applying theme: {ThemeProvider.get_current_theme().name}")
        
        # Apply color theme first
        color_theme = get_current_color_theme()
        apply_color_theme(color_theme)
        
        # Then apply layout theme
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
        # Reset to default Streamlit styling if needed
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
    def create_theme_switcher():
        with st.sidebar:
            st.markdown("### Wybierz layout")
            cols = st.columns(len(UITheme))
            
            for idx, theme in enumerate(UITheme):
                with cols[idx]:
                    if st.button(theme.name.capitalize(), use_container_width=True, 
                               type="primary" if st.session_state.ui_theme == theme else "secondary"):
                        ThemeProvider.set_theme(theme)
                        st.rerun()