from fastapi import FastAPI

from api.shortener import router as links_api


app = FastAPI()
app.include_router(links_api, prefix='/api/v1/links')
