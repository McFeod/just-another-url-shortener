from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.pool import db_session


class DBRepo:
    def __init__(self, session: AsyncSession = Depends(db_session)) -> None:
        self.db = session
