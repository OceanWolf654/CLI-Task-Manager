"""Core task management logic for the CLI application."""

from __future__ import annotations
import json
import os
from dataclasses import asdict, dataclass
from typing import List, Optional


@dataclass
class Task:
    """Represents a single task."""

    id: int
    title: str
    priority: str = "Medium"
    completed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            priority=str(data.get("priority", "Medium")),
            completed=bool(data.get("completed", False)),
        )


class TaskManager:
    """Manages a collection of tasks with validation and file persistence."""

    VALID_PRIORITIES = ("Low", "Medium", "High")

    def __init__(self, storage_file: Optional[str] = None):
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self._next_id: int = 1
        if self.storage_file and os.path.exists(self.storage_file):
            self.load()

    def add_task(self, title: str, priority: str = "Medium") -> Task:
        """Add a new task with validation."""
        cleaned_title = title.strip() if title else ""
        if not cleaned_title:
            raise ValueError("Task title cannot be empty or blank.")

        cleaned_priority = priority.strip().capitalize() if priority else "Medium"
        if cleaned_priority not in self.VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority '{priority}'. Allowed values are: {', '.join(self.VALID_PRIORITIES)}."
            )

        task = Task(
            id=self._next_id,
            title=cleaned_title,
            priority=cleaned_priority,
            completed=False,
        )
        self.tasks.append(task)
        self._next_id += 1
        self._auto_save()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return a copy of tasks, optionally filtering completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if not task:
            raise KeyError(f"Task with ID {task_id} not found.")
        task.completed = True
        self._auto_save()
        return task

    def delete_task(self, task_id: int) -> Task:
        """Delete a task by ID."""
        task = self.get_task(task_id)
        if not task:
            raise KeyError(f"Task with ID {task_id} not found.")
        self.tasks.remove(task)
        self._auto_save()
        return task

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title (case-insensitive)."""
        term = query.strip().lower()
        if not term:
            return []
        return [task for task in self.tasks if term in task.title.lower()]

    def _auto_save(self) -> None:
        """Helper to save if storage file is specified."""
        if self.storage_file:
            self.save()

    def save(self, filepath: Optional[str] = None) -> None:
        """Save tasks to a JSON file."""
        target_path = filepath or self.storage_file
        if not target_path:
            return
        data = {
            "next_id": self._next_id,
            "tasks": [task.to_dict() for task in self.tasks],
        }
        with open(target_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def load(self, filepath: Optional[str] = None) -> None:
        """Load tasks from a JSON file."""
        target_path = filepath or self.storage_file
        if not target_path or not os.path.exists(target_path):
            return
        with open(target_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                self.tasks = [Task.from_dict(item) for item in data.get("tasks", [])]
                self._next_id = int(data.get("next_id", max([t.id for t in self.tasks], default=0) + 1))
            except (json.JSONDecodeError, KeyError, ValueError):
                # If corrupted, start with fresh list
                self.tasks = []
                self._next_id = 1
