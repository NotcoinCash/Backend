from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_supply: Mapped[int] = mapped_column()
    developers: Mapped[int] = mapped_column()
    community: Mapped[int] = mapped_column()
    mined: Mapped[int] = mapped_column()
