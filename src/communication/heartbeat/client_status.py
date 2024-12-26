from enum import Enum


class IZZYStatus(Enum):
    AVAILABLE = 1
    MOVING = 2
    FOLLOWING = 3
    ESTOP = 4
    BROKEN = 5
    UNVERIFIED = 6
