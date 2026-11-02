from enum import Enum
from datetime import date
import uuid


class CardStatus(Enum):
    ACTIVE = "active"
    RETIRED = "retired"

class Card:
    def __init__(self, question: str, answer: str, due: date, position: int, box: int = 1, status: CardStatus = CardStatus.ACTIVE, card_id: str | None = None):
        self.question = question
        self.answer = answer
        self.due = due
        self.position = position
        self.box = box
        self.status = status
        if card_id is None:
            card_id = str(uuid.uuid4())
        self.id = card_id

    def is_due(self, today: date) -> bool:
        return self.status == CardStatus.ACTIVE and today >= self.due
