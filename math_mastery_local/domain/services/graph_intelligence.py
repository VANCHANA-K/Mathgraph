import networkx as nx


class GraphIntelligence:
    def __init__(self, graph_repo, mastery_repo):
        self.mastery_repo = mastery_repo
        self.graph = nx.DiGraph()

        for topic_id in graph_repo.get_all_topics():
            self.graph.add_node(topic_id)
            for child_id in graph_repo.get_children(topic_id):
                self.graph.add_edge(topic_id, child_id)

    def get_bottlenecks(self, mastery_threshold=0.6):
        bottlenecks = []

        for node in self.graph.nodes:
            mastery, _ = self.mastery_repo.get_mastery(node)
            downstream = len(nx.descendants(self.graph, node))

            if mastery < mastery_threshold and downstream >= 2:
                bottlenecks.append((node, downstream))

        return sorted(bottlenecks, key=lambda x: -x[1])

    def get_central_topics(self, top_n=3):
        centrality = nx.betweenness_centrality(self.graph)
        sorted_nodes = sorted(centrality.items(), key=lambda x: -x[1])
        return [node for node, _ in sorted_nodes[:top_n]]

    def shortest_path_to_goal(self, start, goal):
        return nx.shortest_path(self.graph, start, goal)
