"""Database module."""
from os import environ
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging
from threading import Thread
from time import sleep


from const import(
    COMMAND_PAYLOAD
    ,STATUS_PAYLOAD
)


build_type = environ.get('BUILD_TYPE', None)
print(f"build_type: {build_type}")
if build_type == 'release':
    import gpiozero
    from models import Door
else:
    from models import DoorDummy as Door
            


logger = logging.getLogger(__name__)


class DoorService:

    doors = []
    mqttc = None

    def __init__(self, doors_cfg: dict) -> None:
        print(f"doors_cfg: {doors_cfg}")

        for door, cfg in  doors_cfg.items():
            print(f"new_door: {door}")
            if build_type == 'release':
                new_door = Door(name=door, relay=gpiozero.OutputDevice(cfg['pin'], active_high=False, initial_value=False))
            else:
                new_door = Door(name=door, pin=cfg['pin'])
            # new_door.set_relay()
            self.doors.append(new_door)

        self.update_status()

        self.status_thread = Thread(target=self.publish_status_cyclic, daemon=True)
        self.status_thread.start()

    def update_status(self):
        for door in self.doors:
            door.update_status()

    def set_mqttc(self, mqttc):
        self.mqttc = mqttc

    def subscribe(self):
        print(f"subscribing to topics!!!!")
        for door in self.doors:
            print(f"subscribing to topic: {door.topic.command}")
            self.mqttc.subscribe(door.topic.command, qos=0)

    def publish_status(self):
        for door in self.doors:
            if door.state != "Unknown":
                self.mqttc.publish(door.topic.state, payload=door.state)
    
    
    def mqtt_on_message(self, topic, payload):
        for door in self.doors:
            if topic == door.topic.command:
                print("Doormanager message: ", topic, payload) 
                if payload == COMMAND_PAYLOAD.LOCK:
                    print(f"Doormanager message: Locking door {door}") 
                    door.lock()
                elif payload == COMMAND_PAYLOAD.UNLOCK:
                    print(f"Doormanager message: Unlocking door {door}") 
                    door.unlock()

        self.publish_status()


    def toggle_door(self, door_name:str):
        for door in self.doors:
            if door.name == door_name:
                door.toggle_door()
                return door.state


    def unlock_door(self, door_name:str):
        for door in self.doors:
            if door.name == door_name:
                door.unlock()
                return door.state

    def lock_door(self, door_name:str):
        for door in self.doors:
            if door.name == door_name:
                door.lock()
                return door.state
    

    def get_door_state(self, door_name:str):
        for door in self.doors:
            if door.name == door_name:
                return door.state
                
    

    async def async_get_door_state(self, door_name:str):
        for door in self.doors:
            if door.name == door_name:
                return door.state

    def publish_status_cyclic(self):
        if self.mqttc is not None:
            self.publish_status()
            sleep(300)