import pandas as pd

from infrastructure.persistence_sqlite.db import get_connection


def seed_topics(topics_path):
    conn = get_connection()
    df = pd.read_csv(topics_path)

    df.to_sql("topics", conn, if_exists="replace", index=False)
    conn.close()


def seed_items():
    conn = get_connection()
    cursor = conn.cursor()

    items = [
        ("Q1", "T001", "5 + 7 =", "12", 0.2),
        ("Q2", "T003", "6 x 4 =", "24", 0.3),
        ("Q3", "T010", "1/2 + 1/2 =", "1", 0.4),
        ("Q4", "T030", "Solve: x + 3 = 7", "4", 0.5),
    ]

    cursor.executemany(
        """
    INSERT OR REPLACE INTO items
    (id, topic_id, question, correct_answer, difficulty)
    VALUES (?, ?, ?, ?, ?)
    """,
        items,
    )

    conn.commit()
    conn.close()
