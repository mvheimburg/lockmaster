
from typing import List

from repositories import UserRepository, BeaconNotFoundError, PinNotFoundError
from models import BeaconModel, AccessModel

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
            except BeaconNotFoundError as e:
                pass
            else:
                print(f'User found: {user.name}')
                if user.access_level > access_level:
                    access_level = user.access_level     
        
        # return AccessModel(access_level=access_level)
        print(f'Access level to retur: {access_level}')
        return access_level



    def get_access_level_by_pin(self, pin) -> int:
        access_level = 0
 
        try:
            user = self._repository.get_by_pin(pin)
        except PinNotFoundError as e:
            pass
        else:
            print(f'User found: {user.name}')
            if user.access_level > access_level:
                access_level = user.access_level    
        
        # return AccessModel(access_level=access_level)
        print(f'Access level to retur: {access_level}')
        return access_level

    
    def get_current_candidate_list(self) -> List[BeaconModel]:
        return self.candidate_list


    def detected_beacon(self, uuid:str) -> int:
        access_level = 0
 
        try:
            user = self._repository.get_by_uuid(mac=uuid)
        except PinNotFoundError as e:
            pass
        else:
            print(f'User found: {user.name}')
            if user.access_level > access_level:
                access_level = user.access_level    