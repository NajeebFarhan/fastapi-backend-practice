from sqlalchemy import String, TIMESTAMP, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db_setup import engine
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Actor(Base):
    __tablename__ = "actor"

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45))
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP)

    

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(45), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


Base.metadata.create_all(engine)