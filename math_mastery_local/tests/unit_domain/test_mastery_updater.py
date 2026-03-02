from domain.services.mastery_updater import MasteryUpdater


def test_mastery_and_stability_change_on_correct_attempt():
    updater = MasteryUpdater(learning_rate=0.3)
    new_mastery, new_stability, due_at = updater.update(0.4, True, 0.5, 1.0)

    assert new_mastery > 0.4
    assert new_stability > 1.0
    assert due_at is not None


def test_mastery_drops_on_incorrect_attempt():
    updater = MasteryUpdater(learning_rate=0.3)
    new_mastery, new_stability, due_at = updater.update(0.6, False, 0.5, 2.0)

    assert new_mastery < 0.6
    assert new_stability < 2.0
    assert due_at is not None
