from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class UserCreateScheme(BaseModel):
    id: int
    username: str


class UserGetScheme(BaseModel):
    id: int
    username: str
    balance: int = 0
    boosts_info: Optional[dict] = {}
    joined_at: datetime = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class ReferralsGetScheme(BaseModel):
    id: int
    username: str
    balance: int = 0
    joined_at: datetime = None
    is_active: bool = True
    referrer_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TasksGetScheme(BaseModel):
    id: int
    name: str
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
