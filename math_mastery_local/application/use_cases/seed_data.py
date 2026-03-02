import csv

from domain.entities.item import Item
from infrastructure.persistence_sqlite.item_repo import SqliteItemRepository


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
