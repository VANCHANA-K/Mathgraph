from domain.services.mastery_updater import MasteryUpdater


def test_mastery_and_stability_change_on_correct_attempt():
    updater = MasteryUpdater(learning_rate=0.4)
    new_mastery, new_stability, due_at = updater.update(0.4, True, 0.5, 0.6)

    assert new_mastery > 0.4
    assert 0.6 < new_stability <= 1.0
    assert due_at is not None


def test_mastery_drops_on_incorrect_attempt_with_soft_fall_when_high_mastery():
    updater = MasteryUpdater(learning_rate=0.4)
    new_mastery, new_stability, due_at = updater.update(0.9, False, 0.5, 0.9)

    assert 0.8 < new_mastery < 0.9
    assert new_stability < 0.9
    assert due_at is not None


def test_mastery_drop_is_small_when_current_mastery_is_low():
    updater = MasteryUpdater(learning_rate=0.4)
    new_mastery, _, _ = updater.update(0.2, False, 0.5, 0.8)

    assert 0.15 < new_mastery < 0.2
