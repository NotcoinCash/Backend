from typing import List, Optional, Union
from sqlalchemy import JSON, BigInteger, Column, DateTime, ForeignKey, String, Table, func, Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database import Base

users_tasks = Table(
    "users_tasks",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("task_id", ForeignKey("task.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram user id
    balance: Mapped[int] = mapped_column(default=0)
    boosts_info: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    joined_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)

    referrer_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("user.id"))
    referrals: Mapped[Optional["User"]] = relationship(back_populates="referrer")
    referrer: Mapped[Optional["User"]] = relationship(back_populates="referrals", remote_side=[id])

    tasks: Mapped[List["Task"]] = relationship(secondary=users_tasks, back_populates="users")
    
    
class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(256))
    icon: Mapped[str] = mapped_column()
    reward: Mapped[int] = mapped_column()


class Boost(Base):
    __tablename__ = "boost"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(256))
    base_cost: Mapped[int] = mapped_column()
    cost_per_level: Mapped[Union[int, float]] = mapped_column(Numeric)
    base_value: Mapped[int] = mapped_column()
    value_per_level: Mapped[int] = mapped_column()
    max_level: Mapped[int] = mapped_column()
