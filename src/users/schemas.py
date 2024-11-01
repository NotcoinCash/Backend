from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserCreateScheme(BaseModel):
    id: int


class UserGetScheme(BaseModel):
    id: int
    balance: int = 0
    boosts_info: Optional[dict] = {}
    joined_at: datetime = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)
