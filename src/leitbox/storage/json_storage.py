# storage/json_storage.py: JsonUserRepository, the JSON implementation.
import json
from pathlib import Path

from leitbox.domain.user import User
from leitbox.storage.converters import user_from_dict, user_to_dict
from leitbox.storage.repository import UserRepository


class JsonUserRepository(UserRepository):             
    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> dict:
        if not self.path.exists():
            return {"users": [], "reviews": []}    
        return json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, user_id: str) -> User | None:
        data = self._load()
        for entry in data["users"]:
            if entry["id"] == user_id:
                return user_from_dict(entry)
        return None
                

    def save(self, user: User) -> None:        
        data = self._load()
        user_dict = user_to_dict(user)

        for i, entry in enumerate(data["users"]):
            if entry["id"] == user.id:
                data["users"][i] = user_dict     
                break                            
        else:
            data["users"].append(user_dict)      

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

