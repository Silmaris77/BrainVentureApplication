import streamlit as st

# Page title for sidebar - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Test Neuroliderstwa", page_icon="📋")

import pandas as pd
import numpy as np
import json
import os
import sys
import matplotlib.pyplot as plt

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.navigation import create_sidebar_navigation, hide_streamlit_navigation
from components.theme_switcher import initialize_theme
from utils.theme_provider import ThemeProvider
from utils.ui import card

# Hide default Streamlit navigation
hide_streamlit_navigation()

# Initialize themes
initialize_theme()  # Kolory (jasny, ciemny, itp.)
ThemeProvider.initialize()  # Layout (Material3, Fluent, itp.)

# Apply combined theme
ThemeProvider.apply_theme()

# Import additional navigation utilities
from utils.navigation import create_horizontal_submenu

# Navigation is already hidden above

# Apply custom CSS
css_path = os.path.join("static", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to load test questions
def load_test_questions():
    """Load test questions from JSON file."""
    try:
        file_path = os.path.join("data", "content", "test_questions.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Nie udało się wczytać pytań testowych: {e}")
        return []

# Initialize session state
if 'test_step' not in st.session_state:
    st.session_state.test_step = 0
    
if 'test_answers' not in st.session_state:
    st.session_state.test_answers = {}
    
if 'test_complete' not in st.session_state:
    st.session_state.test_complete = False

# Function to show test results
def show_test_results():
    """Display test results with charts and interpretations."""
    st.title("Wyniki Testu Neuroliderstwa")
    
    # Calculate category scores
    category_scores = {}
    for q_id, answer in st.session_state.test_answers.items():
        category = questions[int(q_id)]["category"]
        if category not in category_scores:
            category_scores[category] = []
        # Convert answer from index to value (1-5)
        category_scores[category].append(int(answer) + 1)
    
    # Calculate average scores
    avg_scores = {cat: np.mean(scores) for cat, scores in category_scores.items()}
    
    # Display overall score
    overall_score = np.mean(list(avg_scores.values()))
    st.markdown(f"### Twój wynik ogólny: {overall_score:.1f}/5.0")
    st.progress(float(overall_score/5.0))
    
    # Create radar chart
    categories = list(avg_scores.keys())
    category_names = {
        "samoswiadomosc": "Samoświadomość",
        "zarzadzanie_emocjami": "Zarządzanie emocjami",
        "podejmowanie_decyzji": "Podejmowanie decyzji",
        "empatia": "Empatia",
        "adaptacja": "Adaptacja"
    }
    
    values = [avg_scores[cat] for cat in categories]
    
    # Create a radar chart using matplotlib
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Number of categories
    N = len(categories)
    
    # Angle of each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Values for the chart
    values_plot = values + values[:1]  # Close the loop
    
    # Draw the chart
    ax.plot(angles, values_plot, linewidth=2, linestyle='solid')
    ax.fill(angles, values_plot, alpha=0.25)
    
    # Add category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([str(category_names.get(cat, str(cat))) for cat in categories])
    
    # Set y-axis limits
    ax.set_ylim(0, 5)
    
    # Add grid lines
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.grid(True)
    
    # Add title
    ax.set_title("Profil Neuroliderstwa", fontsize=15)
    
    # Display the chart
    st.pyplot(fig)
    
    # Display interpretations
    st.markdown("### Interpretacja wyników")
    
    for cat in categories:
        score = avg_scores[cat]
        cat_name = category_names.get(cat, cat)
        
        # Create interpretation based on score
        if score < 2:
            interpretation = f"Potrzebujesz rozwoju w obszarze: {cat_name}. To obszar priorytetowy do pracy."
            emoji = "🟥"
        elif score < 3.5:
            interpretation = f"Masz podstawy w obszarze: {cat_name}. Ten obszar warto rozwijać."
            emoji = "🟨"
        else:
            interpretation = f"Jesteś mocny w obszarze: {cat_name}. Rozwijaj dalej swoje silne strony."
            emoji = "🟩"
        
        st.markdown(f"{emoji} **{cat_name}**: {score:.1f}/5.0 - {interpretation}")
    
    # Recommendations
    st.markdown("### Rekomendowane lekcje")
    
    # Find weakest areas and recommend lessons
    weak_areas = [cat for cat, score in avg_scores.items() if score < 3.5]
    if weak_areas:
        for area in weak_areas[:2]:  # Recommend for top 2 weakest areas
            area_name = category_names.get(area, area)
            st.markdown(f"**Dla obszaru {area_name}:**")
            
            # Here you would dynamically recommend lessons based on the area
            # For now, we'll just recommend some static examples
            if area == "samoswiadomosc":
                lessons = ["Co to jest neuroprzywództwo?", "Mózg lidera – struktura i funkcje"]
            elif area == "zarzadzanie_emocjami":
                lessons = ["Neurobiologia emocji a zarządzanie", "Jak mózg przetwarza stres i zmienność?"]
            elif area == "podejmowanie_decyzji":
                lessons = ["Neuronaukowe podstawy podejmowania decyzji", "Przeciwdziałanie błędom poznawczym"]
            elif area == "empatia":
                lessons = ["Teoria przywództwa opartego na empatii", "Neurobiologia współczucia w przywództwie"]
            else:
                lessons = ["Neuroplastyczność a zdolność do adaptacji", "Jak mózg reaguje na zmiany?"]
            
            for lesson in lessons:
                st.markdown(f"- {lesson}")
    else:
        st.success("Gratulacje! Masz silne wyniki we wszystkich obszarach. Kontynuuj rozwój swoich umiejętności.")
    
    # Restart test button
    if st.button("Rozpocznij test ponownie"):
        st.session_state.test_step = 0
        st.session_state.test_answers = {}
        st.session_state.test_complete = False
        st.rerun()

# Function to display the test questions
def show_test_questions(questions):
    """Show the test questions based on current step."""
    total_questions = len(questions)
    current_q = st.session_state.test_step
    
    # Progress bar
    progress = current_q / total_questions if current_q < total_questions else 1.0
    st.progress(progress)
    st.write(f"Pytanie {current_q+1} z {total_questions}")
    
    if current_q < total_questions:
        question = questions[current_q]
        st.markdown(f"### {question['text']}")
        
        # Display options as radio buttons
        option = st.radio(
            "Wybierz odpowiedź:",
            question['options'],
            key=f"q_{current_q}",
            label_visibility="collapsed"
        )
        
        # Get option index
        option_idx = question['options'].index(option)
        
        col1, col2 = st.columns([1, 5])
        
        with col1:
            if st.button("Dalej", key=f"next_{current_q}"):
                # Save answer
                st.session_state.test_answers[str(current_q)] = option_idx
                
                # Move to next question
                if current_q < total_questions - 1:
                    st.session_state.test_step += 1
                else:
                    st.session_state.test_complete = True
                
                st.rerun()
    else:
        st.session_state.test_complete = True
        st.rerun()

# Add sidebar navigation
create_sidebar_navigation("Test")

# Create horizontal submenu for test
test_sections = ["Informacje", "Pytania", "Wyniki"]
test_icons = ["info-circle", "question-circle", "graph-up"]
active_test_section = create_horizontal_submenu("", test_sections, test_icons)

# Main content
st.title("Test Neuroliderstwa")
st.markdown("""
Ten test pomoże Ci zrozumieć swój obecny poziom umiejętności neuroleadershipu. 
Odpowiedz szczerze na wszystkie pytania, aby uzyskać najbardziej dokładny wynik.
""")

# Load test questions
questions = load_test_questions()

# Display test or results based on completion status
if st.session_state.test_complete:
    show_test_results()
else:
    show_test_questions(questions)
