# UI Theme System Documentation

## Overview

The BrainVenture application implements a dual theming system:
1. **Color Theme** - Controls base colors (light, dark, blue, purple)
2. **Layout Theme** - Controls layout and component styling (Material3, Fluent, Default, Neuro)

This document explains how the layout theming system works, how to integrate it with new pages, and how to add new layout themes.

## Initializing and Applying Themes

Every page in the application should include the following code at the beginning, after the `st.set_page_config()` call:

```python
# Initialize themes
initialize_theme()  # Color theme (light, dark, etc.)
ThemeProvider.initialize()  # Layout theme (Material3, Fluent, etc.)

# Apply combined theme
ThemeProvider.apply_theme()
```

This will:
1. Initialize both theming systems
2. Apply the currently selected themes

## Theme Persistence

Themes are persisted using two mechanisms:
1. **Streamlit Session State** - `st.session_state.ui_theme` for the current session
2. **Browser localStorage** - For persistence across page refreshes and navigation

## Creating New Layout Themes

To add a new layout theme:

1. Add a new entry to the `UITheme` enum in `utils/theme_provider.py`:
```python
class UITheme(Enum):
    MATERIAL3 = "material3"
    FLUENT = "fluent"
    DEFAULT = "default"
    NEURO = "neuro"
    NEW_THEME = "new_theme"  # Add your new theme here
```

2. Implement a CSS method for your new theme in the `ThemeProvider` class:
```python
@staticmethod
def _apply_new_theme():
    st.markdown("""
    <style>
    /* Your theme CSS goes here */
    body {
        background-color: #YOUR_COLOR !important;
    }
    
    /* Add more CSS rules for your theme */
    </style>
    """, unsafe_allow_html=True)
```

3. Update the `apply_theme()` method to include your new theme:
```python
@staticmethod
def apply_theme():
    # ...existing code...
    
    if theme == UITheme.MATERIAL3:
        ThemeProvider._apply_material3_theme()
    elif theme == UITheme.FLUENT:
        ThemeProvider._apply_fluent_theme()
    elif theme == UITheme.NEURO:
        ThemeProvider._apply_neuro_theme()
    elif theme == UITheme.NEW_THEME:
        ThemeProvider._apply_new_theme()  # Add your new theme here
    else:
        ThemeProvider._apply_default_theme()
```

## Theme Switching UI

The theme switching UI is provided by the `create_layout_switcher()` function in `utils/navigation.py`. This creates a grid of buttons in the sidebar for switching between available layout themes.

To use it, add this to your page's sidebar:

```python
from utils.navigation import create_layout_switcher

# Add theme switcher to sidebar
create_layout_switcher()
```

## Themed Components

The application also provides a system for creating components that automatically adapt to the current theme. See `components/themed_components.py` for examples.

To use themed components:

```python
from components.themed_components import ThemedCard

# This card will automatically use the styling of the current theme
ThemedCard.create(
    "Card Title", 
    "Card content goes here.",
    "info"
)
```

## Troubleshooting

If you encounter issues with theme persistence:

1. Make sure all pages properly initialize and apply themes
2. Check that the theme switching UI is using the correct methods
3. Verify that the localStorage JavaScript is functioning correctly

## Adding More Visual Distinctiveness

To make themes more visually distinct, focus on modifying these CSS properties:

- Background colors
- Component shapes (border-radius)
- Shadows and depth
- Typography and font weights
- Button styles
- Animation effects
