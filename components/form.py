from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db import Base, session
from pydantic import BaseModel
import time


class Form(Base):
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    _submits = relationship('Submit', backref='forms')
    _owner = Column(BigInteger, ForeignKey('users.id'))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, **kwargs):
        shorts = cls(
            **kwargs,
            id=int(time.time()),
            _owner=kwargs['user_id']
        )
        session.add(shorts)
        session.commit()
        return shorts

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'submits': [submit.to_json() for submit in self._submits],
            'owner': self._owner
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


class FormModel(BaseModel):
    id: int
    name: str