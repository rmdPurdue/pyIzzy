from enum import StrEnum


class OSCAddresses(StrEnum):
    FOLLOW_LINE_STATE = '/IZZY/FollowLineState'
    FOLLOW_LINE_SPEED = '/IZZY/FollowLineSpeed'
    FOLLOW_LINE_TUNE = '/IZZY/FollowLineTune'
    FOLLOW_LINE_THRESHOLD = '/IZZY/FollowLineThreshold'
    STOP_PROCESSING = '/IZZY/StopProcessing'
    FOLLOW_LINE_RESET_SYSTEM = '/IZZY/FollowLineResetSystem'
    FOLLOW_LINE_SOFT_ESTOP = '/IZZY/FollowLineSoftEStop'
    FOLLOW_LINE_SET_SENSOR_RANGES = '/IZZY/FollowLineSetRanges'
