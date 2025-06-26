import os
import pygame
from typing import Dict, List, Optional
from config import Config


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds_dir = Config.SOUNDS_DIR
        self.available_sounds = self._load_sounds()
        self.sound_names = {
            'none': 'No sound',
            'notification': 'Notification',
            'soft_bell': 'Soft bell',
            'bell': 'Bell',
            'bonus_1' : 'Bonus 1',
            'bonus_2' : 'Bonus 2'
        }



    def _load_sounds(self) -> Dict[str, Optional[pygame.mixer.Sound]]:
        sounds = {'none': None}

        if os.path.exists(self.sounds_dir):
            try:
                for file in os.listdir(self.sounds_dir):
                    if file.endswith('.wav'):
                        sound_name = file[:-4]
                        sound_path = os.path.join(self.sounds_dir, file)
                        sounds[sound_name] = pygame.mixer.Sound(sound_path)
            except Exception as e:
                print(f'Error loading sounds: {e}')

        return sounds



    def play_sound(self, sound_name: str):
        if sound_name == 'none' or sound_name not in self.available_sounds:
            return

        sound = self.available_sounds[sound_name]

        try:
            sound.play()
        except Exception as e:
            print(f'Audio playback error {sound_name}: {e}')



    def get_sound_list(self) -> List[str]:
        return list(self.available_sounds.keys())

    def get_display_name(self, sound_name: str) -> str:
        return self.sound_names.get(sound_name, sound_name.replace('_', ' ').title())