# @Time:            2023/8/23 1:48
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            interaction
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com
import pygame
from scene.generic import Generic


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surface = pygame.Surface(size)
        super().__init__(pos, surface, groups)
        self.name = name
