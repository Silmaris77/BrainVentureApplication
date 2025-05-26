import streamlit as st
from utils.theme_provider import ThemeProvider, UITheme

class ThemedCard:
    @staticmethod
    def create(title, content, icon=None):
        theme = ThemeProvider.get_current_theme()
        
        if theme == UITheme.MATERIAL3:
            ThemedCard._material3_card(title, content, icon)
        elif theme == UITheme.FLUENT:
            ThemedCard._fluent_card(title, content, icon)
        elif theme == UITheme.NEURO:
            ThemedCard._neuro_card(title, content, icon)
        else:
            ThemedCard._default_card(title, content, icon)
    
    @staticmethod
    def _material3_card(title, content, icon):
        st.markdown(f"""
        <div style="background-color: white; border-radius: 16px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.12);">
            <h3 style="color: #6750A4; margin-top: 0;">
                {f'<i class="material-icons">{icon}</i> ' if icon else ''}{title}
            </h3>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _fluent_card(title, content, icon):
        st.markdown(f"""
        <div style="background-color: white; border-radius: 4px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #0078D4; margin-top: 0; font-weight: 600;">
                {title}
            </h3>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _neuro_card(title, content, icon):
        st.markdown(f"""
        <div style="background-color: #FFCCBC; border-radius: 12px; padding: 18px; margin-bottom: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
            <h3 style="color: #FF5722; margin-top: 0; font-weight: 500;">
                {title}
            </h3>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _default_card(title, content, icon):
        st.markdown(f"### {title}")
        st.markdown(content)