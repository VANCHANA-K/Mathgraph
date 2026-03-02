import sys
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH))

from application.use_cases.seed_data import seed_items, seed_topics
from infrastructure.persistence_sqlite.db import init_db


def seed():
    topics_path = BASE_PATH / "data" / "topics.csv"

    init_db()
    seed_topics(topics_path)
    seed_items()

    print("Database initialized and seeded.")


if __name__ == "__main__":
    seed()
