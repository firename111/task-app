# Todo Manager Starter

This is a small desktop todo application designed for learning and extension.
It uses only the Python standard library at runtime:

- Tkinter for the desktop UI
- SQLite for local persistence
- pytest for tests

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python main.py
```

The database is created at `data/todo.db` on first start.

## Test

```powershell
python -m pytest -q
```

## Where to modify

| Goal | File | Starting point |
| --- | --- | --- |
| Add a task field | `todo_manager/model.py` | `Task` |
| Add input rules | `todo_manager/validators.py` | `validate_task_input` |
| Add SQL behavior | `todo_manager/repository.py` | `TaskRepository` |
| Add business behavior | `todo_manager/service.py` | `TaskService` |
| Add a control or screen element | `todo_manager/ui.py` | `TodoApp._build_widgets` |
| Prove behavior works | `tests/` | Add a focused test first |

## Architecture

```text
Tkinter UI -> TaskService -> TaskRepository -> Database -> SQLite
```

The UI should not execute SQL. The repository should not contain Tkinter code.
This separation makes each layer easier to test and replace.

## Suggested learning order

1. Run the baseline and read `model.py`.
2. Read one path: Add button -> service -> repository -> database.
3. Add one small feature, such as a status filter.
4. Add tests for the feature.
5. Only then change the UI layout.

