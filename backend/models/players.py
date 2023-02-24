from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class PlayerStatus(str, Enum):
    ACTIVE = "Активен"
    BANNED = "Забанен"


class BasePlayer(BaseModel):
    nickname: str
    status: PlayerStatus
    rating: int = 100


class Player(BasePlayer):
    id: UUID

    class Config:
        orm_mode = True


class PlayerCreate(BasePlayer):
    pass


class PlayerUpdate(BasePlayer):
    pass
