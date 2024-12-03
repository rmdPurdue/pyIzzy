import math

class DriveMovement():
    current_speed = 0
    current_angle = 0
    current_position = {"x": 0, "y": 0, "z": 0}
    def __init__(self, x = 0, y = 0, z = 0):
        self.home = {"x": x, "y": y, "z": z}
        self.current_position = {"x": x, "y": y, "z": z}
        self.angle = 0

    def setup(self, wheel_radius, system_radius, encoder_resolution, motor_ratio):
        self.wheel_radius = wheel_radius
        self.system_radius = system_radius
        self.encoder_resolution = encoder_resolution
        self.motor_ratio = motor_ratio

    def set_channels(self, drive_channel, turn_channel):
        self.drive_channel = drive_channel
        self.turn_channel = turn_channel
        self.drive_channel.start()
        self.turn_channel.start()
        self.drive_channel.units("1 rotation = 512 lines")

    def get_drive_position(self):
        return self.drive_channel.getP()

    def get_drive_speed(self):
        return self.drive_channel.getS()

    def get_coordinates(self):
        return self.current_position

    def get_angle(self):
        return self.angle

    def update_coordinates(self, coords):
        self.current_position = coords

    def update_angle(self, angle):
        self.current_angle = angle

    def turn(self, target_angle, speed = 0):
        angle = self.system_radius * 360 * self.encoder_resolution
        if target_angle == 0: angle = 0
        else: target_angle = angle / (target_angle * self.wheel_radius)
        self.turn_channel.P(target_angle, speed)
        self.current_angle = target_angle

    def increase_turn_angle(self, angle_increase, speed = 0):
        angle = self.system_radius * 360 * self.encoder_resolution
        if angle_increase == 0:
            target_angle = self.current_angle
        elif angle_increase > 0:
            target_angle = angle / ((self.current_angle + angle_increase) * self.wheel_radius)
        else:
            target_angle = angle / ((self.current_angle - angle_increase) * self.wheel_radius)
        self.turn_channel.P(target_angle, speed)
        self.current_angle = target_angle

    def set_speed(self, speed = 0):
        if self.current_speed == speed: pass
        else:
            self.current_speed = speed
            self.drive_channel.S(speed)

    def increase_speed(self, speed = 0):
        if self.current_speed == speed: pass
        else:
            self.current_speed += speed
            self.drive_channel.S(self.current_speed)

    def move(self, distance, speed = 0):
        self.drive_channel.P(distance)
        self.drive_channel.S(speed)
    def soft_estop(self):
        self.drive_channel.power_down()
        self.turn_channel.power_down()
        self.current_speed = 0

    def simple_move(self, target_position, angle_direction):
        if self.position["x"] == target_position["x"] and self.position["y"] != target_position["y"]:
            cw_angle = 90
            ccw_angle = 270
        else:
            tan_angle = math.tan(self.position["y"] / (self.position["x"] * 360 / (2 * math.pi)))
            if target_position["x"] > self.position["x"]:
                if target_position["y"] > self.position["y"]:
                    ccw_angle = tan_angle
                    cw_angle = 360 - tan_angle
                else:
                    ccw_angle = 360 - tan_angle
                    cw_angle = tan_angle
            else:
                if target_position["y"] > self.position["y"]:
                    ccw_angle = 180 - tan_angle
                    cw_angle = 180 + tan_angle
                else:
                    ccw_angle = 180 + tan_angle
                    cw_angle = 180 - tan_angle
        if angle_direction == 1:
            self.turn(-cw_angle)
        elif angle_direction == -1:
            self.turn(ccw_angle)
        else:
            if abs(self.angle - ccw_angle) > abs(self.angle - cw_angle):
                self.turn(-cw_angle)
            else:
                self.turn(ccw_angle)
        distance = math.sqrt(pow(self.position["x"], 2) + pow(self.position["y"], 2))
        self.move(distance, 10)
        self.update_coordinates(target_position)

    def reset_drive(self):
        self.drive_channel.power_down()
        self.turn_channel.power_down()
        self.drive_channel.start()
        self.turn_channel.start()
        wheel_circumference = math.pi * self.wheel_radius * 2
        lines_for_drive = self.encoder_resolution * self.motor_ratio
        lines_for_turn = math.pi * (self.system_radius * 2) / wheel_circumference * lines_for_drive
        drive_message = f"{wheel_circumference + 0.5} mm = {lines_for_drive + 0.5} lines"
        self.drive_channel.units(drive_message)
        turn_message = f"360 degrees = {lines_for_turn + 0.5} lines"
        self.turn_channel.units(turn_message)