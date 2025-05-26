import streamlit as st
from enum import Enum

class UITheme(Enum):
    MATERIAL3 = "material3"
    FLUENT = "fluent"
    DEFAULT = "default"

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
        
        # Apply layout theme (material3/fluent)
        if layout == "material3":
            ThemeProvider._apply_material3_layout()
        else:
            ThemeProvider._apply_fluent_layout()
    
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
        </style>
        """, unsafe_allow_html=True)