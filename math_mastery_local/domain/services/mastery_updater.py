import math
from datetime import datetime, timedelta


class MasteryUpdater:
    def __init__(self, learning_rate=0.3):
        self.lr = learning_rate

    def update(self, current_mastery, correct, difficulty, stability):
        """Update mastery score (0..1)."""
        score = 1.0 if correct else 0.0
        weight = 1 + difficulty

        delta = self.lr * (score - current_mastery) * weight
        new_mastery = max(0.0, min(1.0, current_mastery + delta))

        if correct:
            new_stability = stability * 1.2
        else:
            new_stability = max(0.5, stability * 0.7)

        days = max(1, int(math.log2(new_stability + 1) * 3))
        due_at = datetime.now() + timedelta(days=days)

        return new_mastery, new_stability, due_at
