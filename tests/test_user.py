from datetime import date

import pytest

from leitbox.domain.card import Card
from leitbox.domain.deck import Deck
from leitbox.domain.project import Project
from leitbox.domain.user import User

TODAY = date(2026, 11, 6)

def test_two_users_get_different_id():
    user1 = User('user1')
    user2 = User('user2')
    assert user1.id != user2.id

def test_user_id_created_holds():
    user = User('user1', user_id = "1")
    assert user.id == "1"

def test_duplicate_project_name_is_refused():
    user = User('user1')
    project1 = Project('P1')
    user.add_project(project1)

    project2 = Project('p1')
    with pytest.raises(ValueError):
        user.add_project(project2)

def test_add_project_and_check_it_is_saved():
    user = User('user1')
    project1 = Project('P1')
    user.add_project(project1)

    assert user.projects[0].name == 'P1'

def test_existing_project_found():
    user = User('user1')
    project = Project('German')
    user.add_project(project)
    find_project = user.find_project(" german")
    assert find_project is project
    assert find_project.name == project.name

def test_raise_on_finding_not_existing_project():
    user = User('user1')
    project = Project('German')
    user.add_project(project)
    
    with pytest.raises(ValueError):
        user.find_project("Spanish")

def test_raise_on_no_projects():
    user = User('user1')
    
    with pytest.raises(ValueError):
        user.find_project("Spanish")

def test_existing_card_found_successfully():
    card_a1_german = Card(question='q1_de', answer='a1_de', due=TODAY, position=1)
    card_a1_spanish = Card(question='q1_es', answer='a1_es', due=TODAY, position=1)

    user = User("user1", projects=[
        Project("German", decks=[Deck("A1", cards=[card_a1_german])]),
        Project("Spanish", decks=[Deck("A1", cards=[card_a1_spanish])]),
    ])

    assert user.find_card(card_a1_german.id) is card_a1_german
    assert user.find_card(card_a1_spanish.id) is card_a1_spanish

def test_non_existing_card_is_not_found():
    card_a1_german = Card(question='q1_de', answer='a1_de', due=TODAY, position=1)
    card_a1_spanish = Card(question='q1_es', answer='a1_es', due=TODAY, position=1)

    user = User("user1", projects=[
        Project("German", decks=[Deck("A1", cards=[card_a1_german])]),
        Project("Spanish", decks=[Deck("A1", cards=[card_a1_spanish])]),
    ])

    with pytest.raises(ValueError):
        user.find_card("card_a1_french") 
