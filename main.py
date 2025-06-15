import customtkinter as ctk


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class Settings:
    pass

class Statistics:
    pass

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
    pass



class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('aPomodoro')
        self.geometry('600x550')

        self.timer_label = ctk.CTkLabel(self, text='25:00', font=('Arial', 48))
        self.timer_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text='START', command=self.start_timer)
        self.start_button.pack(pady=5)

        self.pause_button = ctk.CTkButton(self, text='PAUSE', command=self.pause_timer)
        self.pause_button.pack(pady=5)

        self.reset_button = ctk.CTkButton(self, text='STOP', command=self.stop_timer)
        self.reset_button.pack(pady=5)


    def start_timer(self):
        pass

    def pause_timer(self):
        pass

    def stop_timer(self):
        pass




app = PomodoroApp()
app.mainloop()