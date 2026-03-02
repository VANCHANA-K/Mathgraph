import argparse
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))


from application.use_cases.generate_session import generate_session
from application.use_cases.get_next_actions import get_next_actions
from application.use_cases.seed_data import seed_items
from infrastructure.graph_networkx.graph_repo import NetworkXGraphRepository
from infrastructure.persistence_sqlite.db import connect, init_schema
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository
from infrastructure.persistence_sqlite.mastery_repo import SqliteMasteryRepository
from infrastructure.persistence_sqlite.topic_repo import CsvTopicRepository

DB_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "math_mastery.db"))
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "local_user")


def build_services():
    conn = connect(DB_PATH)
    init_schema(conn)
    topic_repo = CsvTopicRepository(str(BASE_DIR / "data/topics.csv"))
    graph_repo = NetworkXGraphRepository(str(BASE_DIR / "data/edges.csv"))
    item_repo = SqliteItemRepository(conn)
    mastery_repo = SqliteMasteryRepository(conn)
    return topic_repo, graph_repo, item_repo, mastery_repo


def main():
    parser = argparse.ArgumentParser(description="Math Mastery local CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed")
    sub.add_parser("actions")
    args = parser.parse_args()

    topic_repo, graph_repo, item_repo, mastery_repo = build_services()

    if args.command == "seed":
        count = seed_items(str(BASE_DIR / "data/items.csv"), item_repo)
        print(f"Seeded {count} items into {DB_PATH}")
    elif args.command == "actions":
        actions = get_next_actions(DEFAULT_USER_ID, topic_repo, graph_repo, mastery_repo)
        session = generate_session(actions, minutes=20)
        print(actions)
        print(session)


if __name__ == "__main__":
    main()
