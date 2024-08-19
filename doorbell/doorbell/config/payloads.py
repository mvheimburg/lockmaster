from enum import StrEnum, auto


class PARTYMODE():
    class COMMAND(StrEnum):
        NORMAL = auto()
        HALLOWEEN = auto()
        CHRISTMAS = auto()

    class STATE(StrEnum):
        NORMAL = auto()
        HALLOWEEN = auto()
        CHRISTMAS = auto()


class BELL():
    class COMMAND(StrEnum):
        DO = auto()


class DOORLOCK():
    class COMMAND(StrEnum):
        LOCK = auto()
        UNLOCK = auto()

    class STATE(StrEnum):
        LOCKED = auto()
        UNLOCKED = auto()
        UNKNOWN = auto()


class GARAGE():
    class COMMAND(StrEnum):
        OPEN = auto()
        CLOSE = auto()
        STOP = auto()

    class STATE(StrEnum):
        OPEN = auto()
        OPENING = auto()
        CLOSED = auto()
        CLOSING = auto()
