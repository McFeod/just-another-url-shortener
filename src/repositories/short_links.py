from typing import Optional, Protocol


class ShortLinkRepoProtocol(Protocol):
    async def create_link(self, slug: str, origin: str) -> None:
        ...

    async def find_origin(self, slug: str) -> Optional[str]:
        ...

    async def remove_link(self, slug: str) -> None:
        ...
