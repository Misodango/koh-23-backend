import json
import os
import sys

from typing import List, Optional
from src import cruds

from fastapi import Depends, APIRouter, HTTPException
from fastapi.logger import logger
from pydantic import BaseSettings
from sqlalchemy.orm import Session

from src import cruds
from src.database import get_db
from src.schemas.schemas import *


class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"


settings = Settings()


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)

router = APIRouter()

@router.get('/bootup')
def index():
    json_data = cruds.bootup.index()
    if not json_data:
        raise HTTPException(status_code=405, detail='Todo not found')
    return json_data

@router.post('/login')
def login(login: Login, db: Session = Depends(get_db)):
    json_data = cruds.login.login(db, login=login)
    if not json_data:
        raise HTTPException(status_code=404, detail='Account not found')
    return {"message": "successed"}

@router.post('/signup')
def signup(signup: Signup, db: Session = Depends(get_db)):
    json_data = cruds.signup.signup(db, signup=signup)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    return json_data

@router.get('/todo', response_model=List[TodoModel])
def index(limit: Optional[int] = 100, db: Session = Depends(get_db)):
    json_data = cruds.todo.index(db, limit=limit)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    return json_data

@router.post('/todo')
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    json_data = cruds.todo.create(db, todo=todo)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    return {"message": "successed"}

@router.patch('/todo/{target_id}')
def update(target_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    json_data = cruds.todo.update(db, todo=todo)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    return {"message": "successed", "id": target_id}

@router.delete('/todo/{target_id}')
def delete(target_id: int, db: Session = Depends(get_db)):
    json_data = cruds.todo.delete(db, target_id=target_id)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    return {"message": "successed"}

@router.get('/user/{email}', response_model=UserModel)
def show(email: str, db: Session = Depends(get_db)):
    json_data = cruds.user.show(db, email=email)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    return {"email":email, "todos": json_data}

@router.post('/ml', response_model=MlResponse)
def ml(data: MlData):
    json_data = cruds.ml.ml(data=data)
    if not json_data:
        raise HTTPException(status_code=405, detail='Todo not found')
    print(json_data)
    return json_data
