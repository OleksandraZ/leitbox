import uuid

from leitbox.domain.deck import Deck

class Project():
    def __init__(self, name: str, decks: list[Deck] | None = None, project_id: str | None = None):
        self.name = name
        if decks is None:
            decks = []          
        self.decks = decks
        if project_id is None:
            project_id = str(uuid.uuid4())
        self.id = project_id

    def add_deck(self, deck: Deck) -> None:
        self.decks.append(deck)

