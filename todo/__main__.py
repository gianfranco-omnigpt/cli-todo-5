"""CLI entry point for the todo application.

This module handles command-line argument parsing and dispatches
commands to the appropriate core functions.

Usage:
    python -m todo add "Task description"
    python -m todo list
    python -m todo done <id>
    python -m todo delete <id>
"""

import sys
from typing import List
from . import core


def print_usage() -> None:
    """Print usage information for the CLI."""
    print("""Usage: python -m todo <command> [arguments]

Commands:
  add "description"    Add a new task
  list                 List all tasks
  done <id>            Mark task as complete
  delete <id>          Delete a task

Examples:
  python -m todo add "Buy groceries"
  python -m todo list
  python -m todo done 1
  python -m todo delete 2
""")


def format_task(task: dict) -> str:
    """Format a task for display.
    
    Args:
        task: Task dictionary with id, description, and completed status
        
    Returns:
        Formatted string representation of the task
    """
    status = "✓" if task["completed"] else " "
    return f"[{status}] {task['id']}. {task['description']}"


def cmd_add(args: List[str]) -> None:
    """Handle the 'add' command.
    
    Args:
        args: Command arguments (should contain task description)
    """
    if not args:
        print("Error: Task description required")
        print("Usage: python -m todo add \"Task description\"")
        sys.exit(1)
    
    description = " ".join(args)
    task = core.add_task(description)
    print(f"Added task {task['id']}: {task['description']}")


def cmd_list(args: List[str]) -> None:
    """Handle the 'list' command.
    
    Args:
        args: Command arguments (unused for list)
    """
    tasks = core.list_tasks()
    
    if not tasks:
        print("No tasks found. Add one with: python -m todo add \"Task description\"")
        return
    
    print(f"\nYou have {len(tasks)} task(s):\n")
    for task in tasks:
        print(format_task(task))
    print()


def cmd_done(args: List[str]) -> None:
    """Handle the 'done' command.
    
    Args:
        args: Command arguments (should contain task ID)
    """
    if not args:
        print("Error: Task ID required")
        print("Usage: python -m todo done <id>")
        sys.exit(1)
    
    try:
        task_id = int(args[0])
    except ValueError:
        print(f"Error: Invalid task ID '{args[0]}'. Must be a number.")
        sys.exit(1)
    
    if core.complete_task(task_id):
        print(f"Marked task {task_id} as complete")
    else:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)


def cmd_delete(args: List[str]) -> None:
    """Handle the 'delete' command.
    
    Args:
        args: Command arguments (should contain task ID)
    """
    if not args:
        print("Error: Task ID required")
        print("Usage: python -m todo delete <id>")
        sys.exit(1)
    
    try:
        task_id = int(args[0])
    except ValueError:
        print(f"Error: Invalid task ID '{args[0]}'. Must be a number.")
        sys.exit(1)
    
    if core.delete_task(task_id):
        print(f"Deleted task {task_id}")
    else:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI application."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "delete": cmd_delete,
    }
    
    if command in commands:
        try:
            commands[command](args)
        except KeyboardInterrupt:
            print("\nOperation cancelled")
            sys.exit(130)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
