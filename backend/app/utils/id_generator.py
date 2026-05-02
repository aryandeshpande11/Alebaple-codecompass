"""
ID generation utilities
"""
import uuid
from datetime import datetime


def generate_id(prefix: str = "proj") -> str:
    """
    Generate a unique ID with a prefix
    
    Args:
        prefix: Prefix for the ID (e.g., 'proj', 'analysis')
    
    Returns:
        Unique ID string (e.g., 'proj_abc123def456')
    """
    # Generate a short UUID (first 12 characters)
    short_uuid = str(uuid.uuid4()).replace('-', '')[:12]
    
    return f"{prefix}_{short_uuid}"


def generate_timestamp_id(prefix: str = "proj") -> str:
    """
    Generate a timestamp-based ID
    
    Args:
        prefix: Prefix for the ID
    
    Returns:
        Timestamp-based ID (e.g., 'proj_20260502_153000_abc')
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    short_uuid = str(uuid.uuid4()).replace('-', '')[:6]
    
    return f"{prefix}_{timestamp}_{short_uuid}"

# Made with Bob
