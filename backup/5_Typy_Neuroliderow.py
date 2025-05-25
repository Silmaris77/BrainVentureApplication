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

from utils.ui import set_theme, card
from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation
from components.theme_switcher import initialize_theme, create_theme_switcher, get_current_theme
# Import NeuroleaderTypes class
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

# Functions for navigation
def go_to_overview():
    st.session_state.page = "overview"
    
def go_to_test():
    st.session_state.page = "test"
    
def go_to_type_details(type_id):
    st.session_state.selected_type = type_id
    st.session_state.page = "type_details"
    
def go_to_results():
    st.session_state.page = "results"

# Create tab navigation
tab1, tab2, tab3 = st.tabs(["📚 Typologia Neuroliderów", "🧠 Test Typu", "📊 Twój Profil"])

# Main content - Tab 1: Typologia
with tab1:
    if st.session_state.page == "overview":
        st.markdown("# Typologia Neuroliderów")
        st.markdown("""
        Poznaj sześć typów neuroliderów, które opisują różne style przywództwa z perspektywy neurobiologicznej.
        Każdy typ ma swoje unikalne mocne strony, wyzwania i neurobiologiczne podstawy.
        
        Odkryj, który typ najlepiej opisuje Twój styl przywództwa!
        """)
        
        # Podział na dwie kolumny dla lepszego układu
        left_col, right_col = st.columns(2)
        
        # Wyświetl wszystkie typy w układzie dwukolumnowym
        types = neuroleader_manager.get_all_types()
        for i, type_info in enumerate(types):
            if i % 2 == 0:
                with left_col:
                    st.markdown("---")
                    neuroleader_manager.render_type_card(type_info["id"])
                    if st.button(f"Poznaj szczegóły typu {type_info['name'].split('–')[0]}", key=f"btn_l_{type_info['id']}"):
                        go_to_type_details(type_info["id"])
            else:
                with right_col:
                    st.markdown("---")
                    neuroleader_manager.render_type_card(type_info["id"])
                    if st.button(f"Poznaj szczegóły typu {type_info['name'].split('–')[0]}", key=f"btn_r_{type_info['id']}"):
                        go_to_type_details(type_info["id"])
        
        # Dodaj przycisk do testu
        st.markdown("---")
        st.markdown("## Odkryj swój typ neuroliderski")
        st.markdown("Wypełnij nasz test, aby dowiedzieć się, który typ neuroliderski najlepiej opisuje Twój styl przywództwa.")
        if st.button("Przejdź do testu", key="btn_go_to_test"):
            go_to_test()
            st.rerun()
    
    elif st.session_state.page == "type_details":
        # Pobierz szczegóły wybranego typu
        selected_type = neuroleader_manager.get_type_by_id(st.session_state.selected_type)
        
        # Przycisk powrotu
        if st.button("← Powrót do wszystkich typów"):
            go_to_overview()
            st.rerun()
        
        # Wyświetl szczegółowy opis typu
        if selected_type:
            neuroleader_manager.render_full_description(selected_type["id"])
        else:
            st.error("Nie znaleziono wybranego typu neuroliderskiego!")
            go_to_overview()
            st.rerun()

# Tab 2: Test Typu
with tab2:
    st.markdown("# Test Typologii Neuroliderów")
    
    if st.session_state.test_results:
        st.success("Gratulacje! Test został już wypełniony. Możesz zobaczyć wyniki w zakładce 'Twój Profil'.")
        if st.button("Wypełnij test ponownie"):
            st.session_state.test_results = None
            st.rerun()
    else:
        # Wyświetl formularz testu
        submit = neuroleader_manager.display_test_form()
        
        if submit:
            # Oblicz wyniki testu
            results = neuroleader_manager.calculate_test_results(st.session_state.neuroleader_test_answers)
            st.session_state.test_results = results
            
            # Zapisz wyniki do profilu użytkownika
            try:
                success = neuroleader_manager.save_test_results("current_user", results)
                if success:
                    st.success("Test został wypełniony i zapisany w Twoim profilu! Przejdź do zakładki 'Twój Profil', aby zobaczyć wyniki.")
                else:
                    st.success("Test został wypełniony! Przejdź do zakładki 'Twój Profil', aby zobaczyć wyniki.")
                    st.warning("Uwaga: Nie udało się zapisać wyników testu w Twoim profilu.")
            except Exception as e:
                st.success("Test został wypełniony! Przejdź do zakładki 'Twój Profil', aby zobaczyć wyniki.")
                st.warning(f"Uwaga: Wystąpił problem podczas zapisywania wyników testu: {e}")

