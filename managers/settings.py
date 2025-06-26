import json
import os
from dataclasses import asdict
from models.timer import TimerSettings
from config import Config


class SettingsManager:
    def __init__(self):
        self.settings_file = Config.SETTINGS_FILE

    def save(self, settings: TimerSettings) -> bool:
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(settings), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'Error saving settings: {e}')
            return False

    def load(self) -> TimerSettings:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                settings = TimerSettings(**data)
                return settings
            except Exception as e:
                print(f'Error loading settings: {e}')

        return TimerSettings()