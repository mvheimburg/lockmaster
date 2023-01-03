
from os import access
from typing import List
from threading import Thread, Lock
from time import sleep
import ujson as json

# import xmlrpc.client

from repositories import UserRepository, BeaconNotFoundError, PinNotFoundError
from models import AccessModel

from api.api import presence_detected
from const import DIST_THRESHOLD, DOOR_ID

class AccessService:
    
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository
        self.candidate_list = {}
        self.candidate_list_lock = Lock()
        self.presence = {}
        self.presence_lock = Lock()
        self.countdown_thread = Thread(target=self.countdown, daemon=True)
    
    
    def set_mqttc(self, mqttc):
        self.mqttc = mqttc

    
    def subscribe(self):
        print(f"subscribing to topic: room-assistant/sensor/#")
        self.mqttc.subscribe("room-assistant/sensor/#", qos=0)


    def user_created(new_user):
        print(new_user)
   

    def mqtt_on_message(self, client, properties, topiclist, payload):
        # print(f"PRECENSE FROM CLIENT: {client}")
        # print(f"properties: {properties}")
        # print(f"payload: {payload}")
        # print(f"topiclist: {topiclist}")
        if topiclist[-1] == "attributes":
            uuid=topiclist[-2].split("-")[1]
            # print("Access message: ", uuid, payload) 
            k = self.presence.get(uuid,None)
            if k is not None:
                if k["state"]==DOOR_ID:
                    beacon_data = json.loads(payload)
                    dist = beacon_data.get('distance',None)
                    
                    #PRINT FOR DEBUG
                    user = self._repository.get_by_uuid(uuid=uuid)
                    print(f"Detected user: {user} at distance: {dist}")

                    if dist is not None:
                        if dist < DIST_THRESHOLD:
                            try:
                                user = self._repository.get_by_uuid(uuid=uuid)
                            except BeaconNotFoundError:
                                pass
                            else:
                                print(f'User found: {user.name}')
                                am = AccessModel(name=user.name, access_level=user.access_level)
                                try:
                                    presence_detected(am=am)
                                except ConnectionRefusedError as e:
                                    print(e)



        elif topiclist[-1] == "state":
            uuid=topiclist[-2].split("-")[1]

            if payload == DOOR_ID:
                try:
                    user = self._repository.get_by_uuid(uuid=uuid)
                except BeaconNotFoundError:
                    self.candidate_list_lock.acquire()
                    if uuid not in self.candidate_list.keys():
                        self.candidate_list.update({uuid:{"state":DOOR_ID, "timer":5}})
                    else:
                        self.candidate_list[uuid]["state"]=DOOR_ID
                        self.candidate_list[uuid]["timer"]=5
                    self.candidate_list_lock.release()

                else:
                    self.presence_lock.acquire()
                    if uuid not in self.presence.keys():
                        print(f"Detected user: {user.name}.. adding to list")
                        self.presence.update({uuid:{"state":DOOR_ID, "timer":5}})
                    else:
                        print(f"Detected user: {user.name}.. updating list")
                        self.presence[uuid]["state"]=DOOR_ID
                        self.presence[uuid]["timer"]=5
                    self.presence_lock.release()

            else:
                if uuid in self.candidate_list.keys():
                    self.candidate_list_lock.acquire()
                    self.candidate_list.pop(uuid)
                    self.candidate_list_lock.release()

                if uuid in self.presence.keys():
                    self.presence_lock.acquire()
                    self.presence.pop(uuid)
                    self.presence_lock.release()

            


    def countdown(self):
        while True:
            remove_list=[]
            self.candidate_list_lock.acquire()
            for c, item in self.candidate_list.items():
                item['timer']-=1
                if item['timer'] == 0:
                    remove_list.append(c)
            for c in remove_list:
                # presence_out_of_bounds(c)
                self.candidate_list.pop(c)
            self.candidate_list_lock.release()
            sleep(30)

    # def post_candidate_list(self, candidates) -> None:
    #     print(f'Received candidate_list call')
    #     print(candidates)
    #     self.candidate_list = candidates.candidates


    # def get_access_level(self) -> int:
    #     access_level = 0

    #     for candidate in self.candidate_list:
    #         try:
    #             user = self._repository.get_by_uuid(candidate.uuid)
    #         except BeaconNotFoundError as e:
    #             pass
    #         else:
    #             print(f'User found: {user.name}')
    #             if user.access_level > access_level:
    #                 access_level = user.access_level     
        
    #     # return AccessModel(access_level=access_level)
    #     print(f'Access level to retur: {access_level}')
    #     return access_level



    def get_access_level_by_pin(self, pin) -> int:
        access_level = 0
 
        try:
            user = self._repository.get_by_pin(pin)
        except PinNotFoundError as e:
            pass
        else:
            access_level = 1
            # print(f'User found: {user.name}')
            # if user.access_level > access_level:
            #     access_level = user.access_level    
        
        # return AccessModel(access_level=access_level)
        print(f'Access level to return: {access_level}')
        return access_level

    
    def get_current_candidate_list(self) -> List[str]:
        print(f"returning candidate list: {self.candidate_list.keys()}")
        return list(self.candidate_list.keys())


    # def detected_beacon(self, beacon:BeaconModel) -> int:
    #     access_level = 0
    #     if beacon.rssi > RSSI_THRESHOLD:
    #         try:
    #             user = self._repository.get_by_uuid(uuid=beacon.uuid)
    #         except BeaconNotFoundError as e:
    #             pass
    #         else:
    #             print(f'User found: {user.name}')
    #             if user.access_level > access_level:
    #                 access_level = user.access_level
    #         finally:
    #             self.candidate_list_lock.acquire()
    #             if beacon.uuid not in self.candidate_list.keys():
    #                 self.candidate_list.update({beacon.uuid:{'rssi':beacon.rssi,'timer':5}})

    #             else:
    #                 self.candidate_list.update({beacon.uuid:{'rssi':beacon.rssi,'timer':5}})
    #             self.candidate_list_lock.release()

    #     else:
    #         self.candidate_list_lock.acquire()
    #         if beacon.uuid in self.candidate_list.keys():
    #             self.candidate_list.pop(beacon.uuid)
    #         self.candidate_list_lock.release()