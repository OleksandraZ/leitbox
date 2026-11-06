from datetime import date
from enum import Enum
import uuid

from leitbox.domain.card import Card

class Visibility(Enum):
    PRIVATE = "private"
    SHARED = "shared"
    DEMO = "demo"

class Deck():
    def __init__(self, name: str, cards: list[Card] | None = None, visibility: Visibility = Visibility.PRIVATE, deck_id: str | None = None):
        self.name = name
        if cards is None:
            cards = []          
        self.cards = cards
        self.visibility = visibility
        if deck_id is None:
            deck_id = str(uuid.uuid4())
        self.id = deck_id

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def due_cards(self, today: date) -> list[Card]:
        due = [card for card in self.cards if card.is_due(today)]
        return sorted(due, key=lambda c: (c.due, c.box, c.position))
        