from movement.pid import PID
from movement.drive_movement import DriveMovement


class LineFollower(DriveMovement):
    following_stopped = False
    moving = False
    new_speed = 0
    def pid_setup(self, sensors, kp = 1, ki = 0, kd = 0):
        self.pid = PID(sensors, kp, ki, kd)

    def follow_line(self):
        if self.following_stopped:
            pass
        else:
            self.pid.adjust_error_analog()
            self.pid.calculate_PID()
            self.set_speed(self.new_speed)
            self.increase_turn_angle((-self.pid.get_error_angle() + 0.5), 90)

    def is_line_detected(self):
        return self.pid.is_line_detected()

    def stop_following(self):
        self.following_stopped = True

    def start_following(self):
        self.following_stopped = False

    def get_following_state(self):
        return not self.following_stopped

    def update_speed(self, speed):
        self.new_speed = speed

    def get_moving_state(self):
        return self.moving

    def set_moving_state(self, state):
        self.moving = state

    def tune_pid_loop(self, kp, ki, kd):
        self.pid.set_kp(kp)
        self.pid.set_ki(ki)
        self.pid.set_kd(kd)

    def get_pid_value(self):
        return self.pid.get_pid_value()

    def reset_system(self):
        self.pid.reset()
        self.reset_drive()

    def stop(self):
        self.move(0)