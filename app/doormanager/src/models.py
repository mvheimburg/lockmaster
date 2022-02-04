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


# class UuidAccessModel(BaseModel):
#     uuid: str
#     access_level: int

    # def __str__(self):
    #  return self.uuid


# class BeaconListModel(BaseModel):
#     candidates: List[BeaconModel]

class AccessModel(BaseModel):
    name:Optional[str]
    access_level: int
# PydanticUser = sqlalchemy_to_pydantic(UserOrm)


class Door(BaseModel):
    name: str
    command_topic: str
    state_topic: str
    state: str = "Unknown"
    # pin: int
    relay: gpiozero.OutputDevice

    class Config:
        arbitrary_types_allowed = True

    # def __init__(self, name:str, command_topic: str, state_topic: str, pin: int):
    #     # self.state = DoorState(name=name, pin=pin, command_topic=command_topic, state_topic=state_topic)
    #     self.name=name
    #     self.command_topic=command_topic
    #     self.state_topic=state_topic


    # def set_relay(self):
    #     self.relay = gpiozero.OutputDevice(self.pin, active_high=False, initial_value=False)


    def startup(self):
        self.update_status()


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
    command_topic: str
    state_topic: str
    state: str = "Unknown"
    pin: int



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