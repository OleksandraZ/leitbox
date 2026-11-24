from datetime import date, datetime

from leitbox.domain.card import Card
from leitbox.domain.review import Review
from leitbox.domain.scheduler import Scheduler
from leitbox.storage.repository import ReviewRepository, UserRepository


class StudyService:
    def __init__(self, users: UserRepository, reviews: ReviewRepository, scheduler: Scheduler, user_id: str):
        self.users = users
        self.reviews = reviews
        self.scheduler = scheduler
        self.user_id = user_id
    

    def due_cards(self, project_name: str, deck_name: str, today: date) -> list[Card]:
        user = self.users.get(self.user_id)
        if user is None:
            raise LookupError(f"No user with ID {self.user_id}")
        return user.find_project(project_name).find_deck(deck_name).due_cards(today)

    def answer(self, card_id: str, knew_it: bool, now: datetime) -> Review:
        user = self.users.get(self.user_id)
        if user is None:
            raise LookupError(f"No user with ID {self.user_id}")
        card = user.find_card(card_id)
        review = self.scheduler.answer(card, knew_it, now, self.user_id)
        self.reviews.add(review)      
        self.users.save(user)         
        return review

    def next_due(self, project_name: str, deck_name: str) -> date | None:
        user = self.users.get(self.user_id)
        if user is None:
            raise LookupError(f"No user with ID {self.user_id}")
        return user.find_project(project_name).find_deck(deck_name).next_due()
