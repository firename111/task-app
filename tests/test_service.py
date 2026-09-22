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
