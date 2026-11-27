import uuid
from leitbox.domain.card import Card
from leitbox.domain.project import Project

class User:
    def __init__(self, name: str, projects: list[Project] | None = None, user_id: str | None = None):
        self.name = name
        if projects is None:
            projects = []
        self.projects = projects
        if user_id is None:
            user_id = str(uuid.uuid4())
        self.id = user_id

    def add_project(self, project: Project) -> None:
        for existing in self.projects:
            if existing.name.casefold() == project.name.casefold():
                raise ValueError(f"A project called '{project.name}' already exists")
        self.projects.append(project)

    def find_project(self, name: str) -> Project:
        for project in self.projects:
            if name.strip().casefold() == project.name.casefold():
                return project
        raise ValueError(f"A project called '{name}' doesn't exist")

    def find_card(self, card_id: str) -> Card:
        for project in self.projects:
            for deck in project.decks:
                for card in deck.cards:
                    if card.id == card_id:
                        return card
        raise ValueError(f"No card with ID {card_id}")
