import json
import os.path
from sys import int_info

import customtkinter as ctk


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class Settings:

    def __init__(self):
        self.settings_file = 'aPomodoro_settings.json'

    def save_settings(self, timer_state):
        try:
            settings = {
                'pomodoro' : timer_state.pomodoro_time,
                'short_break' : timer_state.short_break,
                'long_break' : timer_state.long_break
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as ex:
            print(f'Error saving {ex}')
            return False

    def load_setting(self, timer_state):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    timer_state.pomodoro_time = settings.get('pomodoro', 25 * 60)
                    timer_state.short_break = settings.get('short_break', 5 * 60)
                    timer_state.long_break = settings.get('long_break', 15 * 60)
                    timer_state.current_time = timer_state.pomodoro_time
                return True
            except Exception as ex:
                print(f'Error loading {ex}')
                return False
        return False



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

    def __init__(self, timer_state, notification_manager, update_callback, finish_callback, root):
        self.timer_state = timer_state
        self.notification_manager = notification_manager

        #Маркеры для GUI
        self.update_callback = update_callback
        self.finish_callback = finish_callback

        self.root = root
        self.timer_after = None

    def start(self):
        if not self.timer_state.is_running:
            self.timer_state.is_running = True
            self.next_action_tick()
            return True
        return False

    def pause(self):
        self.timer_state.is_running = False
        if self.timer_after:
            self.root.after_cancel(self.timer_after)
            self.timer_after = None


    def reset(self):
        self.pause()
        if self.timer_state.is_pomodoro_period:
            self.timer_state.current_time = self.timer_state.pomodoro_time
        else:
            if self.timer_state.current_cycle == 0:
                self.timer_state.current_time = self.timer_state.long_break
            else:
                self.timer_state.current_time = self.timer_state.short_break



    def next_action_tick(self):
        if self.timer_state.is_running:
            self.timer_after = self.root.after(1000, self.one_second_tick)

    def one_second_tick(self):
        if self.timer_state.is_running and self.timer_state.current_time > 0:
            self.timer_state.current_time -= 1

            if self.timer_state.is_pomodoro_period:
                initial_time = self.timer_state.pomodoro_time
            else:
                if self.timer_state.current_cycle == 0:
                    initial_time = self.timer_state.long_break
                else:
                    initial_time = self.timer_state.short_break
            progress = self.timer_state.current_time / initial_time if initial_time > 0 else 0.0
            self.update_callback(progress)

            if self.timer_state.current_time > 0:
                self.next_action_tick()
            else:
                self.timer_state.is_running = False
                self.finish_callback()



    def run(self):
        initial_time = self.timer_state.current_time

class UIResource:
    pass

class PomodoroTimer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('aPomodoro')
        self.root.geometry('500x600')


        self.timer_state = TimerState()
        self.settings = Settings()
        self.stats = Statistics()
        self.notification_manager = NotificationManager()


        self.timer_core = TimerCore(self.timer_state, self.notification_manager)


        self.label = ctk.CTkLabel(self.root, text='00:00', font=ctk.CTkFont(size=48, weight='bold'))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self.root, text='Start', command=self.start_timer)
        self.start_button.pack(pady=10)

        self.reset_button = ctk.CTkButton(self.root, text='Reset', command=self.reset_timer)
        self.reset_button.pack(pady=5)


    def start_timer(self):

        #Запуск таймера
        if self.timer_core.start():
            self.start_button.configure(state='disabled')
            print('Таймер запущен')


    def pause(self):
        self.timer_core.pause()



    def reset_timer(self):
        pass

    def run(self):
        self.root.mainloop()





app = PomodoroTimer()
app.run()