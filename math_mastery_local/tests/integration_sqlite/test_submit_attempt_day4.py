from pathlib import Path

from application.use_cases.seed_data import seed_items, seed_topics
from application.use_cases.submit_attempt import submit_attempt
from infrastructure.persistence_sqlite.db import DB_NAME, get_connection, init_db


def test_submit_attempt_updates_mastery_and_persists_attempt():
    root = Path(__file__).resolve().parents[2]
    db_file = root / DB_NAME
    if db_file.exists():
        db_file.unlink()

    init_db()
    seed_topics(root / "data/topics.csv")
    seed_items()

    before, after, due_at = submit_attempt("T030", True, 0.5)

    conn = get_connection()
    attempt_count = conn.execute("SELECT COUNT(*) FROM attempts WHERE topic_id='T030'").fetchone()[0]
    mastery_row = conn.execute(
        "SELECT mastery, stability, due_at FROM mastery_state WHERE topic_id='T030'"
    ).fetchone()
    conn.close()

    assert before >= 0.0
    assert after > before
    assert due_at is not None
    assert attempt_count == 1
    assert mastery_row is not None
    assert mastery_row[0] == after
    assert mastery_row[1] > 1.0
    assert mastery_row[2] is not None
