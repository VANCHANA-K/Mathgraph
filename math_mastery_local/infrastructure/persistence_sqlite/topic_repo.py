import csv
import sqlite3

from domain.entities.topic import Topic


class CsvTopicRepository:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def list_topics(self) -> list[Topic]:
        topics: list[Topic] = []
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                topic_id = r.get("topic_id") or r.get("id")
                name = r.get("name") or r.get("title") or ""
                description = r.get("description") or f"{r.get('domain', '')} L{r.get('level', '')}".strip()
                if topic_id:
                    topics.append(Topic(topic_id=topic_id, name=name, description=description))
        return topics

    def get_topic(self, topic_id: str) -> Topic | None:
        for topic in self.list_topics():
            if topic.topic_id == topic_id:
                return topic
        return None


class SqliteTopicRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_topics(self) -> list[Topic]:
        rows = self.conn.execute("SELECT topic_id, name, description FROM topics ORDER BY topic_id").fetchall()
        return [Topic(topic_id=r["topic_id"], name=r["name"], description=r["description"]) for r in rows]

    def get_topic(self, topic_id: str) -> Topic | None:
        row = self.conn.execute("SELECT topic_id, name, description FROM topics WHERE topic_id=?", (topic_id,)).fetchone()
        if not row:
            return None
        return Topic(topic_id=row["topic_id"], name=row["name"], description=row["description"])

    def upsert_topic(self, topic: Topic) -> None:
        self.conn.execute(
            """INSERT INTO topics(topic_id, name, description)
               VALUES(?,?,?)
               ON CONFLICT(topic_id) DO UPDATE SET
               name=excluded.name, description=excluded.description""",
            (topic.topic_id, topic.name, topic.description),
        )
        self.conn.commit()
