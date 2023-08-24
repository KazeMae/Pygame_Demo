# @Time:            2023/8/24 9:04
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            water_tile
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from game.settings import *


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']
