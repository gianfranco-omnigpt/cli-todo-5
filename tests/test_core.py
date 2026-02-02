"""Unit tests for core business logic.

These tests verify the correctness of task management operations
including adding, listing, completing, and deleting tasks.
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch
from datetime import datetime

# Import the modules to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo import core, storage


class TestCore(unittest.TestCase):
    """Test cases for core task management functions."""
    
    def setUp(self):
        """Set up test environment with temporary storage file."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.temp_path = Path(self.temp_file.name)
        
        # Patch the storage file location
        self.patcher = patch.object(storage, 'STORAGE_FILE', self.temp_path)
        self.patcher.start()
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        self.patcher.stop()
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def test_add_task(self):
        """Test adding a new task."""
        task = core.add_task("Buy groceries")
        
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Buy groceries")
        self.assertFalse(task["completed"])
        self.assertIn("created_at", task)
        
        # Verify task is persisted
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Buy groceries")
    
    def test_add_multiple_tasks(self):
        """Test adding multiple tasks with auto-incrementing IDs."""
        task1 = core.add_task("Task 1")
        task2 = core.add_task("Task 2")
        task3 = core.add_task("Task 3")
        
        self.assertEqual(task1["id"], 1)
        self.assertEqual(task2["id"], 2)
        self.assertEqual(task3["id"], 3)
        
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 3)
    
    def test_add_task_with_special_characters(self):
        """Test adding tasks with special characters and unicode."""
        descriptions = [
            "Buy milk & bread",
            "Review code: TODO.py",
            "Send email to user@example.com",
            "Task with emoji 🚀",
            "Unicode: 中文测试"
        ]
        
        for desc in descriptions:
            task = core.add_task(desc)
            self.assertEqual(task["description"], desc)
    
    def test_list_tasks_empty(self):
        """Test listing tasks when none exist."""
        tasks = core.list_tasks()
        self.assertEqual(tasks, [])
    
    def test_list_tasks(self):
        """Test listing tasks returns all tasks."""
        core.add_task("Task 1")
        core.add_task("Task 2")
        core.add_task("Task 3")
        
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]["description"], "Task 1")
        self.assertEqual(tasks[1]["description"], "Task 2")
        self.assertEqual(tasks[2]["description"], "Task 3")
    
    def test_complete_task(self):
        """Test marking a task as complete."""
        task = core.add_task("Task to complete")
        task_id = task["id"]
        
        result = core.complete_task(task_id)
        self.assertTrue(result)
        
        # Verify task is marked complete
        tasks = core.list_tasks()
        self.assertTrue(tasks[0]["completed"])
    
    def test_complete_task_not_found(self):
        """Test completing a non-existent task."""
        result = core.complete_task(999)
        self.assertFalse(result)
    
    def test_complete_task_invalid_id(self):
        """Test completing task with various invalid IDs."""
        core.add_task("Task 1")
        
        # Non-existent ID
        self.assertFalse(core.complete_task(999))
        self.assertFalse(core.complete_task(0))
        self.assertFalse(core.complete_task(-1))
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = core.add_task("Task to delete")
        task_id = task["id"]
        
        result = core.delete_task(task_id)
        self.assertTrue(result)
        
        # Verify task is deleted
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        result = core.delete_task(999)
        self.assertFalse(result)
    
    def test_delete_task_from_multiple(self):
        """Test deleting a specific task from multiple tasks."""
        task1 = core.add_task("Task 1")
        task2 = core.add_task("Task 2")
        task3 = core.add_task("Task 3")
        
        # Delete middle task
        result = core.delete_task(task2["id"])
        self.assertTrue(result)
        
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["id"], task1["id"])
        self.assertEqual(tasks[1]["id"], task3["id"])
    
    def test_get_task(self):
        """Test retrieving a specific task by ID."""
        task = core.add_task("Test task")
        task_id = task["id"]
        
        retrieved = core.get_task(task_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["id"], task_id)
        self.assertEqual(retrieved["description"], "Test task")
    
    def test_get_task_not_found(self):
        """Test retrieving a non-existent task."""
        retrieved = core.get_task(999)
        self.assertIsNone(retrieved)
    
    def test_task_persistence(self):
        """Test that tasks persist across operations."""
        # Add tasks
        core.add_task("Task 1")
        core.add_task("Task 2")
        
        # Complete one task
        core.complete_task(1)
        
        # Reload and verify
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertTrue(tasks[0]["completed"])
        self.assertFalse(tasks[1]["completed"])
    
    def test_empty_description(self):
        """Test adding task with empty description."""
        task = core.add_task("")
        self.assertEqual(task["description"], "")
        
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 1)
    
    def test_task_timestamp_format(self):
        """Test that task timestamps are in ISO format."""
        task = core.add_task("Test task")
        
        # Verify timestamp can be parsed
        try:
            datetime.fromisoformat(task["created_at"])
        except ValueError:
            self.fail("Task timestamp is not in valid ISO format")


class TestStorage(unittest.TestCase):
    """Test cases for storage operations."""
    
    def setUp(self):
        """Set up test environment with temporary storage file."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.temp_path = Path(self.temp_file.name)
        
        # Patch the storage file location
        self.patcher = patch.object(storage, 'STORAGE_FILE', self.temp_path)
        self.patcher.start()
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        self.patcher.stop()
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def test_load_data_nonexistent_file(self):
        """Test loading data when file doesn't exist."""
        if self.temp_path.exists():
            self.temp_path.unlink()
        
        data = storage.load_data()
        self.assertEqual(data["tasks"], [])
        self.assertEqual(data["next_id"], 1)
    
    def test_save_and_load_data(self):
        """Test saving and loading data."""
        data = {
            "tasks": [
                {"id": 1, "description": "Test", "completed": False, "created_at": "2024-01-01T00:00:00"}
            ],
            "next_id": 2
        }
        
        storage.save_data(data)
        loaded = storage.load_data()
        
        self.assertEqual(loaded["tasks"], data["tasks"])
        self.assertEqual(loaded["next_id"], data["next_id"])
    
    def test_load_corrupted_json(self):
        """Test loading corrupted JSON file."""
        # Write invalid JSON
        with open(self.temp_path, 'w') as f:
            f.write("{invalid json")
        
        # Should return default data and print warning
        data = storage.load_data()
        self.assertEqual(data["tasks"], [])
        self.assertEqual(data["next_id"], 1)
    
    def test_load_invalid_structure(self):
        """Test loading JSON with invalid structure."""
        # Write valid JSON but wrong structure
        with open(self.temp_path, 'w') as f:
            json.dump({"wrong": "structure"}, f)
        
        # Should return default data and print warning
        data = storage.load_data()
        self.assertEqual(data["tasks"], [])
        self.assertEqual(data["next_id"], 1)


if __name__ == "__main__":
    unittest.main()
