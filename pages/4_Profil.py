import streamlit as st
import json
import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page title for sidebar
st.set_page_config(page_title="Profil użytkownika", page_icon="👤")

# Import navigation utilities
from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation, create_horizontal_submenu

# Hide default navigation
hide_streamlit_navigation()

# Apply custom CSS
css_path = os.path.join("static", "css", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add sidebar navigation
create_sidebar_navigation("Profil")

# Page content
st.title("👤 Profil użytkownika")

# Create horizontal submenu for profile sections
sections = ["Dane", "Postępy", "Certyfikaty", "Ustawienia"]
icons = ["person-circle", "graph-up", "award", "gear"]
active_section = create_horizontal_submenu("", sections, icons)

# Load user data
def load_user_data():
    """Load user data from JSON file or return default user data."""
    try:
        with open(os.path.join("data", "content", "user_data.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default user data
        return {
            "name": "Jan Kowalski",
            "email": "jan.kowalski@example.com",
            "join_date": "2025-05-20",
            "progress": 5,
            "skills": {
                "self_awareness": 65,
                "emotion_management": 45,
                "decision_making": 70,
                "empathy": 80,
                "adaptability": 60
            },
            "badges": [
                {
                    "icon": "🏆",
                    "title": "Pierwszy krok",
                    "description": "Ukończenie pierwszej lekcji"
                },
                {
                    "icon": "🧠",
                    "title": "Badacz umysłu",
                    "description": "Ukończenie testu Neuroliderstwa"
                },
                {
                    "icon": "⏱️",
                    "title": "Punktualność",
                    "description": "Logowanie przez 3 dni z rzędu"
                }
            ],
            "preferences": {
                "email_notifications": True,
                "new_lesson_notifications": True,
                "learning_reminders": False
            }
        }

# Get user data
user_data = load_user_data()

# Display content based on selected section
if active_section == "Dane":
    # Profile details
    col1, col2 = st.columns([1, 2])

    with col1:
        # Profile picture
        avatar_path = os.path.join("static", "images", "default_avatar.png")
        if os.path.exists(avatar_path):
            st.image(avatar_path, width=200)
        else:
            st.info("👤 Zdjęcie profilowe")
        st.button("Zmień zdjęcie")

    with col2:
        st.markdown(f"### {user_data['name']}")
        st.markdown(f"**Email:** {user_data['email']}")
        st.markdown(f"**Data dołączenia:** {user_data['join_date']}")
        st.markdown(f"**Postęp kursu:** {user_data['progress']}%")

    st.markdown("---")

    # User settings section
    with st.expander("Edytuj dane profilu"):
        with st.form("profile_form"):
            name = st.text_input("Imię i nazwisko", value=user_data['name'])
            email = st.text_input("Email", value=user_data['email'])
            password = st.text_input("Nowe hasło", type="password")
            confirm_password = st.text_input("Potwierdź hasło", type="password")
            
            submitted = st.form_submit_button("Zapisz zmiany")
            if submitted:
                if password and password != confirm_password:
                    st.error("Hasła nie są identyczne.")
                else:
                    st.success("Zmiany zapisane pomyślnie!")

elif active_section == "Postępy":
    # User progress
    st.markdown("### Twój postęp")
    
    # Progress bars for each category
    st.markdown("#### Kategorie umiejętności")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Samoświadomość neurobiologiczna**")
        st.progress(user_data['skills']['self_awareness'] / 100)
        st.write(f"{user_data['skills']['self_awareness']}%")
        
        st.markdown("**Zarządzanie emocjami w stresie**")
        st.progress(user_data['skills']['emotion_management'] / 100)
        st.write(f"{user_data['skills']['emotion_management']}%")
        
        st.markdown("**Podejmowanie decyzji**")
        st.progress(user_data['skills']['decision_making'] / 100)
        st.write(f"{user_data['skills']['decision_making']}%")
    
    with col2:
        st.markdown("**Empatia i przywództwo**")
        st.progress(user_data['skills']['empathy'] / 100)
        st.write(f"{user_data['skills']['empathy']}%")
        
        st.markdown("**Adaptacja i elastyczność**")
        st.progress(user_data['skills']['adaptability'] / 100)
        st.write(f"{user_data['skills']['adaptability']}%")

elif active_section == "Certyfikaty":
    # Achievement badges
    st.markdown("### Twoje osiągnięcia")
    
    badges = user_data['badges']
    cols = st.columns(len(badges))
    
    for i, badge in enumerate(badges):
        with cols[i]:
            st.markdown(f"""
            <div style='text-align: center'>
                <div style='font-size: 2rem'>{badge['icon']}</div>
                <div><strong>{badge['title']}</strong></div>
                <div style='color: #888; font-size: 0.8em'>{badge['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Available certificates
    st.markdown("### Dostępne certyfikaty")
    st.info("Ukończ 50% kursu, aby odblokować certyfikat 'Podstawy Neuroprzywództwa'")
    st.info("Ukończ 100% kursu, aby odblokować certyfikat 'Ekspert Neuroprzywództwa'")

elif active_section == "Ustawienia":
    # User settings section
    st.markdown("### Ustawienia")
    
    with st.expander("Preferencje powiadomień", expanded=True):
        st.checkbox("Powiadomienia email", value=user_data['preferences']['email_notifications'])
        st.checkbox("Powiadomienia o nowych lekcjach", value=user_data['preferences']['new_lesson_notifications'])
        st.checkbox("Przypomnienia o nauce", value=user_data['preferences']['learning_reminders'])
        
        if st.button("Zapisz preferencje"):
            st.success("Preferencje zapisane pomyślnie!")
            
    with st.expander("Ustawienia aplikacji"):
        theme = st.selectbox("Motyw", ["Jasny", "Ciemny", "Systemowy"])
        language = st.selectbox("Język", ["Polski", "English"])
        
        if st.button("Zapisz ustawienia"):
            st.success("Ustawienia aplikacji zostały zaktualizowane!")
