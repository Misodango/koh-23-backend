import json

from typing import List, Optional
from src import cruds

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src import cruds
from src.database import get_db
from src.schemas.schemas import *

from src.ngrok.settings import setup_ngrok

import openai

settings = setup_ngrok()

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
    print(type(json_data))
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
    return json_data

@router.post('/ml_fundamental', response_model=MlFundamentalResponse)
def ml(data: MlFundamentalModel):
    json_data = cruds.ml_fundamental.ml(data=data)
    if not json_data:
        raise HTTPException(status_code=405, detail='Appropriate Data is Not Provided')
    return json_data

@router.get('/cardset')
def index(db: Session = Depends(get_db)):
    json_data = cruds.cardset.index(db)
    print(json_data)
    if not json_data:
        raise HTTPException(status_code=404, detail='Todo not found')
    res = []
    for cardset in json_data:    
        #print("あああああああああああああああああああああ", cardset.id)
        parsed_cards = json.loads(cardset.cards)
        res.append({"id":cardset.id, "name":cardset.name, "cards":parsed_cards})
    return res

@router.post('/cardset')
def create(data : ICardset):
    #json_data = cruds.cardset.generate()
    print(data)

@router.post('/cardset/create')
def create(data : CardsetCreateData, db: Session = Depends(get_db)):
    sentences = data.sentences
    messages=[
        {"role": "system","content": "次のそれぞれの文章に対して，問題文と答えをそれぞれ作成してください．ただし次のフォーマットに従い，JSON形式で出力してください."},
        {"role": "assistant", "content": "フォーマット"},
        {"role": "assistant", "content": "[{\"qustion\":問題, \"answer\": 答え}, {\"qustion\":問題, \"answer\": 答え}]"},
    ]     
    for sentence in sentences:
        messages.append({
            "role": "assistant",
            "content": sentence
        })
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages
    )
    json_data = res["choices"][0]["message"]["content"]
    cardset = {
        "id": data.id,
        "name": data.name,
        "cards": json_data
    }
    
    #print(res)
    #print(json_data)
    #cruds.cardset.generate(db, json_data)
    return cruds.cardset.generate(db, cardset)
    
@router.get('/cardset/{id}')
def find(id: str, db: Session = Depends(get_db)):
    json_cardset =  cruds.cardset.find(db, id)
    #print(json_cardset)
    
    return {
        "id": json_cardset.id,
        "name": json_cardset.name,
        "cards": json.loads(json_cardset.cards)
    }


@router.put('/cardset/{id}/edit')
def edit(data: PutCardset, db: Session = Depends(get_db)):
    id = data.id
    name = data.name
    card_data = json.dumps(data.cards, ensure_ascii=False)
    cruds.cardset.replace(db, id, name, card_data)
    return {"message": "successed"}

    
    

        
    
