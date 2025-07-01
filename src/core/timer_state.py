class TimerState:
    def __init__(self):
        self.pomodoro_time = 25 * 60
        self.short_break_time = 5 * 60
        self.long_break_time = 15 * 60
        self.current_time = self.pomodoro_time
        self.is_running = False
        self.is_pomodoro_mode = True
        self.cycle_count = 0
        self.notification_type = 'both'
        self.pomodoro_sound = 'soft_bell'
        self.short_break_sound = 'notification'
        self.long_break_sound = 'soft_bell'



    def reset_to_pomodoro(self):
        self.current_time = self.pomodoro_time
        self.is_pomodoro_mode = True
        self.cycle_count = 0
        self.is_running = False



    def next_period(self):
        if self.is_pomodoro_mode:
            self.cycle_count += 1

            if self.cycle_count >= 4:
                self.cycle_count = 0
                self.current_time = self.long_break_time
                self.is_pomodoro_mode = False
                return 'long_break'

            else:
                self.current_time = self.short_break_time
                self.is_pomodoro_mode = False
                return 'short_break'

        else:
            self.current_time = self.pomodoro_time
            self.is_pomodoro_mode = True
            return 'pomodoro'



    def get_current_period_name(self):
        if self.is_pomodoro_mode:
            return 'Pomodoro'

        else:
            if self.cycle_count == 0:
                return 'Long break'

            else:
                return 'Short break'



    def get_initial_time(self):
        if self.is_pomodoro_mode:
            return self.pomodoro_time

        else:
            if self.cycle_count == 0:
                return self.long_break_time

            else:
                return self.short_break_time