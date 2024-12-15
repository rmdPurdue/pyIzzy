from enum import StrEnum


class OSCAddresses(StrEnum):
    """
    An enumeration class for OSC address patterns used by the project.
    Extends class StrEnum from enum.
    """

    FOLLOW_LINE_STATE = '/IZZY/FollowLineState'
    FOLLOW_LINE_SPEED = '/IZZY/FollowLineSpeed'
    FOLLOW_LINE_TUNE = '/IZZY/FollowLineTune'
    FOLLOW_LINE_THRESHOLD = '/IZZY/FollowLineThreshold'
    STOP_PROCESSING = '/IZZY/StopProcessing'
    FOLLOW_LINE_RESET_SYSTEM = '/IZZY/FollowLineResetSystem'
    FOLLOW_LINE_SOFT_ESTOP = '/IZZY/FollowLineSoftEStop'
    FOLLOW_LINE_SET_SENSOR_RANGES = '/IZZY/FollowLineSetRanges'
