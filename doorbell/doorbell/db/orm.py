"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
import datetime as dt

from pydantic import BaseModel
from typing import Optional, List

from database import Base
import gpiozero


from const import(
     COMMAND_PAYLOAD
    ,STATUS_PAYLOAD
)

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic

class UserOrm(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    uuid = Column(String, nullable=True)
    pin = Column(Integer, nullable=False)
    start=Column(DateTime, default=dt.datetime.utcnow)
    end=Column(DateTime, nullable=True)
    access_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User(id="{self.id}", ' \
               f'name="{self.name}", ' \
               f'uuid="{self.uuid}", ' \
               f'pin="{self.pin}", ' \
               f'start="{self.start}", ' \
               f'end="{self.end}", ' \
               f'access_level="{self.access_level}", ' \
               f'is_active="{self.is_active}")>'


class UserModel(BaseModel):
    name:str
    uuid:Optional[str]
    pin:Optional[int]
    end:Optional[dt.datetime]
    access_level:int


class MqttTopics(BaseModel):
    command: Optional[str]
    state: Optional[str]


class AccessModel(BaseModel):
    name:Optional[str]
    access_level: int


class Door(BaseModel):
    name: str
    state: str = "Unknown"
    topic: MqttTopics = MqttTopics()
    relay: gpiozero.OutputDevice

    class Config:
        arbitrary_types_allowed = True

    def startup(self):
        self.update_status()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic.command=f"door/{self.name}/cmd"
        self.topic.state=f"door/{self.name}/state"

    def update_status(self):
        if self.relay.value:
            self.state = STATUS_PAYLOAD.UNLOCKED
        else:
            self.state = STATUS_PAYLOAD.LOCKED

    def unlock(self):
        print(f"Unlocking door {self.name}")
        self.relay.on()
        self.update_status()

    def lock(self):
        print(f"Locking door {self.name}")
        self.relay.off()
        self.update_status()

    def toggle_door(self):
        print(f"Toggling door {self.name}")
        self.relay.toggle()
        self.update_status()


    def get_state(self):
        return self.state




class DoorDummy(BaseModel):
    name: str
    state: str = "Unknown"
    topic: MqttTopics = MqttTopics()
    relay: int



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic.command=f"door/{self.name}/cmd"
        self.topic.state=f"door/{self.name}/state"


    def startup(self):
        self.update_status()


    def update_status(self):
        pass

    def unlock(self):
        print(f"Locking door {self.name}")
        self.update_status()


    def lock(self):
        print(f"Locking door {self.name}")
        self.update_status()

    def toggle_door(self):
        print(f"Toggling door {self.name}")
        self.update_status()

    def get_state(self):
        return self.state