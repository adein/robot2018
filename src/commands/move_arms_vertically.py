from wpilib.command.command import Command

class MoveArmsVertically(Command):

    def __init__(self, robot, speed: float=0.0, name=None, timeout=5):
        super().__init__(name, timeout)
        self.robot = robot
        self._arm_speed: float = speed
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.arm.move_arms_vertically(self._arm_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        if self._arm_speed > 0.0:
            return self.robot.arm.is_raised()
        elif self._arm_speed < 0.0:
            return self.robot.arm.is_lowered()
        else:
            return self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.arm.move_arms_vertically(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()