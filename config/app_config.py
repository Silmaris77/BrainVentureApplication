"""
Application configuration settings for BrainVenture.
"""

# App settings
APP_NAME = "BrainVenture"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "Program dla Neuroliderów"
APP_ICON = "🧠"

# Content settings
CONTENT_LANGUAGE = "pl"
MAX_LESSONS_PER_MODULE = 10
MODULES_PER_BLOCK = 3
MAX_LESSONS_PER_PAGE = 10

# UI settings
UI_THEME = "light"  # light or dark
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2c3e50"
ACCENT_COLOR = "#27ae60"
UI_FONT = "sans-serif"

# Feature flags
ENABLE_LOGIN = False  # Set to True when login system is implemented
ENABLE_GAMIFICATION = False  # Set to True when gamification system is implemented
ANALYTICS_ENABLED = False  # Set to True when analytics system is implemented
DEBUG = True

# User settings
DEFAULT_USER_PREFERENCES = {
    "email_notifications": True,
    "new_lesson_notifications": True,
    "learning_reminders": False,
    "theme": UI_THEME,
}

# Paths
DATA_DIR = "data"
CONTENT_DIR = "data/content"
USER_FILES_DIR = "data/user_files"
STATIC_DIR = "static"
