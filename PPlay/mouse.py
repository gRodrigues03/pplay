import pygame
from . import window, point


class Mouse:

    def __init__(self):
        self.visibility = True

    """Returns the mouse position."""
    @staticmethod
    def get_position():
        return window.Window.mouse_pos

    """Defines the mouse's new position."""
    @staticmethod
    def set_position(x, y):
        pygame.mouse.set_pos([x, y])

    """Hides the mouse."""
    def hide(self):
        pygame.mouse.set_visible(False)
        self.visibility = False

    """Unhides the mouse."""
    def unhide(self):
        pygame.mouse.set_visible(True)
        self.visibility = True

    """Return if the mouse is currently visible or not."""
    def is_visible(self):
        return self.visibility

    """
    Returns True or False if the respective button was pressed.
    BUTTON_LEFT = 1
    BUTTON_MIDDLE = 2
    BUTTON_RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5
    """
    @staticmethod
    def is_button_pressed(button):
        pressed_buttons = pygame.mouse.get_pressed()
        if pressed_buttons[button-1] == 1:
            return True
        else:
            return False            

    """Returns a boolean if the mouse is over an area."""
    def is_over_area(self, start_point, end_point):
        mouse_pos = self.get_position()
        mouse_point = point.Point(mouse_pos[0], mouse_pos[1])
        start_point = point.Point(start_point[0], start_point[1])
        end_point = point.Point(end_point[0], end_point[1])
        
        if((mouse_point.x < start_point.x) or
           (mouse_point.y < start_point.y) or
           (mouse_point.x > end_point.x) or
           (mouse_point.y > end_point.y)):
            return False
        else:
            return True
        
    """Returns if the mouse is over a game_object."""
    def is_over_object(self, game_object):
        # Takes camera offset by account
        target = point.Point(game_object.x + window.Window.actual_camera.x, game_object.y + window.Window.actual_camera.y)
        return self.is_over_area([target.x, target.y],
                                 [target.x + game_object.width, target.y + game_object.height])

    """Returns a boolean if the mouse is over the game screen."""
    @staticmethod
    def is_on_screen():
        return pygame.mouse.get_focused()

    """Returns a boolean if the mouse is NOT over the game screen."""
    @staticmethod
    def is_off_screen():
        return not pygame.mouse.get_focused()

    """
    Returns the amount of mouse relative-movement since
    the previous call to this function.
    """
    @staticmethod
    def delta_movement():
        return pygame.mouse.get_rel()

    # Mouse drag?

    
        

        
