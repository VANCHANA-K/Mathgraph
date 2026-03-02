import sys
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH))

from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository


def test_graph() -> None:
    base_path = Path(__file__).resolve().parents[1]
    topics_path = base_path / "data" / "topics.csv"
    edges_path = base_path / "data" / "edges.csv"

    graph_repo = NetworkXGraphRepository(topics_path, edges_path)

    print("All Topics:")
    print(graph_repo.get_all_topics())

    print("\nPrerequisites of T030:")
    print(graph_repo.get_prerequisites("T030"))

    mastered = ["T001", "T003", "T010", "T011", "T020"]

    print("\nIs T030 unlockable?")
    print(graph_repo.is_unlockable("T030", mastered))


if __name__ == "__main__":
    test_graph()
