import pytest
import tempfile
import os
from src.utils.settings_manager import SettingsManager
from src.core.timer_state import TimerState


@pytest.fixture(scope='function')
def settings():

    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file.close()

    settings_manager = SettingsManager()
    settings_manager.settings_file = temp_file.name

    yield settings_manager

    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)



# Positive tests
@pytest.mark.settings
@pytest.mark.parametrize('pomodoro_time, expected_result', [
    (1500, 1500),
    (1800, 1800),
    (3600, 3600),
])
def test_settings_save_load_pomodoro_time_positive(settings, pomodoro_time, expected_result):
    timer_state = TimerState()
    timer_state.pomodoro_time = pomodoro_time

    result = settings.save_settings(timer_state)
    assert result is True

    new_timer = TimerState()
    settings.load_settings(new_timer)

    assert new_timer.pomodoro_time == expected_result



@pytest.mark.settings
@pytest.mark.parametrize('notification_type, expected_result', [
    ('sound', 'sound'),
    ('popup', 'popup'),
    ('both', 'both'),
])
def test_settings_notification_types_positive(settings, notification_type, expected_result):
    timer_state = TimerState()
    timer_state.notification_type = notification_type

    settings.save_settings(timer_state)

    new_timer = TimerState()
    settings.load_settings(new_timer)

    assert new_timer.notification_type == expected_result



# Border tests
@pytest.mark.settings
@pytest.mark.parametrize('time_value, expected_result', [
    (1, 1),
    (7200, 7200),
])
def test_settings_time_boundaries_border(settings, time_value, expected_result):
    timer_state = TimerState()
    timer_state.pomodoro_time = time_value

    settings.save_settings(timer_state)

    new_timer = TimerState()
    settings.load_settings(new_timer)

    assert new_timer.pomodoro_time == expected_result



@pytest.mark.settings
@pytest.mark.parametrize('sound_type, expected_result', [
    ('bell', 'bell'),
    ('soft_bell', 'soft_bell'),
    ('none', 'none'),
])
def test_settings_sound_types_border(settings, sound_type, expected_result):
    timer_state = TimerState()
    timer_state.pomodoro_sound = sound_type

    settings.save_settings(timer_state)

    new_timer = TimerState()
    settings.load_settings(new_timer)

    assert new_timer.pomodoro_sound == expected_result



# Negatives tests
@pytest.mark.settings
def test_settings_corrupted_file_negative(settings):
    with open(settings.settings_file, 'w') as f:
        f.write('invalid json content')

    timer_state = TimerState()
    result = settings.load_settings(timer_state)

    assert timer_state.pomodoro_time == 25 * 60



@pytest.mark.settings
def test_settings_save_invalid_object_negative(settings):
    invalid_timer = "not a timer object"

    try:
        result = settings.save_settings(invalid_timer)
        assert result is False
    except AttributeError:
        pass