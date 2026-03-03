from pathlib import Path
import csv


class NetworkXGraphRepository:
    def __init__(self, topics_path: str | Path, edges_path: str | Path | None = None):
        self.nodes = {}
        self.predecessors = {}
        self.successors = {}

        if edges_path is None:
            edges_path = topics_path
            topics_path = None

        self._load_graph(topics_path, edges_path)

    def _load_graph(self, topics_path: str | Path | None, edges_path: str | Path):
        if topics_path is not None:
            with open(topics_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    topic_id = row["id"]
                    self.nodes[topic_id] = {
                        "title": row["title"],
                        "domain": row["domain"],
                        "level": int(row["level"]),
                    }
                    self.predecessors.setdefault(topic_id, set())
                    self.successors.setdefault(topic_id, set())

        with open(edges_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                src = row["src"]
                dst = row["dst"]

                self.predecessors.setdefault(src, set())
                self.successors.setdefault(src, set())
                self.predecessors.setdefault(dst, set())
                self.successors.setdefault(dst, set())

                if src not in self.nodes:
                    self.nodes[src] = {}
                if dst not in self.nodes:
                    self.nodes[dst] = {}

                self.successors[src].add(dst)
                self.predecessors[dst].add(src)

    def get_prerequisites(self, topic_id: str) -> list[str]:
        return list(self.predecessors.get(topic_id, set()))

    def get_children(self, topic_id: str) -> list[str]:
        return list(self.successors.get(topic_id, set()))

    def get_all_topics(self) -> list[str]:
        return list(self.nodes.keys())

    def is_unlockable(self, topic_id: str, mastered_topics: list[str]) -> bool:
        prereqs = self.get_prerequisites(topic_id)
        return all(p in mastered_topics for p in prereqs)

    def prerequisites_of(self, topic_id: str) -> list[str]:
        return self.get_prerequisites(topic_id)

    def children_of(self, topic_id: str) -> list[str]:
        return self.get_children(topic_id)
