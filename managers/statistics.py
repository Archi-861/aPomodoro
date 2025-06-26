import json
import os
from dataclasses import asdict
from datetime import date, datetime, timedelta
from typing import Dict
from models.timer import DayStats, SessionStats
from config import Config


class StatisticsManager:
    def __init__(self):
        self.stats_file = Config.STATS_FILE
        self._cache = {}  # Кэш для оптимизации



    def save_completed_pomodoro(self, duration: int):
        stats = self._load_all_stats()
        today = date.today().strftime('%Y-%m-%d')

        if today not in stats:
            stats[today] = DayStats()
        else:
            stats[today] = DayStats(**stats[today])

        stats[today].completed_pomodoros += 1
        stats[today].total_work_time += duration
        stats[today].sessions.append(SessionStats(
            timestamp=datetime.now().strftime('%H:%M:%S'),
            duration=duration
        ))

        self._save_all_stats(stats)
        self._invalidate_cache()



    def _load_all_stats(self) -> Dict:
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f'Error loading statistics: {e}')
        return {}



    def _save_all_stats(self, stats: Dict):
        try:
            serializable_stats = {}
            for key, value in stats.items():
                if isinstance(value, DayStats):
                    serializable_stats[key] = asdict(value)
                else:
                    serializable_stats[key] = value

            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f'Error saving statistics: {e}')



    def _invalidate_cache(self):
        self._cache.clear()



    def get_summary(self) -> Dict:
        if 'summary' in self._cache:
            return self._cache['summary']

        stats = self._load_all_stats()
        today = date.today()

        summary = {
            'today': self._get_day_stats(stats, today),
            'week': self._get_period_stats(stats, today, 7),
            'month': self._get_month_stats(stats, today)
        }

        self._cache['summary'] = summary
        return summary



    def _get_day_stats(self, stats: Dict, day: date) -> Dict:
        day_str = day.strftime('%Y-%m-%d')
        return stats.get(day_str, {'completed_pomodoros': 0, 'total_work_time': 0})



    def _get_period_stats(self, stats: Dict, end_date: date, days: int) -> Dict:
        result = {'completed_pomodoros': 0, 'total_work_time': 0}

        for i in range(days):
            day = end_date - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            if day_str in stats:
                result['completed_pomodoros'] += stats[day_str].get('completed_pomodoros', 0)
                result['total_work_time'] += stats[day_str].get('total_work_time', 0)

        return result



    def _get_month_stats(self, stats: Dict, today: date) -> Dict:
        result = {'completed_pomodoros': 0, 'total_work_time': 0}

        for day_str, day_data in stats.items():
            try:
                stat_date = datetime.strptime(day_str, '%Y-%m-%d').date()
                if stat_date.year == today.year and stat_date.month == today.month:
                    result['completed_pomodoros'] += day_data.get('completed_pomodoros', 0)
                    result['total_work_time'] += day_data.get('total_work_time', 0)
            except:
                continue

        return result



    def reset(self) -> bool:
        try:
            if os.path.exists(self.stats_file):
                os.remove(self.stats_file)
            self._invalidate_cache()
            return True
        except Exception as e:
            print(f'Ошибка сброса статистики: {e}')
            return False