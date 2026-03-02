from infrastructure.persistence_sqlite.db import get_connection


def get_mastery(topic_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT mastery, stability FROM mastery_state WHERE topic_id=?
    """,
        (topic_id,),
    )
    row = cursor.fetchone()

    if row:
        mastery, stability = row
    else:
        mastery, stability = 0.0, 1.0
        cursor.execute(
            """
        INSERT INTO mastery_state (topic_id, mastery, stability)
        VALUES (?, ?, ?)
        """,
            (topic_id, mastery, stability),
        )
        conn.commit()

    conn.close()
    return mastery, stability


def update_mastery(topic_id, mastery, stability, due_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT OR REPLACE INTO mastery_state
    (topic_id, mastery, stability, due_at)
    VALUES (?, ?, ?, ?)
    """,
        (topic_id, mastery, stability, due_at),
    )

    conn.commit()
    conn.close()
