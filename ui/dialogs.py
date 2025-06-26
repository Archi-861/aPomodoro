from typing import Dict
import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime, timedelta
from abc import ABC
from managers.statistics import StatisticsManager
from models.timer import TimerSettings
from managers.sound import SoundManager
import tkinter as tk


class BaseWindow(ABC):
    def __init__(self, parent=None, title='Window', geometry='400x300'):
        self.window = ctk.CTkToplevel() if parent else ctk.CTk()
        self.window.title(title)
        self.window.geometry(geometry)

        if parent:
            self.window.transient(parent)
            self.center_window(parent)



    def center_window(self, parent):
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.window.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f'+{x}+{y}')



class NotificationPopup:
    def __init__(self, parent, title: str, message: str):
        self.popup = ctk.CTkToplevel(parent)
        self.popup.title(title)
        self.popup.geometry('300x150+50+50')
        self.popup.transient(parent)
        self.popup.attributes('-topmost', True)

        self._create_content(title, message)
        self.popup.after(5000, self._destroy_safe)



    def _create_content(self, title: str, message: str):
        frame = ctk.CTkFrame(self.popup, corner_radius=10)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 5))

        ctk.CTkLabel(frame, text=message, font=ctk.CTkFont(size=12)).pack(pady=5)



    def _destroy_safe(self):
        try:
            if self.popup.winfo_exists():
                self.popup.destroy()
        except:
            pass



