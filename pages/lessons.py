import streamlit as st
import json
import os
from utils.ui import card, grid

def show_lessons():
    """Display the lessons page with course content."""
    st.title("📚 Lekcje Neuroprzywództwa")
    
    # Course structure tabs
    tabs = st.tabs(["Wszystkie moduły", "Moduł 1: Wprowadzenie", "Twoja ścieżka"])
    
    with tabs[0]:
        show_all_modules()
    
    with tabs[1]:
        show_module_details(1)
    
    with tabs[2]:
        show_personalized_path()

def show_all_modules():
    """Show all course modules in a grid layout."""
    st.markdown("### Wszystkie moduły kursu")
    
    # Load course structure
    course_structure = load_course_structure()
    
    for block_idx, block in enumerate(course_structure):
        st.markdown(f"## {block['emoji']} Blok {block_idx+1}: {block['title']}")
        
        modules = []
        for module_idx, module in enumerate(block['modules']):
            # Create module card data
            module_num = module_idx + 1
            lessons_count = len(module['lessons'])
            completed_count = sum(1 for lesson in module['lessons'] if lesson.get('completed', False))
            
            modules.append({
                "title": f"Moduł {module_num}: {module['title']}",
                "content": f"{completed_count}/{lessons_count} lekcji ukończonych",
                "button_text": "Przejdź do modułu",
                "button_url": f"#module-{module_num}"
            })
        
        # Display modules in grid
        grid(modules, num_columns=3)

def show_module_details(module_id):
    """Show details of a specific module."""
    st.markdown(f"### Moduł {module_id}: Wprowadzenie do neuroprzywództwa")
    
    # Example lesson
    st.markdown("#### Lekcja 1: Co to jest neuroprzywództwo?")
    
    # Lesson content
    st.markdown("""
    ## Co to jest neuroprzywództwo?
    
    Neuroprzywództwo to podejście do zarządzania i przewodzenia zespołom, które opiera się na zrozumieniu neurobiologicznych podstaw zachowań ludzkich i procesów decyzyjnych.
    
    ### Kluczowe aspekty neuroprzywództwa:
    
    1. **Integracja nauki o mózgu z przywództwem**
       - Wykorzystanie wiedzy o funkcjonowaniu mózgu do lepszego zarządzania
       - Zrozumienie neurobiologicznych podstaw motywacji i zaangażowania
    
    2. **Samoświadomość lidera**
       - Rozpoznawanie własnych wzorców neurologicznych
       - Zrozumienie wpływu stresu na procesy decyzyjne
    
    3. **Empatia i inteligencja społeczna**
       - Neurologiczne podstawy budowania relacji
       - Rozumienie reakcji emocjonalnych innych osób
    
    ### Korzyści z neuroprzywództwa:
    
    - Lepsze podejmowanie decyzji
    - Skuteczniejsze zarządzanie stresem
    - Wyższy poziom zaangażowania zespołu
    - Efektywniejsza komunikacja
    - Zwiększona zdolność adaptacji do zmian
    
    ### Jak neuroprzywództwo zmienia tradycyjne podejście do zarządzania?
    
    Tradycyjne podejście do zarządzania często skupia się na zewnętrznych czynnikach motywacyjnych i formalnych strukturach. Neuroprzywództwo koncentruje się na zrozumieniu wewnętrznych mechanizmów motywacji, procesów poznawczych i reakcji emocjonalnych.
    """)
    
    # Video placeholder
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    # Quiz
    st.markdown("### Sprawdź swoją wiedzę")
    
    with st.form("quiz_form"):
        st.markdown("**Pytanie: Które z poniższych NIE jest kluczowym aspektem neuroprzywództwa?**")
        quiz_answer = st.radio(
            "Wybierz odpowiedź:",
            ["Integracja nauki o mózgu z przywództwem", 
             "Samoświadomość lidera", 
             "Mikromanagement zespołu", 
             "Empatia i inteligencja społeczna"],
            index=None
        )
        
        submitted = st.form_submit_button("Sprawdź odpowiedź")
        
        if submitted:
            if quiz_answer == "Mikromanagement zespołu":
                st.success("Poprawna odpowiedź! Mikromanagement jest przeciwny zasadom neuroprzywództwa.")
            elif quiz_answer:
                st.error("Niepoprawna odpowiedź. Spróbuj ponownie.")
    
    # Complete lesson button
    if st.button("Oznacz lekcję jako ukończoną"):
        st.success("Lekcja oznaczona jako ukończona! Możesz przejść do następnej lekcji.")

def show_personalized_path():
    """Show personalized learning path based on user profile."""
    st.markdown("### Twoja spersonalizowana ścieżka nauki")
    
    # Example personalized recommendations based on test results
    st.info("Na podstawie wyników testu Neuroliderstwa, rekomendujemy rozpoczęcie od następujących lekcji:")
    
    recommended_lessons = [
        {
            "title": "Jak mózg przetwarza stres i zmienność?",
            "content": "Ta lekcja pomoże Ci lepiej zrozumieć reakcje swojego mózgu na sytuacje stresowe.",
            "button_text": "Rozpocznij lekcję",
            "button_url": "#"
        },
        {
            "title": "Neurobiologia emocji a zarządzanie",
            "content": "Poznaj związek między emocjami a procesami decyzyjnymi w kontekście przywództwa.",
            "button_text": "Rozpocznij lekcję",
            "button_url": "#"
        },
        {
            "title": "Jak skutecznie motywować zespół?",
            "content": "Dowiedz się, jak wykorzystać wiedzę o neurobiologii do skutecznego motywowania członków zespołu.",
            "button_text": "Rozpocznij lekcję",
            "button_url": "#"
        }
    ]
    
    # Display recommended lessons
    grid(recommended_lessons, num_columns=3)

def load_course_structure():
    """Load the course structure from a JSON file or return default structure."""
    try:
        with open(os.path.join("data", "content", "course_structure.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
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
                    },
                    {
                        "title": "💡 Mózg, emocje i decyzje",
                        "lessons": [
                            {"title": "Jak emocje wpływają na decyzje liderów?"},
                            {"title": "Rola limbicznego układu w podejmowaniu decyzji"},
                            {"title": "Przeciwdziałanie błędom poznawczym"},
                            {"title": "Jak zrozumieć emocje w pracy zespołowej?"},
                            {"title": "Mechanizmy adaptacji do stresu"},
                            {"title": "Inteligencja emocjonalna lidera"},
                            {"title": "Decyzje pod wpływem emocji a efektywność"},
                            {"title": "Mózg a odporność na krytykę"},
                            {"title": "Przykłady z życia liderów: jak radzili sobie z emocjami"},
                            {"title": "Neurobiologia współczucia w przywództwie"}
                        ]
                    },
                    {
                        "title": "Mechanizmy mózgu w interakcjach społecznych",
                        "lessons": [
                            {"title": "Współczucie jako narzędzie przywódcze"},
                            {"title": "Jak mózg interpretuje zachowanie innych?"},
                            {"title": "Neurologiczne podstawy komunikacji"},
                            {"title": "Zarządzanie konfliktem – mózg i emocje"},
                            {"title": "Teoria przywództwa opartego na empatii"},
                            {"title": "Mózg gadzi vs. racjonalny: jak to wpływa na decyzje?"},
                            {"title": "Jak skutecznie motywować zespół?"},
                            {"title": "Mechanizmy wpływu i perswazji"},
                            {"title": "Neuroprzywództwo a budowanie relacji"},
                            {"title": "Mózg a dynamika grupy"}
                        ]
                    }
                ]
            }
        ]
