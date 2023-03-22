from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger
from sqlalchemy.orm import relationship
from db import Base, session
from pydantic import BaseModel
import time


class Submit(Base):
    __tablename__ = 'submits'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    _form_id = Column(Integer, ForeignKey('forms.id'))


    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, **kwargs):
        shorts = cls(
            **kwargs,
            id=round(time.time()),
        )
        session.add(shorts)
        session.commit()
        return shorts

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'form_id': self._form_id
        }


    @classmethod
    def get(cls, id):
        return session.query(cls).filter(cls.id == id).first()

    def delete(self):
        session.delete(self)
        session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def save(self):
        session.commit()


class SubmitModel(BaseModel):
    id: int
    name: str