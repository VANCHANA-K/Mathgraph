from pathlib import Path

from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.persistence_sqlite.db import DB_NAME, get_connection, init_db


def test_init_and_seed_db():
    root = Path(__file__).resolve().parents[2]
    db_file = root / DB_NAME
    if db_file.exists():
        db_file.unlink()

    init_db()
    seed_topics(root / "data/topics.csv")
    seed_items()

    conn = get_connection()
    topic_count = conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
    item_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    conn.close()

    assert topic_count == 9
    assert item_count == 4
