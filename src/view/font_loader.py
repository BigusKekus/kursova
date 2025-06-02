import pygame
import os
import sys

def load_font(size):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    font_path = os.path.join(base_path, "assets", "fonts", "PressStart2P-Regular.ttf")
    return pygame.font.Font(font_path, size)
