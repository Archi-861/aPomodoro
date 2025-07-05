import customtkinter as ctk
from src.core.timer_state import TimerState
from src.utils.sound_manager import SoundManager
from src.utils.settings_manager import SettingsManager
from src.core.stats_manager import StatsManager
from src.ui.ui_windows import UIWindows
import sys

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class PomodoroApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('aPomodoro')
        self.root.after(100, lambda: self.root.state('zoomed'))
        self.root.minsize(600, 700)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.timer_state = TimerState()
        self.sound_manager = SoundManager()
        self.settings_manager = SettingsManager()
        self.stats_manager = StatsManager()

        try:
            self.stats_manager.get_general_stats()
        except Exception:
            self.stats_manager.repair_stats_file()

        self.timer_job = None
        self.colors = {
            'pomodoro': {'text': '#ff0505', 'circle': '#ff0505'},
            'short_break': {'text': '#51c1e6', 'circle': '#51c1e6'},
            'long_break': {'text': '#0048f0', 'circle': '#0048f0'}
        }
        self.settings_manager.load_settings(self.timer_state)
        self.create_interface()
        self.update_display()



    def create_interface(self):
        self.create_menu()

        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text='',
                     font=ctk.CTkFont(size=32, weight='bold')).pack(pady=(30, 10))

        self.status_label = ctk.CTkLabel(main_frame, text='Pomodoro',
                                         font=ctk.CTkFont(size=20, weight='bold'))
        self.status_label.pack(pady=(0, 20))

        self.cycle_label = ctk.CTkLabel(main_frame, text='● ○ ○ ○',
                                        font=ctk.CTkFont(size=20))
        self.cycle_label.pack(pady=(0, 20))

        self.time_frame = ctk.CTkFrame(main_frame, width=300, height=300, corner_radius=150)
        self.time_frame.pack(pady=(0, 20))
        self.time_frame.pack_propagate(False)

        self.time_label = ctk.CTkLabel(self.time_frame, text='',
                                       font=ctk.CTkFont(size=48, weight='bold'))
        self.time_label.place(relx=0.5, rely=0.5, anchor='center')

        self.progress = ctk.CTkProgressBar(main_frame, width=400, height=20)
        self.progress.pack(pady=(0, 30))

        self.create_control_buttons(main_frame)



    def create_menu(self):
        menu_frame = ctk.CTkFrame(self.root)
        menu_frame.pack(fill='x', pady=(5, 10))

        ctk.CTkLabel(menu_frame, text='aPomodoro',
                     font=ctk.CTkFont(size=20, weight='bold')).pack(side='left', padx=10)

        ctk.CTkButton(menu_frame, text='About', command=self.show_about,
                      width=70).pack(side='right', padx=5)
        ctk.CTkButton(menu_frame, text='Settings', command=self.show_settings,
                      width=70).pack(side='right', padx=5)
        ctk.CTkButton(menu_frame, text='Stats', command=self.show_stats,
                      width=70).pack(side='right', padx=5)



    def create_control_buttons(self, parent):
        button_frame = ctk.CTkFrame(parent, fg_color='transparent')
        button_frame.pack(pady=(0, 30))

        self.start_btn = ctk.CTkButton(
            button_frame, text='▶ Start', width=120, height=50,
            font=ctk.CTkFont(size=16, weight='bold'), corner_radius=25,
            command=self.start_timer
        )
        self.start_btn.pack(side='left', padx=10)

        self.pause_btn = ctk.CTkButton(
            button_frame, text='⏸ Pause', width=120, height=50,
            font=ctk.CTkFont(size=16, weight='bold'), corner_radius=25,
            command=self.pause_timer, state='disabled'
        )
        self.pause_btn.pack(side='left', padx=10)

        self.reset_btn = ctk.CTkButton(
            button_frame, text='Reset', width=120, height=50,
            font=ctk.CTkFont(size=16, weight='bold'), corner_radius=25,
            command=self.reset_timer
        )
        self.reset_btn.pack(side='left', padx=10)



    def format_time(self, seconds):
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f'{minutes:02d}:{seconds:02d}'



    def get_current_colors(self):
        if self.timer_state.is_pomodoro_mode:
            return self.colors['pomodoro']
        else:
            if self.timer_state.cycle_count == 0:
                return self.colors['long_break']
            else:
                return self.colors['short_break']



    def update_display(self):
        self.time_label.configure(text=self.format_time(self.timer_state.current_time))
        colors = self.get_current_colors()
        status = self.timer_state.get_current_period_name()
        self.status_label.configure(text=status, text_color=colors['text'])
        self.time_frame.configure(fg_color=colors['circle'])
        self.progress.configure(progress_color=colors['text'])
        initial_time = self.timer_state.get_initial_time()
        progress_value = self.timer_state.current_time / initial_time if initial_time > 0 else 0
        self.progress.set(progress_value)

        if self.timer_state.is_running:
            self.root.title(f'{self.format_time(self.timer_state.current_time)} - aPomodoro')
        else:
            self.root.title('aPomodoro')

        filled = '● ' * self.timer_state.cycle_count
        empty = '○ ' * (4 - self.timer_state.cycle_count)
        self.cycle_label.configure(text=(filled + empty).strip())



    def start_timer(self):
        self.timer_state.is_running = True
        self.start_btn.configure(state='disabled')
        self.pause_btn.configure(state='normal')
        self.tick()



    def pause_timer(self):
        self.timer_state.is_running = False
        self.start_btn.configure(state='normal')
        self.pause_btn.configure(state='disabled')
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None



    def reset_timer(self):
        self.pause_timer()
        self.timer_state.reset_to_pomodoro()
        self.update_display()



    def tick(self):
        if self.timer_state.is_running and self.timer_state.current_time > 0:
            self.timer_state.current_time -= 1
            self.update_display()
            self.timer_job = self.root.after(1000, self.tick)
        elif self.timer_state.is_running:
            self.timer_finished()



    def timer_finished(self):
        self.timer_state.is_running = False
        self.start_btn.configure(state='normal')
        self.pause_btn.configure(state='disabled')

        if self.timer_state.is_pomodoro_mode:
            completed_mode = 'pomodoro'
            self.stats_manager.save_completed_pomodoro(self.timer_state.pomodoro_time)
        else:
            if self.timer_state.cycle_count == 0:
                completed_mode = 'long_break'
            else:
                completed_mode = 'short_break'

        self.sound_manager.handle_timer_finished(self.timer_state, completed_mode)

        next_period = self.timer_state.next_period()
        self.update_display()
        self.root.after(2000, self.auto_start_next)



    def auto_start_next(self):
        self.start_timer()



    def show_about(self):
        UIWindows.show_about(self.root)



    def show_settings(self):
        UIWindows.show_settings(
            self.root,
            self.timer_state,
            self.settings_manager,
            self.update_display
        )



    def show_stats(self):
        try:
            UIWindows.show_stats(self.root, self.stats_manager)
        except Exception as e:
            self.stats_manager.repair_stats_file()
            try:
                UIWindows.show_stats(self.root, self.stats_manager)
            except Exception:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Error", "Couldn't load statistics.\nThe statistics file will be reset..")
                self.stats_manager.reset_stats()



    def on_closing(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.settings_manager.save_settings(self.timer_state)
        self.sound_manager.cleanup()
        self.root.destroy()
        sys.exit()



    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


if __name__ == '__main__':
    app = PomodoroApp()
    app.run()