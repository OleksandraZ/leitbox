from datetime import date

from leitbox.domain.card import Card
from leitbox.domain.deck import Deck
from leitbox.storage.repository import UserRepository


class DeckService:
    def __init__(self, users: UserRepository, user_id: str):
        self.users = users
        self.user_id = user_id

    def import_deck(self, project_name: str, deck_name: str, rows: list[tuple[str, str]], today: date) -> Deck:
        user = self.users.get(self.user_id)
        if user is None:
            raise LookupError(f"No user with ID {self.user_id}")
        project = user.find_project(project_name)
        deck = Deck(deck_name)
        for position, (question, answer) in enumerate(rows):
            deck.add_card(Card(question, answer, due=today, position=position))
        project.add_deck(deck)
        self.users.save(user)
        return deck


