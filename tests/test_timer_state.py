import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.timer_state import TimerState


@pytest.fixture(scope='function')
def timer():
    timer = TimerState()
    yield timer


# Positive tests
@pytest.mark.timer
@pytest.mark.parametrize('pomodoro_time, expected_result', [
    (1500, 1500),
    (1800, 1800),
    (2100, 2100),
])
def test_timer_set_pomodoro_time_positive(timer, pomodoro_time, expected_result):
    timer.pomodoro_time = pomodoro_time
    assert timer.pomodoro_time == expected_result



@pytest.mark.timer
@pytest.mark.parametrize('is_pomodoro, cycle_count, expected_name', [
    (True, 1, 'Pomodoro'),
    (False, 1, 'Short break'),
    (False, 0, 'Long break'),
])
def test_timer_get_period_name_positive(timer, is_pomodoro, cycle_count, expected_name):
    timer.is_pomodoro_mode = is_pomodoro
    timer.cycle_count = cycle_count
    assert timer.get_current_period_name() == expected_name


@pytest.mark.timer
@pytest.mark.parametrize('start_mode, expected_transition', [
    (True, 'short_break'),
    (False, 'pomodoro'),
])
def test_timer_transitions_positive(timer, start_mode, expected_transition):
    timer.is_pomodoro_mode = start_mode
    timer.cycle_count = 1

    result = timer.next_period()
    assert result == expected_transition


@pytest.mark.timer
def test_timer_reset_positive(timer):
    timer.is_pomodoro_mode = False
    timer.cycle_count = 3
    timer.current_time = 100
    timer.is_running = True

    timer.reset_to_pomodoro()

    assert timer.is_pomodoro_mode is True
    assert timer.cycle_count == 0
    assert timer.current_time == timer.pomodoro_time
    assert timer.is_running is False


# Border tests
@pytest.mark.timer
@pytest.mark.parametrize('time_value, expected_result', [
    (0, 0),
    (1, 1),
    (86400, 86400)
])
def test_timer_set_time_border(timer, time_value, expected_result):
    timer.pomodoro_time = time_value
    assert timer.pomodoro_time == expected_result


@pytest.mark.timer
@pytest.mark.parametrize('cycle_count, expected_period', [
    (3, 'short_break'),
    (4, 'long_break'),
])
def test_timer_cycle_transitions_border(timer, cycle_count, expected_period):
    timer.cycle_count = cycle_count - 1
    timer.is_pomodoro_mode = True
    result = timer.next_period()
    assert result == expected_period


@pytest.mark.timer
@pytest.mark.parametrize('mode, cycle, expected_time_source', [
    (True, 1, 'pomodoro_time'),
    (False, 1, 'short_break_time'),
    (False, 0, 'long_break_time'),
])
def test_timer_get_initial_time_border(timer, mode, cycle, expected_time_source):
    timer.is_pomodoro_mode = mode
    timer.cycle_count = cycle

    result = timer.get_initial_time()
    expected = getattr(timer, expected_time_source)

    assert result == expected


# Negative tests
@pytest.mark.timer
@pytest.mark.parametrize('invalid_time', [
    'string',
    None,
    [],
])
def test_timer_set_invalid_time_negative(timer, invalid_time):
    original_time = timer.pomodoro_time

    timer.pomodoro_time = invalid_time

    assert timer.pomodoro_time == invalid_time

    try:
        result = timer.get_initial_time()
        assert result == invalid_time or result == original_time
    except (TypeError, AttributeError):
        assert True



@pytest.mark.timer
def test_timer_negative_time_handling_negative(timer):
    timer.pomodoro_time = -1500
    timer.current_time = -100

    name = timer.get_current_period_name()
    assert isinstance(name, str)

    initial_time = timer.get_initial_time()
    assert initial_time == -1500



@pytest.mark.timer
def test_timer_extreme_cycle_count_negative(timer):
    timer.cycle_count = 999999
    timer.is_pomodoro_mode = True

    result = timer.next_period()
    assert result == 'long_break'
    assert timer.cycle_count == 0



@pytest.mark.timer
def test_timer_inconsistent_state_negative(timer):
    timer.is_pomodoro_mode = True
    timer.current_time = timer.long_break_time
    timer.cycle_count = -5

    name = timer.get_current_period_name()
    assert name == 'Pomodoro'

    initial_time = timer.get_initial_time()
    assert initial_time == timer.pomodoro_time
