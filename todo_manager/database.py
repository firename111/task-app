from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Self

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    priority TEXT NOT NULL DEFAULT 'Medium'
        CHECK (priority IN ('High', 'Medium', 'Low')),
    category TEXT NOT NULL DEFAULT 'General',
    due_date TEXT,
    completed INTEGER NOT NULL DEFAULT 0
        CHECK (completed IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
"""


class Database:
    """Own one SQLite connection and its schema lifecycle."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")

    def initialize(self) -> None:
        self.connection.executescript(SCHEMA)
        columns = {
            row["name"] for row in self.connection.execute("PRAGMA table_info(tasks)")
        }
        if "category" not in columns:
            self.connection.execute(
                "ALTER TABLE tasks ADD COLUMN category TEXT NOT NULL DEFAULT 'General'"
            )
        self.connection.commit()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.close()
