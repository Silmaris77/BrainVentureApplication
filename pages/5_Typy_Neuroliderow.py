# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import sys
from datetime import datetime

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Typy Neuroliderów", 
    page_icon="👥",
    layout="wide"
)

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui import card
from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation
from components.theme_switcher import initialize_theme, create_theme_switcher, get_current_theme
from utils.neuroleader_types import NeuroleaderTypes

# Hide default Streamlit navigation
hide_streamlit_navigation()

# Initialize and apply theme
initialize_theme()

# Create sidebar navigation
create_sidebar_navigation("Typy Neuroliderów")

# Add theme switcher to sidebar
st.sidebar.markdown("### Zmień styl interfejsu")
theme_changed = create_theme_switcher(st.sidebar)
if theme_changed:
    st.rerun()  # Rerun app to apply theme changes

# Initialize neuroleader types manager
neuroleader_manager = NeuroleaderTypes()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "overview"  # 'overview', 'test', 'type_details', 'results'

if "selected_type" not in st.session_state:
    st.session_state.selected_type = None

if "test_results" not in st.session_state:
    st.session_state.test_results = None

# Helper functions
def go_to_overview():
    st.session_state.page = "overview"
    
def go_to_test():
    st.session_state.page = "test"
    
def go_to_type_details(type_id):
    st.session_state.page = "type_details"
    st.session_state.selected_type = type_id
    
def go_to_results():
    st.session_state.page = "results"

# Create tabs
tab1, tab2, tab3 = st.tabs(["Przegląd Typów", "Test", "Twój Profil"])

# Tab 1: Przegląd Typów
with tab1:
    # Check if we're in type details view
    if st.session_state.page == "type_details" and st.session_state.selected_type:
        # Show type details
        type_id = st.session_state.selected_type
        type_info = neuroleader_manager.get_type_by_id(type_id)
        
        if type_info:
            # Add back button
            if st.button("← Powrót do przeglądu typów"):
                go_to_overview()
                st.rerun()
                
            # Show type header
            st.markdown(f"# {type_info['icon']} {type_info['name']}")
            
            # Show full description
            neuroleader_manager.render_full_description(type_id)
        else:
            st.error("Nie znaleziono informacji o wybranym typie.")
            if st.button("Wróć do przeglądu typów"):
                go_to_overview()
                st.rerun()
    else:
        # Show overview of all types
        st.markdown("# Typy Neuroliderów")
        st.markdown("""
        Poznaj 6 typów neuroliderów, które wyróżniamy w naszym podejściu do przywództwa opartym na neurobiologii.
        Każdy z nas ma dominujący typ, ale wszyscy mamy cechy każdego z nich w różnym stopniu.
        """)
        
        # Display all types in a grid
        for i, type_info in enumerate(neuroleader_manager.get_all_types()):
            with st.container():
                st.markdown("---")
                neuroleader_manager.render_type_card(type_info["id"])
                
                # Button to view details
                if st.button(f"Poznaj szczegóły typu {type_info['name']}", key=f"btn_details_{i}"):
                    go_to_type_details(type_info["id"])
                    st.rerun()

# Tab 2: Test
with tab2:
    st.markdown("# Test Typologii Neuroliderów")
    
    if st.session_state.page == "test":
        # Show test form
        submit_clicked = neuroleader_manager.display_test_form()
        
        if submit_clicked:
            # Calculate results
            answers = {
                q_id: st.session_state[f"question_{q_id}"]
                for q_id in [q["id"] for q in neuroleader_manager.get_test_questions()]
            }
            
            # Process test results
            try:
                results = neuroleader_manager.calculate_test_results(answers)
                st.session_state.test_results = results
                
                # Try to save results to user data
                try:
                    neuroleader_manager.save_test_results("user", results)
                    st.success("Wyniki testu zostały zapisane!")
                except Exception as e:
                    st.success("Test został wypełniony! Przejdź do zakładki 'Twój Profil', aby zobaczyć wyniki.")
                    st.warning(f"Uwaga: Wystąpił problem podczas zapisywania wyników testu: {e}")
            except Exception as e:
                st.error(f"Wystąpił błąd podczas przetwarzania wyników testu: {e}")
    else:
        # Show introduction to the test
        st.markdown("""
        Ten test pomoże Ci odkryć Twój dominujący typ neuroliderski oraz zrozumieć, jak Twój mózg 
        wpływa na Twój styl przywództwa.
        
        Test składa się z 30 pytań i zajmie około 10-15 minut.
        """)
        
        if st.button("Rozpocznij test"):
            go_to_test()
            st.rerun()

