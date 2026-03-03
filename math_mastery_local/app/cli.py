import sys
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH))

from application.use_cases.get_unlocked_topics import get_unlocked_topics
from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import init_db
from infrastructure.persistence_sqlite.mastery_repo import MasteryRepository


def run_test():
    topics_path = BASE_PATH / "data" / "topics.csv"
    edges_path = BASE_PATH / "data" / "edges.csv"

    init_db()
    seed_topics(topics_path)
    seed_items()

    graph_repo = NetworkXGraphRepository(topics_path, edges_path)
    mastery_repo = MasteryRepository()

    unlocked = get_unlocked_topics(graph_repo, mastery_repo)

    print("Unlocked Topics:")
    print(unlocked)


if __name__ == "__main__":
    run_test()
