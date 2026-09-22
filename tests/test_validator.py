import pytest

from todo_manager.validators import validate_task_input


def test_validator_strips_values():
    result = validate_task_input("  Learn  ", " notes ", "High", "2026-09-30")
    assert result == ("Learn", "notes", "High", "2026-09-30")


@pytest.mark.parametrize(
    "values",
    [
        ("", "", "Medium", ""),
        ("Task", "", "Urgent", ""),
        ("Task", "", "Medium", "2026-02-30"),
    ],
)
def test_validator_rejects_invalid_values(values):
    with pytest.raises(ValueError):
        validate_task_input(*values)