class SettingsWindow(BaseWindow):
    def __init__(self, parent, settings: TimerSettings, sound_manager: SoundManager, on_save):
        super().__init__(parent, 'Settings', '450x550')
        self.settings = settings
        self.sound_manager = sound_manager
        self.on_save = on_save

        self.create_widgets()
        self.load_values()
        self.window.grab_set()



    def create_widgets(self):
        main_frame = ctk.CTkScrollableFrame(self.window, corner_radius=15)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text='Settings', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=(0, 20))

        self._create_time_section(main_frame)
        self._create_notification_section(main_frame)
        self._create_autostart_section(main_frame)

        self._create_buttons(main_frame)



    def _create_time_section(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill='x', pady=10)

        ctk.CTkLabel(frame, text='Pomodoro durability', font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 5))

        self.pomodoro_var = tk.StringVar()
        self.short_break_var = tk.StringVar()
        self.long_break_var = tk.StringVar()

        entries = [
            ('Pomodoro (min):', self.pomodoro_var),
            ('Short break (min):', self.short_break_var),
            ('Long break (min):', self.long_break_var)
        ]

        for label, var in entries:
            row = ctk.CTkFrame(frame)
            row.pack(fill='x', pady=5, padx=10)
            ctk.CTkLabel(row, text=label).pack(side='left', padx=10)
            ctk.CTkEntry(row, textvariable=var, width=100).pack(side='right', padx=10)



    def _create_notification_section(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill='x', pady=10)

        ctk.CTkLabel(frame, text='Notification', font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 5))

        self.notification_var = tk.StringVar()
        notification_options = {
            'none': 'Off',
            'sound': 'Only sound',
            'popup': 'Popup',
            'both': 'Sound and popup'
        }

        row = ctk.CTkFrame(frame)
        row.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(row, text='Type:').pack(side='left', padx=10)
        ctk.CTkOptionMenu(row, variable=self.notification_var, values=list(notification_options.values())).pack(side='right', padx=10)

        self.sound_vars = {
            'pomodoro': tk.StringVar(),
            'short_break': tk.StringVar(),
            'long_break': tk.StringVar()
        }

        sound_labels = {
            'pomodoro': 'Pomodoro sound:',
            'short_break': 'Short break sound:',
            'long_break': 'Long break sound:'
        }

        sound_list = [self.sound_manager.get_display_name(s)
                      for s in self.sound_manager.get_sound_list()]

        for key, label in sound_labels.items():
            row = ctk.CTkFrame(frame)
            row.pack(fill='x', pady=5, padx=10)
            ctk.CTkLabel(row, text=label).pack(side='left', padx=10)
            ctk.CTkOptionMenu(row, variable=self.sound_vars[key], values=sound_list).pack(side='right', padx=10)

        ctk.CTkButton(frame, text='🔊 Test sound', command=self._test_sound, width=200).pack(pady=10)



    def _create_autostart_section(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill='x', pady=10)

        ctk.CTkLabel(frame, text='Auto-restart', font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 5))

        self.auto_breaks_var = tk.BooleanVar()
        self.auto_pomodoros_var = tk.BooleanVar()

        ctk.CTkCheckBox(frame, text='Autostart break', variable=self.auto_breaks_var).pack(pady=5, padx=20)

        ctk.CTkCheckBox(frame, text='Autostart pomodoro', variable=self.auto_pomodoros_var).pack(pady=5, padx=20)



    def _create_buttons(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill='x', pady=20)

        ctk.CTkButton(frame, text='Save', command=self._save, width=120).pack(side='left', padx=5)

        ctk.CTkButton(frame, text='Cancel', command=self.window.destroy, width=120).pack(side='right', padx=5)



    def load_values(self):
        self.pomodoro_var.set(str(self.settings.pomodoro_time // 60))
        self.short_break_var.set(str(self.settings.short_break // 60))
        self.long_break_var.set(str(self.settings.long_break // 60))

        self.notification_var.set(self._get_notification_display(self.settings.notification_type))
        self.auto_breaks_var.set(self.settings.auto_start_breaks)
        self.auto_pomodoros_var.set(self.settings.auto_start_pomodoros)

        self.sound_vars['pomodoro'].set(
            self.sound_manager.get_display_name(self.settings.pomodoro_sound)
        )
        self.sound_vars['short_break'].set(
            self.sound_manager.get_display_name(self.settings.short_break_sound)
        )
        self.sound_vars['long_break'].set(
            self.sound_manager.get_display_name(self.settings.long_break_sound)
        )



    def _get_notification_display(self, value: str) -> str:
        mapping = {
            'none': 'Off',
            'sound': 'Only sound',
            'popup': 'Popup',
            'both': 'Sound and popup'
        }
        return mapping.get(value, value)



    def _get_notification_value(self, display: str) -> str:
        mapping = {
            'Off': 'none',
            'Only sound': 'sound',
            'Popup': 'popup',
            'Sound and popup': 'both'
        }
        return mapping.get(display, 'both')



    def _test_sound(self):
        sound_display = self.sound_vars['pomodoro'].get()
        sound_id = self._get_sound_id(sound_display)
        self.sound_manager.play_sound(sound_id)



    def _get_sound_id(self, display_name: str) -> str:
        for sound_id in self.sound_manager.get_sound_list():
            if self.sound_manager.get_display_name(sound_id) == display_name:
                return sound_id
        return 'none'



    def _save(self):
        try:
            pomodoro = int(self.pomodoro_var.get())
            short_break = int(self.short_break_var.get())
            long_break = int(self.long_break_var.get())

            if pomodoro <= 0 or short_break <= 0 or long_break <= 0:
                messagebox.showerror('Error', 'The time must be greater than 0!')
                return

            self.settings.pomodoro_time = pomodoro * 60
            self.settings.short_break = short_break * 60
            self.settings.long_break = long_break * 60
            self.settings.notification_type = self._get_notification_value(self.notification_var.get())
            self.settings.pomodoro_sound = self._get_sound_id(self.sound_vars['pomodoro'].get())
            self.settings.short_break_sound = self._get_sound_id(self.sound_vars['short_break'].get())
            self.settings.long_break_sound = self._get_sound_id(self.sound_vars['long_break'].get())
            self.settings.auto_start_breaks = self.auto_breaks_var.get()
            self.settings.auto_start_pomodoros = self.auto_pomodoros_var.get()

            if self.on_save(self.settings):
                messagebox.showinfo('Success', 'The settings are saved!')
                self.window.destroy()

        except ValueError:
            messagebox.showerror('Error', 'Enter the correct numbers!')



class StatisticsWindow(BaseWindow):
    def __init__(self, parent, stats_manager: StatisticsManager):
        super().__init__(parent, 'Statistics', '600x700')
        self.stats_manager = stats_manager
        self.create_widgets()
        self.window.grab_set()



    def create_widgets(self):
        main_frame = ctk.CTkScrollableFrame(self.window, corner_radius=15)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text='Statistics', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=(0, 20))

        summary = self.stats_manager.get_summary()

        self._create_summary_section(main_frame, summary)
        self._create_daily_section(main_frame)
        self._create_weekly_section(main_frame)

        self._create_buttons(main_frame)



    def _create_summary_section(self, parent, summary: Dict):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill='x', pady=10)

        ctk.CTkLabel(frame, text='Summary', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 15))

        grid = ctk.CTkFrame(frame)
        grid.pack(padx=20, pady=(0, 15))

        headers = ['Period', 'Pomodoro', 'Work time']
        for i, header in enumerate(headers):
            ctk.CTkLabel(grid, text=header, font=ctk.CTkFont(weight='bold')).grid(row=0, column=i, padx=20, pady=5)

        periods = [
            ('Today', summary['today']),
            ('Week', summary['week']),
            ('Month', summary['month'])
        ]

        for row, (period_name, data) in enumerate(periods, 1):
            ctk.CTkLabel(grid, text=period_name).grid(row=row, column=0, padx=20, pady=5)
            ctk.CTkLabel(grid, text=str(data['completed_pomodoros'])).grid(row=row, column=1, padx=20, pady=5)
            ctk.CTkLabel(grid, text=self._format_time(data['total_work_time'])).grid(row=row, column=2, padx=20, pady=5)



    def _create_daily_section(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill='x', pady=10)

        ctk.CTkLabel(frame, text='Last 7 days', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 15))

        stats_data = self.stats_manager._load_all_stats()
        today = date.today()

        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            day_data = stats_data.get(day_str, {'completed_pomodoros': 0, 'total_work_time': 0})

            day_frame = ctk.CTkFrame(frame)
            day_frame.pack(fill='x', pady=2, padx=20)

            day_name = day.strftime('%A, %d %B')
            if day == today:
                day_name += ' (Today)'

            ctk.CTkLabel(day_frame, text=day_name, font=ctk.CTkFont(size=12, weight='bold')).pack(side='left', padx=10, pady=5)

            stats_text = f'{day_data["completed_pomodoros"]} pomodoros, {self._format_time(day_data["total_work_time"])}'
            ctk.CTkLabel(day_frame, text=stats_text, font=ctk.CTkFont(size=12)).pack(side='right', padx=10, pady=5)



    def _create_weekly_section(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill='x', pady=10)

        ctk.CTkLabel(frame, text='Weekly', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(10, 15))

        stats_data = self.stats_manager._load_all_stats()
        weekly_data = {}

        for day_str, day_data in stats_data.items():
            try:
                day = datetime.strptime(day_str, '%Y-%m-%d').date()
                year, week, _ = day.isocalendar()
                week_key = f'{year}-W{week:02d}'

                if week_key not in weekly_data:
                    weekly_data[week_key] = {'pomodoros': 0, 'time': 0}

                weekly_data[week_key]['pomodoros'] += day_data.get('completed_pomodoros', 0)
                weekly_data[week_key]['time'] += day_data.get('total_work_time', 0)
            except:
                continue

        sorted_weeks = sorted(weekly_data.keys())[-4:]

        for week_key in sorted_weeks:
            week_data = weekly_data[week_key]

            week_frame = ctk.CTkFrame(frame)
            week_frame.pack(fill='x', pady=2, padx=20)

            ctk.CTkLabel(week_frame, text=f'Week {week_key}', font=ctk.CTkFont(size=12, weight='bold')).pack(side='left', padx=10, pady=5)

            stats_text = f'{week_data["pomodoros"]} pomodoros, {self._format_time(week_data["time"])}'
            ctk.CTkLabel(week_frame, text=stats_text, font=ctk.CTkFont(size=12)).pack(side='right', padx=10, pady=5)



    def _create_buttons(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill='x', pady=20)

        ctk.CTkButton(frame, text='Reset statistics', command=self._reset_stats, fg_color='#dc3545', hover_color='#c82333').pack(side='left', padx=10)

        ctk.CTkButton(frame, text='Close', command=self.window.destroy).pack(side='right', padx=10)



    def _format_time(self, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return f'{hours}ч {minutes}м'
        else:
            return f'{minutes}м'



    def _reset_stats(self):
        result = messagebox.askyesno('Confirmation', 'Are you sure you want to reset all statistics?\nThis action cannot be undone.'
        )

        if result:
            if self.stats_manager.reset():
                messagebox.showinfo('Success', 'Statistics reset successfully.')
                self.window.destroy()



class AboutWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, 'About', '400x350')
        self.create_widgets()
        self.window.grab_set()



    def create_widgets(self):
        ctk.CTkLabel(self.window, text='aPomodoro Timer', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)

        info_text = """The Pomodoro Technique is a time management method
developed by Francesco Cirillo in the late 1980s.

 How it works:
• 25 minutes of focused work
• 5 minutes of short break
• After 4 cycles, a long break (15 minutes)

Version: 1.0 (Beta)
Developed using CustomTkinter

© 2024 aPomodoro"""

        ctk.CTkLabel(self.window, text=info_text, font=ctk.CTkFont(size=12), justify='left').pack(pady=20, padx=20)

        ctk.CTkButton(self.window, text='Close', command=self.window.destroy, width=100).pack(pady=20)