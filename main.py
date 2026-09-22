from __future__ import annotations

import argparse
from pathlib import Path

from todo_manager.database import Database
from todo_manager.repository import TaskRepository
from todo_manager.service import TaskService
from todo_manager.ui import TodoApp

PROJECT_DIR = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Desktop todo manager")
    parser.add_argument(
        "--db",
        type=Path,
        default=PROJECT_DIR / "data" / "todo.db",
        help="SQLite database path",
    )
    args = parser.parse_args()

    database = Database(args.db)
    database.initialize()
    service = TaskService(TaskRepository(database))

    try:
        TodoApp(service).run()
    finally:
        database.close()


if __name__ == "__main__":
    main()
