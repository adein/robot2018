import pytest
from subsystems.drivetrain import Drivetrain
from commands.abort_commands import Abort


@pytest.fixture(scope="function")
def drivetrain_default(robot):
    return Drivetrain(robot, None, '../tests/test_configs/drivetrain_default.ini')


@pytest.fixture(scope="function")
def command_default(robot, drivetrain_default):
    robot.drivetrain = drivetrain_default
    return Abort(robot, None, 15)


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.drivetrain is not None
    assert command_default.name == "Abort"
    assert command_default.timeout == 15


def test_init_full(robot, drivetrain_default):
    robot.drivetrain = drivetrain_default
    abrt = Abort(robot, "CustomAbort", 5)
    assert abrt is not None
    assert abrt.robot is not None
    assert abrt.robot.drivetrain is not None
    assert abrt.name == "CustomAbort"
    assert abrt.timeout == 5


def test_initialize(command_default):
    assert command_default._ran_once is False


def test_execute(robot, hal_data, drivetrain_default):
    robot.drivetrain = drivetrain_default
    abrt = Abort(robot, None, None)
    assert abrt is not None
    abrt.initialize()
    abrt.execute()
    assert hal_data['pwm'][1]['value'] == 0.0
    assert hal_data['pwm'][2]['value'] == 0.0
    assert hal_data['pwm'][3]['value'] == 0.0


@pytest.mark.parametrize("call_execute,finished", [
    (False, False),
    (True, True)
])
def test_is_finished(command_default, call_execute, finished):
    command_default.initialize()
    if call_execute:
        command_default.execute()
    assert command_default.isFinished() is finished


def test_interrupted(command_default):
    pass  # interrupted method is empty


def test_end(command_default):
    pass
