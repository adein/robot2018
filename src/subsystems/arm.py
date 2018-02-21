import configparser
from configparser import ConfigParser
from commands.move_arms_vertically import MoveArmsVertically
from wpilib.command.subsystem import Subsystem
from wpilib.digitalinput import DigitalInput
from wpilib.talon import Talon


class Arm(Subsystem):
    _vertical_motor_section: str = "ArmVerticalMotor"
    _lateral_motor_section: str = "ArmLateralMotor"
    _general_section: str = "ArmGeneral"
    _raised_switch_section: str = "ArmRaisedSwitch"
    _lowered_switch_section: str = "ArmLoweredSwitch"
    _closed_switch_section: str = "ArmClosedSwitch"
    _open_switch_section: str = "ArmOpenSwitch"

    _enabled_key: str = "ENABLED"
    _channel_key: str = "CHANNEL"
    _inverted_key: str = "INVERTED"
    _move_speed_scale_key: str = "ARM_MOVE_SPEED"

    _vertical_motor_channel: int = None
    _lateral_motor_channel: int = None
    _raised_switch_channel: int = None
    _lowered_switch_channel: int = None
    _closed_switch_channel: int = None
    _open_switch_channel: int = None

    _vertical_motor_inverted: bool = False
    _lateral_motor_inverted: bool = False

    _robot = None
    _config: ConfigParser = None
    _vertical_motor: Talon = None
    _lateral_motor: Talon = None
    _raised_switch: DigitalInput = None
    _lowered_switch: DigitalInput = None
    _closed_switch: DigitalInput = None
    _opened_switch: DigitalInput = None

    _move_speed_scale: float = 1.0

    def __init__(self, robot, name=None, configfile: str='/home/lvuser/configs/subsystems.ini'):
        super().__init__(name=name)
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self.init_components()

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveArmsVertically(self._robot))

    def is_raised(self) -> bool:
        if self._raised_switch:
            return self._raised_switch.get()
        else:
            return False

    def is_lowered(self) -> bool:
        if self._lowered_switch:
            return self._lowered_switch.get()
        else:
            return False

    def is_closed(self) -> bool:
        if self._closed_switch:
            return self._closed_switch.get()
        else:
            return False

    def is_open(self) -> bool:
        if self._opened_switch:
            return self._opened_switch.get()
        else:
            return False

    def move_arm_laterally(self, speed: float):
        if self._lateral_motor:
            if speed < 0.0 and not self.is_closed():
                self._lateral_motor.set(speed * self._move_speed_scale)
            elif speed > 0.0 and not self.is_open():
                self._lateral_motor.set(speed * self._move_speed_scale)
            else:
                self._lateral_motor.set(0.0)


    def move_arms_vertically(self, speed: float):
        if self._vertical_motor:
            if speed > 0.0 and not self.is_raised():
                self._vertical_motor.set(speed * self._move_speed_scale)
            elif speed < 0.0 and not self.is_lowered():
                self._vertical_motor.set(speed * self._move_speed_scale)
            else:
                self._lateral_motor.set(0.0)

    def init_components(self):
        if self._config.getfloat(self._general_section, self._move_speed_scale_key) != None:
            self._move_speed_scale = self._config.getfloat(self._general_section, self._move_speed_scale_key)

        if self._config.getboolean(Arm._lateral_motor_section, Arm._enabled_key):
            self._lateral_motor_channel = self._config.getint(self._lateral_motor_section, self._channel_key)
            self._lateral_motor_inverted = self._config.getboolean(self._lateral_motor_section, self._inverted_key)

        if self._config.getboolean(Arm._vertical_motor_section, Arm._enabled_key):
            self._vertical_motor_channel = self._config.getint(self._vertical_motor_section, self._channel_key)
            self._vertical_motor_inverted = self._config.getboolean(self._vertical_motor_section, self._inverted_key)

        if self._vertical_motor_channel:
            self._vertical_motor = Talon(self._vertical_motor_channel)
            if self._vertical_motor:
                self._vertical_motor.setInverted(self._vertical_motor_inverted)

        if self._lateral_motor_channel:
            self._lateral_motor = Talon(self._lateral_motor_channel)
            if self._lateral_motor:
                self._lateral_motor.setInverted(self._lateral_motor_inverted)

        if self._config.getboolean(Arm._raised_switch_section, Arm._enabled_key):
            self._raised_switch_channel = self._config.getint(self._raised_switch_section, self._channel_key)
            if self._raised_switch_channel:
                self._raised_switch = DigitalInput(self._raised_switch_channel)

        if self._config.getboolean(Arm._lowered_switch_section, Arm._enabled_key):
            self._lowered_switch_channel = self._config.getint(self._lowered_switch_section, self._channel_key)
            if self._lowered_switch_channel:
                self._lowered_switch = DigitalInput(self._lowered_switch_channel)

        if self._config.getboolean(Arm._closed_switch_section, Arm._enabled_key):
            self._closed_switch_channel = self._config.getint(self._closed_switch_section, self._channel_key)
            if self._closed_switch_channel:
                self._closed_switch = DigitalInput(self._closed_switch_channel)

        if self._config.getboolean(Arm._open_switch_section, Arm._enabled_key):
            self._open_switch_channel = self._config.getint(self._open_switch_section, self._channel_key)
            if self._open_switch_channel:
                self._opened_switch = DigitalInput(self._open_switch_channel)
