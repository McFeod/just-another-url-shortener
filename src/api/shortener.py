from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, status

from api.shemas import FullURLPayload, ShortURL, ShortURLPayload
from config import settings
from exceptions import LinkNotFound
from repositories.short_links import ShortLinkRepo
from services.shortener import ShortenerService


router = APIRouter()


def service(repo: ShortLinkRepo = Depends()) -> ShortenerService:
    return ShortenerService(repo=repo, config=settings.app)


def catch_not_found_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except LinkNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='URL not found')
    return wrapper


@router.post('/', response_model=ShortURLPayload)
async def create_link(payload: FullURLPayload, service: ShortenerService = Depends(service)):
    link = await service.create_short_url(payload.url)
    return ShortURLPayload(url=link)


@router.get('/{url:path}', response_model=FullURLPayload)
@catch_not_found_error
async def get_full_link(url: ShortURL, service: ShortenerService = Depends(service)):
    origin = await service.get_full_url(url)
    return FullURLPayload(url=origin)


@router.delete('/{url:path}')
@catch_not_found_error
async def delete_link(url: ShortURL, service: ShortenerService = Depends(service)):
    await service.remove_short_url(url)
