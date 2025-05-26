import streamlit as st
import os
import sys

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Theme Tester", 
    page_icon="🎨",
    layout="wide"
)

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.navigation import hide_streamlit_navigation, create_sidebar_navigation
from components.theme_switcher import initialize_theme
from utils.theme_provider import ThemeProvider, UITheme
from components.themed_components import ThemedCard

# Hide default Streamlit navigation
hide_streamlit_navigation()

# Initialize and apply themes
initialize_theme()  # Initialize color theme (light, dark, etc.)
ThemeProvider.initialize()  # Initialize layout theme (Material3, Fluent, etc.)

# Apply combined theme
ThemeProvider.apply_theme()

# Create sidebar navigation
create_sidebar_navigation("Theme Tester")

# Page content
st.title("🎨 Theme Tester")
st.markdown("""
This page demonstrates all available UI layouts in the BrainVenture application.
You can switch between different layouts using the sidebar controls.
""")

# Display current theme info
st.info(f"Current theme: **{ThemeProvider.get_current_theme().name}**")

# Create sections to demonstrate different UI elements
st.header("Headers and Typography")
st.subheader("This is a subheader")
st.markdown("Regular paragraph text looks like this.")
st.markdown("**Bold text** and *italic text* can be used for emphasis.")
st.markdown("---")

# Buttons and interactive elements
st.header("Buttons and Controls")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Primary Button")
with col2:
    st.button("Secondary Button", type="secondary")
with col3:
    st.button("Small Button", use_container_width=False)

# Form elements
st.markdown("---")
st.header("Form Elements")
col1, col2 = st.columns(2)
with col1:
    st.text_input("Text Input", "Enter some text")
    st.number_input("Number Input", min_value=0, max_value=100, value=50)
with col2:
    st.slider("Slider", 0, 100, 50)
    options = ["Option 1", "Option 2", "Option 3"]
    st.selectbox("Select Box", options)

# Cards using themed components
st.markdown("---")
st.header("Themed Components")
col1, col2 = st.columns(2)
with col1:
    ThemedCard.create(
        "Information Card", 
        "This card automatically adapts to the current theme.",
        "info"
    )
with col2:
    ThemedCard.create(
        "Another Card", 
        "Cards are useful for organizing content.",
        "card"
    )

# Progress indicators
st.markdown("---")
st.header("Progress Indicators")
col1, col2 = st.columns(2)
with col1:
    st.progress(0.7)
    st.text("70% Complete")
with col2:
    st.metric(label="Score", value=85, delta=5)

# Theme switching controls
st.markdown("---")
st.header("Theme Controls")
st.markdown("""
Use the sidebar controls to switch between different UI layouts:
- **Material3**: Google's Material Design 3 with rounded corners and subtle shadows
- **Fluent**: Microsoft's Fluent Design with square corners and flat appearance
- **Default**: Standard Streamlit styling
- **Neuro**: Custom BrainVenture theme with orange accents
""")

# Show theme-specific details
current_theme = ThemeProvider.get_current_theme()
if current_theme == UITheme.MATERIAL3:
    st.success("You're currently using the Material3 theme with purple accents and rounded elements.")
elif current_theme == UITheme.FLUENT:
    st.success("You're currently using the Fluent theme with blue accents and sharp corners.")
elif current_theme == UITheme.DEFAULT:
    st.success("You're currently using the Default Streamlit theme.")
elif current_theme == UITheme.NEURO:
    st.success("You're currently using the Neuro theme with orange accents and organic shapes.")

# Debugging information
with st.expander("Debug Information"):
    st.write({
        "Current UI Theme": st.session_state.ui_theme.name if "ui_theme" in st.session_state else "Not set",
        "Current Color Theme": st.session_state.get("theme", "Not set"),
        "Theme Just Changed": st.session_state.get("theme_just_changed", False),
        "Session State Keys": list(st.session_state.keys())
    })
