from sqlalchemy.orm import Session

from src.models import *
from src.schemas import *

def index(db: Session, limit):
  return db.query(Todo).limit(limit).all()

def create(db: Session, todo: TodoCreate):
  new_todo = Todo(title=todo.title, text=todo.text, owner_id=todo.owner_id)
  db.add(new_todo)
  db.commit()
  db.refresh(new_todo)
  return new_todo

def update(db: Session, todo: TodoUpdate):
  update_todo = db.query(Todo).filter(Todo.id == todo.id)
  update_todo.update(
    {
      Todo.text: todo.text
    }
  )
  db.commit()
  return update_todo

def delete(db: Session, target_id: int):
  delete_todo = db.query(Todo).filter(Todo.id == target_id)
  delete_todo.delete()
  db.commit()
  return delete_todo
