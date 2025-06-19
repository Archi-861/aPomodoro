import json
import os.path
import winsound
from win10toast import ToastNotifier
import customtkinter as ctk
from PIL import Image


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
                'long_break' : timer_state.long_break,
                'notification_type' : timer_state.notification_type
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
                    timer_state.notification_type = settings.get('notification_type', 'both')
                    timer_state.current_time = timer_state.pomodoro_time
                return True
            except Exception as ex:
                print(f'Error loading {ex}')
                return False
        return False



class MenuManager:
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        self.create_menu()


    def create_menu(self):
        menu = ctk.CTkFrame(self.root)
        menu.pack(side='top', fill='x', pady=(5, 10))

        title_label = ctk.CTkLabel(menu, text='aPomodoro', font=ctk.CTkFont(size=20, weight='bold'))
        title_label.pack(side='left', padx=10)

        about_icon = ctk.CTkImage(light_image=Image.open('icons/about.png'), size=(20, 20))
        statistics_icon = ctk.CTkImage(light_image=Image.open('icons/statistics.png'), size=(20,20))
        settings_icon = ctk.CTkImage(light_image=Image.open('icons/settings.png'),  size=(20, 20))

        about_button = ctk.CTkButton(menu, text='', image=about_icon, command=self.show_about, width=80)
        about_button.pack(side='right', padx=(0, 10))

        settings_button = ctk.CTkButton(menu, text='',image=settings_icon, command=self.show_settings, width=80)
        settings_button.pack(side='right', padx=(0, 10))

        statistic_button = ctk.CTkButton(menu, text='', image=statistics_icon, command=self.show_statistics, width=80)
        statistic_button.pack(side='right', padx=(0, 10))



    def show_about(self):
        about_window = ctk.CTkToplevel(self.root)
        about_window.title('About')
        about_window.geometry('400x300')
        about_window.transient(self.root)
        about_window.grab_set()

        title = ctk.CTkLabel(about_window, text='Pomodoro Timer', font=ctk.CTkFont(size=24, weight='bold'))
        title.pack(pady=20)

        info_text = """
        Техника Помодоро - это метод управления временем,
        разработанный Франческо Чирилло в конце 1980-х годов.

        Принцип работы:
        • 25 минут работы
        • 5 минут короткий перерыв
        • После 4 циклов - длинный перерыв (15 минут)

        Версия: 2.0
        Создано с использованием CustomTkinter
        """

        info_label = ctk.CTkLabel(about_window, text=info_text, font=ctk.CTkFont(size=12), justify='left')
        info_label.pack(pady=20, padx=20)

        close_btn = ctk.CTkButton(about_window, text='Close', command=about_window.destroy, width=100)
        close_btn.pack(pady=20)

    def show_statistics(self):
        pass

    def show_settings(self):
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
    def __init__(self, root):
        self.root = root
        self.toaster = ToastNotifier()


    def play_sound(self):
        winsound.Beep(1200, 150)
        winsound.Beep(1200, 150)
        winsound.Beep(1200, 150)



    def show_popup_notification(self, title, message, duration=3000):
        self.toaster.show_toast(title, message, duration=duration, threaded=True)



class TimerState:
    #управление состоянием таймера
    def __init__(self):
        self.pomodoro_time = 0.1 * 60
        self.short_break = 0.2 * 60
        self.long_break = 15 * 60
        self.current_time = self.pomodoro_time
        self.is_running = False
        self.is_pomodoro_mode = True
        self.completed_pomodoros = 0
        self.current_cycle = 0
        self.notification_type = 'both'

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
            self.reset_to_break(is_long_break=False)
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


        if self.timer_state.is_pomodoro_mode:
            self.timer_state.current_time = self.timer_state.pomodoro_time
        else:
            if self.timer_state.current_cycle == 0:
                self.timer_state.current_time = self.timer_state.long_break
            else:
                self.timer_state.current_time = self.timer_state.short_break


        self.update_callback() #маркер GUI



    def next_action_tick(self):
        if self.timer_state.is_running:
            self.timer_after = self.root.after(1000, self.one_second_tick)



    def one_second_tick(self):
        if self.timer_state.is_running and self.timer_state.current_time > 0:
            self.timer_state.current_time -= 1


            if self.timer_state.is_pomodoro_mode:
                initial_time = self.timer_state.pomodoro_time
            else:
                if self.timer_state.current_cycle == 0:
                    initial_time = self.timer_state.long_break
                else:
                    initial_time = self.timer_state.short_break


            progress = self.timer_state.current_time / initial_time if initial_time > 0 else 0.0
            self.update_callback(progress) #маркер GUI по прогрессу


            if self.timer_state.current_time > 0:
                self.next_action_tick()
            else:
                self.timer_state.is_running = False
                self.finish_callback() #маркер GUI по завершению таймера



    def run(self):
        initial_time = self.timer_state.current_time



