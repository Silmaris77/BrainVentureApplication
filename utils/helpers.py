"""
Helper utility functions for BrainVenture application.
"""
import os
import json
import datetime

from typing import Dict, List, Any, Optional, Union

def load_json_data(filepath: str, default: Optional[Any] = None) -> Any:
    """Load JSON data from a file, with a default return value if the file doesn't exist."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else {}
        
def save_json_data(filepath: str, data: Any) -> bool:
    """Save data to a JSON file."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False
        
def get_course_progress(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate course progress statistics based on user data."""
    total_lessons = 150  # Total number of lessons in the course
    completed_lessons = user_data.get('completed_lessons', [])
    completed_count = len(completed_lessons)
    
    # Calculate progress percentage
    progress_percentage = (completed_count / total_lessons) * 100 if total_lessons > 0 else 0
    
    # Calculate module completion
    modules_completion = {}
    for lesson_id in completed_lessons:
        module_id = lesson_id.split('.')[0]
        if module_id not in modules_completion:
            modules_completion[module_id] = 1
        else:
            modules_completion[module_id] += 1
    
    return {
        'total_lessons': total_lessons,
        'completed_lessons': completed_count,
        'progress_percentage': progress_percentage,
        'modules_completion': modules_completion
    }
    
def format_date(date_str: str, output_format: str = "%d %B %Y") -> str:
    """Format a date string into a human-readable format."""
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str
        
def get_lesson_status(user_data: Dict[str, Any], lesson_id: str) -> str:
    """Get the status of a lesson for a user."""
    completed_lessons = user_data.get('completed_lessons', [])
    
    if lesson_id in completed_lessons:
        return "completed"
        
    # Check if prerequisites are met
    prerequisites = user_data.get('prerequisites', {}).get(lesson_id, [])
    if all(prereq in completed_lessons for prereq in prerequisites):
        return "available"
        
    return "locked"
    
def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug."""
    import re
    from unidecode import unidecode
    
    # Convert to lowercase and remove accents
    text = unidecode(text.lower())
    
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    
    # Remove special characters
    text = re.sub(r'[^a-z0-9\-]', '', text)
    
    # Remove duplicate hyphens
    text = re.sub(r'-+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text

# Example usage
if __name__ == "__main__":
    print(slugify("Przykładowy tekst ze spacjami i Polskimi Znakami ĄĆĘ"))
    # Powinno wyświetlić: "przykladowy-tekst-ze-spacjami-i-polskimi-znakami-ace"
