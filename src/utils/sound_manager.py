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
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            return None



    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, relative_path)



    def play_sound(self, key):
        sound = self.sounds.get(key)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass


    def handle_timer_finished(self, timer_state, completed_mode):
        if timer_state.notification_type in ('sound', 'both'):
            if completed_mode == 'pomodoro':
                sound_key = timer_state.pomodoro_sound
                self.play_sound(sound_key)

            elif completed_mode == 'short_break':
                sound_key = timer_state.short_break_sound
                self.play_sound(sound_key)

            elif completed_mode == 'long_break':
                sound_key = timer_state.long_break_sound
                self.play_sound(sound_key)



    def cleanup(self):
        try:
            pygame.mixer.quit()
        except Exception:
            pass