class UIResource:
    def __init__(self, root):
        self.root = root
        self.pomodoro_color = '#ff6b6b'
        self.short_break_color = '#51cf66'
        self.long_break_color = '#339af0'
        self.pomodoro_circle_color = '#ff8787'
        self.short_break_circle_color = '#69f0ae'
        self.long_break_circle_color = '#74c0fc'



    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self.root, corner_radius = 20)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        return main_frame



    def create_title(self, parent):
        title_label = ctk.CTkLabel(parent, text='aPomodoro', font=ctk.CTkFont(size=32, weight='bold'))
        title_label.pack(pady=(30, 10))
        return title_label



    def create_status_label(self, parent):
        status_label = ctk.CTkLabel(parent, text='Pomodoro', font=ctk.CTkFont(size=20, weight='bold'), text_color=self.pomodoro_color)
        status_label.pack(pady=(0, 20))
        return status_label



    def create_timer_display(self, parent, current_time):
        progress_frame = ctk.CTkFrame(parent, width=300, height=300, corner_radius=150)
        progress_frame.pack(pady=(0, 20))
        progress_frame.pack_propagate(False)

        time_label = ctk.CTkLabel(
            progress_frame,
            text=self.format_time(current_time),
            font=ctk.CTkFont(size=48, weight='bold')
        )
        time_label.place(relx=0.5, rely=0.5, anchor='center')

        progress_bar = ctk.CTkProgressBar(
            parent,
            width=400,
            height=20,
            corner_radius=10
        )
        progress_bar.pack(pady=(0, 30))
        progress_bar.set(1.0)

        return progress_frame, time_label, progress_bar



    def create_control_button(self, parent):
        button_frame = ctk.CTkFrame(parent, fg_color='transparent')
        button_frame.pack(pady=(0, 30))

        start_button = ctk.CTkButton(button_frame, text='▶ Start', width=120, height=50, font=ctk.CTkFont(size=16, weight='bold'), corner_radius=25)
        start_button.pack(side='left', padx=10)

        pause_button = ctk.CTkButton(button_frame, text='⏸ Pause', width=120, height=50, font=ctk.CTkFont(size=16, weight='bold'), corner_radius=25)
        pause_button.pack(side='left', padx=10)

        reset_button = ctk.CTkButton(button_frame, text='Reset', width=120, height=50, font=ctk.CTkFont(size=16, weight='bold'), corner_radius=25)
        reset_button.pack(side='left', padx=10)

        return start_button, pause_button, reset_button



    def format_time(self, seconds):
        if not isinstance(seconds, (int, float)):
            seconds = 0
        seconds = int(seconds)
        minutes = seconds // 60
        seconds = seconds % 60
        return f'{minutes:02d}:{seconds:02d}'



class PomodoroTimer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('aPomodoro')
        self.root.geometry('600x700')


        self.timer_state = TimerState()
        self.settings = Settings()
        self.menu_manager = MenuManager(self.root, self.settings)
        self.stats = Statistics()
        self.notification_manager = NotificationManager(self.root)
        self.ui_resource = UIResource(self.root)


        self.settings.load_setting(self.timer_state)


        self.timer_core = TimerCore(self.timer_state, self.notification_manager, self.update_display, self.timer_finished, self.root)


        self.setup_ui()



    def update_display(self, progress=1.0):
        try:
            self.time_label.configure(text=self.ui_resource.format_time(self.timer_state.current_time))
            self.progress_bar.set(progress)


            if self.timer_state.is_pomodoro_mode:
                status_text  = 'aPomodoro'
                color = self.ui_resource.pomodoro_color

            else:
                if self.timer_state.current_cycle == 0:
                    status_text = 'Long break'
                    color = self.ui_resource.long_break_color
                else:
                    status_text = 'Short break'
                    color = self.ui_resource.short_break_color

            if self.timer_state.is_pomodoro_mode:
                self.progress_frame.configure(fg_color=self.ui_resource.pomodoro_circle_color)
            elif self.timer_state.current_cycle == 0:
                self.progress_frame.configure(fg_color=self.ui_resource.long_break_circle_color)
            else:
                self.progress_frame.configure(fg_color=self.ui_resource.short_break_circle_color)

            self.progress_bar.configure(progress_color=color)
            self.status_label.configure(text=status_text, text_color=color)


            time_str = self.ui_resource.format_time(self.timer_state.current_time)
            if self.timer_state.is_running:
                self.root.title(f'{time_str} - aPomodoro')
            else:
                self.root.title('aPomodoro')


        except Exception as ex:
            print(f'Error update display: {ex}')



    def timer_finished(self):
        self.timer_state.is_running = False

        self.start_button.configure(state='normal')
        self.pause_button.configure(state='disabled')

        if self.timer_state.is_pomodoro_mode:
            next_period = self.timer_state.complete_pomodoro_period()
            #Добавить занесение в статистику

            if next_period == 'Long_break':
                title = 'The cycle is completed!'
                message = 'Long break'
                color = self.ui_resource.long_break_color
            else:
                title = 'The pomodoro is completed!'
                message = 'Short break'
                color = self.ui_resource.short_break_color

        else:
            self.timer_state.complete_break_period()
            title = 'The break is over'
            message = 'Pomodoro'
            color = self.ui_resource.pomodoro_color


        notification = self.timer_state.notification_type
        if notification in ['sound', 'both']:
            self.notification_manager.play_sound()

        if notification in ['popup', 'both']:
            self.notification_manager.show_popup_notification(title, message, color=color)

        self.update_display()
        self.start()



    def setup_ui(self):
        main_frame = self.ui_resource.create_main_frame()
        self.ui_resource.create_title(main_frame)
        self.status_label = self.ui_resource.create_status_label(main_frame)
        self.progress_frame, self.time_label, self.progress_bar = self.ui_resource.create_timer_display(main_frame, self.timer_state.current_time)


        self.start_button, self.pause_button, self.reset_button = self.ui_resource.create_control_button(main_frame)
        self.start_button.configure(command=self.start)
        self.pause_button.configure(command=self.pause)
        self.reset_button.configure(command=self.reset)

    #Добавить панель настроек и панель статистики

        self.update_display()



    def start(self):
        #Запуск таймера
        if self.timer_core.start():
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')



    def pause(self):
        self.timer_core.pause()
        self.start_button.configure(state='normal')
        self.pause_button.configure(state='disabled')



    def reset(self):
        self.timer_core.reset()
        self.start_button.configure(state='normal')
        self.reset_button.configure(state='disabled')
        self.update_display()



    def run(self):
        self.root.mainloop()





app = PomodoroTimer()
app.run()