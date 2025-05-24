# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui import card, grid

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

# Page configuration
st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# Apply custom CSS
css_path = os.path.join("static", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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