from enum import StrEnum


class OSCAddresses(StrEnum):
    FOLLOW_LINE_STATE = '/IZZY/FollowLineState'
    FOLLOW_LINE_SPEED = '/IZZY/FollowLineSpeed'
    FOLLOW_LINE_TUNE = '/IZZY/FollowLineTune'
    FOLLOW_LINE_THRESHOLD = '/IZZY/FollowLineThreshold'
    STOP_PROCESSING = '/IZZY/StopProcessing'
    RESET_SYSTEM = '/IZZY/ResetSystem'
    FOLLOW_LINE_SOFT_ESTOP = '/IZZY/SoftEStop'
    SET_SENSOR_RANGES = '/IZZY/SetRanges'