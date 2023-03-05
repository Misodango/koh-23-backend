from typing import List, Any, Optional

from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Signup(BaseModel):
    email: str
    password: str


class TodoModel(BaseModel):
    id: int
    title: str
    text: str
    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    title: str
    text: str
    owner_id: str

class TodoUpdate(BaseModel):
    id : int
    text: str

class ShowUser(BaseModel):
    id: int

class UserModel(BaseModel):
    email: str
    todos: List[TodoModel]
    class Config:
        orm_mode = True

class MlFundamentalModel(BaseModel):
    data: List[List[Any]]

class MlFundamentalResponse(BaseModel):
    results: List[float]

class MlData(BaseModel):
    data: List[List]

class MlResponse(BaseModel):
    result: List
    class Config:
        orm_mode = True