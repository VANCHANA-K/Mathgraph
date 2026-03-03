from datetime import datetime, timedelta
from pathlib import Path

from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import DB_NAME, get_connection, init_db
from infrastructure.persistence_sqlite.mastery_repo import MasteryRepository


def test_get_next_actions_returns_review_remediate_new_groups():
    root = Path(__file__).resolve().parents[2]
    db_file = root / DB_NAME
    if db_file.exists():
        db_file.unlink()

    init_db()
    seed_topics(root / "data/topics.csv")
    seed_items()

    due_past = (datetime.now() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO mastery_state (topic_id, mastery, stability, due_at) VALUES (?, ?, ?, ?)",
        ("T001", 0.4, 1.0, due_past),
    )
    conn.execute(
        "INSERT OR REPLACE INTO mastery_state (topic_id, mastery, stability, due_at) VALUES (?, ?, ?, ?)",
        ("T003", 0.9, 1.0, None),
    )
    conn.commit()
    conn.close()

    graph_repo = NetworkXGraphRepository(root / "data/topics.csv", root / "data/edges.csv")
    mastery_repo = MasteryRepository()

    actions = get_next_actions(graph_repo, mastery_repo)

    assert "review" in actions
    assert "remediate" in actions
    assert "new" in actions
    assert "T001" in actions["review"]
    assert "T001" in actions["remediate"]
    assert "T002" in actions["new"]
