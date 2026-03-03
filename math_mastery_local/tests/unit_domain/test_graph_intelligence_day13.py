from domain.services.graph_intelligence import GraphIntelligence


class FakeGraphRepo:
    def __init__(self):
        self.edges = {
            "T001": ["T003", "T002"],
            "T002": ["T020"],
            "T003": ["T010"],
            "T010": ["T020"],
            "T020": ["T030"],
            "T030": [],
        }

    def get_all_topics(self):
        return list(self.edges.keys())

    def get_children(self, topic_id):
        return self.edges.get(topic_id, [])


class FakeMasteryRepo:
    def __init__(self):
        self.mastery = {
            "T001": 0.95,
            "T002": 0.8,
            "T003": 0.4,
            "T010": 0.45,
            "T020": 0.5,
            "T030": 0.9,
        }

    def get_mastery(self, topic_id):
        return self.mastery.get(topic_id, 0.0), 1.0


def test_graph_intelligence_bottlenecks_and_central_topics():
    intelligence = GraphIntelligence(FakeGraphRepo(), FakeMasteryRepo())

    bottlenecks = intelligence.get_bottlenecks(mastery_threshold=0.6)
    central = intelligence.get_central_topics(top_n=2)
    shortest = intelligence.shortest_path_to_goal("T001", "T030")

    assert any(node == "T003" for node, _ in bottlenecks)
    assert len(central) == 2
    assert shortest[0] == "T001"
    assert shortest[-1] == "T030"
