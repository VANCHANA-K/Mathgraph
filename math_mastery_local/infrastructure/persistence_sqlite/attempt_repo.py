from infrastructure.persistence_sqlite.db import get_connection


def save_attempt(topic_id, correct):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO attempts (topic_id, correct)
    VALUES (?, ?)
    """,
        (topic_id, int(correct)),
    )

    conn.commit()
    conn.close()


def get_recent_attempts(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT topic_id, correct
    FROM attempts
    ORDER BY id DESC
    LIMIT ?
    """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


class AttemptRepository:
    def get_recent_attempts(self):
        return get_recent_attempts()
