from sqlalchemy import String, TIMESTAMP, Text
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

    def __repr__(self) -> str:
        return f"full name - {self.first_name} {self.last_name}\n"
    

class Film(Base):
    __tablename__ = "film"

    film_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[int] = mapped_column(String(128))
    description: Mapped[int] = mapped_column(Text)


Base.metadata.create_all(engine)