import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH))

from application.use_cases.generate_session import generate_session
from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import get_connection, init_db
from infrastructure.persistence_sqlite.item_repo import ItemRepository
from infrastructure.persistence_sqlite.mastery_repo import MasteryRepository


def run_test():
    topics_path = BASE_PATH / "data" / "topics.csv"
    edges_path = BASE_PATH / "data" / "edges.csv"

    init_db()
    seed_topics(topics_path)
    seed_items()

    conn = get_connection()
    conn.execute("DELETE FROM mastery_state")
    conn.execute(
        "INSERT OR REPLACE INTO mastery_state (topic_id, mastery, stability, due_at) VALUES (?, ?, ?, ?)",
        ("T001", 0.4, 1.0, (datetime.now() - timedelta(days=1)).isoformat()),
    )
    conn.execute(
        "INSERT OR REPLACE INTO mastery_state (topic_id, mastery, stability, due_at) VALUES (?, ?, ?, ?)",
        ("T003", 0.9, 1.0, (datetime.now() + timedelta(days=3)).isoformat()),
    )
    conn.commit()
    conn.close()

    graph_repo = NetworkXGraphRepository(topics_path, edges_path)
    mastery_repo = MasteryRepository()
    item_repo = ItemRepository()

    actions = get_next_actions(graph_repo, mastery_repo)
    session = generate_session(actions, item_repo)

    print("Session Plan:")
    print("Review:", session["review"])
    print("Remediate:", session["remediate"])
    print("New:", session["new"])


if __name__ == "__main__":
    run_test()
