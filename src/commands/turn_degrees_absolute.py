from wpilib.command.command import Command
import math


class TurnDegreesAbsolute(Command):
    _speed = None
    _degree_threshold = None
    _target_degrees = None

    def __init__(self, robot, degrees_target, speed, threshold, name=None, timeout=15):
        """Constructor"""
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.drivetrain)
        self._target_degrees = degrees_target
        self._speed = speed
        self._degree_threshold = threshold

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        current = self.robot.drivetrain.get_gyro_angle()
        degrees_left = self._target_degrees - current
        direction = self._determine_direction(degrees_left)
        turn_speed = self._speed * direction
        # Set drivetrain using speed and direction
        self.robot.drivetrain.arcade_drive(0.0, turn_speed, False)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        current = self.robot.drivetrain.get_gyro_angle()
        # If abs(target - current) < threshold then return true
        return math.fabs(self._target_degrees - current) <= self._degree_threshold or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        # Stop driving
        self.robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def _determine_direction(self, degrees_left: float) -> float:
        """Based on the degrees left, returns -1 for turn right, returns 1 for turn left"""
        if degrees_left >= 0:
            return 1.0
        else:
            return -1.0
