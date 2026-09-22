from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from .model import Task
from .repository import TaskRepository
from .validators import validate_task_input


class TaskService:
    """Application rules. The UI calls this class instead of SQL."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        due_date: str = "",
    ) -> Task:
        values = validate_task_input(title, description, priority, due_date)
        return self.repository.create(*values)

    def list_tasks(self, query: str = "", status: str = "All") -> list[Task]:
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
        due_date: str,
    ) -> Task:
        values = validate_task_input(title, description, priority, due_date)
        task = self.repository.get_by_id(task_id)
        return self.repository.update(
            replace(
                task,
                title=values[0],
                description=values[1],
                priority=values[2],
                due_date=values[3],
            )
        )

    def delete_task(self, task_id: int) -> None:
        self.repository.delete(task_id)

    @staticmethod
    def is_overdue(task: Task) -> bool:
        today = datetime.now(UTC).date().isoformat()
        return bool(task.due_date and not task.completed and task.due_date < today)
