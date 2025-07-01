import pygame
import os
import sys

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {
            'bell': self.load_sound('sounds/bell.wav'),
            'soft_bell': self.load_sound('sounds/soft_bell.wav'),
            'notification': self.load_sound('sounds/notification.wav'),
            'bonus_1': self.load_sound('sounds/bonus_1.wav'),
            'bonus_2': self.load_sound('sounds/bonus_2.wav'),
            'none': None
        }

    def load_sound(self, filename):
        path = self.resource_path(filename)
        print(f"[DEBUG] Loading sound from: {path}")  # временно для отладки
        return pygame.mixer.Sound(path)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            # Поднимаемся до корня проекта из src/utils/
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, relative_path)

    def play_sound(self, key):
        sound = self.sounds.get(key)
        if sound:
            sound.play()

    def handle_timer_finished(self, timer_state, next_mode):
        if timer_state.notification_type in ('sound', 'both'):
            if timer_state.is_pomodoro_mode:
                self.play_sound(timer_state.pomodoro_sound)
            elif timer_state.cycle_count == 0:
                self.play_sound(timer_state.long_break_sound)
            else:
                self.play_sound(timer_state.short_break_sound)

    def cleanup(self):
        pygame.mixer.quit()
