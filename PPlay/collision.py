# coding= utf-8

# Modules import
from . import point
import pygame

# -*- coding: utf-8 -*-

"""A simple class to deal with basic collision methods"""
"""
Must note that the collision is inclusive, i.e.,
occurs when one enters the other effectively,
not only when over the same position of the edge.
"""
class Collision():
    """
    minN: the Point of the top left of the N rect
    maxN: the Point of the bottom right of the N rect
    """
    game_object1_min = point.Point()
    game_object1_max = point.Point()

    game_object2_min = point.Point()
    game_object2_max = point.Point()

    @classmethod
    def collided_rect(cls):
        if cls.game_object1_min.x >= cls.game_object2_max.x or cls.game_object1_max.x <= cls.game_object2_min.x:
            return False
        if cls.game_object1_min.y >= cls.game_object2_max.y or cls.game_object1_max.y <= cls.game_object2_min.y:
            return False
        return True

    """
    args[0]: the origin GameObject
    args[1]: the target GameObject
    """
    @classmethod
    def collided(cls, *args):
        cls.game_object1_min.x, cls.game_object1_min.y = args[0].x, args[0].y
        cls.game_object1_max.x, cls.game_object1_max.y = args[0].x + args[0].width, args[0].y + args[0].height

        cls.game_object2_min.x, cls.game_object2_min.y = args[1].x, args[1].y
        cls.game_object2_max.x, cls.game_object2_max.y = args[1].x + args[1].width, args[1].y + args[1].height

        return Collision.collided_rect()

    """
    Perfect-pixel collision using masks.
    """
    @classmethod
    def perfect_collision(cls, gameimage1, gameimage2):
        """
        Both objects must extend a GameImage, 
        since it has the pygame.mask and pygame.Rect
        """
        offset_x = (gameimage2.rect.left - gameimage1.rect.left)
        offset_y = (gameimage2.rect.top - gameimage1.rect.top)
        
        mask_1 = pygame.mask.from_surface(gameimage1.image)
        mask_2 = pygame.mask.from_surface(gameimage2.image)
        
        if(mask_1.overlap(mask_2, (offset_x, offset_y)) != None):
            return True
        return False

    """
    Perfect collision aux - is called by GameImage
    """
    @classmethod
    def collided_perfect(cls, gameimage1, gameimage2):
        return (Collision.perfect_collision(gameimage1, gameimage2))
                      
            
        
    
