from enum import StrEnum


class OSCAddresses(StrEnum):
    """
    An enumeration class for OSC address patterns used by the project.
    Extends class StrEnum from enum.
    """
    IZZY = "/izzy"
    MANUAL = "/izzy/manual_control"
    FOLLOW_LINE = "/izzy/line_following"
    AVOID_OBSTACLE = "/izzy/obstacle_avoidance"
    TRACK_LOCATION = "/izzy/location_tracking"

    SOFT_STOP = "/soft_stop"  # Global method {none}

    # methods for MANUAL, FOLLOW_LINE, AVOID_OBSTACLE, TRACK_LOCATION
    ENABLE = "/enable"  # {bool}

    # methods for MANUAL
    RESET = "/reset"  # {none}
    MOVE = "/move"  # {distance: int} {optional speed: int}
    ACCEL_TO = "/accelto"  # {speed: int}
    ACCEL_BY = "/accelby"  # {speed: int}
    TURN_TO = "/turnto"  # {angle: int} {optional speed: int}
    TURN = "/turn"  # {angle: int} {optional speed: int}

    # methods for FOLLOW_LINE
    SPEED = "/speed"  # {speed: int}
    TUNE = "/tune"  # {kp: float} {ki: float} {kd: float}

    # address patterns for FOLLOW_LINE
    SENSOR1 = "/sensor1"
    SENSOR2 = "/sensor2"

    # address patterns for SENSOR
    THRESHOLD = "/threshold"

    # methods for THRESHOLD
    MIN = "/min"  # {minimum: int}
    MAX = "/max"  # {maximum: int}