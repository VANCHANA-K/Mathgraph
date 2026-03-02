import sqlite3
from datetime import datetime

from domain.entities.attempt import Attempt


class SqliteAttemptRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def add_attempt(self, attempt: Attempt) -> None:
        self.conn.execute(
            """INSERT INTO attempts(user_id,item_id,topic_id,is_correct,response_seconds,used_hint,attempted_at)
               VALUES(?,?,?,?,?,?,?)""",
            (
                attempt.user_id,
                attempt.item_id,
                attempt.topic_id,
                int(attempt.is_correct),
                attempt.response_seconds,
                int(attempt.used_hint),
                attempt.attempted_at.isoformat(),
            ),
        )
        self.conn.commit()

    def list_attempts(self, user_id: str, topic_id: str | None = None) -> list[Attempt]:
        if topic_id:
            rows = self.conn.execute(
                "SELECT * FROM attempts WHERE user_id=? AND topic_id=? ORDER BY attempted_at DESC", (user_id, topic_id)
            ).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM attempts WHERE user_id=? ORDER BY attempted_at DESC", (user_id,)).fetchall()
        return [
            Attempt(
                user_id=r["user_id"],
                item_id=r["item_id"],
                topic_id=r["topic_id"],
                is_correct=bool(r["is_correct"]),
                response_seconds=r["response_seconds"],
                used_hint=bool(r["used_hint"]),
                attempted_at=datetime.fromisoformat(r["attempted_at"]),
            )
            for r in rows
        ]
