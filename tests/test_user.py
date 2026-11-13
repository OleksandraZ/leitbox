import pytest

from leitbox.domain.project import Project
from leitbox.domain.user import User


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


