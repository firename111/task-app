from __future__ import annotations

import pytest

from todo_manager.database import Database
from todo_manager.repository import TaskRepository
from todo_manager.service import TaskService


@pytest.fixture
def service(tmp_path):
    database = Database(tmp_path / "test.db")
    database.initialize()
    yield TaskService(TaskRepository(database))
    database.close()
