import customtkinter as ctk
from models.timer import TimerSettings
from managers.settings import SettingsManager
from managers.statistics import StatisticsManager
from managers.sound import SoundManager
from ui.dialogs import AboutWindow, SettingsWindow, StatisticsWindow, NotificationPopup
from config import Config

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

class TimerCore:
    def __init__(self, settings: TimerSettings):
        self.settings = settings
        self.current_time = settings.pomodoro_time
        self.is_running = False
        self.is_pomodoro_mode = True
        self.completed_pomodoros = 0
        self.current_cycle = 0
        self.action_handler = []



    def add_action(self, action):
        self.action_handler.append(action)



    def notify_handler(self, event: str, data=None):
        for action in self.action_handler:
            action.on_timer_event(event, data)



    def start(self):
        if not self.is_running:
            self.is_running = True
            self.notify_handler('started')



    def pause(self):
        if self.is_running:
            self.is_running = False
            self.notify_handler('paused')



    def reset(self):
        self.is_running = False

        if self.is_pomodoro_mode:
            self.current_time = self.settings.pomodoro_time
        else:
            if self.current_cycle == 0:
                self.current_time = self.settings.long_break
            else:
                self.current_time = self.settings.short_break

        self.notify_handler('reset')



    def one_second_tick(self):
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            self.notify_handler('tick', self.current_time)

            if self.current_time == 0:
                self.on_timer_complete()



    def on_timer_complete(self):
        self.is_running = False

        if self.is_pomodoro_mode:
            self.completed_pomodoros += 1
            self.current_cycle = (self.current_cycle + 1) % 4

            if self.current_cycle == 0:
                self.switch_to_break(is_long=True)
                self.notify_handler('long_break_started')
            else:
                self.switch_to_break(is_long=False)
                self.notify_handler('short_break_started')
        else:
            self.switch_to_pomodoro()
            self.notify_handler('pomodoro_started')



    def switch_to_pomodoro(self):
        self.current_time = self.settings.pomodoro_time
        self.is_pomodoro_mode = True



    def switch_to_break(self, is_long: bool):
        self.current_time = self.settings.long_break if is_long else self.settings.short_break
        self.is_pomodoro_mode = False



    def get_progress(self) -> float:
        if self.is_pomodoro_mode:
            total_time = self.settings.pomodoro_time
        elif self.current_cycle == 0:
            total_time = self.settings.long_break
        else:
            total_time = self.settings.short_break

        return self.current_time / total_time if total_time > 0 else 0.0




    def get_current_sound(self) -> str:
        if self.is_pomodoro_mode:
            return self.settings.pomodoro_sound
        elif self.current_cycle == 0:
            return self.settings.long_break_sound
        else:
            return self.settings.short_break_sound


