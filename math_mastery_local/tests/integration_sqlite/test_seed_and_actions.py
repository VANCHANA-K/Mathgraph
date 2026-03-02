from pathlib import Path

from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import init_db
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository
from infrastructure.persistence_sqlite.mastery_repo import SqliteMasteryRepository
from infrastructure.persistence_sqlite.topic_repo import SqliteTopicRepository


def test_seed_and_actions(tmp_path: Path):
    db = tmp_path / "test.db"
    conn = init_db(str(db))

    root = Path(__file__).resolve().parents[2]
    topic_repo = SqliteTopicRepository(conn)
    graph_repo = NetworkXGraphRepository(str(root / "data/topics.csv"), str(root / "data/edges.csv"))
    item_repo = SqliteItemRepository(conn)
    mastery_repo = SqliteMasteryRepository(conn)

    seeded_topics = seed_topics(str(root / "data/topics.csv"), topic_repo)
    seeded_items = seed_items(str(root / "data/items.csv"), item_repo)
    actions = get_next_actions("u1", topic_repo, graph_repo, mastery_repo)

    assert seeded_topics == 9
    assert seeded_items == 3
    assert "New" in actions
