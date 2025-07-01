import json
import os
import sys
from datetime import datetime, timedelta


class StatsManager:
    def __init__(self):
        self.stats_file = self.resource_path('aPomodoro_stats.json')

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        return os.path.join(base_path, relative_path)

    def save_completed_pomodoro(self, pomodoro_duration):
        stats = self._load_stats()
        today_str = datetime.now().strftime('%Y-%m-%d')
        if today_str not in stats:
            stats[today_str] = {'pomodoros': 0, 'work_time': 0}

        stats[today_str]['pomodoros'] += 1
        stats[today_str]['work_time'] += pomodoro_duration

        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def _load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading stats: {e}")
        return {}

    def reset_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            return True
        except Exception as e:
            print(f"Error resetting stats: {e}")
            return False

    def get_general_stats(self):
        stats = self._load_stats()
        total_pomodoros = sum(day['pomodoros'] for day in stats.values())
        total_time = sum(day['work_time'] for day in stats.values())
        total_days = len(stats)
        avg_per_day = total_pomodoros / total_days if total_days > 0 else 0

        return {
            'total_pomodoros': total_pomodoros,
            'total_time': total_time,
            'total_days': total_days,
            'avg_per_day': avg_per_day
        }

    def get_daily_stats(self, days=7):
        stats = self._load_stats()
        today = datetime.now()
        result = []

        for i in range(days):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            data = stats.get(day_str, {'pomodoros': 0, 'work_time': 0})
            result.append({
                'date': day,
                'pomodoros': data['pomodoros'],
                'work_time': data['work_time'],
                'is_today': (i == 0)
            })

        return result[::-1]
