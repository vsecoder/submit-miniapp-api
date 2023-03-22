from sqlalchemy import Column, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import relationship
from db import Base, session
from pydantic import BaseModel
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    register_date = Column(DateTime)
    token = Column(String)

    is_premium = Column(Boolean)
    premium_expire = Column(DateTime)

    notifications = Column(Boolean)

    _forms = relationship('Form', backref='users')

    def __init__(self, id, name, register_date, notifications, is_premium, premium_expire):
        self.id = id
        self.name = name
        self.register_date = register_date
        self.notifications = notifications
        self.is_premium = is_premium
        self.premium_expire = premium_expire
    
    def create(id, name):
        if session.query(User).filter_by(id=id).first():
            raise Exception('User already exists')
        user = User(
            id=id,
            name=name,
            register_date=datetime.datetime.now(),
            notifications=True,
            is_premium=False,
            premium_expire=datetime.datetime.now()
        )
        session.add(user)
        session.commit()
        return user
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'register_date': str(self.register_date),
            'is_premium': self.is_premium,
            'premium_expire': str(self.premium_expire),
            'notifications': self.notifications,
            'forms': [form.to_json() for form in self._forms]
        }


    @classmethod
    def get(cls, id):
        return session.query(User).filter_by(id=id).first()


    @classmethod
    def get_by_token(cls, token):
        return session.query(User).filter_by(token=token).first()

class UserModel(BaseModel):
    id: int
    name: str