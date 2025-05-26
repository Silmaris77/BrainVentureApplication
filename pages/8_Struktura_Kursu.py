import streamlit as st
import json
import os
import sys

# Page config
st.set_page_config(
    page_title="Struktura Kursu", 
    page_icon="📋",
    layout="wide"
)

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation
from utils.theme_provider import ThemeProvider
from components.theme_switcher import initialize_theme, create_theme_switcher, get_current_theme, get_current_layout

# Hide default Streamlit navigation
hide_streamlit_navigation()

# Initialize and apply themes
initialize_theme()
ThemeProvider.initialize()
ThemeProvider.apply_theme()

# Add sidebar navigation
create_sidebar_navigation("Struktura Kursu")

# Add theme switcher to sidebar
st.sidebar.markdown("### Zmień styl interfejsu")
theme_changed = create_theme_switcher(st.sidebar)
if theme_changed:
    st.rerun()

# Function to load course structure
def load_course_structure():
    """Load the course structure from the JSON file."""
    try:
        file_path = os.path.join("data", "content", "course_structure.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Nie udało się wczytać struktury kursu: {e}")
        return []

# Page title
st.title("📚 Struktura Kursu")
st.markdown("""
Poniżej znajdziesz pełną strukturę kursu BrainVenture. Kliknij na nazwę modułu, 
aby zobaczyć dostępne lekcje. Możesz bezpośrednio przejść do wybranej lekcji klikając na jej tytuł.
""")

# Load course structure
course_structure = load_course_structure()

# Function to generate a unique key for each item
def get_unique_key(block_idx, module_idx=None, lesson_idx=None):
    if lesson_idx is not None:
        return f"lesson_{block_idx}_{module_idx}_{lesson_idx}"
    elif module_idx is not None:
        return f"module_{block_idx}_{module_idx}"
    else:
        return f"block_{block_idx}"

# Display course blocks with expandable modules
for block_idx, block in enumerate(course_structure):
    with st.container():
        st.markdown(f"## {block.get('emoji', '📒')} {block.get('title', 'Blok')}")
        st.markdown(block.get('description', ''))
        
        # Display modules as expandable sections
        for module_idx, module in enumerate(block.get('modules', [])):
            module_key = get_unique_key(block_idx, module_idx)
            with st.expander(f"**{module.get('title', 'Moduł')}**"):
                # Module description if available
                if 'description' in module:
                    st.markdown(module.get('description', ''))
                
                # Display lessons as cards
                for lesson_idx, lesson in enumerate(module.get('lessons', [])):
                    lesson_key = get_unique_key(block_idx, module_idx, lesson_idx)
                    
                    # Create a card-like container for each lesson
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            title = lesson.get('title', 'Lekcja')
                            # Add completed indicator if lesson is completed
                            if lesson.get('completed', False):
                                st.markdown(f"✅ **{title}**")
                            else:
                                st.markdown(f"◻️ **{title}**")
                                
                            # Add description if available
                            if 'description' in lesson:
                                st.markdown(f"<small>{lesson['description']}</small>", unsafe_allow_html=True)
                        
                        with col2:
                            if st.button("Rozpocznij", key=lesson_key):
                                # Store lesson info in session state
                                st.session_state['selected_lesson'] = {
                                    'block': block_idx,
                                    'module': module_idx,
                                    'lesson': lesson_idx,
                                    'title': title
                                }
                                # Navigate to lesson page
                                st.switch_page("pages/3_Lekcja.py")
                    
                    # Add small divider between lessons
                    st.markdown("<hr style='margin: 8px 0; opacity: 0.3'>", unsafe_allow_html=True)
        
        # Add divider between blocks
        st.markdown("---")