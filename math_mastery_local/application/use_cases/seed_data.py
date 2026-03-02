import csv

from domain.entities.item import Item
from domain.entities.topic import Topic
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository
from infrastructure.persistence_sqlite.topic_repo import SqliteTopicRepository


def seed_topics(topics_csv_path: str, topic_repo: SqliteTopicRepository) -> int:
    count = 0
    with open(topics_csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            topic_repo.upsert_topic(
                Topic(
                    topic_id=row.get("topic_id") or row.get("id"),
                    name=row.get("name") or row.get("title") or "",
                    description=row.get("description") or f"{row.get('domain', '')} L{row.get('level', '')}".strip(),
                )
            )
            count += 1
    return count


def seed_items(items_csv_path: str, item_repo: SqliteItemRepository) -> int:
    count = 0
    with open(items_csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            item_repo.upsert_item(
                Item(
                    item_id=row["item_id"],
                    topic_id=row["topic_id"],
                    question=row["question"],
                    answer=row["answer"],
                    difficulty=float(row.get("difficulty", 0.5)),
                )
            )
            count += 1
    return count
