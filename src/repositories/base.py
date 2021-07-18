from fastapi import Depends
from sqlalchemy import literal
from sqlalchemy.ext.asyncio import AsyncSession

from db.pool import db_session


class DBRepo:
    def __init__(self, session: AsyncSession = Depends(db_session)) -> None:
        self._session = session

    async def apply_query(self, query) -> int:
        cursor = await self._session.execute(query)
        affected_rows = cursor.rowcount
        if cursor.rowcount:
            await self._session.commit()
        return affected_rows

    async def fetch_single_value(self, query, column: int = 0):
        cursor = await self._session.execute(query.limit(literal(1)))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[column]