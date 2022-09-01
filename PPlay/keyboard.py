# coding= utf-8

import pygame
from pygame.locals import *

# Initializes pygame's modules
pygame.init()

class Keyboard():
    """
    Returns True if the key IS pressed, it means
    the press-check occurs every frame
    """
    def key_pressed(self, key):
        key = self.to_pattern(key)
        keys = pygame.key.get_pressed()
        if(keys[key]):
            return True

        return False
    
    """Shows the int code of the key"""
    def show_key_pressed(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                print(event.key)
                
    def to_pattern(self, key):
        """
        if((key=="LEFT") or (key=="left")):
            return pygame.K_LEFT
        elif((key=="RIGHT") or (key=="right")):
            return pygame.K_RIGHT
        elif((key=="UP") or (key=="up")):
            return pygame.K_UP
        elif((key=="DOWN") or (key=="down")):
            return pygame.K_DOWN
        elif((key=="ENTER") or (key=="enter") or
             (key=="RETURN") or (key=="return")):
            return pygame.K_RETURN
        elif((key=="ESCAPE") or (key=="escape") or
             (key=="ESC") or (key=="esc")):
            return pygame.K_ESCAPE
        elif((key=="SPACE") or (key=="space")):
            return pygame.K_SPACE
        elif((key=="LEFT_CONTROL") or (key=="left_control")):
            return pygame.K_LCTRL
        elif((key=="LEFT_SHIFT") or (key=="left_shift")):
            return pygame.K_LSHIFT
        elif((key=="RIGHT_SHIFT") or (key=="right_shift")):
            return pygame.K_RSHIFT
        elif ((key == "BACKSPACE") or (key == "backspace")):  # Very important addition! Now i can finally write text in-game
            return pygame.K_BACKSPACE
        elif(((key >= "A") and (key <= "Z")) or
             ((key  >= "a") and (key <= "z"))):
            return getattr(pygame, "K_" + key.lower())
        elif((key >= "0") and (key <= "9")):
            return getattr(pygame, "K_" + key)
        """
        key = key.upper()
        if key == "ENTER":
            return pygame.K_RETURN
        elif key == "ESC":
            return pygame.K_ESCAPE
        elif key == "LEFT_CONTROL":
            return pygame.K_LCTRL
        elif key == "LEFT_SHIFT":
            return pygame.K_LSHIFT
        elif key == "RIGHT_SHIFT":
            return pygame.K_RSHIFT
        elif len(key) == 1 and (key >= "A" and key <= "Z"):
            #return getattr(pygame, "K_" + key.lower())
            return pygame.__dict__.get("K_" + key.lower())
        #return getattr(pygame, "K_"+key)
        return pygame.__dict__.get("K_" + key)
