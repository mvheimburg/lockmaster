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

logger = logging.getLogger(__name__)


class Doormanager:

    def __init__(self, doors_cfg: dict) -> None:
        # host = environ.get('MQTT_HOST', 'mqtt://localhost')
        # port = environ.get('MQTT_PORT', '1883')
        # username = environ.get('MQTT_USERNAME', None)
        # password = environ.get('MQTT_PASSWORD', None)

        self._mqttc = mqtt.Client('doormanager')
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe

        self.doors = []
        for door, cfg in  doors_cfg.items():
            new_door = Door(name=door, command_topic=cfg.command_topic, state_topic=cfg.state_topic, pin=cfg.pin)
            self.doors.append(new_door)


    def connect_to_broker(self) -> None:
        broker = environ.get('MQTT_HOST', 'mqtt://localhost')
        port = environ.get('MQTT_PORT', '1883')
        username = environ.get('MQTT_USERNAME', None)
        password = environ.get('MQTT_PASSWORD', None)
        logger.debug(f"Username: {username}, Password: {password}")
        # broker_parsed = urllib.parse.urlparse(host+':'+port)
        self._mqttc.username_pw_set(username, password=password)
        self._mqttc.connect(broker, port, keepalive=60)


    def subsribe(self) -> None:
        for door in self.doors:
            logger.debug(f"subscribing to topic: {door.command_topic}")
            self._mqttc.subscribe(door.command_topic, qos=0)


    def update_status(self):
        for door in self.doors:
            door.update_status()


    def publish_status(self):
        for door in self.doors:
            if door.state != "Unknown":
                self.mqtt.publish(door.state_topic, payload=door.state)


    def mqtt_on_message(self, topic, payload):
        logger.debug("Doormanager message: ", topic, payload) 
        for door in self.doors:
            if topic == door.command_topic:
                if payload == COMMAND_PAYLOAD.LOCK:
                    logger.debug(f"Doormanager message: Locking door {door}") 
                    door.lock()
                elif payload == COMMAND_PAYLOAD.UNLOCK:
                    logger.debug(f"Doormanager message: Unlocking door {door}") 
                    door.unlock()

        self.publish_status()


    def mqtt_on_publish(self, mqttc, obj, mid):
        logger.debug("mid: "+str(mid))

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.debug("Subscribed: "+str(mid)+" "+str(granted_qos))

    def mqtt_on_log(self, mqttc, obj, level, string):
        logger.debug(string)

    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        logger.debug("rc: "+str(rc))
        logger.debug(f"flag: {flags}")
        self.update_status()
        self.publish_status()

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