from infrastructure.persistence_sqlite.db import get_connection


def get_session_summary(recent_n: int = 50) -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
    SELECT correct FROM attempts
    ORDER BY id DESC
    LIMIT ?
    """,
        (recent_n,),
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {"attempts": 0, "accuracy": None}

    attempts = len(rows)
    correct = sum(row[0] for row in rows)
    accuracy = correct / attempts
    return {"attempts": attempts, "accuracy": accuracy}
