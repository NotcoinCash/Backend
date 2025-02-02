from pydantic import BaseModel, ConfigDict, PositiveInt
from typing import List, Optional, Dict
from datetime import datetime


class UserCreateScheme(BaseModel):
    id: int
    username: str
    photo: Optional[str] = None
    referrer_id: Optional[int] = None


class UserGetBoostsScheme(BaseModel):
    level: int
    base_value: int
    value_per_level: int


class UserGetScheme(BaseModel):
    id: int
    username: str
    photo: Optional[str] = None
    balance: int = 0
    boosts_info: Dict[str, UserGetBoostsScheme]
    joined_at: datetime = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class ReferralsGetScheme(BaseModel):
    id: int
    username: str
    photo: Optional[str] = None
    balance: int = 0
    joined_at: datetime = None

    model_config = ConfigDict(from_attributes=True)


class TasksGetScheme(BaseModel):
    id: int
    name: str
    url: str
    description: Optional[str] = None
    icon: str
    reward: int

    model_config = ConfigDict(from_attributes=True)


class UpdateUserBoostsInfoScheme(BaseModel):
    user_id: int
    boost_id: int
    boost_level: int


class UpdateUserTasksScheme(BaseModel):
    user_id: int
    task_id: int


class UpdateUserBalanceScheme(BaseModel):
    user_id: int
    tokens: int


class WebSocketMiningTokensMessageScheme(BaseModel):
    tokens: PositiveInt

