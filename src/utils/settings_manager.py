import json
import os
import sys


class SettingsManager:
    def __init__(self):
        self.settings_file = self.resource_path('aPomodoro_settings.json')

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(os.path.dirname(__file__))
            base_path = os.path.abspath(os.path.join(base_path, '..', '..'))

        return os.path.join(base_path, relative_path)

    def save_settings(self, timer_state):
        try:
            settings = {
                'pomodoro_time': timer_state.pomodoro_time,
                'short_break_time': timer_state.short_break_time,
                'long_break_time': timer_state.long_break_time,
                'notification_type': timer_state.notification_type,
                'pomodoro_sound': timer_state.pomodoro_sound,
                'short_break_sound': timer_state.short_break_sound,
                'long_break_sound': timer_state.long_break_sound
            }

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True

        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def load_settings(self, timer_state):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                    timer_state.pomodoro_time = settings.get('pomodoro_time', 25 * 60)
                    timer_state.short_break_time = settings.get('short_break_time', 5 * 60)
                    timer_state.long_break_time = settings.get('long_break_time', 15 * 60)
                    timer_state.notification_type = settings.get('notification_type', 'both')
                    timer_state.pomodoro_sound = settings.get('pomodoro_sound', 'bonus_1')
                    timer_state.short_break_sound = settings.get('short_break_sound', 'soft_bell')
                    timer_state.long_break_sound = settings.get('long_break_sound', 'bell')
                    timer_state.current_time = timer_state.pomodoro_time

                return True

        except Exception as e:
            print(f"Error loading settings: {e}")

        return False
