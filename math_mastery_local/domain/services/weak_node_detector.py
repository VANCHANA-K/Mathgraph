class WeakNodeDetector:
    def __init__(self, attempt_repo):
        self.attempt_repo = attempt_repo

    def get_weak_topics(self, threshold=0.5, min_attempts=3):
        attempts = self.attempt_repo.get_recent_attempts()

        stats = {}

        for topic_id, correct in attempts:
            if topic_id not in stats:
                stats[topic_id] = {"correct": 0, "total": 0}
            stats[topic_id]["total"] += 1
            stats[topic_id]["correct"] += int(correct)

        weak = []

        for topic_id, data in stats.items():
            if data["total"] >= min_attempts:
                accuracy = data["correct"] / data["total"]
                if accuracy < threshold:
                    weak.append(topic_id)

        return weak
