from enum import Enum


class Directions(Enum):
    """
    An enumeration class for direction values used by the project.
    Extends class Enum from enum.
    """

    FORWARD = 1
    REVERSE = 2
    CLOCKWISE = 3
    COUNTERCLOCKWISE = 4
    CW = 3
    CCW = 4
    UP = 5
    DOWN = 6