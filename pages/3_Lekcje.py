import streamlit as st
import json
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui import card, grid

# Page title for sidebar
st.set_page_config(page_title="Lekcje", page_icon="📚")

# Import navigation utilities
from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation

# Hide default navigation
hide_streamlit_navigation()

# Apply custom CSS
css_path = os.path.join("static", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import the horizontal submenu function
from utils.navigation import create_horizontal_submenu

# Add sidebar navigation
create_sidebar_navigation("Lekcje")

# Create horizontal submenu for lessons categories
lesson_categories = ["Neurobiologia", "Emocje", "Podejmowanie decyzji", "Praktyka"]
lesson_icons = ["diagram-3", "emoji-smile", "lightning", "gear"]
active_category = create_horizontal_submenu("", lesson_categories, lesson_icons)

# Page content
st.title("📚 Lekcje")
st.markdown("""
Poniżej znajdziesz dostępne lekcje kursu Neuroliderstwa. Wybierz interesującą Cię lekcję,
aby rozpocząć naukę.
""")

# Initialize session state if needed
if 'selected_lesson' not in st.session_state:
    st.session_state.selected_lesson = None

# Definicja funkcji show_sample_lesson najpierw, zanim zostanie wywołana
def show_sample_lesson():
    """Show the sample lesson content."""
    st.markdown("""
    ## Wprowadzenie do neuroprzywództwa
    
    Neuroprzywództwo to nowoczesne podejście do przywództwa, które łączy wiedzę z dziedziny neurobiologii
    z praktykami zarządzania i kierowania zespołami. Opiera się na zrozumieniu, jak mózg przetwarza informacje,
    podejmuje decyzje i reaguje na różne sytuacje.
    
    ### Kluczowe aspekty neuroprzywództwa:
    
    1. **Zrozumienie procesów mózgowych** - wiedza o tym, jak mózg funkcjonuje w sytuacjach związanych z przywództwem
    2. **Świadomość wpływu emocji** - rozpoznawanie, jak emocje wpływają na podejmowanie decyzji
    3. **Wykorzystanie mocnych stron mózgu** - optymalizacja procesów myślowych do skutecznego przywództwa
    4. **Rozwijanie inteligencji emocjonalnej** - kluczowego aspektu w zarządzaniu relacjami
    """)
    
    st.image("https://www.coachingcognition.com/wp-content/uploads/2016/08/NeuroLeadership_4pillars.png", 
             caption="Cztery filary neuroprzywództwa")
    
    st.markdown("""
    ## Dlaczego neuroprzywództwo jest ważne?
    
    Tradycyjne modele przywództwa często nie uwzględniają tego, jak mózg faktycznie działa. 
    Neuroprzywództwo pozwala:
    
    - Podejmować lepsze decyzje oparte na zrozumieniu procesów neurobiologicznych
    - Efektywniej zarządzać stresem i emocjami w zespole
    - Tworzyć środowisko pracy wspierające optymalne funkcjonowanie mózgu
    - Budować bardziej autentyczne i skuteczne relacje z zespołem
    """)
    
    st.video("https://www.youtube.com/watch?v=tGdsOXZTyEA")
    
    st.markdown("""
    ## Quiz sprawdzający wiedzę
    """)
    
    with st.form("lesson_quiz"):
        st.markdown("**Pytanie 1: Co jest głównym celem neuroprzywództwa?**")
        q1 = st.radio(
            "Wybierz odpowiedź:",
            [
                "Zwiększanie zysków firmy",
                "Kontrolowanie zachowań pracowników",
                "Łączenie wiedzy neurobiologicznej z praktyką przywództwa",
                "Wprowadzanie sztucznej inteligencji do zarządzania"
            ],
            index=None
        )
        
        st.markdown("**Pytanie 2: Który obszar NIE należy do kluczowych aspektów neuroprzywództwa?**")
        q2 = st.radio(
            "Wybierz odpowiedź:",
            [
                "Zrozumienie procesów mózgowych",
                "Mikromanagement pracowników",
                "Świadomość wpływu emocji",
                "Rozwijanie inteligencji emocjonalnej"
            ],
            index=None
        )
        
        submitted = st.form_submit_button("Sprawdź odpowiedzi")
        
        if submitted:
            score = 0
            
            if q1 == "Łączenie wiedzy neurobiologicznej z praktyką przywództwa":
                st.success("✓ Pytanie 1: Poprawna odpowiedź!")
                score += 1
            else:
                st.error("✗ Pytanie 1: Niepoprawna odpowiedź. Neuroprzywództwo łączy wiedzę neurobiologiczną z praktyką przywództwa.")
            
            if q2 == "Mikromanagement pracowników":
                st.success("✓ Pytanie 2: Poprawna odpowiedź!")
                score += 1
            else:
                st.error("✗ Pytanie 2: Niepoprawna odpowiedź. Mikromanagement nie jest elementem neuroprzywództwa.")
            
            st.markdown(f"**Twój wynik: {score}/2 punktów**")
            
            if score == 2:
                st.balloons()
                st.success("Gratulacje! Ukończyłeś lekcję pomyślnie!")
                
                # Mark the lesson as completed
                for block in course_structure:
                    for module in block['modules']:
                        for lesson in module['lessons']:
                            if lesson['title'] == "Co to jest neuroprzywództwo?":
                                lesson['completed'] = True

# Load course structure
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
                        "title": "Wprowadzenie do neuroprzywództwa",
                        "lessons": [
                            {"title": "Co to jest neuroprzywództwo?", "completed": True},
                            {"title": "Mózg lidera – struktura i funkcje"}
                        ]
                    }
                ]
            }
        ]

course_structure = load_course_structure()

# If no lesson is selected, show the course structure
if st.session_state.selected_lesson is None:
    for block in course_structure:
        st.markdown(f"## {block['emoji']} {block['title']}")
        
        for module in block['modules']:
            st.markdown(f"### {module['title']}")
            
            # Create lesson cards
            lesson_cards = []
            for i, lesson in enumerate(module['lessons']):
                lesson_status = "✅" if lesson.get("completed", False) else "📝"
                card_content = {
                    "title": f"{lesson_status} {lesson['title']}",
                    "content": "Kliknij, aby rozpocząć lekcję",
                    "button_text": "Rozpocznij lekcję",
                    "button_url": f"#{i}",
                    "progress": 1.0 if lesson.get("completed", False) else 0.0
                }
                lesson_cards.append(card_content)
            
            # Display the lessons in a grid layout
            grid(lesson_cards, 3)
            
            # Add buttons for each lesson
            cols = st.columns(3)
            for i, lesson in enumerate(module['lessons']):
                col_idx = i % 3
                with cols[col_idx]:
                    if st.button(f"Otwórz: {lesson['title']}", key=f"lesson_{block['title']}_{module['title']}_{i}"):
                        st.session_state.selected_lesson = {
                            "block": block['title'],
                            "module": module['title'],
                            "lesson": lesson['title'],
                            "index": i
                        }
                        st.rerun()
else:
    # Display the selected lesson
    lesson_data = st.session_state.selected_lesson
    st.markdown(f"#### {lesson_data['block']} > {lesson_data['module']}")
    st.markdown(f"# {lesson_data['lesson']}")
    
    # Display lesson content
    if lesson_data['lesson'] == "Co to jest neuroprzywództwo?":
        show_sample_lesson()
    else:
        st.info("Ta lekcja jest jeszcze w przygotowaniu.")
        
    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⬅️ Wróć do listy lekcji"):
            st.session_state.selected_lesson = None
            st.rerun()
