# @Time:            2023/7/13 1:26
# @User:            风前絮
# @Site:            cloudfall.top
# @File:            sprites.py
# @Software:        PyCharm
# @Author:          KazeMae
# @Email:           xiaochunfeng.x@foxmail.com

import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        """
        初始化
        :param pos: 精灵的初始位置，即左上角的坐标
        :param surface: 用于表示精灵图像的表面对象
        :param groups: 精灵组
        :param z: 精灵所在的图层
        """
        # 初始化pygame.sprite.Sprite
        super().__init__(groups)
        # 获取精灵的图像
        self.image = surface
        # 传入的位置信息创建精灵的矩形区域
        self.rect = self.image.get_rect(topleft = pos)
        # 精灵所在的图层
        self.z = z

