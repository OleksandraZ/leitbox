from datetime import date, timedelta

from leitbox.domain.card import Card, CardStatus

DUE = date(2026, 11, 10)

def test_new_card_is_box1_and_active():
    card = Card("question", "answer", DUE, 1)
    assert card.status == CardStatus.ACTIVE
    assert card.box == 1 
    assert card.id is not None

def test_two_new_cards_have_different_ids():
    card1 = Card("question1", "answer1", DUE, 1)
    card2 = Card("question2", "answer2", DUE, 1)
    assert card1.id != card2.id

def test_card_id_created_holds():
    card = Card("question", "answer", DUE, 1, card_id = "abc")
    assert card.id == "abc"

def test_is_due_day_before():
    card = Card("question", "answer", DUE, 1)
    assert card.is_due(DUE - timedelta(days=1)) is False

def test_is_due_on_due_date():
    card = Card("question", "answer", DUE, 1)
    assert card.is_due(DUE) is True

def test_is_due_the_day_after():
    card = Card("question", "answer", DUE, 1)
    assert card.is_due(DUE + timedelta(days=1)) is True

def test_is_due_for_retired_card_on_due_date():
    card = Card("question", "answer", DUE, 1, status=CardStatus.RETIRED)
    assert card.is_due(DUE) is False

