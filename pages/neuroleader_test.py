import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from utils.ui import card

def show_neuroleader_test():
    """Display the Neuroleader test page."""
    st.title("🧠 Test Neuroliderstwa")
    st.markdown("""
    Test umiejętności Neuroliderskich pozwoli określić Twój obecny poziom 
    i wskazać obszary do rozwoju. Odpowiedz szczerze na wszystkie pytania.
    
    Test składa się z 20 pytań podzielonych na 5 kluczowych obszarów:
    1. **Samoświadomość neurobiologiczna**
    2. **Zarządzanie emocjami w stresie**
    3. **Podejmowanie decyzji**
    4. **Empatia i przywództwo**
    5. **Adaptacja i elastyczność**
    
    Wyniki testu zostaną zapisane w Twoim profilu i posłużą do 
    spersonalizowania ścieżki nauki.
    """)
    
    # Initialize session state for storing test progress
    if 'test_step' not in st.session_state:
        st.session_state.test_step = 0
        st.session_state.answers = {}
        st.session_state.test_complete = False
    
    # Load test questions
    questions = load_test_questions()
    
    if st.session_state.test_complete:
        show_test_results()
    else:
        show_test_questions(questions)

def show_test_questions(questions):
    """Show the test questions based on current step."""
    total_questions = len(questions)
    current_q = st.session_state.test_step
    
    # Progress bar
    progress = current_q / total_questions if current_q < total_questions else 1.0
    st.progress(progress)
    st.write(f"Pytanie {current_q+1} z {total_questions}")
    
    if current_q < total_questions:
        # Display current question
        question = questions[current_q]
        st.markdown(f"### {question['text']}")
        
        # Display answer options
        answer = st.radio(
            "Wybierz odpowiedź:",
            options=question['options'],
            key=f"q_{current_q}",
            index=None
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Następne", key="next"):
                if answer is not None:
                    # Store answer and move to next question
                    st.session_state.answers[current_q] = {
                        'question': question['text'],
                        'answer': answer,
                        'category': question['category']
                    }
                    
                    if current_q + 1 < total_questions:
                        st.session_state.test_step += 1
                    else:
                        # Test complete, calculate results
                        st.session_state.test_complete = True
                    
                    st.rerun()
                else:
                    st.error("Proszę wybrać odpowiedź przed przejściem dalej.")
    
def show_test_results():
    """Show the test results page."""
    st.markdown("## Wyniki Testu Neuroliderstwa")
    
    # Calculate scores per category
    categories = {
        'samoswiadomosc': 'Samoświadomość neurobiologiczna',
        'zarzadzanie_emocjami': 'Zarządzanie emocjami w stresie',
        'podejmowanie_decyzji': 'Podejmowanie decyzji',
        'empatia': 'Empatia i przywództwo',
        'adaptacja': 'Adaptacja i elastyczność'
    }
    
    scores = {cat: 0 for cat in categories.keys()}
    counts = {cat: 0 for cat in categories.keys()}
    
    for q_idx, answer_data in st.session_state.answers.items():
        category = answer_data['category']
        # Simplified scoring - assuming 1 to 5 options with higher being better
        option_idx = answer_data['answer'].split('.')[0]
        score = int(option_idx)
        scores[category] += score
        counts[category] += 1
    
    # Calculate percentages
    percentages = {}
    for cat in scores.keys():
        if counts[cat] > 0:
            percentages[cat] = (scores[cat] / (counts[cat] * 5)) * 100  # Normalize to 0-100%
        else:
            percentages[cat] = 0
    
    # Display radar chart of results
    data = {
        'Kategoria': list(categories.values()),
        'Wynik (%)': [percentages[cat] for cat in categories.keys()]
    }
    results_df = pd.DataFrame(data)
    
    # Display results
    st.write("Twoje wyniki w poszczególnych kategoriach:")
    
    # Bar chart showing results
    st.bar_chart(results_df.set_index('Kategoria'))
    
    # Display advice based on results
    st.markdown("### Rekomendowane obszary rozwoju")
    
    # Find weakest and strongest areas
    weakest = min(percentages.items(), key=lambda x: x[1])
    strongest = max(percentages.items(), key=lambda x: x[1])
    
    st.markdown(f"""
    **Najsilniejszy obszar:** {categories[strongest[0]]} ({strongest[1]:.1f}%)
    
    **Obszar do rozwoju:** {categories[weakest[0]]} ({weakest[1]:.1f}%)
    
    Na podstawie Twoich wyników, rekomendujemy skupienie się na rozwijaniu umiejętności
    z obszaru **{categories[weakest[0]]}**. W tym celu przygotowaliśmy spersonalizowaną 
    ścieżkę nauki dostępną w sekcji Lekcje.
    """)
    
    # Button to go to lessons
    if st.button("Przejdź do lekcji"):
        st.session_state.page = "Lekcje"
        st.rerun()

def load_test_questions():
    """Load test questions from JSON file or return default questions."""
    try:
        with open(os.path.join("data", "content", "test_questions.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default questions
        return [
            {
                "text": "Jak dobrze rozumiesz wpływ procesów neurobiologicznych na swoje zachowania jako lider?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "samoswiadomosc"
            },
            {
                "text": "Jak często potrafisz zidentyfikować procesy neurologiczne stojące za Twoimi decyzjami?",
                "options": ["1. Nigdy", "2. Rzadko", "3. Czasami", "4. Często", "5. Zawsze"],
                "category": "samoswiadomosc"
            },
            {
                "text": "W jakim stopniu rozumiesz, jak Twój mózg reaguje na stres?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "samoswiadomosc"
            },
            {
                "text": "Jak skutecznie zarządzasz swoimi emocjami podczas sytuacji stresowych?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "zarzadzanie_emocjami"
            },
            {
                "text": "Jak często potrafisz zachować spokój i jasność myślenia w sytuacjach kryzysowych?",
                "options": ["1. Nigdy", "2. Rzadko", "3. Czasami", "4. Często", "5. Zawsze"],
                "category": "zarzadzanie_emocjami"
            },
            {
                "text": "W jakim stopniu potrafisz rozpoznawać i przeciwdziałać reakcjom \"walcz lub uciekaj\" w pracy?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "zarzadzanie_emocjami"
            },
            {
                "text": "Jak oceniasz swoją zdolność do podejmowania racjonalnych decyzji pod presją?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "podejmowanie_decyzji"
            },
            {
                "text": "Jak często zauważasz u siebie błędy poznawcze w procesie podejmowania decyzji?",
                "options": ["1. Nigdy", "2. Rzadko", "3. Czasami", "4. Często", "5. Zawsze"],
                "category": "podejmowanie_decyzji"
            },
            {
                "text": "W jakim stopniu uwzględniasz aspekty neurobiologiczne przy podejmowaniu strategicznych decyzji?",
                "options": ["1. Wcale", "2. W małym stopniu", "3. Umiarkowanie", "4. W znacznym stopniu", "5. Zawsze"],
                "category": "podejmowanie_decyzji"
            },
            {
                "text": "Jak oceniasz swoją zdolność do empatycznego zrozumienia reakcji emocjonalnych członków zespołu?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "empatia"
            },
            {
                "text": "W jakim stopniu potrafisz dostosować swój styl przywództwa do neurobiologicznych potrzeb innych?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "empatia"
            },
            {
                "text": "Jak często wykorzystujesz wiedzę o neurobiologii w budowaniu relacji w zespole?",
                "options": ["1. Nigdy", "2. Rzadko", "3. Czasami", "4. Często", "5. Zawsze"],
                "category": "empatia"
            },
            {
                "text": "Jak oceniasz swoją zdolność do szybkiego przystosowywania się do nowych okoliczności?",
                "options": ["1. Bardzo słabo", "2. Słabo", "3. Przeciętnie", "4. Dobrze", "5. Bardzo dobrze"],
                "category": "adaptacja"
            },
            {
                "text": "Jak często poszukujesz nowych podejść do rozwiązywania problemów?",
                "options": ["1. Nigdy", "2. Rzadko", "3. Czasami", "4. Często", "5. Zawsze"],
                "category": "adaptacja"
            },
            {
                "text": "W jakim stopniu wykorzystujesz wiedzę o neuroplastyczności w swoim rozwoju jako lider?",
                "options": ["1. Wcale", "2. W małym stopniu", "3. Umiarkowanie", "4. W znacznym stopniu", "5. Zawsze"],
                "category": "adaptacja"
            }
        ]
