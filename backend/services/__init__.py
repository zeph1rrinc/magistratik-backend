from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy.exc
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..database.tables import Base


class BaseService:
    def __init__(self, table: Base, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.table = table

    async def get_many(self) -> List[Base]:
        query = select(self.table)
        res = await self.session.execute(query)
        return list(map(lambda x: x[0], res.fetchall()))

    async def get(self, row_id: int | UUID) -> Base:
        return await self._get(row_id)

    async def create(self, row_data: BaseModel) -> Base:
        new_row = self.table(**row_data.dict())
        try:
            self.session.add(new_row)
            await self.session.flush()
            return new_row
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Player already exists")

    async def update(self, row_id: int | UUID, row_data: BaseModel) -> Base:
        await self._get(row_id)
        query = (
            update(self.table)
            .where(self.table.id == row_id)
            .values(**row_data.dict())
            .returning(self.table)
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        return row[0]

    async def delete(self, row_id: int | UUID):
        await self._get(row_id)
        query = delete(self.table).where(self.table.id == row_id)
        await self.session.execute(query)

    async def _get(self, row_id: int | UUID) -> Optional[Base]:
        query = select(self.table).where(self.table.id == row_id)
        result = await self.session.execute(query)
        row = result.fetchone()

        if not row:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return row[0]
