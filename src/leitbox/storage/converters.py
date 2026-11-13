from datetime import date

from leitbox.domain.card import Card, CardStatus
from leitbox.domain.deck import Deck, Visibility
from leitbox.domain.project import Project
from leitbox.domain.user import User

def card_to_dict(card: Card) -> dict:
    return {
        "question": card.question,
        "answer": card.answer,
        "due": card.due.isoformat(),
        "position": card.position,
        "box": card.box,
        "status": card.status.value,
        "id": card.id,
    }

def card_from_dict(data: dict) -> Card:
    return Card(
        question=data["question"],
        answer=data["answer"],
        due=date.fromisoformat(data["due"]),
        position=data["position"],
        box=data["box"],
        status=CardStatus(data["status"]),
        card_id=data["id"],
    )

def deck_to_dict(deck: Deck) -> dict:
    return {
        "name": deck.name,
        "cards": [card_to_dict(c) for c in deck.cards],
        "visibility": deck.visibility.value,
        "id": deck.id,
    }

def deck_from_dict(data: dict) -> Deck:
    return Deck(
        name=data["name"],
        cards=[card_from_dict(c) for c in data["cards"]],
        visibility=Visibility(data["visibility"]) ,
        deck_id=data["id"],
    )

def project_to_dict(project: Project) -> dict:
    return {
        "name": project.name,
        "decks": [deck_to_dict(d) for d in project.decks],
        "id": project.id,
    }

def project_from_dict(data: dict) -> Project:
    return Project(
        name=data["name"],
        decks=[deck_from_dict(d) for d in data["decks"]],
        project_id=data["id"]
    )

def user_to_dict(user: User) -> dict:
    return {
        "name": user.name,
        "projects": [project_to_dict(p) for p in user.projects],
        "id": user.id,
    }

def user_from_dict(data: dict) -> User:
    return User(
        name=data["name"],
        projects=[project_from_dict(p) for p in data["projects"]],
        user_id=data["id"]
    )

 