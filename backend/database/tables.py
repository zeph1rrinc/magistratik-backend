import uuid

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = "player"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    rating = Column(Integer, nullable=False, default=100, index=True)


class Season(Base):
    __tablename__ = "season"

    id = Column(Integer, primary_key=True)
    final_date = Column(Date)
    winner = Column(
        UUID(as_uuid=True), ForeignKey("player.id", ondelete="CASCADE"), index=True
    )


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, ForeignKey("season.id", ondelete="CASCADE"), index=True)
    series_date = Column(Date)


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    series = Column(
        Integer, ForeignKey("series.id", ondelete="CASCADE"), index=True, nullable=False
    )
    number = Column(Integer, nullable=False)
    winner_command = Column(String, nullable=False)


class PlayerGame(Base):
    __tablename__ = "player_game"

    player_id = Column(
        UUID(as_uuid=True),
        ForeignKey("player.id", ondelete="CASCADE"),
        primary_key=True,
    )
    game_id = Column(
        Integer, ForeignKey("game.id", ondelete="CASCADE"), primary_key=True
    )
    role = Column(String, nullable=False)
