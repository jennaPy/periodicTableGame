import pygame
import os
import random


sound_folder = "sounds"

pygame.mixer.init()

def play_sound(sound_type):
    sound_files = os.listdir(sound_folder)
    sound_type_files = [file for file in sound_files if sound_type in file]
    if sound_type_files:
        random_sound = random.choice(sound_type_files)
        picked_sound = pygame.mixer.Sound(os.path.join(sound_folder, random_sound))
        picked_sound.play()
