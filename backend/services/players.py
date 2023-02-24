from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ..database import get_session
from ..database.tables import Player


class PlayersService(BaseService):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session=session, table=Player)
