from pathlib import Path

from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository


def test_graph_prerequisites_and_unlock_logic():
    root = Path(__file__).resolve().parents[2]
    repo = NetworkXGraphRepository(root / "data/topics.csv", root / "data/edges.csv")

    assert repo.get_prerequisites("T030") == ["T020"]
    assert repo.is_unlockable("T030", ["T001", "T003", "T010", "T011", "T020"]) is True
    assert repo.is_unlockable("T030", ["T001", "T003"]) is False
