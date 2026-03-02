import sqlite3

from domain.entities.item import Item


class SqliteItemRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_items_by_topic(self, topic_id: str) -> list[Item]:
        rows = self.conn.execute("SELECT * FROM items WHERE topic_id = ?", (topic_id,)).fetchall()
        return [Item(**dict(r)) for r in rows]

    def get_item(self, item_id: str) -> Item | None:
        row = self.conn.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
        return Item(**dict(row)) if row else None

    def upsert_item(self, item: Item) -> None:
        self.conn.execute(
            """INSERT INTO items(item_id, topic_id, question, answer, difficulty)
               VALUES(?,?,?,?,?)
               ON CONFLICT(item_id) DO UPDATE SET
               topic_id=excluded.topic_id,question=excluded.question,answer=excluded.answer,difficulty=excluded.difficulty""",
            (item.item_id, item.topic_id, item.question, item.answer, item.difficulty),
        )
        self.conn.commit()
