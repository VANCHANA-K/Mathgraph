import sys
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH))

from application.use_cases.seed_data import seed_items, seed_topics
from application.use_cases.submit_attempt import submit_attempt
from infrastructure.persistence_sqlite.db import init_db


def run_test():
    topics_path = BASE_PATH / "data" / "topics.csv"

    init_db()
    seed_topics(topics_path)
    seed_items()

    topic_id = "T030"
    difficulty = 0.5

    before, after, due_at = submit_attempt(topic_id, correct=True, difficulty=difficulty)

    print("Before mastery:", round(before, 3))
    print("After mastery:", round(after, 3))
    print("Next review:", due_at)


if __name__ == "__main__":
    run_test()
