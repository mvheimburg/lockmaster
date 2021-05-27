"""Services module."""

from uuid import uuid4
from typing import Iterator, List

from repositories import UserRepository, MacNotFoundError
from models import UserOrm, MacModel, AccessModel
import logging

logger = logging.getLogger(__name__)

class UserService:

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



class AccessService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository
        self.candidate_list = []

    
    def post_candidate_list(self, candidates) -> None:
        print(f'Received candidate_list call')
        print(candidates)
        self.candidate_list = candidates.candidates


    def get_access_level(self) -> int:
        access_level = 0

        for candidate in self.candidate_list:
            try:
                user = self._repository.get_by_mac(candidate.mac)
            except MacNotFoundError as e:
                pass
            else:
                if user.access_level > access_level:
                    access_level = user.access_level
        
        # return AccessModel(access_level=access_level)
        return access_level

    
    def get_current_candidate_list(self) -> List[MacModel]:
        return self.candidate_list



class MqttService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository
        self.candidate_list = []

    
    def post_candidate_list(self, candidates) -> None:
        print(f'Received candidate_list call')
        print(candidates)
        self.candidate_list = candidates.candidates


    def get_access_level(self) -> int:
        access_level = 0

        for candidate in self.candidate_list:
            try:
                user = self._repository.get_by_mac(candidate.mac)
            except MacNotFoundError as e:
                pass
            else:
                if user.access_level > access_level:
                    access_level = user.access_level
        
        # return AccessModel(access_level=access_level)
        return access_level

    
    def get_current_candidate_list(self) -> List[MacModel]:
        return self.candidate_list