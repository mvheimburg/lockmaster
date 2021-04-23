"""Database module."""
from os import environ
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
# import urllib
import logging

# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_mqtt import FastMQTT, MQTTConfig

import paho.mqtt.client as mqtt

from door import Door

from const import(
    COMMAND_PAYLOAD
    ,STATUS_PAYLOAD
)


logger = logging.getLogger(__name__)


class Doormanager:

    def __init__(self, doors_cfg: dict) -> None:
        print(f"doors_cfg: {doors_cfg}")
        self.doors = []
        for door, cfg in  doors_cfg.items():
            print(f"new_door: {door}")
            new_door = Door(name=door, command_topic=cfg['command_topic'], state_topic=cfg['state_topic'], pin=cfg['pin'])
            self.doors.append(new_door)

        self.update_status()

    def update_status(self):
        for door in self.doors:
            door.update_status()


    def subscribe(self, mqttc):
        print(f"subscribing to topics!!!!")
        for door in self.doors:
            print(f"subscribing to topic: {door.command_topic}")
            mqttc.subscribe(door.command_topic, qos=0)

    def publish_status(self, mqttc):
        for door in self.doors:
            if door.state != "Unknown":
                mqttc.publish(door.state_topic, payload=door.state)
    
    
    def mqtt_on_message(self, mqttc, topic, payload):
        print("Doormanager message: ", topic, payload) 
        for door in self.doors:
            if topic == door.command_topic:
                if payload == COMMAND_PAYLOAD.LOCK:
                    print(f"Doormanager message: Locking door {door}") 
                    door.lock()
                elif payload == COMMAND_PAYLOAD.UNLOCK:
                    print(f"Doormanager message: Unlocking door {door}") 
                    door.unlock()

        self.publish_status(mqttc)

    # def publish_status(self):
    #     for door in self.doors:
    #         if door.state != "Unknown":
    #             self.mqtt.publish(door.state_topic, payload=door.state)



    # @contextmanager
    # def session(self) -> Callable[..., AbstractContextManager[Session]]:
    #     session: Session = self._session_factory()
    #     try:
    #         yield session
    #     except Exception:
    #         logger.exception('Session rollback because of exception')
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()