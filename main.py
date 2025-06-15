import json
import os.path
from os import times

import customtkinter as ctk


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class Settings:
    pass

class Statistics:

    def __init__(self):
        self.stats_file = 'aPomodoro_stats.json'


    def save_completed_pomodoros(self):
        stats = self.load_stats

        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)


    def load_stats(self):

        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {k: int(v) for k, v in data.items() if str(v).isdigit()}
            except Exception as ex:
                print(f'Error loading {ex}')
                return {}
        return {}



class NotificationManager:
    pass

class TimerState:
    #управление состоянием таймера
    def __init__(self):
        self.pomodoro_time = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        self.current_time = self.pomodoro_time
        self.is_running = False
        self.is_pomodoro_mode = True
        self.completed_pomodoros = 0
        self.current_cycle = 0

    def reset_to_pomodoro(self):

        #Сброс к режиму ПОМОДОРО

        self.current_time = self.pomodoro_time
        self.is_pomodoro_mode = True

    def reset_to_break(self, is_long_break = True):

        #Сброс к режиму короткий/длинный перерыв

        self.current_time = self.long_break if is_long_break else self.short_break
        self.is_pomodoro_mode = False

    def complete_pomodoro_period(self):

        #Окончание циклов ПОМОДОРО

        self.completed_pomodoros += 1
        self.current_cycle += 1

        if self.current_cycle >= 4:
            self.current_cycle = 0
            self.reset_to_break(is_long_break=True)
            return 'Long break'
        else:
            self.reset_to_break()
            return 'Short break'

    def complete_break_period(self):
        self.reset_to_pomodoro()
        return 'Pomodoro'



class TimerCore:

    def __init__(self, timer_state, notification_manager):
        self.timer_state = timer_state
        self.notification_manager = notification_manager
        self.is_stop = False

    def start(self):
        if not self.timer_state.is_running:
            self.timer_state.is_running = True
            self.is_stop = False
            return True
        return False

    def pause(self):
        self.timer_state.is_running = False
        self.is_stop = True

    def reset(self):
        self.pause()
        if self.timer_state.is_pomodoro_period:
            self.timer_state.current_time = self.timer_state.pomodoro_time
        else:
            if self.timer_state.current_cycle == 0:
                self.timer_state.current_time = self.timer_state.long_break
            else:
                self.timer_state.current_time = self.timer_state.short_break

    def run_timer(self):
        initial_time = self.timer_state.current_time








class PomodoroApp(ctk.CTk):
    pass




app = PomodoroApp()
app.mainloop()