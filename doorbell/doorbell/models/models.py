from __future__ import annotations
import yaml
# from typing import Callable
from pathlib import Path
import gpiozero
from pydantic import BaseModel, ConfigDict, model_validator
from doorbell import config
from doorbell.config.common import COMMON, BUILD_TYPE
from doorbell.config.payloads import DOORLOCK
from paho.mqtt.client import MQTTMessage

class MqttTopic(BaseModel):
    command: str
    state: str


class MqttTopics(BaseModel):
    bell: MqttTopic
    garage: MqttTopic
    mode: MqttTopic
    state: MqttTopic

    @classmethod
    def load(cls) -> MqttTopics:
        p = Path(config.__file__).parent
        cfg = p / "topics.yaml"
        with cfg.open('r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        c = cls(**data)
        return c


# class APIConfig(BaseModel):
#     url: str


# class BellConfig(BaseModel):
#     command_topic: str
class AccessModel(BaseModel):
    name: str | None = None
    access_level: int = 0
    # login_state: LoginState = LoginState.OUT



class Subscription(BaseModel):
    """Represents a MQTT subscription.

    Attributes
    ----------
        topic : str
            The topic name.
        qos : int
            The quality of service(QoS) level: 0, 1 and 2. Refer to the MQTT spec for details.
    """

    topic: str
    qos: int
    # callback: Callable[[MQTTMessage], None]



class UserModel(BaseModel):
    name:str
    uuid:Optional[str]
    pin:Optional[int]
    end:Optional[dt.datetime]
    access_level:int


class Door(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    state: DOORLOCK.STATE = "Unknown"
    topic: MqttTopic | None
    relay: gpiozero.OutputDevice | int

    @model_validator(mode="after")
    def relay_mode(self):
        match COMMON.build_type:
            case BUILD_TYPE.RELEASE:
                if isinstance(self.relay, int):
                    self.relay = gpiozero.OutputDevice(self.relay,
                                                      active_high=False,
                                                      initial_value=False)
                self.update_status()
            case _:
                pass

        self.topic = MqttTopic(command=f"door/{self.name}/cmd",
                               state=f"door/{self.name}/state")

    # def startup(self):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.topic.command=f"door/{self.name}/cmd"
    #     self.topic.state=f"door/{self.name}/state"

    def update_status(self):
        if self.relay.value:
            self.state = DOORLOCK.STATE.UNLOCKED
        else:
            self.state = DOORLOCK.STATE.LOCKED

    def unlock(self):
        print(f"Unlocking door {self.name}")
        self.relay.on()
        self.update_status()

    def lock(self):
        print(f"Locking door {self.name}")
        self.relay.off()
        self.update_status()

    def toggle_door(self):
        print(f"Toggling door {self.name}")
        self.relay.toggle()
        self.update_status()


    def get_state(self):
        return self.state




# class DoorDummy(BaseModel):
#     name: str
#     state: str = "Unknown"
#     topic: MqttTopics = MqttTopics()
#     relay: int



#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.topic.command=f"door/{self.name}/cmd"
#         self.topic.state=f"door/{self.name}/state"


#     def startup(self):
#         self.update_status()


#     def update_status(self):
#         pass

#     def unlock(self):
#         print(f"Locking door {self.name}")
#         self.update_status()


#     def lock(self):
#         print(f"Locking door {self.name}")
#         self.update_status()

#     def toggle_door(self):
#         print(f"Toggling door {self.name}")
#         self.update_status()

#     def get_state(self):
#         return self.state