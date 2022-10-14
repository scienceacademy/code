import pygame
from time import sleep

#pygame.mixer.pre_init(devicename="USB-Audio - USB PnP Sound Device")
pygame.init()
pygame.mixer.init()

#rint(pygame.mixer.get_sdl_mixer_version())
#rint(pygame._sdl2.audio.get_audio_device_names(False))
pygame.mixer.music.load("pm_sounds/game_start.wav")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    sleep(1)

pygame.mixer.quit()
