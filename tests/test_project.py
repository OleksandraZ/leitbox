
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