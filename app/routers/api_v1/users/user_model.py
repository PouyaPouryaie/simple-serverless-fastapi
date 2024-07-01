from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, Literal

class UserModel(BaseModel):
    name: str
    sex: Literal[ "Men", "Women", "None"]
    user_id: Optional[str] = uuid4().hex

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "sex": self.sex,
            "name": self.name
    }