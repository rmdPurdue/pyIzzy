import math


class PID:
    pid_value = 0
    error = 0
    error_sum = 0
    previous_error = 0

    def __init__(self, sensors, kp = 1, ki = 0, kd = 0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sensors = sensors

    def get_kp(self):
        return self.kp

    def get_ki(self):
        return self.ki

    def get_kd(self):
        return self.kd

    def set_kp(self, kp):
        self.kp = kp

    def set_ki(self, ki):
        self.ki = ki

    def set_kd(self, kd):
        self.kd = kd

    def get_pid_value(self):
        return self.pid_value

    def is_line_detected(self):
        detected = False
        for sensor in self.sensors:
            detected = detected or sensor.get_state()
        return detected

    def adjust_error(self):
        if self.sensors[0].get_state() and self.sensors[1].get_state(): self.error = 0
        elif not self.sensors[0].get_state() and not self.sensors[1].get_state(): self.error = 0
        elif self.sensors[0].get_state() and not self.sensors[1].get_state():
           self.error = -self.sensors[2] + self.sensors[3]
        elif not self.sensors[0].get_state() and self.sensors[1].get_state():
            self.error = self.sensors[2] + self.sensors[3]

    def adjust_error_analog(self):
        self.error -= self.sensors[0].get_slope() * self.sensors[0].get_reading()
        self.error += self.sensors[1].get_slope() * self.sensors[1].get_reading()

    def calculate_pid(self):
        proportional = self.kp * self.error
        integral = self.ki * self.error_sum
        derivative = self.kd * (self.error - self.previous_error)
        self.pid_value = proportional + integral + derivative
        self.error_sum += self.error
        self.previous_error = self.error
        return self.pid_value

    def get_error_angle(self):
        return -((math.atan(self.pid_value / self.sensors[4])) * 180) / math.pi

    def reset(self):
        self.error = 0
        self.error_sum = 0
        self.previous_error = 0
        self.kp = 1
        self.ki = 0
        self.kd = 0
        self.pid_value = 0
