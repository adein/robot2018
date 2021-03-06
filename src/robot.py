from wpilib import command
import wpilib

from commands.autonomous import StartingPosition, CrossLine, AutoPlaceCube, FieldConfig
from commands.do_nothing import DoNothing
from oi import OI
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.arm import Arm
from subsystems.feeder import Feeder
from subsystems.winch import Winch


class MyRobot(wpilib.IterativeRobot):
    oi = None
    drivetrain = None
    elevator = None
    arm = None
    feeder = None
    winch = None
    autonomous_command = None

    def autonomousInit(self):
        # Schedule the autonomous command
        self.drivetrain.reset_gyro_angle()

        # Determine starting position and filed config
        # starting_position = StartingPosition(self.oi.get_position())
        # game_message = wpilib.DriverStation.getGameSpecificMessage()
        # field_config = FieldConfig[game_message]
        #
        # auto_choice = self.oi.get_auto_choice()
        #
        # if auto_choice == 1:
        #     self.autonomous_command = CrossLine(self)
        # elif auto_choice == 2:
        #     self.autonomous_command = AutoPlaceCube(self, field_config, starting_position)
        # else:
        #     self.autonomous_command = DoNothing(self)
        self.autonomous_command = CrossLine(self)
        self.autonomous_command.start()

    def testInit(self):
        pass

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()
        self.teleopInitialized = True

    def disabledInit(self):
        self.disabledInitialized = True

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drivetrain = Drivetrain(self)
        self.elevator = Elevator(self)
        self.arm = Arm(self)
        self.feeder = Feeder(self)
        self.winch = Winch(self)
        self.oi.setup_button_bindings()
        # wpilib.CameraServer.launch()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        command.Scheduler.getInstance().run()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        command.Scheduler.getInstance().run()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
