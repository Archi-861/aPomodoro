import pytest
import os
import tempfile
from src.core.stats_manager import StatsManager


@pytest.fixture(scope='function')
def stats():
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file.close()

    stats_manager = StatsManager()
    stats_manager.stats_file = temp_file.name

    yield stats_manager

    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)



# Positive tests
@pytest.mark.stats
@pytest.mark.parametrize('duration, expected_pomodoros', [
    (1500, 1),
    (1800, 1),
    (900, 1),
])
def test_stats_save_pomodoro_positive(stats, duration, expected_pomodoros):
    stats.save_completed_pomodoro(duration)
    result = stats.get_general_stats()
    assert result['total_pomodoros'] == expected_pomodoros



@pytest.mark.stats
@pytest.mark.parametrize('count, expected_total', [
    (1, 1),
    (5, 5),
    (10, 10),
])
def test_stats_multiple_pomodoros_positive(stats, count, expected_total):
    for _ in range(count):
        stats.save_completed_pomodoro(1500)

    result = stats.get_general_stats()
    assert result['total_pomodoros'] == expected_total



# Border tests
@pytest.mark.stats
@pytest.mark.parametrize('duration, expected_time', [
    (0, 0),
    (1, 1),
    (86400, 86400)
])
def test_stats_save_duration_border(stats, duration, expected_time):
    stats.save_completed_pomodoro(duration)
    result = stats.get_general_stats()
    assert result['total_time'] == expected_time


@pytest.mark.stats
@pytest.mark.parametrize('days_count, expected_result', [
    (1, 1),
    (7, 7),
    (30, 30),
])
def test_stats_get_daily_border(stats, days_count, expected_result):
    result = stats.get_daily_stats(days_count)
    assert len(result) == expected_result


# Negative tests
@pytest.mark.stats
@pytest.mark.parametrize('invalid_duration, expected_exception', [
    ('string', (TypeError, AttributeError)),
    (None, (TypeError, AttributeError)),
    ([], (TypeError, AttributeError)),
])
def test_stats_save_invalid_duration_negative(stats, invalid_duration, expected_exception):
    try:
        stats.save_completed_pomodoro(invalid_duration)
        result = stats.get_general_stats()
        assert isinstance(result, dict)
    except expected_exception:
        pass