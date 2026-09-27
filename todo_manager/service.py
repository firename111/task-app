from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from .model import Task
from .repository import TaskRepository
from .validators import validate_task_input

DEFAULT_CATEGORY = "General"


class TaskService:
    """Application rules. The UI calls this class instead of SQL."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        category: str = DEFAULT_CATEGORY,
        due_date: str = "",
    ) -> Task:
        values = validate_task_input(title, description, priority, due_date)
        clean_category = self._validate_category(category)
        return self.repository.create(
            values[0], values[1], values[2], clean_category, values[3]
        )

    def list_tasks(
        self,
        query: str = "",
        status: str = "All",
        priority: str = "All",
        category: str = "All",
    ) -> list[Task]:
        tasks = self.repository.list_all()
        query = query.strip().lower()
        if query:
            tasks = [
                task
                for task in tasks
                if query in task.title.lower() or query in task.description.lower()
            ]
        if status == "Active":
            tasks = [task for task in tasks if not task.completed]
        elif status == "Completed":
            tasks = [task for task in tasks if task.completed]
        if priority != "All":
            tasks = [task for task in tasks if task.priority == priority]
        if category != "All":
            tasks = [task for task in tasks if task.category == category]
        return tasks

    def get_task(self, task_id: int) -> Task:
        return self.repository.get_by_id(task_id)

    def toggle_completed(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        return self.repository.update(replace(task, completed=not task.completed))

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str,
        priority: str,
        category: str,
        due_date: str,
    ) -> Task:
        values = validate_task_input(title, description, priority, due_date)
        clean_category = self._validate_category(category)
        task = self.repository.get_by_id(task_id)
        return self.repository.update(
            replace(
                task,
                title=values[0],
                description=values[1],
                priority=values[2],
                category=clean_category,
                due_date=values[3],
            )
        )

    def delete_task(self, task_id: int) -> None:
        self.repository.delete(task_id)

    def categories(self) -> list[str]:
        values = {task.category for task in self.repository.list_all()}
        return sorted(values | {DEFAULT_CATEGORY})

    def statistics(self) -> dict[str, int]:
        tasks = self.repository.list_all()
        return {
            "total": len(tasks),
            "active": sum(not task.completed for task in tasks),
            "completed": sum(task.completed for task in tasks),
            "overdue": sum(self.is_overdue(task) for task in tasks),
        }

    @staticmethod
    def _validate_category(category: str) -> str:
        clean_category = category.strip()
        if not clean_category:
            return DEFAULT_CATEGORY
        if len(clean_category) > 40:
            raise ValueError("Category cannot exceed 40 characters.")
        return clean_category

    @staticmethod
    def is_overdue(task: Task) -> bool:
        today = datetime.now(UTC).date().isoformat()
        return bool(task.due_date and not task.completed and task.due_date < today)
