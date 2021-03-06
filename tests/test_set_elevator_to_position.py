import pytest
from commands.set_elevator_to_position import SetElevatorToPosition
from subsystems.elevator import Elevator


"""
hal_data['pwm'] looks like this:
[{
    'zero_latch': False,
    'initialized': False,
    'raw_value': 0,
    'value': 0,
    'period_scale': None,
    'type': None
}, {
    'zero_latch': True,
    'initialized': True,
    'raw_value': 1011,
    'value': 0.0,
    'period_scale': 0,
    'type': 'talon'
},...]
"""


@pytest.fixture(scope="function")
def elevator_default(robot):
    return Elevator(robot, None, '../tests/test_configs/elevator_encoder_bounds.ini')


@pytest.fixture(scope="function")
def command_default(robot, elevator_default):
    robot.elevator = elevator_default
    return SetElevatorToPosition(robot, 1.0, 0, 0, None, 15)


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def update_encoder(hal_data, command):
    current_0 = hal_data['encoder'][0]['count']
    counts_left = command._encoder_target - current_0
    if counts_left >= 0:
        hal_data['encoder'][0]['count'] += 1
    else:
        hal_data['encoder'][0]['count'] -= 1


def test_init_default(command_default):
    assert command_default is not None
    assert command_default.robot is not None
    assert command_default.robot.elevator is not None
    assert command_default.name == "SetElevatorToPosition"
    assert command_default.timeout == 15
    assert command_default._speed == 1.0
    assert command_default._encoder_target == 0
    assert command_default._encoder_threshold == 0


@pytest.mark.parametrize("initial_count,position,speed,ex_speed", [
    (60, 100, 0.2, 0.2),
    (100, 200, 1.0, 1.0),
    (200, 500, 0.5, 0.5),
    (500, 200, 0.5, -0.5),
    (200, 100, 1.0, -1.0),
    (100, 60, 0.2, -0.2),
])
def test_command_full(robot, elevator_default, hal_data, initial_count, position, speed, ex_speed):
    robot.elevator = elevator_default
    letp = SetElevatorToPosition(robot, speed, position, 5, "SetElevatorToPosition", 15)
    hal_data['encoder'][0]['count'] = initial_count
    letp.initialize()
    while not letp.isFinished():
        letp.execute()
        update_encoder(hal_data, letp)
        assert hal_data['pwm'][3]['value'] == ex_speed
    letp.end()
    assert isclose(hal_data['encoder'][0]['count'], position, 1)
