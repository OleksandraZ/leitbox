from abc import ABC, abstractmethod

from leitbox.domain.review import Review
from leitbox.domain.user import User

class UserRepository(ABC):                        
    @abstractmethod
    def get(self, user_id: str) -> User | None:
        """Return the user, or None if there's none with this ID."""

    @abstractmethod
    def save(self, user: User) -> None:
        """Store the user, replacing an older version with the same ID."""


class ReviewRepository(ABC):
    @abstractmethod 
    def add(self, review: Review) -> None:
        """Store a new review. Reviews are never changed."""
   
    
    @abstractmethod 
    def list_for_user(self, user_id: str) -> list[Review]:
        """All reviews of this user, oldest first."""
