from datetime import datetime, timedelta, timezone
import pytest

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.scheduler import Scheduler

INTERVALS = (1, 2, 7, 14, 30)
NOW = datetime(2026, 11, 2, 9, 0, tzinfo=timezone.utc)
TODAY = NOW.date()
USER_ID = "user-1"
scheduler = Scheduler(INTERVALS)

def test_answer_records_review():
    card = Card("question", "answer",  TODAY, 1, box=3)
    
    review = scheduler.answer(card, True, NOW, USER_ID) 
 
    assert review.card_id == card.id
    assert review.knew_it is True
    assert review.user_id == USER_ID
    assert review.box_after == 4
    assert review.box_before == 3
    assert review.reviewed_at == NOW


def test_knew_it_in_box_3_moves_to_box_4_due_in_14_days():
    card = Card("question", "answer",  TODAY, 1, box=3)
    scheduler.answer(card, True, NOW, USER_ID) 
    assert card.box == 4
    assert card.due == TODAY + timedelta(days = 14)

def test_did_not_know_it_in_box_3_moves_to_box_1_due_tomorrow():
    card = Card("question", "answer",  TODAY, 1, box=3)
    scheduler.answer(card, False, NOW, USER_ID) 
    assert card.box == 1
    assert card.due == TODAY + timedelta(days = 1)

def test_did_not_know_it_in_box_1_stays_in_box_1_due_tomorrow():
    card = Card("question", "answer",  TODAY, 1, box=1)
    scheduler.answer(card, False, NOW, USER_ID) 
    assert card.box == 1
    assert card.due == TODAY + timedelta(days = 1)

def test_did_not_know_it_box_5_moves_to_box_1_tomorrow():
    card = Card("question", "answer",  TODAY, 1, box=5)
    scheduler.answer(card, False, NOW, USER_ID) 
    assert card.box == 1
    assert card.due == TODAY + timedelta(days = 1)

def test_knew_it_in_box_4_moves_to_box_5_due_in_30_days():
    card = Card("question", "answer",  TODAY, 1, box=4)
    scheduler.answer(card, True, NOW, USER_ID) 
    assert card.box == 5
    assert card.due == TODAY + timedelta(days = 30)

def test_knew_it_in_box_5_retires_stays_in_5():
    card = Card("question", "answer",  TODAY, 1, box=5)
    scheduler.answer(card, True, NOW, USER_ID) 
    assert card.status == CardStatus.RETIRED
    assert card.box == 5

def test_retired_card_error():
    card = Card("question", "answer",  TODAY, 1, box=5, status = CardStatus.RETIRED)
    with pytest.raises(ValueError):
        scheduler.answer(card, True, NOW, USER_ID)
