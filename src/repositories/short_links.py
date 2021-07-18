from typing import Protocol

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from db.tables import short_links
from exceptions import LinkCollision, LinkNotFound
from repositories.base import DBRepo


class ShortLinkRepoProtocol(Protocol):
    async def create_link(self, slug: str, origin: str) -> None:
        ...

    async def find_origin(self, slug: str) -> str:
        ...

    async def remove_link(self, slug: str) -> None:
        ...


class ShortLinkRepo(DBRepo, ShortLinkRepoProtocol):
    async def create_link(self, slug: str, origin: str) -> None:
        try:
            query = sa.insert(short_links).values(slug=slug, origin=origin)
            await self.apply_query(query)
        except IntegrityError:
            raise LinkCollision()

    async def find_origin(self, slug: str) -> str:
        query = sa.select([short_links.c.origin]).where(short_links.c.slug == slug)
        result = await self.fetch_single_value(query)
        if result is None:
            raise LinkNotFound()
        return result

    async def remove_link(self, slug: str) -> None:
        query = sa.delete(short_links).where(short_links.c.slug == slug).returning(short_links.c.slug)
        deleted = await self.apply_query(query)
        if not deleted:
            raise LinkNotFound()
