from dataclasses import replace


def test_repository_can_create_update_and_delete(service):
    task = service.add_task("Read Python", priority="High", category="Study")
    assert task.id is not None
    assert task.category == "Study"

    updated = service.repository.update(replace(task, title="Read Python docs"))
    assert updated.title == "Read Python docs"

    service.delete_task(task.id)
    assert service.list_tasks() == []
