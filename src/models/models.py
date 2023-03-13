from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.dialects.mysql import TINYINT as Tinyint

from src.database import Base

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)

    items = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    text = Column(Text)
    owner_id = Column(String(128), ForeignKey("users.email"))

    owner = relationship("User", back_populates="items")

class Cardset(Base):
    __tablename__ = 'cardset'

    id = Column(String(36), primary_key=True, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    cards = Column(Text, nullable=False)

