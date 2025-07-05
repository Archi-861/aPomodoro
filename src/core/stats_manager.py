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

        if not isinstance(stats[today_str], dict):
            stats[today_str] = {'pomodoros': 0, 'work_time': 0}

        if 'pomodoros' not in stats[today_str]:
            stats[today_str]['pomodoros'] = 0
        if 'work_time' not in stats[today_str]:
            stats[today_str]['work_time'] = 0

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
                    data = json.load(f)

                cleaned_data = {}
                for date_str, day_data in data.items():
                    if isinstance(day_data, dict):
                        cleaned_day = {
                            'pomodoros': day_data.get('pomodoros', 0),
                            'work_time': day_data.get('work_time', 0)
                        }
                        try:
                            cleaned_day['pomodoros'] = int(cleaned_day['pomodoros'])
                            cleaned_day['work_time'] = int(cleaned_day['work_time'])
                            cleaned_data[date_str] = cleaned_day
                        except (ValueError, TypeError):
                            continue

                return cleaned_data

            except Exception as e:
                print(f"Error loading stats: {e}")
                return {}

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

        try:
            total_pomodoros = sum(day.get('pomodoros', 0) for day in stats.values())
            total_time = sum(day.get('work_time', 0) for day in stats.values())
            total_days = len([day for day in stats.values() if day.get('pomodoros', 0) > 0])
            avg_per_day = total_pomodoros / total_days if total_days > 0 else 0

            return {
                'total_pomodoros': total_pomodoros,
                'total_time': total_time,
                'total_days': total_days,
                'avg_per_day': avg_per_day
            }
        except Exception as e:
            print(f"Error calculating general stats: {e}")
            return {
                'total_pomodoros': 0,
                'total_time': 0,
                'total_days': 0,
                'avg_per_day': 0
            }



    def get_daily_stats(self, days=7):
        stats = self._load_stats()
        today = datetime.now()
        result = []

        for i in range(days):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            data = stats.get(day_str, {'pomodoros': 0, 'work_time': 0})
            pomodoros = data.get('pomodoros', 0) if isinstance(data, dict) else 0
            work_time = data.get('work_time', 0) if isinstance(data, dict) else 0

            try:
                pomodoros = int(pomodoros)
                work_time = int(work_time)
            except (ValueError, TypeError):
                pomodoros = 0
                work_time = 0

            result.append({
                'date': day,
                'pomodoros': pomodoros,
                'work_time': work_time,
                'is_today': (i == 0)
            })

        return result[::-1]



    def repair_stats_file(self):
        try:
            stats = self._load_stats()  # Уже очищает данные
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error repairing stats: {e}")
            return False