from datetime import date
import json

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck
from leitbox.domain.project import Project
from leitbox.domain.user import User
from leitbox.storage.json_storage import JsonUserRepository

DUE = date(2026, 11, 10)


def test_saved_user_can_be_loaded_again(tmp_path):
    path = tmp_path / "leitbox.json"
    card = Card(question="Q1", answer="A1", due=DUE, position=1, box=3, status=CardStatus.RETIRED, card_id="c1")
    deck = Deck(name="D1", deck_id="d1")
    deck.add_card(card)
    project = Project(name="P1")
    project.add_deck(deck)
    user = User(name="U1")
    user.add_project(project)

    JsonUserRepository(path).save(user)
    loaded = JsonUserRepository(path).get(user.id)    

    assert loaded is not None
    assert loaded.id == user.id
    assert loaded.name == "U1"
    assert loaded.projects[0].decks[0].cards[0].id == card.id
    assert loaded.projects[0].decks[0].cards[0].box == card.box
    assert loaded.projects[0].decks[0].cards[0].due == card.due
    assert loaded.projects[0].decks[0].cards[0].status == card.status

def test_missing_file_returns_none(tmp_path):
    path = tmp_path / "leitbox.json"

    loaded = JsonUserRepository(path).get("any-id")

    assert loaded is None

def test_unknown_user_id_returns_none(tmp_path):
    path = tmp_path / "leitbox.json"
    user = User("U1")
    
    JsonUserRepository(path).save(user)
    loaded = JsonUserRepository(path).get("no-such-id")  

    assert loaded is None

def test_saving_twice_leaves_one_user(tmp_path):
    path = tmp_path / "leitbox.json"
    user = User("U1")
        
    JsonUserRepository(path).save(user)
    project = Project(name="P1")
    user.add_project(project)
    JsonUserRepository(path).save(user)

    loaded = JsonUserRepository(path).get(user.id)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert loaded is not None
    assert len(loaded.projects) == 1
    assert len(data["users"]) == 1

