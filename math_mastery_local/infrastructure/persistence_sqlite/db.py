import sqlite3
from pathlib import Path


DB_NAME = "mastery.db"


def get_connection():
    base_path = Path(__file__).resolve().parents[2]
    db_path = base_path / DB_NAME
    return sqlite3.connect(db_path)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS topics (
        id TEXT PRIMARY KEY,
        title TEXT,
        domain TEXT,
        level INTEGER
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY,
        topic_id TEXT,
        question TEXT,
        correct_answer TEXT,
        difficulty REAL,
        FOREIGN KEY(topic_id) REFERENCES topics(id)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id TEXT,
        correct INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS mastery_state (
        topic_id TEXT PRIMARY KEY,
        mastery REAL DEFAULT 0.0,
        stability REAL DEFAULT 1.0,
        due_at DATETIME,
        FOREIGN KEY(topic_id) REFERENCES topics(id)
    )
    """
    )

    conn.commit()
    conn.close()
