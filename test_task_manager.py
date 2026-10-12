"""Unit tests for the Task Manager application."""

import os
import tempfile
import unittest

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):
    """Test suite for Task and TaskManager classes."""

    def setUp(self):
        """Create a fresh TaskManager instance for each test in an isolated temp file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        # Initialize an empty manager pointing to the temp file
        self.manager = TaskManager(storage_file=self.temp_file.name)

    def tearDown(self):
        """Clean up the temp file after testing."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_task_success(self):
        task = self.manager.add_task("Finish homework", "High")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Finish homework")
        self.assertEqual(task.priority, "High")
        self.assertFalse(task.completed)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_add_task_default_priority(self):
        task = self.manager.add_task("Buy groceries")
        self.assertEqual(task.priority, "Medium")

    def test_add_task_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("   ")

    def test_add_task_invalid_priority_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("Task", "Urgent")

    def test_complete_task_success(self):
        task = self.manager.add_task("Read book")
        completed_task = self.manager.complete_task(task.id)
        self.assertTrue(completed_task.completed)

    def test_complete_nonexistent_task_raises_error(self):
        with self.assertRaises(KeyError):
            self.manager.complete_task(999)

    def test_delete_task_success(self):
        task = self.manager.add_task("Wash dishes")
        self.assertEqual(len(self.manager.tasks), 1)
        deleted = self.manager.delete_task(task.id)
        self.assertEqual(deleted.id, task.id)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_delete_nonexistent_task_raises_error(self):
        with self.assertRaises(KeyError):
            self.manager.delete_task(999)

    def test_list_tasks_filtering(self):
        t1 = self.manager.add_task("Task 1")
        t2 = self.manager.add_task("Task 2")
        self.manager.complete_task(t1.id)

        all_tasks = self.manager.list_tasks(include_completed=True)
        pending_tasks = self.manager.list_tasks(include_completed=False)

        self.assertEqual(len(all_tasks), 2)
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].id, t2.id)

    def test_search_tasks(self):
        self.manager.add_task("Buy milk")
        self.manager.add_task("Call doctor")
        self.manager.add_task("Buy bread")

        results = self.manager.search_tasks("buy")
        self.assertEqual(len(results), 2)

        no_results = self.manager.search_tasks("xylophone")
        self.assertEqual(len(no_results), 0)

        empty_query = self.manager.search_tasks("  ")
        self.assertEqual(empty_query, [])

    def test_persistence_save_and_reload(self):
        self.manager.add_task("Persistent Task 1", "Low")
        self.manager.add_task("Persistent Task 2", "High")
        self.manager.complete_task(1)

        # Create a new manager instance pointing to the same file
        reloaded_manager = TaskManager(storage_file=self.temp_file.name)
        self.assertEqual(len(reloaded_manager.tasks), 2)
        self.assertEqual(reloaded_manager.tasks[0].title, "Persistent Task 1")
        self.assertTrue(reloaded_manager.tasks[0].completed)
        self.assertEqual(reloaded_manager.tasks[1].title, "Persistent Task 2")
        self.assertEqual(reloaded_manager.tasks[1].priority, "High")

        # Adding another task after reload should use the next available ID
        t3 = reloaded_manager.add_task("Persistent Task 3")
        self.assertEqual(t3.id, 3)


if __name__ == "__main__":
    unittest.main()
