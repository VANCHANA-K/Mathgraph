from datetime import datetime, timedelta
from pathlib import Path

from application.use_cases.generate_session import generate_session
from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import DB_NAME, get_connection, init_db
from infrastructure.persistence_sqlite.item_repo import ItemRepository
from infrastructure.persistence_sqlite.mastery_repo import MasteryRepository


def test_generate_session_builds_review_remediate_new_items():
    root = Path(__file__).resolve().parents[2]
    db_file = root / DB_NAME
    if db_file.exists():
        db_file.unlink()

    init_db()
    seed_topics(root / "data/topics.csv")
    seed_items()

    conn = get_connection()
    conn.execute("DELETE FROM mastery_state")
    conn.execute(
        "INSERT OR REPLACE INTO mastery_state (topic_id, mastery, stability, due_at) VALUES (?, ?, ?, ?)",
        ("T001", 0.4, 1.0, (datetime.now() - timedelta(days=1)).isoformat()),
    )
    conn.execute(
        "INSERT OR REPLACE INTO mastery_state (topic_id, mastery, stability, due_at) VALUES (?, ?, ?, ?)",
        ("T003", 0.9, 1.0, (datetime.now() + timedelta(days=2)).isoformat()),
    )
    conn.commit()
    conn.close()

    graph_repo = NetworkXGraphRepository(root / "data/topics.csv", root / "data/edges.csv")
    mastery_repo = MasteryRepository()
    item_repo = ItemRepository()

    actions = get_next_actions(graph_repo, mastery_repo)
    session = generate_session(actions, item_repo)

    assert len(session["review"]) == 6
    assert len(session["remediate"]) == 4
    assert len(session["new"]) == 5
