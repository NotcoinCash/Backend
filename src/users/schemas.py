from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserScheme(BaseModel):
    id: int
    balance: int = 0
    boosts_info: Optional[dict] = {}
    joined_at: datetime = None
    is_active: bool = True
    referrer_id: Optional[int] = None
    referrals: List[int] = []
    tasks: List[int] = []

    model_config = ConfigDict(from_attributes=True)
