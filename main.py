import customtkinter as ctk


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('aPomodoro')
        self.geometry('600x550')

        self.timer_label = ctk.CTkLabel(self, text='25:00', font=('Helvetica', 48))
        self.timer_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text='START', command=self.start_timer)
        self.start_button.pack(pady=5)

        self.pause_button = ctk.CTkButton(self, text='PAUSE', command=self.pause_timer)
        self.pause_button.pack(pady=5)

        self.reset_button = ctk.CTkButton(self, text='STOP', command=self.stop_timer)
        self.reset_button.pack(pady=5)

        self.seconds_left = 25 * 60

    def start_timer(self):
        pass

    def pause_timer(self):
        pass

    def stop_timer(self):
        pass




app = PomodoroApp()
app.mainloop()
