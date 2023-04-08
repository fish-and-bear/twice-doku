import pygame
import pygame_gui
import os
import sys
from mainmenu import intro

if __name__ == "__main__":
    pygame.init()
    # To center the window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    intro()
