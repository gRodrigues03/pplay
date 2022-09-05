# Pygame and system modules
import pygame
from . import window, collision, gameobject

NORMAL = 0
ADD = pygame.BLEND_RGBA_ADD
MULTIPLY = pygame.BLEND_RGBA_MULT
SUBTRACT = pygame.BLEND_RGBA_SUB


# Loads an image (with colorkey and alpha)
def load_image(name):
    """loads an image into memory"""
    return pygame.image.load(name).convert_alpha()


"""GameImage is the base class to deal with images"""


class GameImage(gameobject.GameObject):
    """
    Creates a GameImage from the specified file.
    The width and height are obtained based on the image file.
    """
    def __init__(self, image_file):
        # Parent constructor must be called first
        gameobject.GameObject.__init__(self)
        
        # Loads image from the source, converts to fast-blitting format
        if type(image_file) == str:
            self.image = load_image(image_file)
        else:
            self.image = image_file
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.drawable = True
        self.flipped_x = False
        self.flipped_y = False
        self.opacity = 100
        self.blend_mode = 0
        self.attached_to_camera = False

    """Draws the image on the screen"""
    def draw(self, mode=0):
        # An instance of the Window screen
        # Window object must've been initiated
        if self.drawable:
            if self.attached_to_camera:
                self.attach.x = self.x + window.Window.actual_camera.x
                self.attach.y = self.y + window.Window.actual_camera.y
                self.rect.x, self.rect.y = self.attach.x, self.attach.y
                window.Window.get_screen().blit(self.image, (self.x, self.y), special_flags=self.blend_mode)
            else:
                self.rect.x, self.rect.y = self.x + window.Window.actual_camera.x, self.y + window.Window.actual_camera.y
                window.Window.get_screen().blit(self.image, self.rect, special_flags=mode)

    """Sets the (X,Y) image position on the screen"""
    def set_position(self, x, y):
        self.x = x
        self.y = y

    """Checks collision with hitmask"""
    def collided_perfect(self, target):
        return collision.Collision.collided_perfect(self, target)

    def set_image(self, image):
        if type(image) == str:
            self.image = pygame.transform.flip(load_image(image), self.flipped_x, self.flipped_y)
        else:
            self.image = pygame.transform.flip(image, self.flipped_x, self.flipped_y)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    """Does not allow the image to be drawn on the screen."""
    def hide(self):
        self.drawable = False

    """Allows the image to be drawn on the screen."""
    def unhide(self):
        self.drawable = True

    """Flips the image horizontally or vertically at will"""
    def flip_image(self, x=True, y=False):
        if x:
            self.flipped_x = not self.flipped_x
        if y:
            self.flipped_y = not self.flipped_y
        self.image = pygame.transform.flip(self.image, x, y)

    """Sets image opacity"""
    def set_opacity(self, value):
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        self.opacity = value
        value = (value / 100) * 255
        self.image.set_alpha(value)

    """Changes the blending mode"""
    def set_blending_mode(self, mode):
        if type(mode) == int:
            self.blend_mode = mode
        else:
            mode = mode.upper()
            if mode == 'ADD':
                self.blend_mode = pygame.BLEND_RGBA_ADD  # = 6
            elif mode == 'MULTIPLY':
                self.blend_mode = pygame.BLEND_RGBA_MULT  # = 7
            elif mode == 'SUBTRACT':
                self.blend_mode = pygame.BLEND_RGBA_SUB  # = 8

    """Attaches the image to the camera. It keeps its position on screen ignoring the camera movement."""
    def attach_to_camera(self, value=True):
        self.attached_to_camera = value

    def get_image(self):
        return self.image
