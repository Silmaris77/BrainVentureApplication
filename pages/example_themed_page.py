import streamlit as st
from utils.theme_provider import ThemeProvider
from components.themed_components import ThemedCard

# Initialize theme provider
ThemeProvider.initialize()

# Apply current theme
ThemeProvider.apply_theme()

st.title("Strona z różnymi motywami")

ThemedCard.create(
    "Karta informacyjna", 
    "To jest przykładowa karta, która dostosowuje się do wybranego motywu.",
    "info"
)

st.button("Zwykły przycisk też zmienia wygląd")

# Theme switcher in sidebar
ThemeProvider.create_theme_switcher()