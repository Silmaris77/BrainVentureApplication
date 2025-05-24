"""
Form validation utilities for BrainVenture application.
"""
import re
import streamlit as st
from typing import Dict, Any, Tuple, List, Optional, Callable

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate an email address."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True, ""
    return False, "Nieprawidłowy adres email."

def validate_password(password: str, min_length: int = 8) -> Tuple[bool, str]:
    """Validate a password."""
    if len(password) < min_length:
        return False, f"Hasło musi mieć co najmniej {min_length} znaków."
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Hasło musi zawierać co najmniej jedną dużą literę."
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Hasło musi zawierać co najmniej jedną małą literę."
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Hasło musi zawierać co najmniej jedną cyfrę."
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Hasło musi zawierać co najmniej jeden znak specjalny."
    
    return True, ""

def validate_required(value: Any, field_name: str) -> Tuple[bool, str]:
    """Validate that a field is not empty."""
    if not value:
        return False, f"Pole '{field_name}' jest wymagane."
    return True, ""

def validate_form(form_data: Dict[str, Any], validations: Dict[str, List[Callable]]) -> Tuple[bool, Dict[str, str]]:
    """
    Validate form data against a set of validation functions.
    
    Args:
        form_data: A dictionary containing form field values
        validations: A dictionary mapping field names to lists of validation functions
        
    Returns:
        A tuple containing:
        - A boolean indicating whether all validations passed
        - A dictionary mapping field names to error messages (empty if validation passed)
    """
    errors = {}
    for field, validators in validations.items():
        if field not in form_data:
            continue
            
        for validator in validators:
            is_valid, error_message = validator(form_data[field])
            if not is_valid:
                errors[field] = error_message
                break
                
    return len(errors) == 0, errors

def show_form_errors(errors: Dict[str, str]) -> None:
    """Display form validation errors in Streamlit."""
    if errors:
        error_text = "\n".join([f"- {message}" for field, message in errors.items()])
        st.error(f"Proszę poprawić następujące błędy:\n{error_text}")
        
def create_validation_schema(form_fields: Dict[str, Dict[str, Any]]) -> Dict[str, List[Callable]]:
    """
    Create a validation schema from a form field definition.
    
    Args:
        form_fields: A dictionary mapping field names to field definitions,
                    where each definition may include a 'validations' key
                    
    Returns:
        A dictionary mapping field names to lists of validation functions
    """
    validation_schema = {}
    
    for field_name, field_def in form_fields.items():
        if 'validations' in field_def:
            validation_schema[field_name] = field_def['validations']
            
    return validation_schema
