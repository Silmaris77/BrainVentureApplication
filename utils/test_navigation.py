"""
Test script for the navigation system.
Run this file to check if all navigation components work correctly.
"""
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Navigation Test", page_icon="🧭", layout="wide")

# Demos of different menu styles
st.title("Navigation Component Testing")

st.markdown("## Horizontal Menu Demo")

# Horizontal menu
selected_horizontal = option_menu(
    "",
    ["Home", "Dashboard", "Settings"],
    icons=['house', 'speedometer', 'gear'],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0px", "background-color": "#f0f0f0"},
        "icon": {"color": "orange", "font-size": "16px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "padding": "10px"},
        "nav-link-selected": {"background-color": "#4a4a4a", "color": "white"},
    }
)

# Display selected option 
st.markdown(f"Selected option: **{selected_horizontal}**")

st.markdown("## Vertical Sidebar Menu Demo")

with st.sidebar:
    st.title("Menu Test")
    
    selected_vertical = option_menu(
        "Main Menu",
        ["Home", "Dashboard", "Files", "Settings"],
        icons=['house', 'speedometer2', 'file-earmark', 'gear'],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f0f0"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#4a4a4a", "color": "white"},
        }
    )
    
    # Display selected option
    st.markdown(f"Selected option: **{selected_vertical}**")

st.markdown("## Test Results")

# Check if streamlit-option-menu is working properly
if selected_horizontal and selected_vertical:
    st.success("Navigation components are working correctly! ✅")
else:
    st.error("Navigation components are not working correctly. Check installation of streamlit-option-menu. ❌")

st.markdown("""
### Troubleshooting
If the navigation components are not working correctly:

1. Make sure you have installed the required package:
```
pip install streamlit-option-menu
```

2. Check if there are any errors in the console.

3. Restart the Streamlit server.
""")
