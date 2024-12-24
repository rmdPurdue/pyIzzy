from enum import Enum


class MessageType(Enum):
    HELLO = 0x01
    HERE = 0x02
    SETUP_ERROR = 0x03
    MOVING = 0x04
    FOLLOWING = 0x05
    ESTOP = 0x06
    OSC_COM_ERROR = 0x07
    NOT_VALID = 0x08
