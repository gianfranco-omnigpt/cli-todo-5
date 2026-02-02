"""Integration tests for CLI commands.

These tests verify end-to-end functionality of the CLI interface,
testing the complete flow from command parsing to storage.
"""

import unittest
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Import the modules to test
sys.path.insert(0, str(Path(__file__).parent.parent))

from todo import storage, core
from todo.__main__ import main, cmd_add, cmd_list, cmd_done, cmd_delete


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI commands."""
    
    def setUp(self):
        """Set up test environment with temporary storage file."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.temp_path = Path(self.temp_file.name)
        
        # Patch the storage file location
        self.patcher = patch.object(storage, 'STORAGE_FILE', self.temp_path)
        self.patcher.start()
        
        # Capture stdout
        self.held_stdout = StringIO()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()
    
    def tearDown(self):
        """Clean up temporary files and patches after tests."""
        self.stdout_patcher.stop()
        self.patcher.stop()
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def get_output(self) -> str:
        """Get captured stdout output."""
        return self.held_stdout.getvalue()
    
    def test_add_command(self):
        """Test add command creates task."""
        cmd_add(["Buy", "groceries"])
        output = self.get_output()
        
        self.assertIn("Added task 1", output)
        self.assertIn("Buy groceries", output)
        
        # Verify task was created
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Buy groceries")
    
    def test_add_command_no_description(self):
        """Test add command without description."""
        with self.assertRaises(SystemExit):
            cmd_add([])
        
        output = self.get_output()
        self.assertIn("Error", output)
    
    def test_list_command_empty(self):
        """Test list command with no tasks."""
        cmd_list([])
        output = self.get_output()
        
        self.assertIn("No tasks found", output)
    
    def test_list_command_with_tasks(self):
        """Test list command displays tasks."""
        core.add_task("Task 1")
        core.add_task("Task 2")
        
        cmd_list([])
        output = self.get_output()
        
        self.assertIn("2 task(s)", output)
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)
    
    def test_list_command_shows_completion_status(self):
        """Test list command shows completed tasks with checkmark."""
        task1 = core.add_task("Task 1")
        task2 = core.add_task("Task 2")
        core.complete_task(task1["id"])
        
        cmd_list([])
        output = self.get_output()
        
        # Check for completion indicator
        self.assertIn("✓", output)  # Checkmark for completed task
    
    def test_done_command(self):
        """Test done command marks task complete."""
        task = core.add_task("Task to complete")
        
        cmd_done([str(task["id"])])
        output = self.get_output()
        
        self.assertIn("Marked task", output)
        self.assertIn("complete", output)
        
        # Verify task is completed
        tasks = core.list_tasks()
        self.assertTrue(tasks[0]["completed"])
    
    def test_done_command_no_id(self):
        """Test done command without task ID."""
        with self.assertRaises(SystemExit):
            cmd_done([])
        
        output = self.get_output()
        self.assertIn("Error", output)
        self.assertIn("ID required", output)
    
    def test_done_command_invalid_id(self):
        """Test done command with invalid task ID."""
        with self.assertRaises(SystemExit):
            cmd_done(["abc"])
        
        output = self.get_output()
        self.assertIn("Error", output)
        self.assertIn("Invalid", output)
    
    def test_done_command_not_found(self):
        """Test done command with non-existent task ID."""
        with self.assertRaises(SystemExit):
            cmd_done(["999"])
        
        output = self.get_output()
        self.assertIn("not found", output)
    
    def test_delete_command(self):
        """Test delete command removes task."""
        task = core.add_task("Task to delete")
        
        cmd_delete([str(task["id"])])
        output = self.get_output()
        
        self.assertIn("Deleted task", output)
        
        # Verify task is deleted
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_delete_command_no_id(self):
        """Test delete command without task ID."""
        with self.assertRaises(SystemExit):
            cmd_delete([])
        
        output = self.get_output()
        self.assertIn("Error", output)
        self.assertIn("ID required", output)
    
    def test_delete_command_invalid_id(self):
        """Test delete command with invalid task ID."""
        with self.assertRaises(SystemExit):
            cmd_delete(["xyz"])
        
        output = self.get_output()
        self.assertIn("Error", output)
        self.assertIn("Invalid", output)
    
    def test_delete_command_not_found(self):
        """Test delete command with non-existent task ID."""
        with self.assertRaises(SystemExit):
            cmd_delete(["999"])
        
        output = self.get_output()
        self.assertIn("not found", output)
    
    def test_full_workflow(self):
        """Test complete workflow: add, list, complete, delete."""
        # Add tasks
        cmd_add(["Task 1"])
        cmd_add(["Task 2"])
        cmd_add(["Task 3"])
        
        # List tasks
        self.held_stdout = StringIO()
        self.stdout_patcher.stop()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()
        
        cmd_list([])
        output = self.get_output()
        self.assertIn("3 task(s)", output)
        
        # Complete task 2
        self.held_stdout = StringIO()
        self.stdout_patcher.stop()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()
        
        cmd_done(["2"])
        output = self.get_output()
        self.assertIn("Marked task 2", output)
        
        # Delete task 1
        self.held_stdout = StringIO()
        self.stdout_patcher.stop()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()
        
        cmd_delete(["1"])
        output = self.get_output()
        self.assertIn("Deleted task 1", output)
        
        # Final list
        self.held_stdout = StringIO()
        self.stdout_patcher.stop()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()
        
        cmd_list([])
        output = self.get_output()
        self.assertIn("2 task(s)", output)
        self.assertIn("Task 2", output)
        self.assertIn("Task 3", output)
        self.assertNotIn("Task 1", output)


class TestMainFunction(unittest.TestCase):
    """Test the main entry point function."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.temp_path = Path(self.temp_file.name)
        
        self.patcher = patch.object(storage, 'STORAGE_FILE', self.temp_path)
        self.patcher.start()
        
        self.held_stdout = StringIO()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()
    
    def tearDown(self):
        """Clean up after tests."""
        self.stdout_patcher.stop()
        self.patcher.stop()
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    def test_main_no_arguments(self):
        """Test main function with no arguments."""
        with patch.object(sys, 'argv', ['todo']):
            with self.assertRaises(SystemExit):
                main()
        
        output = self.held_stdout.getvalue()
        self.assertIn("Usage", output)
    
    def test_main_unknown_command(self):
        """Test main function with unknown command."""
        with patch.object(sys, 'argv', ['todo', 'unknown']):
            with self.assertRaises(SystemExit):
                main()
        
        output = self.held_stdout.getvalue()
        self.assertIn("Unknown command", output)
    
    def test_main_add_command(self):
        """Test main function with add command."""
        with patch.object(sys, 'argv', ['todo', 'add', 'Test task']):
            main()
        
        output = self.held_stdout.getvalue()
        self.assertIn("Added task", output)
        
        tasks = core.list_tasks()
        self.assertEqual(len(tasks), 1)


if __name__ == "__main__":
    unittest.main()
