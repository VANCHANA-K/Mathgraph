from datetime import datetime
from pathlib import Path
import csv

from infrastructure.persistence_sqlite.db import get_connection


def export_mastery_csv(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = output_dir / f"mastery_{ts}.csv"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
    SELECT t.id, t.title, t.domain, t.level,
           m.mastery, m.stability, m.due_at
    FROM topics t
    LEFT JOIN mastery_state m ON m.topic_id = t.id
    ORDER BY t.level, t.id
    """
    )
    rows = cur.fetchall()
    conn.close()

    with open(out, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["topic_id", "title", "domain", "level", "mastery", "stability", "due_at"])
        writer.writerows(rows)

    return out


def export_attempts_csv(output_dir: Path, limit: int = 5000) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = output_dir / f"attempts_{ts}.csv"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
    SELECT id, topic_id, correct, timestamp
    FROM attempts
    ORDER BY id DESC
    LIMIT ?
    """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    with open(out, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["attempt_id", "topic_id", "correct", "timestamp"])
        writer.writerows(rows)

    return out
