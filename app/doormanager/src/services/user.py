"""Services module."""

from uuid import uuid4
from typing import Iterator, List

from repositories import UserRepository, BeaconNotFoundError
from models import UserOrm, AccessModel
import logging

logger = logging.getLogger(__name__)

class UserService():

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> Iterator[UserOrm]:
        # logger.debug(f'Received get_users call')
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> UserOrm:
        return self._repository.get_by_id(user_id)

    def create_user(self, user) -> UserOrm:
        logger.debug(f'Received user is: {user}')
        return self._repository.add(**user)

    def create_test_user(self) -> UserOrm:
        return self._repository.add(name='test')

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
    
    def reinstall_db(self) -> None:
        return self._repository.reinstall_db()



