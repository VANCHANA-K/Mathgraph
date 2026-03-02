import argparse
import sys
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH))

from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.persistence_sqlite.db import init_db
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository
from infrastructure.persistence_sqlite.topic_repo import SqliteTopicRepository


def run_graph_demo() -> None:
    from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository

    topics_path = BASE_PATH / "data" / "topics.csv"
    edges_path = BASE_PATH / "data" / "edges.csv"

    graph_repo = NetworkXGraphRepository(topics_path, edges_path)

    print("All Topics:")
    print(graph_repo.get_all_topics())

    print("\nPrerequisites of T030:")
    print(graph_repo.get_prerequisites("T030"))

    mastered = ["T001", "T003", "T010", "T011", "T020"]

    print("\nIs T030 unlockable?")
    print(graph_repo.is_unlockable("T030", mastered))


def run_init_db(db_path: Path) -> None:
    conn = init_db(str(db_path))
    conn.close()
    print(f"Initialized DB schema at {db_path}")


def run_seed(db_path: Path) -> None:
    conn = init_db(str(db_path))
    topic_repo = SqliteTopicRepository(conn)
    item_repo = SqliteItemRepository(conn)

    topics_count = seed_topics(str(BASE_PATH / "data/topics.csv"), topic_repo)
    items_count = seed_items(str(BASE_PATH / "data/items.csv"), item_repo)

    conn.close()
    print(f"Seeded topics={topics_count}, items={items_count} into {db_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Math Mastery local CLI")
    parser.add_argument("command", choices=["graph-test", "init-db", "seed"])
    parser.add_argument("--db-path", default=str(BASE_PATH / "math_mastery.db"))
    args = parser.parse_args()

    db_path = Path(args.db_path)

    if args.command == "graph-test":
        run_graph_demo()
    elif args.command == "init-db":
        run_init_db(db_path)
    elif args.command == "seed":
        run_seed(db_path)


if __name__ == "__main__":
    main()
