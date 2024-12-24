from enum import Enum


class IZZYStatus(Enum):
    MISSING = 1
    AVAILABLE = 2
    MOVING = 3
    FOLLOWING = 4
    ESTOP = 5
    BROKEN = 6
    UNVERIFIED = 7