# Tab 3: Twój Profil
with tab3:
    st.markdown("# Twój Profil Neuroliderski")
      # Przełącznik między aktualnymi wynikami a historią testów
    show_history = st.checkbox("Pokaż historię testów", value=False)
    if show_history:
        # Wyświetl historię testów
        neuroleader_manager.display_test_history()
        
        if st.button("Wróć do aktualnych wyników"):
            st.rerun()
    elif st.session_state.test_results:
        results = st.session_state.test_results
        
        # Sprawdzamy czy results ma wymagane pola
        if not isinstance(results, dict) or "dominant_type" not in results:
            st.error("Nieprawidłowy format wyników testu.")
            st.button("Wykonaj test ponownie", on_click=lambda: setattr(st.session_state, "test_results", None))
            return
        
        try:
            # Pobierz informacje o dominującym i drugorzędnym typie
            dominant_type = neuroleader_manager.get_type_by_id(results["dominant_type"])
            secondary_type = None
            if "secondary_type" in results and results["secondary_type"]:
                secondary_type = neuroleader_manager.get_type_by_id(results["secondary_type"])
        except Exception as e:
            st.error(f"Błąd podczas pobierania informacji o typach: {str(e)}")
            st.button("Wykonaj test ponownie", on_click=lambda: setattr(st.session_state, "test_results", None))
            return
        
        if not dominant_type:
            st.error("Nie udało się załadować informacji o dominującym typie neuroliderskim.")
            if st.button("Wykonaj test ponownie"):
                st.session_state.test_results = None
                go_to_test()
                st.rerun()
            return
        
        # Wyświetl główny wynik
        st.markdown(f"## Twój dominujący typ: {dominant_type['icon']} {dominant_type['name']}")
        st.markdown(dominant_type["short_description"])
        
        # Wykres radarowy wyników
        st.markdown("### Twój profil neuroliderski")
        neuroleader_manager.render_radar_chart(results)
        
        # Wyświetl szczegółowe wyniki
        st.markdown("### Szczegółowe wyniki")
        
        # Przygotuj dane dla tabeli wyników
        types_data = []
        for type_info in neuroleader_manager.get_all_types():
            type_id = type_info["id"]
            score = results["scores"].get(type_id, 0)
            interpretation = results["interpretations"].get(type_id, "")
            
            types_data.append({
                "Typ": f"{type_info['icon']} {type_info['name']}",
                "Wynik (1-5)": round(score, 2),
                "Interpretacja": interpretation
            })
        
        # Wyświetl tabelę
        import pandas as pd
        df = pd.DataFrame(types_data)
        st.dataframe(df, hide_index=True, use_container_width=True)
        
        # Podziel na dwie kolumny dla lepszej prezentacji
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Charakterystyka dominującego typu")
            st.markdown(f"**{dominant_type['name']}**")
            st.markdown(f"**Supermoc:** {dominant_type.get('supermoc', '')}")
            st.markdown(f"**Słabość:** {dominant_type.get('slabość', '')}")
            st.markdown(f"**Neurobiologia:** {dominant_type.get('neurobiologia', '')}")
            
            if st.button("Zobacz pełny opis dominującego typu"):
                go_to_type_details(dominant_type["id"])
                st.rerun()
        
        with col2:
            if secondary_type:
                st.markdown("### Wpływ drugorzędnego typu")
                st.markdown(f"**{secondary_type['name']}**")
                st.markdown("Twój styl przywództwa zawiera również cechy drugorzędnego typu, co wzbogaca Twój profil neuroliderski.")
                st.markdown(f"**Supermoc:** {secondary_type.get('supermoc', '')}")
                
                if st.button("Zobacz pełny opis drugorzędnego typu"):
                    go_to_type_details(secondary_type["id"])
                    st.rerun()
        
        # Rekomendacje rozwojowe
        st.markdown("---")
        st.markdown("### Rekomendacje rozwojowe")
        
        # Dynamiczne rekomendacje w zależności od typu
        if dominant_type["id"] == "neuroanalityk":
            st.markdown("""
            1. **Ustaw jasne deadline'y** - aby przełamać tendencję do nadmiernej analizy
            2. **Praktykuj szybkie podejmowanie decyzji** - zacznij od małych, codziennych wyborów
            3. **Stosuj zasadę 80/20** - 80% informacji często wystarcza do podjęcia dobrej decyzji
            4. **Znajdź zaufaną osobę do konsultacji** - która pomoże Ci przełamać impas decyzyjny
            5. **Prowadź dziennik decyzji** - notuj swoje decyzje i ich konsekwencje, aby uczyć się na doświadczeniach
            """)
        elif dominant_type["id"] == "neuroreaktor":
            st.markdown("""
            1. **Wprowadź zasadę pauzy** - odczekaj przynajmniej 10 minut przed podjęciem ważnej decyzji
            2. **Praktykuj techniki mindfulness** - aby lepiej zarządzać reakcjami emocjonalnymi
            3. **Otaczaj się osobami o analitycznym podejściu** - które będą równoważyć Twoją impulsywność
            4. **Korzystaj z list kontrolnych** - aby nie pomijać istotnych aspektów w stresujących sytuacjach
            5. **Prowadź dziennik emocji** - aby lepiej rozumieć swoje wzorce reagowania na stres
            """)
        elif dominant_type["id"] == "neurobalanser":
            st.markdown("""
            1. **Rozwijaj jeszcze bardziej swoją inteligencję emocjonalną** - to Twoja naturalna siła
            2. **Ucz się szybszego podejmowania decyzji** - aby nie utknąć w analizie zbyt wielu perspektyw
            3. **Dziel się swoim zbalansowanym podejściem z innymi** - możesz być cennym mentorem
            4. **Eksperymentuj z bardziej zdecydowanym stylem** - czasem potrzebna jest szybka decyzja
            5. **Pogłębiaj wiedzę o neurobiologii przywództwa** - aby jeszcze lepiej rozumieć mechanizmy stojące za Twoim stylem
            """)
        elif dominant_type["id"] == "neuroempata":
            st.markdown("""
            1. **Rozwijaj umiejętności analityczne** - aby równoważyć swoje naturalne nastawienie na emocje
            2. **Ucz się asertywności** - aby móc podejmować trudne decyzje mimo emocjonalnych kosztów
            3. **Ustanawiaj jasne granice** - aby chronić siebie przed emocjonalnym wypaleniem
            4. **Praktykuj podejmowanie decyzji w oparciu o dane** - nawet jeśli początkowo wydaje się to niekomfortowe
            5. **Buduj zróżnicowany zespół** - z osobami o bardziej analitycznym podejściu
            """)
        elif dominant_type["id"] == "neuroinnowator":
            st.markdown("""
            1. **Rozwijaj cierpliwość i konsekwencję** - aby doprowadzać swoje innowacyjne pomysły do końca
            2. **Wprowadź strukturę do swojego procesu innowacji** - aby skuteczniej wdrażać nowe pomysły
            3. **Ucz się lepszej komunikacji swoich wizji** - aby skuteczniej angażować innych
            4. **Wprowadź regularne momenty refleksji** - aby oceniać efektywność wprowadzanych zmian
            5. **Pracuj nad umiejętnościami budowania konsensusu** - aby zwiększyć szansę na przyjęcie Twoich innowacyjnych rozwiązań
            """)
        elif dominant_type["id"] == "neuroinspirator":
            st.markdown("""
            1. **Rozwijaj umiejętności słuchania** - aby lepiej rozumieć potrzeby zespołu
            2. **Ucz się działania opartego na danych** - aby równoważyć swoją charyzmę faktami
            3. **Buduj struktury wspierające realizację Twoich wizji** - aby Twoje inspirujące idee zostały wdrożone
            4. **Pracuj nad samoświadomością** - aby lepiej rozumieć wpływ swojej charyzmy na innych
            5. **Deleguj odpowiedzialność** - aby budować autonomię i zaangażowanie w zespole
            """)
        
        # Materiały i zasoby do rozwoju - nowa sekcja
        st.markdown("---")
        st.markdown("### Materiały i zasoby do rozwoju")
        
        resources = neuroleader_manager.get_resources_for_type(dominant_type["id"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📚 Polecane książki")
            for book in resources.get("książki", []):
                st.markdown(f"- {book}")
                
            st.markdown("#### 🏋️ Ćwiczenia rozwojowe")
            for exercise in resources.get("ćwiczenia", []):
                st.markdown(f"- {exercise}")
        
        with col2:
            st.markdown("#### 🎓 Polecane kursy")
            for course in resources.get("kursy", []):
                st.markdown(f"- {course}")
                
            st.markdown("#### 🛠️ Przydatne materiały")
            for material in resources.get("materiały", []):
                st.markdown(f"- {material}")
        
        # Przycisk do ponownego testu
        st.markdown("---")
        if st.button("Wypełnij test ponownie", key="btn_retest"):
            st.session_state.test_results = None
            go_to_test()
            st.rerun()
    else:
        st.info("Nie masz jeszcze wyników testu. Przejdź do zakładki 'Test Typu', aby przeprowadzić diagnozę swojego typu neuroliderskiego.")
        if st.button("Przejdź do testu", key="btn_go_to_test2"):
            go_to_test()
            st.rerun()
