from leitbox.domain.review import Review
from leitbox.domain.card import Card, CardStatus
from datetime import datetime, timedelta




class Scheduler():
    def __init__(self, intervals: tuple[int, ...]):
        self.intervals = intervals

    def answer(self, card: Card, knew_it: bool, now: datetime, user_id: str) -> Review:
        if card.status == CardStatus.RETIRED:
            raise ValueError("This Card is already retired")
        
        box_before = card.box

        if knew_it and card.box == len(self.intervals):
            card.status = CardStatus.RETIRED
        elif knew_it:
            card.box += 1
            card.due = now.date() + timedelta(days = self.intervals[card.box - 1])
        else:
            card.box = 1
            card.due = now.date() + timedelta(days = self.intervals[0])
        return Review(card.id, user_id, now, knew_it, box_before, card.box)

