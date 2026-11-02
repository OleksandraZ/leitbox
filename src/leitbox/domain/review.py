from datetime import datetime
import uuid


class Review():
   def  __init__(self, card_id: str, user_id: str, reviewed_at: datetime, knew_it: bool, box_before: int, box_after: int, review_id: str | None = None):
      self.card_id = card_id
      self.user_id = user_id
      self.reviewed_at = reviewed_at
      self.knew_it = knew_it
      self.box_before = box_before
      self.box_after = box_after
      if review_id is None:
         review_id = str(uuid.uuid4())
      self.id = review_id
