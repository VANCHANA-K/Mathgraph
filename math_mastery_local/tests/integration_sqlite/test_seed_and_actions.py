from pathlib import Path

from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import connect, init_schema
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository
from infrastructure.persistence_sqlite.mastery_repo import SqliteMasteryRepository
from infrastructure.persistence_sqlite.topic_repo import CsvTopicRepository


def test_seed_and_actions(tmp_path: Path):
    db = tmp_path / "test.db"
    conn = connect(str(db))
    init_schema(conn)
    root = Path(__file__).resolve().parents[2]
    topic_repo = CsvTopicRepository(str(root / "data/topics.csv"))
    graph_repo = NetworkXGraphRepository(str(root / "data/edges.csv"))
    item_repo = SqliteItemRepository(conn)
    mastery_repo = SqliteMasteryRepository(conn)

    seeded = seed_items(str(root / "data/items.csv"), item_repo)
    actions = get_next_actions("u1", topic_repo, graph_repo, mastery_repo)

    assert seeded == 3
    assert "New" in actions
