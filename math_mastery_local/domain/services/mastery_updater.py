from datetime import datetime, timedelta


class MasteryUpdater:
    def __init__(self, learning_rate=0.4):
        self.lr = learning_rate

    def update(self, current_mastery, correct, difficulty, stability):
        score = 1.0 if correct else 0.0

        # difficulty weighting
        weight = 1 + difficulty * 1.5

        # confidence-aware smoothing: bigger uncertainty -> smaller update
        confidence_factor = 1 - abs(score - current_mastery) * 0.5

        # softer penalty on wrong answers to avoid sharp collapses
        penalty_scale = 1.0 if correct else 0.25

        delta = self.lr * (score - current_mastery) * confidence_factor * weight * penalty_scale

        new_mastery = max(0.0, min(1.0, current_mastery + delta))

        # improved stability logic
        if correct:
            new_stability = stability * 1.1
        else:
            new_stability = stability * 0.8

        days = max(1, int(2 + new_stability * 5))
        due_at = datetime.now() + timedelta(days=days)

        return new_mastery, new_stability, due_at
