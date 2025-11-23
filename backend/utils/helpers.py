"""
Helper utility functions
"""
import re
from datetime import datetime
from typing import Optional


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format
    
    Args:
        session_id: Session identifier to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not session_id or len(session_id) < 5:
        return False
    
    # Allow alphanumeric, underscores, and hyphens
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, session_id))


def sanitize_input(text: str, max_length: int = 5000) -> str:
    """
    Sanitize user input
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format datetime to ISO string
    
    Args:
        dt: Datetime object (defaults to now)
        
    Returns:
        str: ISO formatted timestamp
    """
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_error_message(exception: Exception) -> str:
    """
    Extract clean error message from exception
    
    Args:
        exception: Exception object
        
    Returns:
        str: Clean error message
    """
    error_msg = str(exception)
    
    # Remove technical stack trace info if present
    if "Traceback" in error_msg:
        lines = error_msg.split("\n")
        error_msg = lines[-1] if lines else error_msg
    
    return error_msg.strip()