from abc import ABC, abstractmethod

from leitbox.domain.user import User

class UserRepository(ABC):                        
    @abstractmethod
    def get(self, user_id: str) -> User | None:
        """Return the user, or None if there's none with this ID."""

    @abstractmethod
    def save(self, user: User) -> None:
        """Store the user, replacing an older version with the same ID."""


