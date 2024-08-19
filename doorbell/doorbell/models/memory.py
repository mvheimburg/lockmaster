from pydantic import BaseModel


class DoorState(BaseModel):
    # name: str
    locked: bool = False


class GarageState(BaseModel):
    closed: bool = True
    moving: bool = False



class ControlMemory(BaseModel):
    door_states: list[DoorState]
    garage_state: GarageState