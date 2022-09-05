import pygame
from pygame.locals import *


class Keyboard:
    """
    Returns True if the key IS pressed, it means
    the press-check occurs every frame
    """
    @staticmethod
    def key_pressed(key):
        key = to_pattern(key)
        keys = pygame.key.get_pressed()
        if keys[key]:
            return True

        return False
    
    """Shows the int code of the key"""
    @staticmethod
    def show_key_pressed():
        return


def to_pattern(key):
    key = key.upper()
    if key == "ENTER":
        return K_RETURN
    elif key == "ESC":
        return K_ESCAPE
    elif key == "LEFT_CONTROL":
        return K_LCTRL
    elif key == "LEFT_SHIFT":
        return K_LSHIFT
    elif key == "RIGHT_SHIFT":
        return K_RSHIFT
    elif len(key) == 1 and ("A" <= key <= "Z"):
        return pygame.__dict__.get("K_" + key.lower())
    else:
        return pygame.__dict__.get("K_" + key)
