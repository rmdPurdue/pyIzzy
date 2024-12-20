from enum import Enum


class MessageType(Enum):
    HELLO = 0x01
    HERE = 0x02
    SETUP_ERROR = 0x03
    MOVING = 0x04
    BROKEN = 0x05
    OSC_COM_ERROR = 0x06
    NOT_VALID = 0x00