# Tab 3: Twój Profil
with tab3:
    st.markdown("# Twój Profil Neuroliderski")
    
    # Zmienna do kontrolowania przepływu
    should_display_results = False
    dominant_type = None
    secondary_type = None
    results = None
    
    # Przełącznik między aktualnymi wynikami a historią testów
    show_history = st.checkbox("Pokaż historię testów", value=False)
    
    if show_history:
        # Wyświetl historię testów
        neuroleader_manager.display_test_history()
        
        if st.button("Wróć do aktualnych wyników"):
            st.session_state.show_history = False
            st.rerun()
    elif "test_results" in st.session_state and st.session_state.test_results is not None:
        results = st.session_state.test_results
        
        # Sprawdzamy czy results ma wymagane pola
        if not isinstance(results, dict) or "dominant_type" not in results:
            st.error("Nieprawidłowy format wyników testu.")
            if st.button("Wykonaj test ponownie"):
                st.session_state.test_results = None
                go_to_test()
                st.rerun()
        else:
            error_occurred = False
            
            try:
                # Pobierz informacje o dominującym i drugorzędnym typie
                dominant_type = neuroleader_manager.get_type_by_id(results["dominant_type"])
                if "secondary_type" in results and results["secondary_type"]:
                    secondary_type = neuroleader_manager.get_type_by_id(results["secondary_type"])
            except Exception as e:
                error_occurred = True
                st.error(f"Błąd podczas pobierania informacji o typach: {str(e)}")
                if st.button("Wykonaj test ponownie"):
                    st.session_state.test_results = None
                    go_to_test()
                    st.rerun()
            
            # Sprawdź czy dominant_type został poprawnie zidentyfikowany
            if not error_occurred and not dominant_type:
                error_occurred = True
                st.error("Nie udało się załadować informacji o dominującym typie neuroliderskim.")
                if st.button("Wykonaj test ponownie"):
                    st.session_state.test_results = None
                    go_to_test()
                    st.rerun()
            
            # Wyświetl wyniki tylko jeśli nie było błędów
            if not error_occurred and dominant_type:
                should_display_results = True
    else:
        st.info("Nie masz jeszcze wyników testu typologii neuroliderów.")
        if st.button("Wykonaj test teraz"):
            go_to_test()
            st.rerun()
    
    # Wyświetl wyniki tylko jeśli wszystko poszło dobrze
    if should_display_results and dominant_type and results:
        # Wyświetl główny wynik
        st.markdown(f"## Twój dominujący typ: {dominant_type['icon']} {dominant_type['name']}")
        st.markdown(dominant_type["short_description"])
        
        # Wykres radarowy wyników
        st.markdown("### Twój profil neuroliderski")
        neuroleader_manager.render_radar_chart(results)
        
        # Wyświetl informacje o drugorzędnym typie jeśli jest dostępny
        if secondary_type:
            st.markdown(f"### Twój drugorzędny typ: {secondary_type['icon']} {secondary_type['name']}")
            st.markdown(secondary_type["short_description"])
        
        # Interpretacje wyników
        st.markdown("### Interpretacja wyników")
        if "interpretations" in results and isinstance(results["interpretations"], dict):
            for type_id, interpretation in results["interpretations"].items():
                type_info = neuroleader_manager.get_type_by_id(type_id)
                if type_info and "scores" in results and type_id in results["scores"]:
                    with st.expander(f"{type_info['icon']} {type_info['name']}: {interpretation}"):
                        st.markdown(f"Wynik: **{results['scores'][type_id]:.1f}/5.0**")
                        resources = neuroleader_manager.get_resources_for_type(type_id)
                        
                        if resources:
                            st.markdown("#### Zalecane materiały rozwojowe:")
                            
                            # Wyświetl zalecane kursy
                            if resources.get("kursy"):
                                st.markdown("**Kursy:**")
                                for course in resources["kursy"]:
                                    st.markdown(f"* {course}")
                            
                            # Wyświetl zalecane książki
                            if resources.get("książki"):
                                st.markdown("**Książki:**")
                                for book in resources["książki"]:
                                    st.markdown(f"* {book}")
        
        # Przyciski akcji
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Wykonaj test ponownie", key="btn_retest_profile"):
                st.session_state.test_results = None
                go_to_test()
                st.rerun()
                
        with col2:
            if st.button("Zapisz wyniki", key="btn_save_profile"):
                try:
                    success = neuroleader_manager.save_test_results("user", results)
                    if success:
                        st.success("Wyniki zostały zapisane pomyślnie!")
                    else:
                        st.error("Nie udało się zapisać wyników.")
                except Exception as e:
                    st.error(f"Wystąpił błąd podczas zapisywania wyników: {e}")
