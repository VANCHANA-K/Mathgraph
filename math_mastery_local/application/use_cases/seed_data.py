import csv

from infrastructure.persistence_sqlite.db import get_connection


def seed_topics(topics_path):
    conn = get_connection()
    cursor = conn.cursor()

    with open(topics_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    cursor.executemany(
        """
        INSERT OR REPLACE INTO topics (id, title, domain, level)
        VALUES (?, ?, ?, ?)
        """,
        [(r["id"], r["title"], r["domain"], int(r["level"])) for r in rows],
    )

    conn.commit()
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
