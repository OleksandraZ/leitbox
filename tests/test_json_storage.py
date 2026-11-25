from datetime import date, datetime
import json

import pytest

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck
from leitbox.domain.project import Project
from leitbox.domain.review import Review
from leitbox.domain.user import User
from leitbox.storage.json_storage import JsonReviewRepository, JsonUserRepository

DUE = date(2026, 11, 10)
REVIEWED_AT = datetime(2026, 11, 10)



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

def test_reviews_are_listed_per_user_in_order(tmp_path):
    path = tmp_path / "leitbox.json"
    review_1 = Review(card_id="c1", user_id="local", reviewed_at=REVIEWED_AT,
                    knew_it=True, box_before=2, box_after=3, review_id="r1")

    review_2 = Review(card_id="c2", user_id="other", reviewed_at=REVIEWED_AT,
                        knew_it=True, box_before=2, box_after=3, review_id="r2")

    review_3 = Review(card_id="c3", user_id="local", reviewed_at=REVIEWED_AT,
                            knew_it=True, box_before=2, box_after=3, review_id="r3")
    
    JsonReviewRepository(path).add(review_1)
    JsonReviewRepository(path).add(review_2)
    JsonReviewRepository(path).add(review_3)

    loaded_local = JsonReviewRepository(path).list_for_user("local")
    
    assert [r.id for r in loaded_local] == ["r1", "r3"]


def test_missing_file_returns_empty_list(tmp_path):
    path = tmp_path / "leitbox.json"

    loaded_local = JsonReviewRepository(path).list_for_user("local")
    
    assert loaded_local == []

def test_users_and_reviews_dont_overwrite_each_other(tmp_path):
    path = tmp_path / "leitbox.json"
    users = JsonUserRepository(path)
    reviews = JsonReviewRepository(path)

    users.save(User(name='U1', user_id='local'))

    review_1 = Review(card_id="c1", user_id="local", reviewed_at=REVIEWED_AT,
                        knew_it=True, box_before=2, box_after=3, review_id="r1")
    
    reviews.add(review_1)

    users.save(User(name='U1', user_id='local'))

    assert len(JsonReviewRepository(path).list_for_user('local')) == 1
    assert JsonUserRepository(path).get('local') is not None

def test_broken_data_file(tmp_path):
    path = tmp_path / "leitbox.json"
    path.write_text('{"users": [', encoding="utf-8")
    
    with pytest.raises(ValueError, match="damaged"):
        JsonUserRepository(path).get("local")
