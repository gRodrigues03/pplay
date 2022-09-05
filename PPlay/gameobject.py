"""The most basic game class"""
# Module import
from . import collision, point


class GameObject:
    """Creates a GameObject in X, Y co-ords, with Width x Height"""
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.attach = point.Point(x, y)
        self.width = h
        self.height = w

    def collided(self, obj):
        return collision.Collision.collided(self, obj)
