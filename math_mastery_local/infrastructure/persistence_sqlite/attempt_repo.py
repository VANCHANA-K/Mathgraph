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
