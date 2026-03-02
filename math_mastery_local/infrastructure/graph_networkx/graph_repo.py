from pathlib import Path

import networkx as nx
import pandas as pd


class NetworkXGraphRepository:
    def __init__(self, topics_path: str | Path, edges_path: str | Path | None = None):
        self.G = nx.DiGraph()
        if edges_path is None:
            # Backward compatibility: old usage passed only edges path.
            edges_path = topics_path
            topics_path = None
        self._load_graph(topics_path, edges_path)

    def _load_graph(self, topics_path: str | Path | None, edges_path: str | Path):
        if topics_path is not None:
            topics = pd.read_csv(topics_path)
            for _, row in topics.iterrows():
                self.G.add_node(
                    row["id"],
                    title=row["title"],
                    domain=row["domain"],
                    level=row["level"],
                )

        edges = pd.read_csv(edges_path)
        for _, row in edges.iterrows():
            self.G.add_edge(row["src"], row["dst"])

    def get_prerequisites(self, topic_id: str) -> list[str]:
        if topic_id not in self.G:
            return []
        return list(self.G.predecessors(topic_id))

    def get_children(self, topic_id: str) -> list[str]:
        if topic_id not in self.G:
            return []
        return list(self.G.successors(topic_id))

    def get_all_topics(self) -> list[str]:
        return list(self.G.nodes)

    def is_unlockable(self, topic_id: str, mastered_topics: list[str]) -> bool:
        prereqs = self.get_prerequisites(topic_id)
        return all(p in mastered_topics for p in prereqs)

    # Compatibility adapters for existing application layer
    def prerequisites_of(self, topic_id: str) -> list[str]:
        return self.get_prerequisites(topic_id)

    def children_of(self, topic_id: str) -> list[str]:
        return self.get_children(topic_id)
