def test_service_filters_and_toggles(service):
    active = service.add_task("Active task")
    completed = service.add_task("Completed task")
    service.toggle_completed(completed.id)

    assert [task.title for task in service.list_tasks(status="Active")] == [
        active.title
    ]
    assert [task.title for task in service.list_tasks(status="Completed")] == [
        completed.title
    ]
    assert [task.title for task in service.list_tasks(query="active")] == [active.title]


def test_service_detects_overdue_tasks(service):
    task = service.add_task("Old task", due_date="2020-01-01")
    assert service.is_overdue(task) is True


def test_completed_overdue_task_is_not_overdue(service):
    task = service.add_task("Finished old task", due_date="2020-01-01")
    completed = service.toggle_completed(task.id)

    assert service.is_overdue(completed) is False


def test_task_due_today_is_not_overdue(service):
    from datetime import UTC, datetime

    today = datetime.now(UTC).date().isoformat()
    task = service.add_task("Task due today", due_date=today)

    assert service.is_overdue(task) is False


def test_service_updates_task_fields(service):
    task = service.add_task("Draft", description="Old")

    updated = service.update_task(
        task.id,
        "Final",
        "New description",
        "High",
        "2026-09-30",
    )

    assert updated.title == "Final"
    assert updated.description == "New description"
    assert updated.priority == "High"
    assert updated.due_date == "2026-09-30"
