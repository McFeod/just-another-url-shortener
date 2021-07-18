from typing import Optional, Protocol

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from db.tables import short_links
from exceptions import LinkCollision, LinkNotFound
from repositories.base import DBRepo


class ShortLinkRepoProtocol(Protocol):
    async def create_link(self, slug: str, origin: str) -> None:
        ...

    async def find_origin(self, slug: str) -> Optional[str]:
        ...

    async def remove_link(self, slug: str) -> None:
        ...


class ShortLinkRepo(DBRepo, ShortLinkRepoProtocol):
    async def create_link(self, slug: str, origin: str) -> None:
        try:
            query = sa.insert(short_links).values(slug=slug, origin=origin)
            await self.db.execute(query)
            await self.db.commit()
        except IntegrityError:
            raise LinkCollision()

    async def find_origin(self, slug: str) -> str:
        query = sa.select([short_links.c.origin]).where(short_links.c.slug == slug).limit(sa.literal(1))
        cursor = await self.db.execute(query)
        result = cursor.fetchone()
        if result is None:
            raise LinkNotFound()
        return result[0]

    async def remove_link(self, slug: str) -> None:
        query = sa.delete(short_links).where(short_links.c.slug == slug).returning(short_links.c.slug)
        cursor = await self.db.execute(query)
        if cursor.rowcount:
            await self.db.commit()
        else:
            raise LinkNotFound()