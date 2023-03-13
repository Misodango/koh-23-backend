from sqlalchemy.orm import Session

from src.models import *
from src.schemas import *
def index(db: Session):
  return db.query(Cardset).all()


def generate(db: Session, cardset:dict):
  new_cards = Cardset(id=cardset['id'], name=cardset['name'], cards=cardset['cards'])
  db.add(new_cards)
  db.commit()
  #db.refresh(new_cards)
  return {"message": "successed"}

def find(db: Session, id:str):
  cardset = db.query(Cardset).filter(Cardset.id == id).one()
  return cardset

def replace(db: Session, id: str, name: str, cards: str):
  test = db.query(Cardset).filter(Cardset.id==id).first()
  test.name = name
  test.cards = cards
  db.commit()
  

  