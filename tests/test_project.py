
import pytest

from leitbox.domain.deck import Deck
from leitbox.domain.project import Project


def test_two_projects_get_different_id():
    project1 = Project('project1')
    project2 = Project('project2')
    assert project1.id != project2.id

def test_project_id_created_holds():
    project = Project('project', project_id = "1")
    assert project.id == "1"

def test_add_deck_to_project_and_check_len():
    project = Project('project')
    deck = Deck('my_deck')
    project.add_deck(deck)

    assert len(project.decks) == 1

def test_project_with_spaces_only_name_is_refused():
    with pytest.raises(ValueError):
        Project('   ')

def test_project_empty_name_is_refused():
    with pytest.raises(ValueError):
        Project('')

def test_project_trimmed_name():
    project = Project(' P ')
    assert project.name == 'P'

def test_duplicate_deck_name_is_refused():
    project = Project('German')
    deck1 = Deck("A1 verbs")
    project.add_deck(deck1)

    deck2 = Deck(" a1 verbs")
    with pytest.raises(ValueError):
        project.add_deck(deck2)

def test_find_deck_by_name():
    project = Project('project')
    deck = Deck('A1 verbs')
    project.add_deck(deck)

    found_deck = project.find_deck('  a1 verbs')

    assert found_deck.name == 'A1 verbs'

def test_unknown_deck_is_not_found():
    project = Project('project')
    deck = Deck('A1 verbs')
    project.add_deck(deck)

    with pytest.raises(ValueError, match = "doesn't exist"):
        project.find_deck('  a2 verbs')

def test_remove_deck_successfully():
    project = Project('project')
    deck_1 = Deck('A1 verbs')
    deck_2 = Deck('A2 verbs')

    project.add_deck(deck_1)
    project.add_deck(deck_2)

    project.remove_deck(' a1 verbs')
    assert len(project.decks) == 1
    assert project.decks[0].name == "A2 verbs"

def test_removing_unknown_deck():
    project = Project('project')

    with pytest.raises(ValueError):
        project.remove_deck('A1 verbs')
