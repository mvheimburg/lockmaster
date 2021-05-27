
from pydantic import BaseModel
import gpiozero


from const import(
     COMMAND_PAYLOAD
    ,STATUS_PAYLOAD
)




class Door():
    name: str
    command_topic: str
    state_topic: str
    state: str = "Unkknown"


    def __init__(self, name:str, command_topic: str, state_topic: str, pin: int):
        # self.state = DoorState(name=name, pin=pin, command_topic=command_topic, state_topic=state_topic)
        self.name=name
        self.command_topic=command_topic
        self.state_topic=state_topic
        self.relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)


    def startup(self):
        self.update_status()


    def update_status(self):
        if self.relay.value:
            self.state = STATUS_PAYLOAD.LOCKED
        else:
            self.state = STATUS_PAYLOAD.UNLOCKED


    def unlock(self):
        print(f"Locking door {self.name}")
        self.relay.off()
        self.update_status()
        # self.publish_status()


    def lock(self):
        print(f"Locking door {self.name}")
        self.relay.on()
        self.update_status()
        # self.publish_status()

    def toggle_door(self):
        print(f"Toggling door {self.name}")
        self.relay.toggle()
        self.update_status()
        # self.publish_status()

    def get_state(self):
        return self.state




class DoorDummy():
    name: str
    command_topic: str
    state_topic: str
    state: str = "Unkknown"


    def __init__(self, name:str, command_topic: str, state_topic: str, pin: int):
        # self.state = DoorState(name=name, pin=pin, command_topic=command_topic, state_topic=state_topic)
        self.name=name
        self.command_topic=command_topic
        self.state_topic=state_topic
        # self.relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)


    def startup(self):
        self.update_status()


    def update_status(self):
        pass
        # if self.relay.value:
        #     self.state = STATUS_PAYLOAD.LOCKED
        # else:
        #     self.state = STATUS_PAYLOAD.UNLOCKED


    def unlock(self):
        print(f"Locking door {self.name}")
        # self.relay.off()
        self.update_status()
        # self.publish_status()


    def lock(self):
        print(f"Locking door {self.name}")
        # self.relay.on()
        self.update_status()
        # self.publish_status()

    def toggle_door(self):
        print(f"Toggling door {self.name}")
        # self.relay.toggle()
        self.update_status()
        # self.publish_status()

    def get_state(self):
        return self.state