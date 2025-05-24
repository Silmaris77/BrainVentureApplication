"""
Logger utility for BrainVenture application.
"""
import logging
import os
import datetime
from typing import Optional

def setup_logger(name: str, log_level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Set up a logger with the specified configuration."""
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

# Create default application logger
app_logger = setup_logger(
    'brainventure',
    log_level=logging.INFO,
    log_file=os.path.join('data', 'logs', f'app_{datetime.datetime.now().strftime("%Y%m%d")}.log')
)

def log_user_activity(user_id: str, action: str, details: Optional[dict] = None) -> None:
    """Log user activity for analytics purposes."""
    if details is None:
        details = {}
        
    app_logger.info(f"User {user_id} - {action} - {details}")
