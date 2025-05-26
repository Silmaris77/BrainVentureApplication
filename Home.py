import streamlit as st
import os
import sys
from utils.theme_provider import ThemeProvider
from components.theme_switcher import initialize_theme as initialize_color_theme

# Set page config - MUSI być pierwszą komendą Streamlit!
st.set_page_config(
    page_title="BrainVenture",
    page_icon="🧠",
    layout="wide"
)

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Automatyczne przekierowanie do Dashboard
st.switch_page("pages/1_Dashboard.py")

# Apply custom CSS
css_path = os.path.join("static", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning(f"CSS file not found at {css_path}")

# Initialize current_page in session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

# Initialize both theming systems
initialize_color_theme()  # Initialize color theme (jasny, ciemny, etc.)
ThemeProvider.initialize() # Initialize layout theme (Material3, Fluent, etc.)

# Apply the current theme
ThemeProvider.apply_theme() # This will apply both color and layout themes

# Add debug info about current theme
st.sidebar.text(f"Active theme: {ThemeProvider.get_current_theme().name}")

# Main dashboard content
st.title("🧠 BrainVenture - Program dla Neuroliderów")
st.markdown("""
Witaj w programie BrainVenture! To kompleksowy kurs neuroprzywództwa, 
który pomoże Ci rozwinąć umiejętności przywódcze w oparciu o najnowsze 
odkrycia z dziedziny neurobiologii.
""")

# Progress card
st.markdown("### Twój postęp")
cols = st.columns([2, 1])
with cols[0]:
    st.progress(0.05)
    st.write("5% kursu ukończone")
with cols[1]:
    st.metric(label="Ukończone lekcje", value="1/20")

st.markdown("---")

st.markdown("### Ostatnia aktywność")
st.info("Ukończono test Neuroliderstwa!")

st.markdown("---")

st.markdown("### Co nowego")
st.success("Nowa lekcja: Podstawy neurobiologii przywództwa już dostępna!")

# Create the navigation sidebar with our utility
from utils.navigation import create_sidebar_navigation
create_sidebar_navigation("Home")

# Display note about the sidebar navigation
st.sidebar.markdown("### ⬅️ Menu nawigacyjne")
st.sidebar.info("Użyj menu po lewej stronie, aby poruszać się po aplikacji!")
