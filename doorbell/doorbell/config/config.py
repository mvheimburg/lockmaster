from __future__ import annotations

from pydantic import BaseModel

from doorbell.models.models import MqttTopic

class Door(BaseModel):
    id: str
    name: str
    topic: MqttTopic | None = None
    state: str = "Unknown"

    def get_state(self):
        return self.state

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic.command=f"door/{self.id}/cmd"
        self.topic.state=f"door/{self.id}/state"

    def unlock(self):
        pass

    def lock(self):
        pass

class DoorsConfig(BaseModel):
    doors: list[Door]

    def get_name_by_id(self, id: str):
        for door in self.doors:
            if door.id == id:
                return door.name

        return None

    def get_by_name(self, name: str):
        for door in self.doors:
            if door.name == name:
                return door
                
        return None

    def get_by_state_topic(self, topic: str):
        for door in self.doors:
            if door.topic.state == topic:
                return door

        return None