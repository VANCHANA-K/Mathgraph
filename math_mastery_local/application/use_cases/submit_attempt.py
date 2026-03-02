from domain.services.mastery_updater import MasteryUpdater
from infrastructure.persistence_sqlite.attempt_repo import save_attempt
from infrastructure.persistence_sqlite.mastery_repo import get_mastery, update_mastery


def submit_attempt(topic_id, correct, difficulty):
    mastery, stability = get_mastery(topic_id)

    updater = MasteryUpdater()
    new_mastery, new_stability, due_at = updater.update(
        mastery,
        correct,
        difficulty,
        stability,
    )

    save_attempt(topic_id, correct)
    update_mastery(topic_id, new_mastery, new_stability, due_at)

    return mastery, new_mastery, due_at
