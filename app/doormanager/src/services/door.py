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
if build_type == 'staging':
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
            if build_type == 'staging':
                new_door = Door(name=door, command_topic=cfg['command_topic'], state_topic=cfg['state_topic'], relay=gpiozero.OutputDevice(cfg['pin'], active_high=False, initial_value=False))
            else:
                new_door = Door(name=door, command_topic=cfg['command_topic'], state_topic=cfg['state_topic'], pin=cfg['pin'])
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
            print(f"subscribing to topic: {door.command_topic}")
            self.mqttc.subscribe(door.command_topic, qos=0)

    def publish_status(self):
        for door in self.doors:
            if door.state != "Unknown":
                self.mqttc.publish(door.state_topic, payload=door.state)
    
    
    def mqtt_on_message(self, topic, payload):
        print("Doormanager message: ", topic, payload) 
        for door in self.doors:
            if topic == door.command_topic:
                if payload == COMMAND_PAYLOAD.LOCK:
                    print(f"Doormanager message: Locking door {door}") 
                    door.lock()
                elif payload == COMMAND_PAYLOAD.UNLOCK:
                    print(f"Doormanager message: Unlocking door {door}") 
                    door.unlock()

        self.publish_status()


    def publish_status_cyclic(self):
        if self.mqttc is not None:
            self.publish_status()
            sleep(300)