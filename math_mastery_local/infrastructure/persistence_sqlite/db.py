import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS topics (
  topic_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS items (
  item_id TEXT PRIMARY KEY,
  topic_id TEXT NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  difficulty REAL NOT NULL DEFAULT 0.5,
  FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
);

CREATE TABLE IF NOT EXISTS attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  item_id TEXT NOT NULL,
  topic_id TEXT NOT NULL,
  is_correct INTEGER NOT NULL,
  response_seconds INTEGER NOT NULL,
  used_hint INTEGER NOT NULL,
  attempted_at TEXT NOT NULL,
  FOREIGN KEY(item_id) REFERENCES items(item_id),
  FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
);

CREATE TABLE IF NOT EXISTS mastery_state (
  user_id TEXT NOT NULL,
  topic_id TEXT NOT NULL,
  mastery REAL NOT NULL,
  stability REAL NOT NULL,
  due_at TEXT,
  last_practiced_at TEXT,
  PRIMARY KEY (user_id, topic_id),
  FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
);
"""


def connect(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()


def init_db(db_path: str) -> sqlite3.Connection:
    conn = connect(db_path)
    init_schema(conn)
    return conn
