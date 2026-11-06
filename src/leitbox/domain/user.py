import uuid
from leitbox.domain.project import Project

class User():
    def __init__(self, name: str, projects: list[Project] | None = None, user_id: str | None = None):
        self.name = name
        if projects is None:
            projects = []          
        self.projects = projects
        if user_id is None:
            user_id = str(uuid.uuid4())
        self.id = user_id
