from __future__ import annotations

from datetime import date

PRIORITIES = ("High", "Medium", "Low")


def validate_task_input(
    title: str,
    description: str,
    priority: str,
    due_date: str,
) -> tuple[str, str, str, str | None]:
    """Validate and normalize values from the UI."""
    clean_title = title.strip()
    clean_description = description.strip()
    clean_priority = priority.strip()
    clean_due_date = due_date.strip() or None

    if not clean_title:
        raise ValueError("Title cannot be empty.")
    if len(clean_title) > 100:
        raise ValueError("Title cannot exceed 100 characters.")
    if len(clean_description) > 500:
        raise ValueError("Description cannot exceed 500 characters.")
    if clean_priority not in PRIORITIES:
        raise ValueError("Priority must be High, Medium, or Low.")
    if clean_due_date is not None:
        try:
            date.fromisoformat(clean_due_date)
        except ValueError as exc:
            raise ValueError("Due date must use YYYY-MM-DD.") from exc

    return clean_title, clean_description, clean_priority, clean_due_date
