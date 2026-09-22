from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Task:
    """The domain object used by every layer of the application."""

    id: int | None
    title: str
    description: str
    priority: str
    due_date: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime
