"""
Content configuration for BrainVenture course.
This file contains the structure definitions for course content.
"""

# Test configuration
TEST_CATEGORIES = {
    "samoswiadomosc": {
        "name": "Samoświadomość neurobiologiczna",
        "description": "Rozumienie własnych procesów neurologicznych i ich wpływu na zachowanie",
        "min_score": 0,
        "max_score": 100
    },
    "zarzadzanie_emocjami": {
        "name": "Zarządzanie emocjami w stresie",
        "description": "Umiejętność kontrolowania reakcji emocjonalnych w sytuacjach stresowych",
        "min_score": 0,
        "max_score": 100
    },
    "podejmowanie_decyzji": {
        "name": "Podejmowanie decyzji",
        "description": "Zdolność do racjonalnego podejmowania decyzji z uwzględnieniem aspektów neurologicznych",
        "min_score": 0,
        "max_score": 100
    },
    "empatia": {
        "name": "Empatia i przywództwo",
        "description": "Umiejętność rozumienia i odpowiedniego reagowania na emocje innych osób",
        "min_score": 0,
        "max_score": 100
    },
    "adaptacja": {
        "name": "Adaptacja i elastyczność",
        "description": "Zdolność do dostosowywania się do zmieniających się okoliczności",
        "min_score": 0,
        "max_score": 100
    }
}

# Course structure configuration
COURSE_BLOCKS = [
    {
        "id": "neurobiologia",
        "emoji": "🔥",
        "title": "Neurobiologia przywództwa",
        "description": "Zrozumienie podstaw neurobiologicznych przywództwa i ich wpływu na zachowanie"
    },
    {
        "id": "procesy_decyzyjne",
        "emoji": "🧠",
        "title": "Procesy decyzyjne lidera",
        "description": "Neurobiologiczne podejście do podejmowania decyzji i rozwiązywania problemów"
    },
    {
        "id": "psychologia_motywacja",
        "emoji": "🌍",
        "title": "Psychologia i motywacja w przywództwie",
        "description": "Neurobiologiczne podstawy motywacji i ich zastosowanie w przywództwie"
    },
    {
        "id": "praktyczne_aspekty",
        "emoji": "💪",
        "title": "Praktyczne aspekty neuroprzywództwa",
        "description": "Praktyczne zastosowania neuroprzywództwa w codziennej pracy lidera"
    },
    {
        "id": "przyszlosc",
        "emoji": "🚀",
        "title": "Przyszłość neuroprzywództwa",
        "description": "Trendy i przyszły rozwój neuroprzywództwa w zmieniającym się świecie"
    }
]

# Badge configuration
BADGES = [
    {
        "id": "first_lesson",
        "icon": "🏆",
        "title": "Pierwszy krok",
        "description": "Ukończenie pierwszej lekcji",
        "requirement": "complete_lesson",
        "requirement_count": 1
    },
    {
        "id": "neuroleader_test",
        "icon": "🧠",
        "title": "Badacz umysłu",
        "description": "Ukończenie testu Neuroliderstwa",
        "requirement": "complete_test",
        "requirement_count": 1
    },
    {
        "id": "login_streak",
        "icon": "⏱️",
        "title": "Punktualność",
        "description": "Logowanie przez 3 dni z rzędu",
        "requirement": "login_streak",
        "requirement_count": 3
    },
    {
        "id": "module_master",
        "icon": "📚",
        "title": "Mistrz modułu",
        "description": "Ukończenie całego modułu",
        "requirement": "complete_module",
        "requirement_count": 1
    },
    {
        "id": "insights_sharer",
        "icon": "💬",
        "title": "Dzielący się wiedzą",
        "description": "Podzielenie się swoimi przemyśleniami w 5 lekcjach",
        "requirement": "share_insights",
        "requirement_count": 5
    }
]
