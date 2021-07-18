from pydantic import BaseModel, constr, HttpUrl

from config import settings


class FullURLPayload(BaseModel):
    url: HttpUrl


ShortURL = constr(regex='%s/[a-zA-Z0-9]{1,12}' % settings.app.short_domain)


class ShortURLPayload(BaseModel):
    url: ShortURL
