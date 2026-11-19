from datetime import date

import pytest

from leitbox.domain.user import User
from leitbox.services.deck_service import DeckService
from leitbox.services.project_service import ProjectService
from leitbox.storage.json_storage import JsonUserRepository

TODAY = date(2026, 11, 17)

def stored_project(tmp_path, name="German"):
    return JsonUserRepository(tmp_path / "leitbox.json").get("local").find_project(name)


def test_deck_is_imported_successfully(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))        
    project = ProjectService(repo, "local").create_project("German")
    DeckService(repo, "local").import_deck(project.name, "A1 verbs", [("sein", "to be"), ("gehen", "to go")], TODAY)
    stored = stored_project(tmp_path)
    assert stored.name == "German"
    assert stored.decks[0].name == "A1 verbs"
    assert len(stored.decks[0].cards) == 2
    assert stored.decks[0].cards[0].question == "sein"
    assert stored.decks[0].cards[1].question == "gehen"
    assert stored.decks[0].cards[0].box == 1
    assert stored.decks[0].cards[0].due == TODAY

def test_deck_is_not_imported_into_unknown_project(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))        
    ProjectService(repo, "local").create_project("German")

    with pytest.raises(ValueError):
        DeckService(repo, "local").import_deck("Spanish", "A1 verbs", [("sein", "to be"), ("gehen", "to go")], TODAY)
    
    stored = stored_project(tmp_path)
    assert len(stored.decks) == 0

def test_duplicate_deck_is_not_imported(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))        
    project = ProjectService(repo, "local").create_project("German")

    DeckService(repo, "local").import_deck(project.name, "A1 verbs", [("sein", "to be"), ("gehen", "to go")], TODAY)

    with pytest.raises(ValueError):
        DeckService(repo, "local").import_deck(project.name, "  a1 verbs", [("sein", "to be"), ("gehen", "to go")], TODAY)
    
    stored = stored_project(tmp_path)
    assert len(stored.decks) == 1

def test_deck_with_empty_name_is_not_imported(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))        
    project = ProjectService(repo, "local").create_project("German")
    
    with pytest.raises(ValueError):
        DeckService(repo, "local").import_deck(project.name, "", [("sein", "to be"), ("gehen", "to go")], TODAY)
    stored = stored_project(tmp_path)
    assert len(stored.decks) == 0

    