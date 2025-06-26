from dataclasses import dataclass
from typing import List
from config import Config


@dataclass
class TimerSettings:
    pomodoro_time: int = Config.DEFAULT_POMODORO
    short_break: int = Config.DEFAULT_SHORT_BREAK
    long_break: int = Config.DEFAULT_LONG_BREAK
    notification_type: str = 'both'
    pomodoro_sound: str = 'bonus_1'
    short_break_sound: str = 'soft_bell'
    long_break_sound: str = 'bell'
    auto_start_breaks: bool = True
    auto_start_pomodoros: bool = False


@dataclass
class SessionStats:
    timestamp: str
    duration: int


@dataclass
class DayStats:
    completed_pomodoros: int = 0
    total_work_time: int = 0
    sessions: List[SessionStats] = None

    def __post_init__(self):
        if self.sessions is None:
            self.sessions = []