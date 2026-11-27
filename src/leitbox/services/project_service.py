from leitbox.domain.project import Project
from leitbox.storage.repository import UserRepository


class ProjectService:
    def __init__(self, users: UserRepository, user_id: str):
        self.users = users
        self.user_id = user_id

    def create_project(self, name: str) -> Project:
        user = self.users.get(self.user_id)
        if user is None:
            raise LookupError(f"No user with ID {self.user_id}")
        project = Project(name)
        user.add_project(project)
        self.users.save(user)
        return project

    def list_projects(self) -> list[Project]:
        user = self.users.get(self.user_id)
        if user is None:
            raise LookupError(f"No user with ID {self.user_id}")
        return user.projects
