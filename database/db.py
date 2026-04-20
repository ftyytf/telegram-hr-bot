import aiosqlite
from config import DB_PATH
from datetime import date


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                registered_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS daily_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_date TEXT NOT NULL,
                sleep TEXT DEFAULT 'none',
                work TEXT DEFAULT 'none',
                growth TEXT DEFAULT 'none',
                sport TEXT DEFAULT 'none',
                finance TEXT DEFAULT 'none',
                no_chaos TEXT DEFAULT 'none',
                joy TEXT DEFAULT 'none',
                day_score INTEGER DEFAULT 0,
                note TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, entry_date)
            )
        """)
        await db.commit()


async def add_user(user_id: int, username: str, first_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name),
        )
        await db.commit()


async def get_or_create_entry(user_id: int, entry_date: str = None):
    if entry_date is None:
        entry_date = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM daily_entries WHERE user_id = ? AND entry_date = ?",
            (user_id, entry_date),
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
        await db.execute(
            "INSERT INTO daily_entries (user_id, entry_date) VALUES (?, ?)",
            (user_id, entry_date),
        )
        await db.commit()
        cursor = await db.execute(
            "SELECT * FROM daily_entries WHERE user_id = ? AND entry_date = ?",
            (user_id, entry_date),
        )
        row = await cursor.fetchone()
        return dict(row)


async def update_category(user_id: int, entry_date: str, category: str, status: str):
    allowed = ["sleep", "work", "growth", "sport", "finance", "no_chaos", "joy"]
    if category not in allowed:
        return
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"UPDATE daily_entries SET {category} = ? WHERE user_id = ? AND entry_date = ?",
            (status, user_id, entry_date),
        )
        await db.commit()


async def update_score(user_id: int, entry_date: str, score: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE daily_entries SET day_score = ? WHERE user_id = ? AND entry_date = ?",
            (score, user_id, entry_date),
        )
        await db.commit()


async def update_note(user_id: int, entry_date: str, note: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE daily_entries SET note = ? WHERE user_id = ? AND entry_date = ?",
            (note, user_id, entry_date),
        )
        await db.commit()


async def get_entries_for_period(user_id: int, date_from: str, date_to: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM daily_entries WHERE user_id = ? AND entry_date BETWEEN ? AND ? ORDER BY entry_date",
            (user_id, date_from, date_to),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_all_entries(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM daily_entries WHERE user_id = ? ORDER BY entry_date",
            (user_id,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
