"""
Moduł zarządzający motywami (theme) w aplikacji BrainVenture.
"""
import streamlit as st

# Dostępne motywy
THEMES = {
    "light": {
        "primaryColor": "#1c6e42",
        "secondaryColor": "#90c8ac",
        "backgroundColor": "#ffffff",
        "textColor": "#333333",
    },
    "dark": {
        "primaryColor": "#38b676",
        "secondaryColor": "#90c8ac",
        "backgroundColor": "#121212",
        "textColor": "#f1f1f1",
    },
    "blue": {
        "primaryColor": "#0077b6",
        "secondaryColor": "#90e0ef",
        "backgroundColor": "#f5f5ff",
        "textColor": "#333333",
    },
    "purple": {
        "primaryColor": "#8338ec",
        "secondaryColor": "#c8b6ff",
        "backgroundColor": "#f5f0ff",
        "textColor": "#333333",
    }
}

def initialize_theme():
    """
    Inicjalizuje motyw aplikacji. Sprawdza, czy użytkownik wybrał motyw i aplikuje go.
    """
    # Ustaw domyślny motyw jeśli nie został wybrany
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    
    # Aplikuj motyw z session state
    apply_theme(st.session_state.theme)

def apply_theme(theme_name):
    """
    Aplikuje wybrany motyw do interfejsu Streamlit.
    
    Args:
        theme_name: Nazwa motywu do aplikowania
    """
    theme = THEMES.get(theme_name, THEMES["light"])
    
    # Aplikuj kolory CSS
    custom_css = f"""
    <style>
        :root {{
            --primary-color: {theme["primaryColor"]};
            --secondary-color: {theme["secondaryColor"]};
            --background-color: {theme["backgroundColor"]};
            --text-color: {theme["textColor"]};
        }}
        
        .stApp {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        
        .stButton>button, div.stButton button {{
            background-color: var(--primary-color);
            color: white;
        }}
        
        .stProgress .st-bo {{
            background-color: var(--primary-color);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: var(--primary-color);
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def create_theme_switcher(container):
    """
    Tworzy interfejs do wyboru motywu.
    
    Args:
        container: Container Streamlit, w którym ma być wyświetlony przełącznik motywów
    
    Returns:
        bool: True jeśli motyw został zmieniony, False w przeciwnym razie
    """
    theme_changed = False
    current_theme = st.session_state.get('theme', 'light')
    
    theme_options = {
        "light": "☀️ Jasny",
        "dark": "🌙 Ciemny",
        "blue": "🔵 Niebieski",
        "purple": "🟣 Fioletowy"
    }
    
    selected_theme = container.selectbox(
        "Wybierz motyw",
        options=list(theme_options.keys()),
        format_func=lambda x: theme_options[x],
        index=list(theme_options.keys()).index(current_theme)
    )
    
    if selected_theme != current_theme:
        st.session_state.theme = selected_theme
        theme_changed = True
    
    return theme_changed

def get_current_theme():
    """
    Zwraca nazwę aktualnie używanego motywu.
    
    Returns:
        str: Nazwa aktualnie używanego motywu
    """
    return st.session_state.get('theme', 'light')
