from datetime import date, datetime

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck
from leitbox.domain.project import Project
from leitbox.domain.review import Review
from leitbox.domain.user import User
from leitbox.storage.converters import card_to_dict, card_from_dict, review_from_dict, review_to_dict, user_from_dict, user_to_dict

DUE = date(2026, 11, 10)
REVIEWED_AT = datetime(2026, 11, 10)


def test_card_round_trip():
    card = Card(question="Q1", answer="A1", due=DUE, position=1, box=3, status=CardStatus.RETIRED, card_id="c1")
    card_loaded = card_from_dict(card_to_dict(card))

    assert card.id == card_loaded.id
    assert card.question == card_loaded.question
    assert card.answer == card_loaded.answer
    assert card.position == card_loaded.position
    assert card.box == card_loaded.box
    assert card.due == card_loaded.due
    assert card.status == card_loaded.status

def test_user_round_trip():
    card = Card(question="Q1", answer="A1", due=DUE, position=1, box=3, status=CardStatus.RETIRED, card_id="c1")
    deck = Deck(name="D1", deck_id="d1")
    deck.add_card(card)
    project = Project(name="P1")
    project.add_deck(deck)
    user = User(name="U1")
    user.add_project(project)

    user_loaded = user_from_dict(user_to_dict(user))

    assert user.id == user_loaded.id
    assert user.projects[0].id == user_loaded.projects[0].id
    assert user.projects[0].decks[0].id == user_loaded.projects[0].decks[0].id
    assert user.projects[0].decks[0].cards[0].id == user_loaded.projects[0].decks[0].cards[0].id

def test_review_round_trip():
    review = Review(card_id="c1", user_id="local", reviewed_at=REVIEWED_AT,
                    knew_it=True, box_before=2, box_after=3, review_id="r1")
    loaded = review_from_dict(review_to_dict(review))

    assert loaded.card_id == review.card_id
    assert loaded.user_id == review.user_id
    assert loaded.reviewed_at == review.reviewed_at
    assert loaded.knew_it == review.knew_it
    assert loaded.box_before == review.box_before
    assert loaded.box_after == review.box_after
    assert loaded.id == "r1"
