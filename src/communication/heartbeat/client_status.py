from enum import Enum


class IZZYStatus(Enum):
    MISSING = 1
    AVAILABLE = 2
    MOVING = 3
    ESTOP = 4
    BROKEN = 5
    UNVERIFIED = 6
