from datetime import datetime

from domain.entities.mastery_state import MasteryState
from domain.services.mastery_updater import MasteryUpdater


def test_mastery_increases_on_correct_attempt():
    st = MasteryState(user_id="u", topic_id="t", mastery=0.2, stability=2)
    out = MasteryUpdater.update(st, is_correct=True, response_seconds=25, used_hint=False, now=datetime.utcnow())
    assert out.mastery > 0.2
    assert out.stability > 2
