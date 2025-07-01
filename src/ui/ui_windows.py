import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox


class UIWindows:

    @staticmethod
    def show_about(parent):
        window = ctk.CTkToplevel(parent)
        window.title('About')
        window.geometry('400x300')
        window.transient(parent)
        window.grab_set()
        window.minsize(400, 300)

        ctk.CTkLabel(window, text='Pomodoro Timer',
                     font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)

        info = """The Pomodoro Technique is a time management method
        developed by Francesco Cirillo in the late 1980s.

         How it works:
        • 25 minutes of focused work
        • 5 minutes of short break
        • After 4 cycles, a long break (15 minutes)

        Version: 1.0 (Beta)

        © 2025 aPomodoro"""

        ctk.CTkLabel(window, text=info, font=ctk.CTkFont(size=12)).pack(pady=20, padx=20)
        ctk.CTkButton(window, text='Close', command=window.destroy).pack(pady=20)



    @staticmethod
    def show_settings(parent, timer_state, settings_manager, update_callback):
        window = ctk.CTkToplevel(parent)
        window.title('Settings')
        window.geometry('360x500')
        window.transient(parent)
        window.grab_set()
        window.minsize(360, 500)

        frame = ctk.CTkFrame(window, corner_radius=15)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text='Settings',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=15)

        pomodoro_var = tk.StringVar(value=str(timer_state.pomodoro_time // 60))
        short_var = tk.StringVar(value=str(timer_state.short_break_time // 60))
        long_var = tk.StringVar(value=str(timer_state.long_break_time // 60))
        notif_var = tk.StringVar(value=timer_state.notification_type)
        pom_sound_var = tk.StringVar(value=timer_state.pomodoro_sound)
        short_sound_var = tk.StringVar(value=timer_state.short_break_sound)
        long_sound_var = tk.StringVar(value=timer_state.long_break_sound)

        sound_dict = {
            'bell': 'Bell',
            'notification': 'Notification',
            'bonus_1': 'Bonus 1',
            'bonus_2': 'Bonus 2',
            'soft_bell': 'Soft bell',
            'none': 'No sound'
        }

        reverse_sound_dict = {
            'Bell': 'bell',
            'Soft bell': 'soft_bell',
            'Notification': 'notification',
            'Bonus 1': 'bonus_1',
            'Bonus 2': 'bonus_2',
            'No sound': 'none'
        }

        sound_names = ['Bell', 'Soft bell', 'Notification', 'Bonus 1', 'Bonus 2', 'No sound']

        pom_sound_var.set(sound_dict.get(timer_state.pomodoro_sound, 'Bonus 1'))
        short_sound_var.set(sound_dict.get(timer_state.short_break_sound, 'Soft bell'))
        long_sound_var.set(sound_dict.get(timer_state.long_break_sound, 'Bell'))

        settings_data = [
            ('Pomodoro (min):', pomodoro_var, None),
            ('Short break (min):', short_var, None),
            ('Long break (min):', long_var, None),
            ('Notification:', notif_var, ['sound', 'popup', 'both']),
            ('Pomodoro sound:', pom_sound_var, sound_names),
            ('Short break sound:', short_sound_var, sound_names),
            ('Long break sound:', long_sound_var, sound_names)
        ]

        for label_text, var, values in settings_data:
            row = ctk.CTkFrame(frame)
            row.pack(fill='x', pady=5, padx=10)
            ctk.CTkLabel(row, text=label_text).pack(side='left', padx=10)

            if values:
                ctk.CTkOptionMenu(row, variable=var, values=values).pack(side='right', padx=10)
            else:
                ctk.CTkEntry(row, textvariable=var, width=100).pack(side='right', padx=10)



        def apply_settings():
            try:
                pom_time = int(pomodoro_var.get()) * 60
                short_time = int(short_var.get()) * 60
                long_time = int(long_var.get()) * 60

                if pom_time <= 0 or short_time <= 0 or long_time <= 0:
                    raise ValueError("Time must be greater than 0")

                old_pom = timer_state.pomodoro_time
                timer_state.pomodoro_time = pom_time
                timer_state.short_break_time = short_time
                timer_state.long_break_time = long_time
                timer_state.notification_type = notif_var.get()
                timer_state.pomodoro_sound = reverse_sound_dict.get(pom_sound_var.get(), 'bonus_1')
                timer_state.short_break_sound = reverse_sound_dict.get(short_sound_var.get(), 'soft_bell')
                timer_state.long_break_sound = reverse_sound_dict.get(long_sound_var.get(), 'bell')

                if not timer_state.is_running:
                    if timer_state.is_pomodoro_mode and old_pom != pom_time:
                        timer_state.current_time = pom_time
                    elif not timer_state.is_pomodoro_mode:
                        if timer_state.cycle_count == 0:
                            timer_state.current_time = long_time
                        else:
                            timer_state.current_time = short_time

                if settings_manager.save_settings(timer_state):
                    messagebox.showinfo('Success', 'Settings saved!')
                    update_callback()  # Обновляем интерфейс
                    window.destroy()
                else:
                    messagebox.showerror('Error', 'Failed to save settings')

            except ValueError as e:
                messagebox.showerror('Error', f'Invalid values: {e}')

        ctk.CTkButton(frame, text='Apply', height=40, corner_radius=20,
                      command=apply_settings).pack(pady=15)

    @staticmethod
    def show_stats(parent, stats_manager):
        window = ctk.CTkToplevel(parent)
        window.title('Statistics')
        window.geometry('500x600')
        window.transient(parent)
        window.grab_set()
        window.minsize(500, 600)

        frame = ctk.CTkScrollableFrame(window)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text='Statistics',
                     font=ctk.CTkFont(size=24, weight='bold')).pack(pady=15)

        general_stats = stats_manager.get_general_stats()

        general_frame = ctk.CTkFrame(frame)
        general_frame.pack(fill='x', pady=10)

        ctk.CTkLabel(general_frame, text='General Statistics',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10)

        if general_stats['total_days'] > 0:
            general_text = f"""Total Pomodoros: {general_stats['total_pomodoros']}
Total Work Time: {general_stats['total_time'] // 3600}h {(general_stats['total_time'] % 3600) // 60}m
Active Days: {general_stats['total_days']}
Average per Day: {general_stats['avg_per_day']:.1f} pomodoros"""
        else:
            general_text = "No data yet"

        ctk.CTkLabel(general_frame, text=general_text).pack(pady=10)

        daily_frame = ctk.CTkFrame(frame)
        daily_frame.pack(fill='x', pady=10)

        ctk.CTkLabel(daily_frame, text='Last 7 Days',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10)

        daily_stats = stats_manager.get_daily_stats(7)
        for day_data in daily_stats:
            day_row = ctk.CTkFrame(daily_frame)
            day_row.pack(fill='x', pady=2, padx=10)

            day_name = day_data['date'].strftime('%A, %b %d')
            if day_data['is_today']:
                day_name += ' (Today)'

            ctk.CTkLabel(day_row, text=day_name).pack(side='left', padx=10, pady=5)

            stats_text = f"{day_data['pomodoros']} pomodoros, {day_data['work_time'] // 60}m"
            ctk.CTkLabel(day_row, text=stats_text).pack(side='right', padx=10, pady=5)



        def reset_stats():
            if messagebox.askyesno('Reset Statistics', 'Are you sure? This cannot be undone.'):
                if stats_manager.reset_stats():
                    messagebox.showinfo('Success', 'Statistics reset!')
                    window.destroy()
                else:
                    messagebox.showerror('Error', 'Failed to reset statistics')

        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill='x', pady=20)

        ctk.CTkButton(button_frame, text='Reset Statistics', command=reset_stats,
                      fg_color='#dc3545', hover_color='#c82333').pack(side='left', padx=10, pady=10)
        ctk.CTkButton(button_frame, text='Close', command=window.destroy).pack(side='right', padx=10, pady=10)