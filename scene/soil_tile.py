# @Time:            2023/8/23 3:51
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            soil_tile
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *


class SoilTile(pygame.sprite.Sprite):
    """
    显示开垦后的土地贴图
    """
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']
