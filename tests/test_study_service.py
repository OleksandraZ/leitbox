from datetime import date, datetime, timezone

import pytest

from leitbox import config
from leitbox.domain.scheduler import Scheduler
from leitbox.domain.user import User
from leitbox.services.deck_service import DeckService
from leitbox.services.project_service import ProjectService
from leitbox.services.study_service import StudyService
from leitbox.storage.json_storage import JsonReviewRepository, JsonUserRepository

TODAY = date(2026, 11, 17)
NOW = datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)

def study_service(tmp_path) -> StudyService:
    path = tmp_path / "leitbox.json"
    users = JsonUserRepository(path)
    users.save(User("me", user_id="local"))
    project = ProjectService(users, "local").create_project("German")
    DeckService(users, "local").import_deck(project.name, "A1 verbs", [("sein", "to be"), ("gehen", "to go")], TODAY)
    return StudyService(users, JsonReviewRepository(path), Scheduler(config.INTERVALS), "local")

def test_due_cards_returns_imported_cards(tmp_path):
    service = study_service(tmp_path)
    cards = service.due_cards("German", "A1 verbs", NOW.date())
    assert len(cards) == 2

def test_knew_it_updates_box_due_and_reviews(tmp_path):
    service = study_service(tmp_path)
    cards = service.due_cards("German", "A1 verbs", NOW.date())
    card_id = cards[0].id
    service.answer(card_id, True, NOW)

    stored = service.users.get("local").find_card(card_id)
    assert stored.box == 2
    assert stored.due == date(2026, 11, 22)
    reviews = service.reviews.list_for_user("local")
    assert len(reviews) == 1
    assert reviews[0].card_id == card_id
    assert reviews[0].box_before == 1
    assert reviews[0].box_after == 2

def test_didnt_know_it_updates_box_due_and_reviews(tmp_path):
    service = study_service(tmp_path)
    cards = service.due_cards("German", "A1 verbs", NOW.date())
    card_id = cards[0].id
    service.answer(card_id, False, NOW)

    stored = service.users.get("local").find_card(card_id)
    assert stored.box == 1
    assert stored.due == date(2026, 11, 21)
    reviews = service.reviews.list_for_user("local")
    assert len(reviews) == 1
    assert reviews[0].card_id == card_id
    assert reviews[0].box_before == 1
    assert reviews[0].box_after == 1

def test_unknown_id_raises_error(tmp_path):
    service = study_service(tmp_path)

    with pytest.raises(ValueError):
        service.answer("no-such-id", True, NOW)

    assert service.reviews.list_for_user("local") == []

def test_next_due(tmp_path):
    service = study_service(tmp_path)
    assert service.next_due("German", "A1 verbs") == TODAY
