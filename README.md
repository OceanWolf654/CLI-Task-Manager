# CLI Task Manager

A lightweight, beginner-friendly command-line task management tool built with Python. It allows you to create, view, complete, search, and delete tasks directly from your terminal.

---

## Features

- **Interactive Menu**: Simple numbered choices for ease of use.
- **Input Validation**:
  - Rejects empty task titles.
  - Validates priority inputs (`Low`, `Medium`, `High`).
  - Ensures task IDs entered are valid numbers and exist in the list.
- **Task Filtering & Search**: View all tasks or pending tasks only, and search tasks by keyword (case-insensitive).
- **Automatic Persistence**: Tasks are saved automatically to a `tasks.json` file in the project folder and reloaded on start.
- **Zero Third-Party Dependencies**: Uses only standard Python built-ins.

---

## Prerequisites

- **Python 3.8+** (Python 3.10 is installed and tested on this machine)
- No external packages (`pip install`) are required.

---

## Project Structure

```text
First Project/
├── main.py              # CLI entry point and user interaction loops
├── task_manager.py      # Core data models, validation, and storage logic
├── test_task_manager.py # Automated unit test suite
└── README.md            # Documentation and instructions
```

---

## How to Run the Application

Open PowerShell or Command Prompt in this folder and run:

```powershell
python main.py
```

or using the Python launcher:

```powershell
py main.py
```

### Menu Overview

```text
Main Menu:
  1. View all tasks
  2. View pending tasks only
  3. Add a new task
  4. Mark task as completed
  5. Delete a task
  6. Search tasks
  7. Exit
```

---

## How to Run the Unit Tests

To run the automated test suite with verbose output:

```powershell
python -m unittest -v test_task_manager.py
```

All tests are self-contained and run using temporary test files to avoid altering your actual saved tasks.
