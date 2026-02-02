# CLI ToDo App - Usage Guide

## Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/gianfranco-omnigpt/cli-todo-5.git
cd cli-todo-5

# Install the package
pip install -e .
```

### Option 2: Run without installation

```bash
# Clone the repository
git clone https://github.com/gianfranco-omnigpt/cli-todo-5.git
cd cli-todo-5

# Run directly using Python module
python -m todo <command> [arguments]
```

## Quick Start

After installation, you can use the `todo` command from anywhere:

```bash
# Add a new task
todo add "Buy groceries"

# List all tasks
todo list

# Mark task as complete
todo done 1

# Delete a task
todo delete 1
```

## Commands

### Add a Task

Create a new task with a description:

```bash
todo add "Task description"
```

**Examples:**
```bash
todo add "Buy milk and bread"
todo add "Review PR #123"
todo add "Call dentist for appointment"
```

**Notes:**
- Task descriptions can contain any characters
- Use quotes for multi-word descriptions
- Tasks are automatically assigned an incremental ID

### List Tasks

Display all tasks with their status:

```bash
todo list
```

**Output format:**
```
You have 3 task(s):

[✓] 1. Buy groceries
[ ] 2. Review code
[ ] 3. Send email
```

**Legend:**
- `[✓]` - Completed task
- `[ ]` - Pending task
- Number indicates task ID

### Complete a Task

Mark a task as done:

```bash
todo done <task_id>
```

**Examples:**
```bash
todo done 1
todo done 5
```

**Notes:**
- Task ID must be a valid number
- Returns error if task doesn't exist
- Completed tasks remain in the list

### Delete a Task

Remove a task from the list:

```bash
todo delete <task_id>
```

**Examples:**
```bash
todo delete 1
todo delete 3
```

**Notes:**
- Task ID must be a valid number
- Returns error if task doesn't exist
- Deletion is permanent

## Data Storage

Tasks are stored in a JSON file at `~/.todo.json`

**Data structure:**
```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "completed": false,
      "created_at": "2024-01-15T10:30:00.123456"
    }
  ],
  "next_id": 2
}
```

**Notes:**
- Data persists across sessions
- File is created automatically on first use
- Manual editing is not recommended
- Backup the file to preserve your tasks

## Error Handling

The app handles common errors gracefully:

### Invalid Task ID
```bash
$ todo done 999
Error: Task 999 not found
```

### Missing Arguments
```bash
$ todo add
Error: Task description required
Usage: python -m todo add "Task description"
```

### Invalid Command
```bash
$ todo unknown
Error: Unknown command 'unknown'
```

### Corrupted Data File
If the JSON file is corrupted, the app will:
1. Display a warning message
2. Reset to an empty task list
3. Continue operation normally

## Tips and Best Practices

### 1. Regular Reviews
Run `todo list` regularly to stay on top of your tasks.

### 2. Clear Descriptions
Use clear, actionable descriptions:
- Good: "Review PR #123 and provide feedback"
- Bad: "Review stuff"

### 3. Archive Completed Tasks
Periodically delete completed tasks to keep your list manageable:
```bash
todo list  # Note completed task IDs
todo delete 1
todo delete 2
```

### 4. Backup Your Data
Create periodic backups of your task list:
```bash
cp ~/.todo.json ~/.todo.json.backup
```

### 5. Shell Aliases
Create shortcuts in your shell configuration:

**Bash/Zsh (~/.bashrc or ~/.zshrc):**
```bash
alias t='todo'
alias ta='todo add'
alias tl='todo list'
alias td='todo done'
alias tx='todo delete'
```

Then use:
```bash
ta "New task"
tl
td 1
```

## Performance

The app is designed for speed:
- All operations complete in <100ms for typical workloads
- No network dependencies
- Minimal memory footprint
- Instant startup time

## Limitations

By design, this app is minimal and does not include:
- Due dates or deadlines
- Task priorities
- Categories or tags
- Multi-user support
- Cloud synchronization
- Task notes or attachments

For these features, consider more advanced tools like Todoist, Things, or org-mode.

## Troubleshooting

### Command not found after installation
Ensure pip's bin directory is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Permission denied errors
Check file permissions:
```bash
ls -la ~/.todo.json
chmod 644 ~/.todo.json
```

### Tasks not persisting
Verify the data file exists and is writable:
```bash
ls -la ~/.todo.json
```

## Running Tests

To run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_core
python -m unittest tests.test_integration

# Run with verbose output
python -m unittest discover tests -v
```

## Contributing

This is a learning project demonstrating clean code practices:
- Follow PEP 8 style guidelines
- Write tests for new features
- Keep it simple and maintainable
- Document your changes

## License

This project is open source and available for educational purposes.
