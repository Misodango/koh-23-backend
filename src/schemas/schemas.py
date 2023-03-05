from typing import List, Optional

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

class MlData(BaseModel):
    data: List[List]

class MlResponse(BaseModel):
    result: List
    class Config:
        orm_mode = True