class PomodoroTimerApp:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.stats_manager = StatisticsManager()
        self.sound_manager = SoundManager()
        self.settings = self.settings_manager.load()
        self.timer_core = TimerCore(self.settings)
        self.timer_core.add_action(self)
        self.root = ctk.CTk()
        self.root.title('aPomodoro')
        self.root.geometry(f'{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}')
        self.timer_after = None
        self.create_ui()
        self._update_display()
        self.root.protocol('WM_DELETE_WINDOW', self._on_closing)



    def create_ui(self):
        self._create_menu()
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))

        ctk.CTkLabel(main_frame, text='', font=ctk.CTkFont(size=32, weight='bold')).pack(pady=(30, 10))

        self.status_label = ctk.CTkLabel(main_frame, text='Pomodoro', font=ctk.CTkFont(size=20, weight='bold'))
        self.status_label.pack(pady=(0, 20))

        self.cycle_indicator = ctk.CTkLabel(main_frame, text='● ○ ○ ○', font=ctk.CTkFont(size=20))
        self.cycle_indicator.pack(pady=(0, 20))

        self.progress_frame = ctk.CTkFrame(main_frame, width=300, height=300, corner_radius=150)
        self.progress_frame.pack(pady=(0, 20))
        self.progress_frame.pack_propagate(False)

        self.time_label = ctk.CTkLabel(self.progress_frame, text='25:00', font=ctk.CTkFont(size=48, weight='bold'))
        self.time_label.place(relx=0.5, rely=0.5, anchor='center')

        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400, height=20, corner_radius=10)
        self.progress_bar.pack(pady=(0, 30))
        self.progress_bar.set(1.0)

        self._create_control_buttons(main_frame)



    def _create_menu(self):
        menu_frame = ctk.CTkFrame(self.root)
        menu_frame.pack(side='top', fill='x', pady=(5, 10))

        ctk.CTkLabel(menu_frame, text='aPomodoro', font=ctk.CTkFont(size=20, weight='bold')).pack(side='left', padx=20)

        ctk.CTkButton(menu_frame, text='About', width=100, command=self._show_about).pack(side='right', padx=(0, 10))
        ctk.CTkButton(menu_frame, text='Settings', width=100, command=self._show_settings).pack(side='right', padx=(0, 10))
        ctk.CTkButton(menu_frame, text='Statistics', width=100, command=self._show_statistics).pack(side='right', padx=(0, 10))



    def _create_control_buttons(self, parent):
        button_frame = ctk.CTkFrame(parent, fg_color='transparent')
        button_frame.pack(pady=(0, 30))

        self.start_button = ctk.CTkButton(button_frame,
            text='▶ Start',
            width=120,
            height=50,
            font=ctk.CTkFont(size=16, weight='bold'),
            corner_radius=25,
            command=self._start_timer
        )
        self.start_button.pack(side='left', padx=10)

        self.pause_button = ctk.CTkButton(
            button_frame,
            text='⏸ Pause',
            width=120,
            height=50,
            font=ctk.CTkFont(size=16, weight='bold'),
            corner_radius=25,
            command=self._pause_timer,
            state='disabled'
        )
        self.pause_button.pack(side='left', padx=10)

        self.reset_button = ctk.CTkButton(
            button_frame,
            text='↻ Reset',
            width=120,
            height=50,
            font=ctk.CTkFont(size=16, weight='bold'),
            corner_radius=25,
            command=self._reset_timer
        )
        self.reset_button.pack(side='left', padx=10)

    def _update_display(self):
        minutes = self.timer_core.current_time // 60
        seconds = self.timer_core.current_time % 60
        time_str = f'{minutes:02d}:{seconds:02d}'
        self.time_label.configure(text=time_str)

        if self.timer_core.is_pomodoro_mode:
            status_text = 'Pomodoro'
            color = Config.COLORS['pomodoro']
            circle_color = Config.COLORS['pomodoro_circle']
        else:
            if self.timer_core.current_cycle == 0:
                status_text = 'Long break'
                color = Config.COLORS['long_break']
                circle_color = Config.COLORS['long_break_circle']
            else:
                status_text = 'Short break'
                color = Config.COLORS['short_break']
                circle_color = Config.COLORS['short_break_circle']

        self.status_label.configure(text=status_text, text_color=color)
        self.progress_frame.configure(fg_color=circle_color)
        self.progress_bar.configure(progress_color=color)

        progress = self.timer_core.get_progress()
        self.progress_bar.set(progress)

        filled = '● ' * self.timer_core.current_cycle
        empty = '○ ' * (4 - self.timer_core.current_cycle)
        self.cycle_indicator.configure(text=(filled + empty).strip())

        if self.timer_core.is_running:
            self.root.title(f'{time_str} - aPomodoro')
        else:
            self.root.title('aPomodoro')

    def on_timer_event(self, event: str, data=None):
        if event == 'started':
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')
            self._schedule_tick()

        elif event == 'paused':
            self.start_button.configure(state='normal')
            self.pause_button.configure(state='disabled')
            if self.timer_after:
                self.root.after_cancel(self.timer_after)

        elif event == 'reset':
            self._update_display()

        elif event == 'tick':
            self._update_display()
            if self.timer_core.is_running:
                self._schedule_tick()

        elif event in ['pomodoro_started', 'short_break_started', 'long_break_started']:
            self._handle_timer_complete(event)

    def _schedule_tick(self):
        self.timer_after = self.root.after(Config.UPDATE_INTERVAL, self.timer_core.one_second_tick)

    def _handle_timer_complete(self, event: str):
        if event != 'pomodoro_started':
            self.stats_manager.save_completed_pomodoro(self.settings.pomodoro_time)

        messages = {
            'long_break_started': ('The cycle is completed!', 'Time for a long break!'),
            'short_break_started': ('Pomodoro is completed!', 'Time for a short break!'),
            'pomodoro_started': ('The break is over!', 'Time to work!')
        }

        title, message = messages[event]

        if self.settings.notification_type in ['sound', 'both']:
            self.sound_manager.play_sound(self.timer_core.get_current_sound())

        if self.settings.notification_type in ['popup', 'both']:
            NotificationPopup(self.root, title, message)

        self._update_display()

        should_autostart = (
            self.settings.auto_start_breaks if event != 'pomodoro_started'
            else self.settings.auto_start_pomodoros
        )

        if should_autostart:
            self.root.after(1000, self._start_timer)



    def _start_timer(self):
        self.timer_core.start()



    def _pause_timer(self):
        self.timer_core.pause()



    def _reset_timer(self):
        self.timer_core.reset()



    def _show_about(self):
        AboutWindow(self.root)



    def _show_settings(self):

        def on_save(new_settings: TimerSettings):
            self.settings = new_settings
            self.timer_core.settings = new_settings
            return self.settings_manager.save(new_settings)

        SettingsWindow(self.root, self.settings, self.sound_manager, on_save)



    def _show_statistics(self):
        StatisticsWindow(self.root, self.stats_manager)



    def _on_closing(self):
        self.timer_core.pause()
        self.settings_manager.save(self.settings)
        self.root.destroy()



    def run(self):
        self.root.mainloop()