import uuid

from leitbox.domain.deck import Deck

class Project():
    def __init__(self, name: str, decks: list[Deck] | None = None, project_id: str | None = None):
        name = name.strip()  
        if not name:                          
            raise ValueError("A project needs a name")
        self.name = name
        if decks is None:
            decks = []          
        self.decks = decks
        if project_id is None:
            project_id = str(uuid.uuid4())
        self.id = project_id

    def add_deck(self, deck: Deck) -> None:
        for existing in self.decks:
            if existing.name.casefold() == deck.name.casefold():
                raise ValueError(f"A deck called '{deck.name}' already exists")
        self.decks.append(deck)    

    def find_deck(self, name: str) -> Deck:
        for deck in self.decks:
            if name.strip().casefold() == deck.name.casefold():
                return deck
        raise ValueError(f"A deck called '{name}' doesn't exist")
        

