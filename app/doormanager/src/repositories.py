"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator
import datetime

from models import UserOrm

class Repository():
    def __init__(self, session_factory: Callable) -> None:
        self.session_factory = session_factory


class UserRepository(Repository):

    def get_all(self) -> Iterator[UserOrm]:
        with self.session_factory() as session:
            return session.query(UserOrm).all()

    def get_by_id(self, user_id: int) -> UserOrm:
        with self.session_factory() as session:
            entity = session.query(UserOrm).filter(UserOrm.id == user_id).first()
            if not entity:
                raise UserIdNotFoundError(user_id)
            return entity

    def get_by_uuid(self, uuid: str) -> UserOrm:
        with self.session_factory() as session:
            entity = session.query(UserOrm).filter(UserOrm.uuid == uuid).first()
            if not entity:
                raise BeaconNotFoundError(uuid)
            return entity

    def get_by_pin(self, pin: int) -> UserOrm:
        with self.session_factory() as session:
            entity = session.query(UserOrm).filter(UserOrm.pin == pin).first()
            if not entity:
                raise PinNotFoundError(pin)
            return entity
    
    def get_by_pin(self, pin: int) -> UserOrm:
        with self.session_factory() as session:
            entity = session.query(UserOrm).filter(UserOrm.pin == pin).first()
            if not entity:
                raise PinNotFoundError(pin)
            return entity


    def add(self, name: str, uuid: str = None, pin: int = None, end: datetime.datetime = None, access_level: int = 1, is_active: bool = True) -> UserOrm:
        with self.session_factory() as session:
            entity = UserOrm(name=name, uuid=uuid, pin=pin, end=end, access_level=access_level, is_active=is_active)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity


    def edit(self, user_id: int, name: str, uuid: str = None, pin: int = None, end: datetime.datetime = None, access_level: int = 1, is_active: bool = True) -> UserOrm:
        with self.session_factory() as session:
            entity = session.query(UserOrm).filter(UserOrm.id == user_id).first()
            entity.name = name
            entity.uuid = uuid
            entity.pin = pin
            entity.end = end
            entity.access_level = access_level
            entity.is_active = is_active
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity


    def delete_by_id(self, user_id: int) -> None:
        with self.session_factory() as session:
            entity: UserOrm = session.query(UserOrm).filter(UserOrm.id == user_id).first()
            if not entity:
                raise UserIdNotFoundError(user_id)
            session.delete(entity)
            session.commit()
    
    def reinstall_db(self, user_id: int) -> None:
       pass



    # def evaluate_mac(self, mac: int) -> None:





class NotFoundError(Exception):
    entity_name: str
    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found: {entity_id}')

class IdNotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found: id: {entity_id}')



class UserIdNotFoundError(IdNotFoundError):
    entity_name: str = 'User'


class BeaconNotFoundError(NotFoundError):
    entity_name: str = 'UUID'

class PinNotFoundError(NotFoundError):
    entity_name: str = 'Pin'
