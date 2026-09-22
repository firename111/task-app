from __future__ import annotations

from datetime import datetime, timezone

from .database import Database
from .model import Task


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _task_from_row(row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        priority=row["priority"],
        due_date=row["due_date"],
        completed=bool(row["completed"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


class TaskRepository:
    """All SQL for tasks lives here."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self, title: str, description: str, priority: str, due_date: str | None
    ) -> Task:
        now = _now().isoformat()
        cursor = self.database.connection.execute(
            """
            INSERT INTO tasks
                (title, description, priority, due_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, description, priority, due_date, now, now),
        )
        self.database.connection.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, task_id: int) -> Task:
        row = self.database.connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"Task {task_id} was not found.")
        return _task_from_row(row)

    def list_all(self) -> list[Task]:
        rows = self.database.connection.execute(
            "SELECT * FROM tasks ORDER BY completed, due_date IS NULL, due_date, id"
        ).fetchall()
        return [_task_from_row(row) for row in rows]

    def update(self, task: Task) -> Task:
        now = _now().isoformat()
        self.database.connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, priority = ?, due_date = ?,
                completed = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                task.title,
                task.description,
                task.priority,
                task.due_date,
                int(task.completed),
                now,
                task.id,
            ),
        )
        self.database.connection.commit()
        return self.get_by_id(task.id)

    def delete(self, task_id: int) -> None:
        cursor = self.database.connection.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        self.database.connection.commit()
        if cursor.rowcount == 0:
            raise KeyError(f"Task {task_id} was not found.")
