from random import sample
from typing import Generator, Optional, Tuple

from config import AppSettings
from exceptions import LinkCollision
from repositories.short_links import ShortLinkRepoProtocol


def alphabet_ranges(*ranges: Tuple[str, str]) -> Generator[str, None, None]:
    for start, end in ranges:
        for i in range(ord(start), ord(end) + 1):
            yield chr(i)


ALPHABET = ''.join(alphabet_ranges(('0', '9'), ('A', 'Z'), ('a', 'z')))


class SlugCreator:
    def __init__(self, alphabet: str = ALPHABET) -> None:
        self._alphabet = sorted(alphabet)

    def create(self, size: int) -> str:
        return ''.join(sample(self._alphabet, size))


class ShortenerService:
    def __init__(self, repo: ShortLinkRepoProtocol, config: AppSettings) -> None:
        self._repo = repo
        self._creator = SlugCreator()
        self._slug_size = config.preferred_slug_length
        self._short_domain = config.short_domain

    def _make_url(self, slug: str) -> str:
        return f'{self._short_domain}/{slug}'

    def _make_slug(self, url: str) -> str:
        return url.lstrip(f'{self._short_domain}/')

    async def _save_with_original_slug(self, origin: str, max_attempts: int = 10) -> Optional[str]:
        if max_attempts > 0:
            slug = self._creator.create(self._slug_size)
            try:
                await self._repo.create_link(slug=slug, origin=origin)
            except LinkCollision:
                return self._save_with_original_slug(origin=origin, max_attempts=max_attempts - 1)
            return slug
        return None

    async def create_short_url(self, origin: str) -> Optional[str]:
        slug = await self._save_with_original_slug(origin=origin)
        if slug:
            return self._make_url(slug=slug)
        return None
    
    async def remove_short_url(self, url: str) -> None:
        await self._repo.remove_link(slug=self._make_slug(url=url))

    async def get_full_url(self, url: str) -> str:
        return await self._repo.find_origin(slug=self._make_slug(url=url))