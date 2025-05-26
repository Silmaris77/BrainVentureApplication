# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import sys
import datetime

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Dashboard Neurolideara", 
    page_icon="📊",
    layout="wide"
)

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui import card, grid
from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation
from components.theme_switcher import initialize_theme, create_theme_switcher, get_current_theme
from utils.theme_provider import ThemeProvider
from utils.neuroleader_types import NeuroleaderTypes  # Używamy zaktualizowanej klasy neuroliderów

# Hide default Streamlit navigation
hide_streamlit_navigation()

# Initialize and apply themes
initialize_theme()  # Inicjalizacja kolorów (jasny, ciemny, etc.)
ThemeProvider.initialize()  # Inicjalizacja layoutu (Material3, Fluent, etc.)

# Apply combined theme
ThemeProvider.apply_theme()

# Debug information
if st.session_state.get("theme_just_changed", False):
    st.info("Theme has been changed! Reloading...")
    # Reset the flag
    st.session_state.theme_just_changed = False

# Function to load course structure
def load_course_structure():
    """Load the course structure from the JSON file."""
    try:
        file_path = os.path.join("data", "content", "course_structure.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Nie udało się wczytać struktury kursu: {e}")
        # Return default structure (first block only for MVP)
        return [
            {
                "emoji": "🔥",
                "title": "Neurobiologia przywództwa",
                "modules": [
                    {
                        "title": "🧠 Wprowadzenie do neuroprzywództwa",
                        "lessons": [
                            {"title": "Co to jest neuroprzywództwo?", "completed": True},
                            {"title": "Mózg lidera – struktura i funkcje"},
                            {"title": "Neuronaukowe podstawy podejmowania decyzji"},
                            {"title": "Jak mózg przetwarza stres i zmienność?"},
                            {"title": "Neurobiologia emocji a zarządzanie"},
                            {"title": "Rola oksytocyny w przywództwie"},
                            {"title": "Dopamina – motywacja i nagroda"},
                            {"title": "Neuroprzywództwo a zarządzanie stresem"},
                            {"title": "Przewodzenie w kontekście teorii neurobiologicznych"},
                            {"title": "Neuroprzywództwo w praktyce – przykłady z życia"}
                        ]
                    }
                ]
            }
        ]

# Create sidebar navigation
create_sidebar_navigation("Dashboard")

# Add theme switcher to sidebar
st.sidebar.markdown("### Zmień styl interfejsu")
theme_changed = create_theme_switcher(st.sidebar)
if theme_changed:
    st.rerun()  # Rerun app to apply theme changes

# Page content
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
    st.metric(label="Ukończone lekcje", value="1/150")

# Last activity
st.markdown("---")
st.markdown("### Ostatnia aktywność")
st.info("Ukończono test Neuroliderstwa!")

# Inicjalizacja managera typów neuroliderów
neuroleader_manager = NeuroleaderTypes()

# Neurolider type section
st.markdown("---")
st.markdown("### Twój typ neuroliderski")

# Sprawdzenie czy użytkownik ma już wyniki testu:
# 1. Najpierw spróbuj załadować z historii
test_history = neuroleader_manager.get_user_test_history()
has_saved_results = bool(test_history)

# 2. Jeśli nie ma historii, sprawdź czy wyniki są w session_state
if not has_saved_results and "test_results" in st.session_state and st.session_state.test_results:
    # Sprawdzamy czy dane w session_state zawierają wymagane pola
    session_results = st.session_state.test_results
    if isinstance(session_results, dict) and "dominant_type" in session_results:
        has_results = True
        results = session_results
    else:
        has_results = False
        results = None
        st.warning("Nieprawidłowy format wyników testu w sesji.")
else:
    # 3. Jeśli są wyniki w historii, użyj najnowszych
    if has_saved_results and test_history and len(test_history) > 0:
        # Sprawdzamy czy pierwszy element w historii zawiera wymagane pola
        if isinstance(test_history[0], dict) and "dominant_type" in test_history[0]:
            has_results = True
            results = test_history[0]  # Najnowszy wynik jest na początku listy
        else:
            has_results = False
            results = None
            st.warning("Nieprawidłowy format zapisanych wyników testu.")
    else:
        has_results = False
        results = None

if has_results and results is not None:  # Upewniamy się, że results nie jest None
    # Pobranie szczegółów typu
    try:
        dominant_type = neuroleader_manager.get_type_by_id(results["dominant_type"])
    except (TypeError, KeyError):
        # Obsługa przypadku gdy results nie ma klucza "dominant_type" lub jest None
        st.error("Problem z danymi typologii neuroliderów. Skontaktuj się z administratorem.")
        dominant_type = None
    
    if dominant_type:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<h1 style='font-size: 3rem; margin: 0;'>{dominant_type.get('icon', '')}</h1>", unsafe_allow_html=True)
            
            # Pokaż obrazek typu jeśli istnieje
            image_path = os.path.join("static", "images", "neuroleader_types", 
                                      f"{dominant_type['id']}.png")
            if os.path.exists(image_path):
                st.image(image_path, width=120)
        
        with col2:
            st.markdown(f"#### Twój dominujący typ: {dominant_type['name']}")
            st.markdown(dominant_type['short_description'])
        
        st.markdown(f"**Supermoc:** {dominant_type.get('supermoc', '')}")
        
        # Dodaj informację o historii testów jeśli istnieje
        if has_saved_results and len(test_history) > 1:
            st.info(f"Masz {len(test_history)} zapisanych testów Neuroliderstwa w swoim profilu!")
        
        # Przyciski do szczegółowych informacji
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Zobacz szczegółowy profil"):
                # Link do strony z typami neuroliderów
                st.switch_page("pages/5_Typy_Neuroliderow_fixed.py")
        with col2:
            if st.button("Wykonaj test ponownie"):
                # Link do strony z testem
                st.session_state.page = "test"
                st.session_state.test_results = None
                st.switch_page("pages/5_Typy_Neuroliderow_fixed.py")
    else:
        st.info("Ups! Nie udało się załadować Twojego typu neuroliderskiego.")
else:
    # Użytkownik nie ma jeszcze wyników testu
    st.info("Nie wykonałeś jeszcze testu typologii neuroliderów!")
    if st.button("Wykonaj test teraz"):
        # Link do strony z testem
        st.switch_page("pages/5_Typy_Neuroliderow_fixed.py")

# What's new
st.markdown("---")
st.markdown("### Co nowego")
st.success("Nowa lekcja: Podstawy neurobiologii przywództwa już dostępna!")

# Course structure
st.markdown("---")
st.markdown("### Struktura kursu")

# Load and display the course structure
course_structure = load_course_structure()

# Display the course structure with a card-based grid layout
for i, block in enumerate(course_structure):
    with st.expander(f"{block.get('emoji', '📚')} {block['title']}", expanded=i==0):
        for j, module in enumerate(block['modules']):
            st.subheader(f"{module['title']}")
            
            # Create a grid for lessons
            lesson_columns = st.columns(3)
            for k, lesson in enumerate(module['lessons']):
                with lesson_columns[k % 3]:
                    completed = lesson.get('completed', False)
                    status = "✅ Ukończono" if completed else "🔒 Dostępne wkrótce"
                    color = "#1c6e42" if completed else "#4a4a4a"
                    
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:15px; border-radius:8px; margin-bottom:15px; background-color:{'#f0f9f4' if completed else '#f7f7f7'}">
                        <h5 style="margin-top:0">{k+1}. {lesson['title']}</h5>
                        <div style="color:{color}; font-size:0.8em; margin-top:8px">
                            {status}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
