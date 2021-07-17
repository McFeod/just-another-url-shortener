from typing import Optional

from fastapi import FastAPI

from config import settings


app = FastAPI()


@app.get('/')
def stub():
    return {'todo': 'api'}
