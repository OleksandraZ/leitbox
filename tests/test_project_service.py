import pytest

from leitbox.domain.user import User
from leitbox.services.project_service import ProjectService
from leitbox.storage.json_storage import JsonUserRepository


def test_created_project_is_listed_and_saved(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))
    project = ProjectService(repo, "local").create_project("German")
    fresh = ProjectService(JsonUserRepository(tmp_path / "leitbox.json"), "local")
    assert [project.name for project in fresh.list_projects()] == ["German"]
    assert project.name == "German"


def test_duplicate_project_name_is_rejected(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))
    ProjectService(repo, "local").create_project("German")
    with pytest.raises(ValueError):
        ProjectService(repo, "local").create_project(" german")
    fresh = ProjectService(repo, "local")
    assert [project.name for project in fresh.list_projects()] == ["German"]

def test_empty_project_name_is_rejected(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))
    with pytest.raises(ValueError):
        ProjectService(repo, "local").create_project("")
    fresh = ProjectService(repo, "local")
    assert [project.name for project in fresh.list_projects()] == []

def test_spaces_only_project_name_is_rejected(tmp_path):
    repo = JsonUserRepository(tmp_path / "leitbox.json")
    repo.save(User("me", user_id="local"))
    with pytest.raises(ValueError):
        ProjectService(repo, "local").create_project("   ")
    fresh = ProjectService(repo, "local")
    assert [project.name for project in fresh.list_projects()] == []
