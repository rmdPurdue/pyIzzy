from enum import Enum


class Ports(Enum):
    """
    An enumeration class for network ports used by the project.
    Extends class Enum from enum.
    """

    UDP_SEND_PORT = 9000
    UDP_RECEIVE_PORT = 9001
    OSC_SEND_PORT = 8000
    OSC_RECEIVE_PORT = 8001