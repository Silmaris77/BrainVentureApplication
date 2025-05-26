import streamlit as st
from enum import Enum

class UITheme(Enum):
    MATERIAL3 = "material3"
    FLUENT = "fluent"
    DEFAULT = "default"
    NEURO = "neuro"

class ThemeProvider:
    @staticmethod
    def initialize():
        """Initialize theme settings if not already set"""
        if "theme" not in st.session_state:
            st.session_state.theme = "light"
        if "layout" not in st.session_state:
            st.session_state.layout = "material3"
        if "theme_just_changed" not in st.session_state:
            st.session_state.theme_just_changed = False
        
        # Add JavaScript to check localStorage
        st.markdown(
            """
            <script>
            function syncThemeWithStreamlit() {
                // Get theme from localStorage
                const storedTheme = localStorage.getItem('brainventure_theme');
                const storedLayout = localStorage.getItem('brainventure_layout');
                
                // Log for debugging
                console.log("Stored theme:", storedTheme);
                console.log("Stored layout:", storedLayout);
                
                // We'll use a hidden element to communicate with Streamlit
                const themeInput = document.createElement('input');
                themeInput.type = 'hidden';
                themeInput.id = 'theme-storage-sync';
                themeInput.value = JSON.stringify({
                    theme: storedTheme || 'light',
                    layout: storedLayout || 'material3'
                });
                document.body.appendChild(themeInput);
            }
            
            // Run on page load
            document.addEventListener('DOMContentLoaded', syncThemeWithStreamlit);
            </script>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def set_layout(layout_name):
        """Set the layout theme and persist it"""
        st.session_state.layout = layout_name
        st.session_state.theme_just_changed = True
        
        # Add JavaScript to store in localStorage
        st.markdown(
            f"""
            <script>
            localStorage.setItem('brainventure_layout', '{layout_name}');
            console.log("Layout set to:", '{layout_name}');
            </script>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def set_theme(theme_name):
        """Set the color theme and persist it"""
        st.session_state.theme = theme_name
        st.session_state.theme_just_changed = True
        
        # Add JavaScript to store in localStorage
        st.markdown(
            f"""
            <script>
            localStorage.setItem('brainventure_theme', '{theme_name}');
            console.log("Theme set to:", '{theme_name}');
            </script>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def apply_theme():
        """Apply the current theme settings"""
        theme = st.session_state.get("theme", "light")
        layout = st.session_state.get("layout", "material3")
        
        # Apply color theme (light/dark)
        if theme == "light":
            ThemeProvider._apply_light_theme()
        else:
            ThemeProvider._apply_dark_theme()
        
        # Apply layout theme
        if layout == "material3":
            ThemeProvider._apply_material3_layout()
        elif layout == "fluent":
            ThemeProvider._apply_fluent_layout()
        elif layout == "neuro":
            ThemeProvider._apply_neuro_layout()
        else:
            ThemeProvider._apply_default_layout()
    
    @staticmethod
    def _apply_light_theme():
        """Apply light color theme"""
        st.markdown("""
        <style>
        :root {
            --text-color: #333333;
            --background-color: #ffffff;
            --secondary-background: #f8f8f8;
            --highlight-color: #ff9800;
            --border-color: #e0e0e0;
            --shadow-color: rgba(0,0,0,0.1);
        }
        
        body {
            color: var(--text-color);
            background-color: var(--background-color);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_dark_theme():
        """Apply dark color theme"""
        st.markdown("""
        <style>
        :root {
            --text-color: #e0e0e0;
            --background-color: #1e1e1e;
            --secondary-background: #2d2d2d;
            --highlight-color: #ff9800;
            --border-color: #444444;
            --shadow-color: rgba(0,0,0,0.3);
        }
        
        body {
            color: var(--text-color);
            background-color: var(--background-color);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--secondary-background);
        }
        
        .stTabs [data-baseweb="tab"] {
            color: var(--text-color);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_material3_layout():
        """Apply Material 3 layout style"""
        st.markdown("""
        <style>
        /* Material 3 Design System */
        .stButton > button {
            border-radius: 12px;
            padding: 10px 24px;
            transition: all 0.3s;
            box-shadow: 0 1px 3px var(--shadow-color);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px var(--shadow-color);
        }
        
        div.stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        div.stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: 500;
        }
        
        .stExpander {
            border-radius: 12px;
            box-shadow: 0 1px 2px var(--shadow-color);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background);
            border-radius: 16px;
            margin: 10px;
            padding: 20px;
        }
        
        /* Sidebar navigation menu */
        [data-testid="stSidebar"] .nav-link {
            border-radius: 12px !important;
            margin: 4px 0 !important;
            transition: all 0.2s ease !important;
        }
        
        [data-testid="stSidebar"] .nav-link.active {
            background-color: var(--highlight-color) !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_fluent_layout():
        """Apply Fluent design layout style"""
        st.markdown("""
        <style>
        /* Fluent Design System */
        .stButton > button {
            border-radius: 4px;
            padding: 8px 16px;
            transition: background-color 0.2s;
            box-shadow: 0 0 0 1px var(--border-color);
        }
        
        .stButton > button:hover {
            background-color: rgba(0,0,0,0.05);
        }
        
        div.stTabs [data-baseweb="tab-list"] {
            border-bottom: 1px solid var(--border-color);
        }
        
        div.stTabs [data-baseweb="tab"] {
            border-radius: 0;
            border-bottom: 2px solid transparent;
            padding: 8px 16px;
        }
        
        div.stTabs [aria-selected="true"] {
            background-color: transparent;
            border-bottom: 2px solid var(--highlight-color);
        }
        
        .stExpander {
            border: 1px solid var(--border-color);
            border-radius: 3px;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background);
            border-right: 1px solid var(--border-color);
            padding: 20px;
        }
        
        /* Sidebar navigation menu */
        [data-testid="stSidebar"] .nav-link {
            border-radius: 2px !important;
            margin: 2px 0 !important;
        }
        
        [data-testid="stSidebar"] .nav-link.active {
            background-color: var(--highlight-color) !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_neuro_layout():
        """Apply Neuro layout style"""
        st.markdown("""
        <style>
        /* Neuro Design System */
        .stButton > button {
            border-radius: 30px;
            padding: 10px 25px;
            background: linear-gradient(145deg, #f0f0f0, #e6e6e6);
            box-shadow: 5px 5px 10px #d1d1d1, -5px -5px 10px #ffffff;
            border: none;
            font-weight: bold;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            box-shadow: 3px 3px 6px #d1d1d1, -3px -3px 6px #ffffff;
            transform: translateY(-2px);
        }
        
        .stButton > button:active {
            box-shadow: inset 5px 5px 10px #d1d1d1, inset -5px -5px 10px #ffffff;
        }
        
        div.stTabs [data-baseweb="tab-list"] {
            background: var(--secondary-background);
            border-radius: 20px;
            padding: 5px;
        }
        
        div.stTabs [data-baseweb="tab"] {
            border-radius: 15px;
            padding: 10px 20px;
            margin: 0 5px;
            transition: all 0.2s ease;
        }
        
        div.stTabs [aria-selected="true"] {
            background: linear-gradient(145deg, #f0f0f0, #e6e6e6);
            box-shadow: 3px 3px 6px #d1d1d1, -3px -3px 6px #ffffff;
        }
        
        .stExpander {
            border-radius: 20px;
            background: var(--background-color);
            box-shadow: 5px 5px 10px #d1d1d1, -5px -5px 10px #ffffff;
            border: none;
            overflow: hidden;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: var(--background-color);
            border-radius: 20px;
            margin: 10px;
            padding: 20px;
            box-shadow: inset 3px 3px 7px var(--shadow-color), inset -3px -3px 7px #ffffff;
        }
        
        /* Sidebar navigation menu */
        [data-testid="stSidebar"] .nav-link {
            border-radius: 15px !important;
            margin: 8px 0 !important;
            transition: all 0.3s ease !important;
            box-shadow: 3px 3px 7px var(--shadow-color), -3px -3px 7px rgba(255,255,255,0.8);
        }
        
        [data-testid="stSidebar"] .nav-link.active {
            background-color: var(--highlight-color) !important;
            color: white !important;
            box-shadow: inset 3px 3px 7px rgba(0,0,0,0.2), inset -3px -3px 7px rgba(255,255,255,0.2);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_default_layout():
        """Apply default Streamlit layout style"""
        st.markdown("""
        <style>
        /* Reset to default Streamlit styles */
        /* This is intentionally minimal to let Streamlit's default styles take effect */
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def get_current_theme():
        """Get the current UI theme from session state"""
        layout = st.session_state.get("layout", "material3")
        
        if layout == "material3":
            return UITheme.MATERIAL3
        elif layout == "fluent":
            return UITheme.FLUENT
        elif layout == "neuro":
            return UITheme.NEURO
        else:
            return UITheme.DEFAULT