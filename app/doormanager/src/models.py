"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
import datetime as dt

from pydantic import BaseModel
from typing import Optional, List

from database import Base

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic

class UserOrm(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    mac = Column(String, unique=True, nullable=True)
    pin = Column(Integer, unique=True, nullable=True)
    start=Column(DateTime, default=dt.datetime.utcnow)
    end=Column(DateTime, nullable=True)
    access_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User(id="{self.id}", ' \
               f'name="{self.name}", ' \
               f'mac="{self.mac}", ' \
               f'pin="{self.pin}", ' \
               f'start="{self.start}", ' \
               f'end="{self.end}", ' \
               f'access_level="{self.access_level}", ' \
               f'is_active="{self.is_active}")>'


class UserModel(BaseModel):
    name:str
    mac:Optional[str]
    pin:Optional[int]
    end:Optional[dt.datetime]
    access_level:int


class MacModel(BaseModel):
    mac: str
    rssi: int

class MacListModel(BaseModel):
    candidates: List[MacModel]

class AccessModel(BaseModel):
    access_level: int
# PydanticUser = sqlalchemy_to_pydantic(UserOrm)
