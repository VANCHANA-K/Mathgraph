import sqlite3
from datetime import datetime

from domain.entities.mastery_state import MasteryState


class SqliteMasteryRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_state(self, user_id: str, topic_id: str) -> MasteryState | None:
        row = self.conn.execute(
            "SELECT * FROM mastery_state WHERE user_id=? AND topic_id=?", (user_id, topic_id)
        ).fetchone()
        return self._to_state(row) if row else None

    def upsert_state(self, state: MasteryState) -> None:
        self.conn.execute(
            """INSERT INTO mastery_state(user_id,topic_id,mastery,stability,due_at,last_practiced_at)
               VALUES(?,?,?,?,?,?)
               ON CONFLICT(user_id,topic_id) DO UPDATE SET
               mastery=excluded.mastery, stability=excluded.stability, due_at=excluded.due_at,
               last_practiced_at=excluded.last_practiced_at""",
            (
                state.user_id,
                state.topic_id,
                state.mastery,
                state.stability,
                state.due_at.isoformat() if state.due_at else None,
                state.last_practiced_at.isoformat() if state.last_practiced_at else None,
            ),
        )
        self.conn.commit()

    def list_states(self, user_id: str) -> list[MasteryState]:
        rows = self.conn.execute("SELECT * FROM mastery_state WHERE user_id=?", (user_id,)).fetchall()
        return [self._to_state(r) for r in rows]

    @staticmethod
    def _to_state(row) -> MasteryState:
        return MasteryState(
            user_id=row["user_id"],
            topic_id=row["topic_id"],
            mastery=row["mastery"],
            stability=row["stability"],
            due_at=datetime.fromisoformat(row["due_at"]) if row["due_at"] else None,
            last_practiced_at=datetime.fromisoformat(row["last_practiced_at"]) if row["last_practiced_at"] else None,
        )
