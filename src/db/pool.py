from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings


engine = create_async_engine(settings.db.dsn, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
