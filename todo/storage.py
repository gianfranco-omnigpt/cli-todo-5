"""Storage module for managing task persistence in JSON format.

This module handles reading and writing tasks to a JSON file stored in
the user's home directory (~/.todo.json).
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


STORAGE_FILE = Path.home() / ".todo.json"


def _get_default_data() -> Dict[str, Any]:
    """Return the default data structure for a new storage file.
    
    Returns:
        Dict with empty tasks list and next_id of 1
    """
    return {
        "tasks": [],
        "next_id": 1
    }


def load_data() -> Dict[str, Any]:
    """Load task data from the JSON storage file.
    
    Returns:
        Dictionary containing tasks and next_id
        
    Notes:
        - If file doesn't exist, returns default empty structure
        - If file is corrupted, resets to empty state with warning
        - Handles file permission errors with clear error messages
    """
    if not STORAGE_FILE.exists():
        return _get_default_data()
    
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Validate data structure
        if not isinstance(data, dict) or "tasks" not in data or "next_id" not in data:
            print("Warning: Corrupted data file. Resetting to empty state.")
            return _get_default_data()
            
        return data
        
    except json.JSONDecodeError:
        print("Warning: Corrupted JSON file. Resetting to empty state.")
        return _get_default_data()
        
    except PermissionError:
        print(f"Error: Permission denied when reading {STORAGE_FILE}")
        raise
        
    except Exception as e:
        print(f"Error: Failed to load data: {e}")
        raise


def save_data(data: Dict[str, Any]) -> None:
    """Save task data to the JSON storage file.
    
    Args:
        data: Dictionary containing tasks and next_id
        
    Notes:
        - Creates the file if it doesn't exist
        - Handles file permission errors with clear error messages
        - Uses atomic write (write to temp, then rename) for data safety
    """
    try:
        # Ensure parent directory exists
        STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to temporary file first for atomic operation
        temp_file = STORAGE_FILE.with_suffix('.tmp')
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        temp_file.replace(STORAGE_FILE)
        
    except PermissionError:
        print(f"Error: Permission denied when writing to {STORAGE_FILE}")
        raise
        
    except Exception as e:
        print(f"Error: Failed to save data: {e}")
        raise
