import json
from pathlib import Path

from leitbox.domain.review import Review
from leitbox.domain.user import User
from leitbox.storage.converters import review_from_dict, review_to_dict, user_from_dict, user_to_dict
from leitbox.storage.repository import ReviewRepository, UserRepository


def _read(path: Path) -> dict:
    if not path.exists():
        return {"users": [], "reviews": []}    
    return json.loads(path.read_text(encoding="utf-8"))

def _write(path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp.replace(path)

class JsonUserRepository(UserRepository):             
    def __init__(self, path: Path):
        self.path = path

    def get(self, user_id: str) -> User | None:
        data = _read(self.path)
        for entry in data["users"]:
            if entry["id"] == user_id:
                return user_from_dict(entry)
        return None     

    def save(self, user: User) -> None:        
        data = _read(self.path)
        user_dict = user_to_dict(user)

        for i, entry in enumerate(data["users"]):
            if entry["id"] == user.id:
                data["users"][i] = user_dict     
                break                            
        else:
            data["users"].append(user_dict)      

        _write(self.path, data)

class JsonReviewRepository(ReviewRepository):
    def __init__(self, path: Path):
        self.path = path

    def add(self, review: Review) -> None:            
        data = _read(self.path)
        data["reviews"].append(review_to_dict(review))
        _write(self.path, data)
    
    def list_for_user(self, user_id: str) -> list[Review]:
        return [review_from_dict(d) for d in _read(self.path)["reviews"] if d["user_id"] == user_id]
