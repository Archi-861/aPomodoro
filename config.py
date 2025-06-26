class Config:
    DEFAULT_POMODORO = 25 * 60
    DEFAULT_SHORT_BREAK = 5 * 60
    DEFAULT_LONG_BREAK = 15 * 60

    SETTINGS_FILE = 'aPomodoro_settings.json'
    STATS_FILE = 'aPomodoro_stats.json'
    SOUNDS_DIR = 'sounds'

    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 750
    UPDATE_INTERVAL = 1000

    COLORS = {
        'pomodoro': '#ff0505',
        'short_break': '#51c1e6',
        'long_break': '#0048f0',
        'pomodoro_circle': '#ff0505',
        'short_break_circle': '#51c1e6',
        'long_break_circle': '#0048f0'
    }