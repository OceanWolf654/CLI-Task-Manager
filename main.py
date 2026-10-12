"""Main interactive command-line interface for the Task Manager."""

import os
import sys
from task_manager import TaskManager

DEFAULT_STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def display_tasks(tasks, title_banner="TASKS"):
    """Format and print a list of tasks cleanly."""
    print(f"\n--- {title_banner} ---")
    if not tasks:
        print("  No tasks found.")
        return

    print(f"  {'ID':<5} {'Status':<10} {'Priority':<10} {'Title'}")
    print("  " + "-" * 50)
    for task in tasks:
        status_symbol = "[X] Done" if task.completed else "[ ] Pending"
        print(f"  {task.id:<5} {status_symbol:<10} {task.priority:<10} {task.title}")


def prompt_positive_int(prompt_text: str) -> int:
    """Prompt the user for a valid positive integer ID."""
    while True:
        value = input(prompt_text).strip()
        if not value:
            raise ValueError("Input cancelled.")
        if not value.isdigit() or int(value) <= 0:
            print("  [!] Please enter a valid positive number.")
            continue
        return int(value)


def main():
    manager = TaskManager(storage_file=DEFAULT_STORAGE_FILE)

    print("=" * 55)
    print("      Welcome to My CLI Task Manager")
    print("=" * 55)

    while True:
        print("\nMain Menu:")
        print("  1. View all tasks")
        print("  2. View pending tasks only")
        print("  3. Add a new task")
        print("  4. Mark task as completed")
        print("  5. Delete a task")
        print("  6. Search tasks")
        print("  7. Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            display_tasks(manager.list_tasks(), "ALL TASKS")

        elif choice == "2":
            pending = manager.list_tasks(include_completed=False)
            display_tasks(pending, "PENDING TASKS")

        elif choice == "3":
            print("\n--- Add New Task ---")
            title = input("Enter task title (or leave blank to cancel): ").strip()
            if not title:
                print("  [!] Task addition cancelled.")
                continue

            print("Priority options: Low, Medium, High (Default: Medium)")
            priority_input = input("Enter priority: ").strip()
            if not priority_input:
                priority_input = "Medium"

            try:
                task = manager.add_task(title=title, priority=priority_input)
                print(f"  [+] Success! Task #{task.id} added with '{task.priority}' priority.")
            except ValueError as err:
                print(f"  [!] Error: {err}")

        elif choice == "4":
            print("\n--- Mark Task as Completed ---")
            pending = manager.list_tasks(include_completed=False)
            if not pending:
                print("  You have no pending tasks to complete.")
                continue

            try:
                task_id = prompt_positive_int("Enter Task ID to complete (or press Enter to cancel): ")
                task = manager.complete_task(task_id)
                print(f"  [+] Task #{task.id} ('{task.title}') marked as completed!")
            except ValueError:
                print("  [!] Operation cancelled.")
            except KeyError as err:
                print(f"  [!] Error: {err}")

        elif choice == "5":
            print("\n--- Delete Task ---")
            if not manager.tasks:
                print("  No tasks available to delete.")
                continue

            try:
                task_id = prompt_positive_int("Enter Task ID to delete (or press Enter to cancel): ")
                task = manager.delete_task(task_id)
                print(f"  [-] Task #{task.id} ('{task.title}') deleted successfully.")
            except ValueError:
                print("  [!] Operation cancelled.")
            except KeyError as err:
                print(f"  [!] Error: {err}")

        elif choice == "6":
            print("\n--- Search Tasks ---")
            query = input("Enter search keyword: ").strip()
            if not query:
                print("  [!] Search keyword cannot be blank.")
                continue
            results = manager.search_tasks(query)
            display_tasks(results, f"SEARCH RESULTS FOR '{query}'")

        elif choice == "7":
            print("\nGoodbye! Have a productive day!\n")
            sys.exit(0)

        else:
            print("  [!] Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
