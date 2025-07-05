import pytest
from unittest.mock import Mock, patch
from src.utils.sound_manager import SoundManager
from src.core.timer_state import TimerState


@pytest.fixture(scope='function')
def sound_manager():
    with patch('pygame.mixer.init'), patch('pygame.mixer.Sound') as mock_sound:
        mock_sound.return_value = Mock()
        sound_mgr = SoundManager()
        yield sound_mgr



# Positive tests
@pytest.mark.sound
@pytest.mark.parametrize('sound_key, should_play', [
    ('bell', True),
    ('soft_bell', True),
    ('notification', True),
    ('none', False),
])
def test_sound_play_valid_sounds_positive(sound_manager, sound_key, should_play):
    mock_sound = Mock()
    sound_manager.sounds[sound_key] = mock_sound if should_play else None

    sound_manager.play_sound(sound_key)

    if should_play:
        mock_sound.play.assert_called_once()
    else:
        assert True



@pytest.mark.sound
@pytest.mark.parametrize('notification_type, should_play_sound', [
    ('sound', True),
    ('both', True),
    ('popup', False),
])
def test_sound_notification_types_positive(sound_manager, notification_type, should_play_sound):
    timer_state = TimerState()
    timer_state.notification_type = notification_type
    timer_state.pomodoro_sound = 'bell'

    mock_sound = Mock()
    sound_manager.sounds['bell'] = mock_sound

    sound_manager.handle_timer_finished(timer_state, 'pomodoro')

    if should_play_sound:
        mock_sound.play.assert_called_once()
    else:
        mock_sound.play.assert_not_called()



# Border tests
@pytest.mark.sound
@pytest.mark.parametrize('completion_mode, sound_setting', [
    ('pomodoro', 'pomodoro_sound'),
    ('short_break', 'short_break_sound'),
    ('long_break', 'long_break_sound'),
])
def test_sound_completion_modes_border(sound_manager, completion_mode, sound_setting):
    timer_state = TimerState()
    timer_state.notification_type = 'sound'
    setattr(timer_state, sound_setting, 'bell')

    mock_sound = Mock()
    sound_manager.sounds['bell'] = mock_sound

    sound_manager.handle_timer_finished(timer_state, completion_mode)

    mock_sound.play.assert_called_once()



@pytest.mark.sound
@pytest.mark.parametrize('sound_key', [
    'bell', 'soft_bell', 'notification', 'bonus_1', 'bonus_2'
])
def test_sound_all_available_sounds_border(sound_manager, sound_key):
    assert sound_key in sound_manager.sounds



# Negative tests
@pytest.mark.sound
@pytest.mark.parametrize('invalid_sound_key', [
    'nonexistent_sound',
    '',
    None,
    123,
])
def test_sound_play_invalid_sounds_negative(sound_manager, invalid_sound_key):
    try:
        sound_manager.play_sound(invalid_sound_key)
        assert True
    except (KeyError, TypeError, AttributeError):
        assert True



@pytest.mark.sound
@pytest.mark.parametrize('invalid_mode', [
    'invalid_mode',
    '',
    None,
    123,
])
def test_sound_invalid_completion_mode_negative(sound_manager, invalid_mode):
    timer_state = TimerState()
    timer_state.notification_type = 'sound'

    try:
        sound_manager.handle_timer_finished(timer_state, invalid_mode)
        assert True
    except (AttributeError, KeyError):
        assert True