import streamlit as st
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the navigation utilities instead
from utils.navigation import create_sidebar_navigation

def sidebar_menu(current_page=None):
    """Display the sidebar navigation menu using the updated navigation system."""
    # This now simply calls our centralized navigation system
    create_sidebar_navigation(current_page)
