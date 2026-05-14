import aiosqlite


DB_NAME = "tasks.db"

async def init_db() -> None:
    """Initialize the database and create the tasks table if it doesn't exist."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                is_done BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        await db.commit()

async def add_task(user_id: int, description: str) -> None:
    """Add a new task to the database."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", (user_id, description))
        await db.commit()

async def get_tasks(user_id: int) -> list:
    """Retrieve all tasks for a specific user."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, description, is_done FROM tasks WHERE user_id = ? ORDER BY id",
            (user_id,)
        )
        tasks = await cursor.fetchall()
        return tasks

async def get_task_id_by_index(user_id: int, index: int) -> int | None:
    """Get the real task ID by the user's task list position."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id FROM tasks WHERE user_id = ? ORDER BY id LIMIT 1 OFFSET ?",
            (user_id, index - 1)
        )
        row = await cursor.fetchone()
        return row[0] if row else None

async def mark_task_done(task_id: int) -> None:
    """Mark a task as done."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
        await db.commit()

async def delete_task(task_id: int) -> None:
    """Delete a task from the database."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await db.commit()