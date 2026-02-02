"""Core business logic for task management.

This module provides functions for adding, listing, completing, and deleting tasks.
All functions interact with the storage module for persistence.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from . import storage


def add_task(description: str) -> Dict[str, Any]:
    """Create a new task with the given description.
    
    Args:
        description: The task description text
        
    Returns:
        The created task object with id, description, completed status, and timestamp
        
    Example:
        >>> task = add_task("Buy groceries")
        >>> print(task['description'])
        Buy groceries
    """
    data = storage.load_data()
    
    task = {
        "id": data["next_id"],
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    data["tasks"].append(task)
    data["next_id"] += 1
    
    storage.save_data(data)
    
    return task


def list_tasks() -> List[Dict[str, Any]]:
    """Retrieve all tasks.
    
    Returns:
        List of all task objects
        
    Example:
        >>> tasks = list_tasks()
        >>> for task in tasks:
        ...     print(f"{task['id']}: {task['description']}")
    """
    data = storage.load_data()
    return data["tasks"]


def complete_task(task_id: int) -> bool:
    """Mark a task as completed.
    
    Args:
        task_id: The ID of the task to complete
        
    Returns:
        True if task was found and marked complete, False otherwise
        
    Example:
        >>> success = complete_task(1)
        >>> if success:
        ...     print("Task completed!")
    """
    data = storage.load_data()
    
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["completed"] = True
            storage.save_data(data)
            return True
    
    return False


def delete_task(task_id: int) -> bool:
    """Remove a task from the list.
    
    Args:
        task_id: The ID of the task to delete
        
    Returns:
        True if task was found and deleted, False otherwise
        
    Example:
        >>> success = delete_task(1)
        >>> if success:
        ...     print("Task deleted!")
    """
    data = storage.load_data()
    
    initial_length = len(data["tasks"])
    data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
    
    if len(data["tasks"]) < initial_length:
        storage.save_data(data)
        return True
    
    return False


def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific task by ID.
    
    Args:
        task_id: The ID of the task to retrieve
        
    Returns:
        The task object if found, None otherwise
    """
    data = storage.load_data()
    
    for task in data["tasks"]:
        if task["id"] == task_id:
            return task
    
    return None
