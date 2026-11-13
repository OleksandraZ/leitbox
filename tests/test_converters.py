# A user round trip: user → project → deck → that card. 
# Then check the IDs and names at each level, 
# e.g. loaded.projects[0].decks[0].cards[0].id.
# A quick mutation check: change "id" to "deck_id" in deck_to_dict, 
# see the test go red, then change it back.

from datetime import date

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck
from leitbox.domain.project import Project
from leitbox.domain.user import User
from leitbox.storage.converters import card_to_dict, card_from_dict, user_from_dict, user_to_dict

DUE = date(2026, 11, 10)


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