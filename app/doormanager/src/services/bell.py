"""Database module."""
from os import environ
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging


from const import(
    COMMAND_PAYLOAD
    ,STATUS_PAYLOAD
)
            

logger = logging.getLogger(__name__)


class BellService:

    mqttc = None

    def __init__(self, bell_cfg: dict) -> None:
        print(f"bell_cfg: {bell_cfg}")
        self.cfg=bell_cfg

    def set_mqttc(self, mqttc):
        self.mqttc = mqttc

    def ring_doorbell(self):
        print(f"Ringing that mqtt bell!") 
        self.mqttc.publish(self.cfg['command_topic'], payload=self.cfg['command'])