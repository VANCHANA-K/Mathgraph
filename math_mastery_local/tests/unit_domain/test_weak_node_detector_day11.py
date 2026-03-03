from domain.services.weak_node_detector import WeakNodeDetector


class FakeAttemptRepo:
    def get_recent_attempts(self):
        return [
            ("T001", 0),
            ("T001", 0),
            ("T001", 1),
            ("T003", 1),
            ("T003", 1),
            ("T003", 0),
            ("T010", 1),
            ("T010", 1),
        ]


def test_weak_node_detector_flags_low_accuracy_topics():
    detector = WeakNodeDetector(FakeAttemptRepo())
    weak_topics = detector.get_weak_topics(threshold=0.5, min_attempts=3)

    assert "T001" in weak_topics
    assert "T003" not in weak_topics
    assert "T010" not in weak_topics
