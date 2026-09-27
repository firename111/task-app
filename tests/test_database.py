import sqlite3


def test_existing_v1_database_gets_category_migration(tmp_path):
    from todo_manager.database import Database

    path = tmp_path / "legacy.db"
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium',
            due_date TEXT,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        INSERT INTO tasks (title, created_at, updated_at)
        VALUES ('Legacy task', '2026-09-27T00:00:00+00:00', '2026-09-27T00:00:00+00:00');
        """
    )
    connection.commit()
    connection.close()

    database = Database(path)
    database.initialize()
    row = database.connection.execute("SELECT title, category FROM tasks").fetchone()
    database.close()

    assert dict(row) == {"title": "Legacy task", "category": "General"}
